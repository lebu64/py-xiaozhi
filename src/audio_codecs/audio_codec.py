import asyncio
import gc
import time
from collections import deque
from typing import Optional

import numpy as np
import opuslib
import sounddevice as sd
import soxr

from src.audio_codecs.aec_processor import AECProcessor
from src.constants.constants import AudioConfig
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class AudioCodec:
    """
    Audio codec, responsible for recording encoding and playback decoding
    Main functions:
    1. Recording: Microphone -> Resample 16kHz -> Opus encoding -> Send
    2. Playback: Receive -> Opus decode 24kHz -> Playback queue -> Speaker
    """

    def __init__(self):
        # Get configuration manager
        self.config = ConfigManager.get_instance()

        # Opus codec: 16kHz encoding for recording, 24kHz decoding for playback
        self.opus_encoder = None
        self.opus_decoder = None

        # Device information
        self.device_input_sample_rate = None
        self.device_output_sample_rate = None
        self.mic_device_id = None  # Microphone device ID (fixed index, not overwritten once written to config)
        self.speaker_device_id = None  # Speaker device ID (fixed index)

        # Resamplers: Recording resample to 16kHz, playback resample to device sample rate
        self.input_resampler = None  # Device sample rate -> 16kHz
        self.output_resampler = None  # 24kHz -> Device sample rate (for playback)

        # Resample buffers
        self._resample_input_buffer = deque()
        self._resample_output_buffer = deque()

        self._device_input_frame_size = None
        self._is_closing = False

        # Audio stream objects
        self.input_stream = None  # Recording stream
        self.output_stream = None  # Playback stream

        # Queues: Wake word detection and playback buffer
        self._wakeword_buffer = asyncio.Queue(maxsize=100)
        self._output_buffer = asyncio.Queue(maxsize=500)

        # Real-time encoding callback (direct send, not through queue)
        self._encoded_audio_callback = None

        # AEC processor
        self.aec_processor = AECProcessor()
        self._aec_enabled = False

    # -----------------------
    # Helper methods for automatic device selection
    # -----------------------
    def _auto_pick_device(self, kind: str) -> Optional[int]:
        """
        Automatically select a stable device index (prefer WASAPI).
        kind: 'input' or 'output'
        """
        assert kind in ("input", "output")
        try:
            devices = sd.query_devices()
            hostapis = sd.query_hostapis()
        except Exception as e:
            logger.warning(f"Failed to enumerate devices: {e}")
            return None

        # 1) Prefer WASAPI HostAPI default device (if available)
        wasapi_index = None
        for idx, ha in enumerate(hostapis):
            name = ha.get("name", "")
            if "WASAPI" in name:
                key = "default_input_device" if kind == "input" else "default_output_device"
                cand = ha.get(key, -1)
                if isinstance(cand, int) and 0 <= cand < len(devices):
                    d = devices[cand]
                    if (kind == "input" and d["max_input_channels"] > 0) or (
                        kind == "output" and d["max_output_channels"] > 0
                    ):
                        wasapi_index = cand
                        break
        if wasapi_index is not None:
            return wasapi_index

        # 2) Fallback: Match system default (kind) returned name + prefer WASAPI
        try:
            default_info = sd.query_devices(kind=kind)  # Won't trigger -1
            default_name = default_info.get("name")
        except Exception:
            default_name = None

        scored = []
        for i, d in enumerate(devices):
            if kind == "input":
                ok = d["max_input_channels"] > 0
            else:
                ok = d["max_output_channels"] > 0
            if not ok:
                continue
            host_name = hostapis[d["hostapi"]]["name"]
            score = 0
            if "WASAPI" in host_name:
                score += 5
            if default_name and d["name"] == default_name:
                score += 10
            # Small bonus: Common available endpoint keywords
            if any(k in d["name"] for k in ["Speaker", "Realtek", "USB", "AMD", "HDMI", "Monitor"]):
                score += 1
            scored.append((score, i))

        if scored:
            scored.sort(reverse=True)
            return scored[0][1]

        # 3) Final fallback: First device with channels
        for i, d in enumerate(devices):
            if (kind == "input" and d["max_input_channels"] > 0) or (
                kind == "output" and d["max_output_channels"] > 0
            ):
                return i
        return None

    async def initialize(self):
        """
        Initialize audio devices.
        """
        try:
            # Display and select audio devices (first time auto-select and write to config; later don't overwrite)
            await self._select_audio_devices()

            # Safely get input/output default info (avoid -1)
            if self.mic_device_id is not None and self.mic_device_id >= 0:
                input_device_info = sd.query_devices(self.mic_device_id)
            else:
                input_device_info = sd.query_devices(kind="input")

            if self.speaker_device_id is not None and self.speaker_device_id >= 0:
                output_device_info = sd.query_devices(self.speaker_device_id)
            else:
                output_device_info = sd.query_devices(kind="output")

            self.device_input_sample_rate = int(input_device_info["default_samplerate"])
            self.device_output_sample_rate = int(output_device_info["default_samplerate"])

            frame_duration_sec = AudioConfig.FRAME_DURATION / 1000
            self._device_input_frame_size = int(self.device_input_sample_rate * frame_duration_sec)

            logger.info(
                f"Input sample rate: {self.device_input_sample_rate}Hz, Output: {self.device_output_sample_rate}Hz"
            )

            await self._create_resamplers()

            # Don't force global defaults, let each stream carry its own device/samplerate
            sd.default.samplerate = None
            sd.default.channels = AudioConfig.CHANNELS
            sd.default.dtype = np.int16

            await self._create_streams()

            # Opus codec
            self.opus_encoder = opuslib.Encoder(
                AudioConfig.INPUT_SAMPLE_RATE,
                AudioConfig.CHANNELS,
                opuslib.APPLICATION_AUDIO,
            )
            self.opus_decoder = opuslib.Decoder(
                AudioConfig.OUTPUT_SAMPLE_RATE, AudioConfig.CHANNELS
            )

            # Initialize AEC processor
            try:
                await self.aec_processor.initialize()
                self._aec_enabled = True
                logger.info("AEC processor enabled")
            except Exception as e:
                logger.warning(f"AEC processor initialization failed, will use raw audio: {e}")
                self._aec_enabled = False

            logger.info("Audio initialization completed")
        except Exception as e:
            logger.error(f"Failed to initialize audio devices: {e}")
            await self.close()
            raise

    async def _create_resamplers(self):
        """
        Create resamplers Input: Device sample rate -> 16kHz (for encoding) Output: 24kHz -> Device sample rate (for playback)
        """
        # Input resampler: Device sample rate -> 16kHz (for encoding)
        if self.device_input_sample_rate != AudioConfig.INPUT_SAMPLE_RATE:
            self.input_resampler = soxr.ResampleStream(
                self.device_input_sample_rate,
                AudioConfig.INPUT_SAMPLE_RATE,
                AudioConfig.CHANNELS,
                dtype="int16",
                quality="QQ",
            )
            logger.info(f"Input resampling: {self.device_input_sample_rate}Hz -> 16kHz")

        # Output resampler: 24kHz -> Device sample rate
        if self.device_output_sample_rate != AudioConfig.OUTPUT_SAMPLE_RATE:
            self.output_resampler = soxr.ResampleStream(
                AudioConfig.OUTPUT_SAMPLE_RATE,
                self.device_output_sample_rate,
                AudioConfig.CHANNELS,
                dtype="int16",
                quality="QQ",
            )
            logger.info(
                f"Output resampling: {AudioConfig.OUTPUT_SAMPLE_RATE}Hz -> {self.device_output_sample_rate}Hz"
            )

    async def _select_audio_devices(self):
        """
        Display and select audio devices.
        Prefer devices from configuration file, if not available then auto-select and save to config (only write first time, don't overwrite later).
        """
        try:
            audio_config = self.config.get_config("AUDIO_DEVICES", {}) or {}

            # Whether already has explicit configuration (determines whether to write back)
            had_cfg_input = "input_device_id" in audio_config
            had_cfg_output = "output_device_id" in audio_config

            input_device_id = audio_config.get("input_device_id")
            output_device_id = audio_config.get("output_device_id")

            devices = sd.query_devices()

            # --- Validate input device from configuration ---
            if input_device_id is not None:
                try:
                    if isinstance(input_device_id, int) and 0 <= input_device_id < len(devices):
                        d = devices[input_device_id]
                        if d["max_input_channels"] > 0:
                            self.mic_device_id = input_device_id
                            logger.info(f"Using configured microphone device: [{input_device_id}] {d['name']}")
                        else:
                            logger.warning(f"Configured device [{input_device_id}] doesn't support input, will auto-select")
                            self.mic_device_id = None
                    else:
                        logger.warning(f"Configured input device ID [{input_device_id}] is invalid, will auto-select")
                        self.mic_device_id = None
                except Exception as e:
                    logger.warning(f"Failed to validate configured input device: {e}, will auto-select")
                    self.mic_device_id = None
            else:
                self.mic_device_id = None

            # --- Validate output device from configuration ---
            if output_device_id is not None:
                try:
                    if isinstance(output_device_id, int) and 0 <= output_device_id < len(devices):
                        d = devices[output_device_id]
                        if d["max_output_channels"] > 0:
                            self.speaker_device_id = output_device_id
                            logger.info(f"Using configured speaker device: [{output_device_id}] {d['name']}")
                        else:
                            logger.warning(f"Configured device [{output_device_id}] doesn't support output, will auto-select")
                            self.speaker_device_id = None
                    else:
                        logger.warning(f"Configured output device ID [{output_device_id}] is invalid, will auto-select")
                        self.speaker_device_id = None
                except Exception as e:
                    logger.warning(f"Failed to validate configured output device: {e}, will auto-select")
                    self.speaker_device_id = None
            else:
                self.speaker_device_id = None

            # --- If any is empty, auto-select (only first time will write to config) ---
            picked_input = self.mic_device_id
            picked_output = self.speaker_device_id

            if picked_input is None:
                picked_input = self._auto_pick_device("input")
                if picked_input is not None:
                    self.mic_device_id = picked_input
                    d = devices[picked_input]
                    logger.info(f"Auto-selected microphone device: [{picked_input}] {d['name']}")
                else:
                    logger.warning("No available input device found (will use system default, and not write index).")

            if picked_output is None:
                picked_output = self._auto_pick_device("output")
                if picked_output is not None:
                    self.speaker_device_id = picked_output
                    d = devices[picked_output]
                    logger.info(f"Auto-selected speaker device: [{picked_output}] {d['name']}")
                else:
                    logger.warning("No available output device found (will use system default, and not write index).")

            # --- Only write when configuration originally lacked corresponding entry (avoid second overwrite) ---
            need_write = (not had_cfg_input and picked_input is not None) or (not had_cfg_output and picked_output is not None)
            if need_write:
                await self._save_default_audio_config(
                    input_device_id=picked_input if not had_cfg_input else None,
                    output_device_id=picked_output if not had_cfg_output else None,
                )

        except Exception as e:
            logger.warning(f"Device selection failed: {e}, will use system default (not write to config)")
            # Allow None, let PortAudio use system default endpoints
            self.mic_device_id = self.mic_device_id if isinstance(self.mic_device_id, int) else None
            self.speaker_device_id = self.speaker_device_id if isinstance(self.speaker_device_id, int) else None

    async def _save_default_audio_config(self, input_device_id: Optional[int], output_device_id: Optional[int]):
        """
        Save default audio device configuration to config file (only for non-empty devices passed in; won't overwrite existing fields).
        """
        try:
            devices = sd.query_devices()
            audio_config_patch = {}

            # Save input device configuration
            if input_device_id is not None and 0 <= input_device_id < len(devices):
                d = devices[input_device_id]
                audio_config_patch.update({
                    "input_device_id": input_device_id,
                    "input_device_name": d["name"],
                    "input_sample_rate": int(d["default_samplerate"]),
                })

            # Save output device configuration
            if output_device_id is not None and 0 <= output_device_id < len(devices):
                d = devices[output_device_id]
                audio_config_patch.update({
                    "output_device_id": output_device_id,
                    "output_device_name": d["name"],
                    "output_sample_rate": int(d["default_samplerate"]),
                })

            if audio_config_patch:
                # merge: don't overwrite existing keys
                current = self.config.get_config("AUDIO_DEVICES", {}) or {}
                for k, v in audio_config_patch.items():
                    if k not in current:  # Only write when originally didn't have
                        current[k] = v
                success = self.config.update_config("AUDIO_DEVICES", current)
                if success:
                    logger.info("Default audio devices written to config (first time).")
                else:
                    logger.warning("Failed to save audio device configuration")
        except Exception as e:
            logger.error(f"Failed to save default audio device configuration: {e}")

    async def _create_streams(self):
        """
        Create audio streams.
        """
        try:
            # Microphone input stream
            self.input_stream = sd.InputStream(
                device=self.mic_device_id,  # None=system default; or fixed index
                samplerate=self.device_input_sample_rate,
                channels=AudioConfig.CHANNELS,
                dtype=np.int16,
                blocksize=self._device_input_frame_size,
                callback=self._input_callback,
                finished_callback=self._input_finished_callback,
                latency="low",
            )

            # Select output sample rate based on device support
            if self.device_output_sample_rate == AudioConfig.OUTPUT_SAMPLE_RATE:
                # Device supports 24kHz, use directly
                output_sample_rate = AudioConfig.OUTPUT_SAMPLE_RATE
                device_output_frame_size = AudioConfig.OUTPUT_FRAME_SIZE
            else:
                # Device doesn't support 24kHz, use device default sample rate and enable resampling
                output_sample_rate = self.device_output_sample_rate
                device_output_frame_size = int(
                    self.device_output_sample_rate * (AudioConfig.FRAME_DURATION / 1000)
                )

            self.output_stream = sd.OutputStream(
                device=self.speaker_device_id,  # None=system default; or fixed index
                samplerate=output_sample_rate,
                channels=AudioConfig.CHANNELS,
                dtype=np.int16,
                blocksize=device_output_frame_size,
                callback=self._output_callback,
                finished_callback=self._output_finished_callback,
                latency="low",
            )

            self.input_stream.start()
            self.output_stream.start()

            logger.info("Audio streams started")

        except Exception as e:
            logger.error(f"Failed to create audio streams: {e}")
            raise

    def _input_callback(self, indata, frames, time_info, status):
        """
        Recording callback, called by hardware driver Processing flow: Raw audio -> Resample 16kHz -> Encode send + Wake word detection.
        """
        if status and "overflow" not in str(status).lower():
            logger.warning(f"Input stream status: {status}")

        if self._is_closing:
            return

        try:
            audio_data = indata.copy().flatten()

            # Resample to 16kHz (if device is not 16kHz)
            if self.input_resampler is not None:
                audio_data = self._process_input_resampling(audio_data)
                if audio_data is None:
                    return

            # Apply AEC processing (only macOS needs)
            if (self._aec_enabled and len(audio_data) == AudioConfig.INPUT_FRAME_SIZE and self.aec_processor._is_macos):
                try:
                    audio_data = self.aec_processor.process_audio(audio_data)
                except Exception as e:
                    logger.warning(f"AEC processing failed, using raw audio: {e}")

            # Real-time encoding and send (not through queue, reduce latency)
            if len(audio_data) == AudioConfig.INPUT_FRAME_SIZE:
                try:
                    encoded_data = self.opus_encoder.encode(audio_data.tobytes(), AudioConfig.INPUT_FRAME_SIZE)
                    if self._encoded_audio_callback:
                        self._encoded_audio_callback(encoded_data)
                except Exception as e:
                    logger.warning(f"Audio encoding failed: {e}")

            # Add to wake word detection queue
            try:
                self._wakeword_buffer.put_nowait(audio_data)
            except asyncio.QueueFull:
                pass  # Drop oldest data when queue is full

        except Exception as e:
            logger.error(f"Input callback error: {e}")

    def _process_input_resampling(self, audio_data):
        """
        Process input resampling: device sample rate -> 16kHz.
        """
        try:
            self._resample_input_buffer.extend(audio_data)
            resampled_data = self.input_resampler.resample_chunk(
                np.array(self._resample_input_buffer, dtype=np.int16)
            )
            self._resample_input_buffer.clear()
            return resampled_data
        except Exception as e:
            logger.warning(f"Input resampling failed: {e}")
            return None

    def _input_finished_callback(self):
        """
        Input stream finished callback.
        """
        logger.info("Input stream finished")

    def _output_callback(self, outdata, frames, time_info, status):
        """
        Playback callback, called by hardware driver.
        Processing flow: Decoded audio -> Resample to device sample rate -> Play.
        """
        if status and "underflow" not in str(status).lower():
            logger.warning(f"Output stream status: {status}")

        if self._is_closing:
            return

        try:
            # Get audio data from output buffer
            try:
                audio_data = self._output_buffer.get_nowait()
            except asyncio.QueueEmpty:
                # Fill with silence when no data
                outdata[:] = np.zeros((frames, AudioConfig.CHANNELS), dtype=np.int16)
                return

            # Resample to device sample rate (if needed)
            if self.output_resampler is not None:
                audio_data = self._process_output_resampling(audio_data)
                if audio_data is None:
                    outdata[:] = np.zeros((frames, AudioConfig.CHANNELS), dtype=np.int16)
                    return

            # Ensure correct shape and size
            if len(audio_data) >= frames:
                outdata[:] = audio_data[:frames].reshape(-1, AudioConfig.CHANNELS)
            else:
                # Pad with silence if data is insufficient
                padded_data = np.zeros(frames * AudioConfig.CHANNELS, dtype=np.int16)
                padded_data[: len(audio_data)] = audio_data
                outdata[:] = padded_data.reshape(-1, AudioConfig.CHANNELS)

        except Exception as e:
            logger.error(f"Output callback error: {e}")
            outdata[:] = np.zeros((frames, AudioConfig.CHANNELS), dtype=np.int16)

    def _process_output_resampling(self, audio_data):
        """
        Process output resampling: 24kHz -> device sample rate.
        """
        try:
            self._resample_output_buffer.extend(audio_data)
            resampled_data = self.output_resampler.resample_chunk(
                np.array(self._resample_output_buffer, dtype=np.int16)
            )
            self._resample_output_buffer.clear()
            return resampled_data
        except Exception as e:
            logger.warning(f"Output resampling failed: {e}")
            return None

    def _output_finished_callback(self):
        """
        Output stream finished callback.
        """
        logger.info("Output stream finished")

    async def close(self):
        """
        Close audio streams and release resources.
        """
        self._is_closing = True

        try:
            if self.input_stream:
                self.input_stream.stop()
                self.input_stream.close()
                self.input_stream = None

            if self.output_stream:
                self.output_stream.stop()
                self.output_stream.close()
                self.output_stream = None

            # Clear queues
            while not self._wakeword_buffer.empty():
                try:
                    self._wakeword_buffer.get_nowait()
                except asyncio.QueueEmpty:
                    break

            while not self._output_buffer.empty():
                try:
                    self._output_buffer.get_nowait()
                except asyncio.QueueEmpty:
                    break

            # Close AEC processor
            if self._aec_enabled:
                await self.aec_processor.close()

            logger.info("Audio codec closed")
        except Exception as e:
            logger.error(f"Error closing audio codec: {e}")

        # Force garbage collection
        gc.collect()

    def set_encoded_audio_callback(self, callback):
        """
        Set real-time encoded audio callback.
        """
        self._encoded_audio_callback = callback

    async def get_wakeword_audio(self):
        """
        Get audio data for wake word detection.
        """
        try:
            return await asyncio.wait_for(self._wakeword_buffer.get(), timeout=1.0)
        except asyncio.TimeoutError:
            return None

    async def play_audio(self, audio_data: bytes):
        """
        Play decoded audio data.
        """
        try:
            if self.opus_decoder is None:
                logger.warning("Opus decoder not initialized")
                return

            # Decode audio
            decoded_data = self.opus_decoder.decode(audio_data, AudioConfig.OUTPUT_FRAME_SIZE)
            audio_array = np.frombuffer(decoded_data, dtype=np.int16)

            # Add to output buffer
            try:
                self._output_buffer.put_nowait(audio_array)
            except asyncio.QueueFull:
                logger.warning("Output buffer full, dropping audio data")
        except Exception as e:
            logger.error(f"Audio playback error: {e}")

    def is_initialized(self):
        """
        Check if audio codec is initialized.
        """
        return (
            self.input_stream is not None
            and self.output_stream is not None
            and self.opus_encoder is not None
            and self.opus_decoder is not None
        )
