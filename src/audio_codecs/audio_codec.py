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
    1. Recording: Microphone -> Resample to 16kHz -> Opus encoding -> Send
    2. Playback: Receive -> Opus decode to 24kHz -> Playback queue -> Speaker
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

        # Resamplers: Recording resampled to 16kHz, playback resampled to device sample rate
        self.input_resampler = None  # Device sample rate -> 16kHz
        self.output_resampler = None  # 24kHz -> Device sample rate (for playback)

        # Resampling buffers
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

        # 2) Fallback: Match by system default (kind) returned name + prefer WASAPI
        try:
            default_info = sd.query_devices(kind=kind)  # Will not trigger -1
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
            if any(k in d["name"] for k in ["Speaker", "扬声器", "Realtek", "USB", "AMD", "HDMI", "Monitor"]):
                score += 1
            scored.append((score, i))

        if scored:
            scored.sort(reverse=True)
            return scored[0][1]

        # 3) Final fallback: First device with available channels
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
            # Display and select audio devices (automatically selected and written to config on first run; not overwritten afterwards)
            await self._select_audio_devices()

            # Safely get input/output default information (avoid -1)
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

            # Do not force global defaults, let each stream carry its own device/samplerate
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
        Prefer devices from configuration file, if not available then automatically select and save to config (only written on first run, not overwritten afterwards).
        """
        try:
            audio_config = self.config.get_config("AUDIO_DEVICES", {}) or {}

            # Whether there is already explicit configuration (determines whether to write back)
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
                            logger.warning(f"Configured device [{input_device_id}] does not support input, will auto-select")
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
                            logger.warning(f"Configured device [{output_device_id}] does not support output, will auto-select")
                            self.speaker_device_id = None
                    else:
                        logger.warning(f"Configured output device ID [{output_device_id}] is invalid, will auto-select")
                        self.speaker_device_id = None
                except Exception as e:
                    logger.warning(f"Failed to validate configured output device: {e}, will auto-select")
                    self.speaker_device_id = None
            else:
                self.speaker_device_id = None

            # --- If any is empty, auto-select (only written to config on first run) ---
            picked_input = self.mic_device_id
            picked_output = self.speaker_device_id

            if picked_input is None:
                picked_input = self._auto_pick_device("input")
                if picked_input is not None:
                    self.mic_device_id = picked_input
                    d = devices[picked_input]
                    logger.info(f"Auto-selected microphone device: [{picked_input}] {d['name']}")
                else:
                    logger.warning("No available input device found (will use system default and not write index).")

            if picked_output is None:
                picked_output = self._auto_pick_device("output")
                if picked_output is not None:
                    self.speaker_device_id = picked_output
                    d = devices[picked_output]
                    logger.info(f"Auto-selected speaker device: [{picked_output}] {d['name']}")
                else:
                    logger.warning("No available output device found (will use system default and not write index).")

            # --- Only write when configuration originally lacked corresponding entries (avoid overwriting on second run) ---
            need_write = (not had_cfg_input and picked_input is not None) or (not had_cfg_output and picked_output is not None)
            if need_write:
                await self._save_default_audio_config(
                    input_device_id=picked_input if not had_cfg_input else None,
                    output_device_id=picked_output if not had_cfg_output else None,
                )

        except Exception as e:
            logger.warning(f"Device selection failed: {e}, will use system default (not writing to config)")
            # Allow None, let PortAudio use system default endpoints
            self.mic_device_id = self.mic_device_id if isinstance(self.mic_device_id, int) else None
            self.speaker_device_id = self.speaker_device_id if isinstance(self.speaker_device_id, int) else None

    async def _save_default_audio_config(self, input_device_id: Optional[int], output_device_id: Optional[int]):
        """
        Save default audio device configuration to config file (only for non-empty devices passed in; will not overwrite existing fields).
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
                # merge: Do not overwrite existing keys
                current = self.config.get_config("AUDIO_DEVICES", {}) or {}
                for k, v in audio_config_patch.items():
                    if k not in current:  # Only write when originally not present
                        current[k] = v
                success = self.config.update_config("AUDIO_DEVICES", current)
                if success:
                    logger.info("Default audio devices written to configuration (first time).")
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
        Recording callback, called by hardware driver. Processing flow: Raw audio -> Resample to 16kHz -> Encoding send + Wake word detection.
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

            # Apply AEC processing (only needed for macOS)
            if (self._aec_enabled and len(audio_data) == AudioConfig.INPUT_FRAME_SIZE and self.aec_processor._is_macos):
                try:
                    audio_data = self.aec_processor.process_audio(audio_data)
                except Exception as e:
                    logger.warning(f"AEC processing failed, using raw audio: {e}")

            # Real-time encoding and sending (not through queue, reduces latency)
            if (
                self._encoded_audio_callback
                and len(audio_data) == AudioConfig.INPUT_FRAME_SIZE
            ):
                try:
                    pcm_data = audio_data.astype(np.int16).tobytes()
                    encoded_data = self.opus_encoder.encode(
                        pcm_data, AudioConfig.INPUT_FRAME_SIZE
                    )
                    if encoded_data:
                        self._encoded_audio_callback(encoded_data)
                except Exception as e:
                    logger.warning(f"Real-time recording encoding failed: {e}")

            # Also provide to wake word detection (through queue)
            self._put_audio_data_safe(self._wakeword_buffer, audio_data.copy())

        except Exception as e:
            logger.error(f"Input callback error: {e}")

    def _process_input_resampling(self, audio_data):
        """
        Input resampling to 16kHz.
        """
        try:
            resampled_data = self.input_resampler.resample_chunk(audio_data, last=False)
            if len(resampled_data) > 0:
                self._resample_input_buffer.extend(resampled_data.astype(np.int16))

            expected_frame_size = AudioConfig.INPUT_FRAME_SIZE
            if len(self._resample_input_buffer) < expected_frame_size:
                return None

            frame_data = []
            for _ in range(expected_frame_size):
                frame_data.append(self._resample_input_buffer.popleft())

            return np.array(frame_data, dtype=np.int16)

        except Exception as e:
            logger.error(f"Input resampling failed: {e}")
            return None

    def _put_audio_data_safe(self, queue, audio_data):
        """
        Safe enqueue, discard oldest data when queue is full.
        """
        try:
            queue.put_nowait(audio_data)
        except asyncio.QueueFull:
            try:
                queue.get_nowait()
                queue.put_nowait(audio_data)
            except asyncio.QueueEmpty:
                queue.put_nowait(audio_data)

    def _output_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """
        Playback callback, called by hardware driver. Get data from playback queue and output to speaker.
        """
        if status:
            if "underflow" not in str(status).lower():
                logger.warning(f"Output stream status: {status}")

        try:
            if self.output_resampler is not None:
                # Need resampling: 24kHz -> Device sample rate
                self._output_callback_with_resample(outdata, frames)
            else:
                # Direct playback: 24kHz
                self._output_callback_direct(outdata, frames)

        except Exception as e:
            logger.error(f"Output callback error: {e}")
            outdata.fill(0)

    def _output_callback_direct(self, outdata: np.ndarray, frames: int):
        """
        Direct playback of 24kHz data (when device supports 24kHz)
        """
        try:
            # Get audio data from playback queue
            audio_data = self._output_buffer.get_nowait()

            if len(audio_data) >= frames * AudioConfig.CHANNELS:
                output_frames = audio_data[: frames * AudioConfig.CHANNELS]
                outdata[:] = output_frames.reshape(-1, AudioConfig.CHANNELS)
            else:
                out_len = len(audio_data) // AudioConfig.CHANNELS
                if out_len > 0:
                    outdata[:out_len] = audio_data[: out_len * AudioConfig.CHANNELS].reshape(
                        -1, AudioConfig.CHANNELS
                    )
                if out_len < frames:
                    outdata[out_len:] = 0

        except asyncio.QueueEmpty:
            # Output silence when no data
            outdata.fill(0)

    def _output_callback_with_resample(self, outdata: np.ndarray, frames: int):
        """
        Resampled playback (24kHz -> Device sample rate)
        """
        try:
            # Continuously process 24kHz data for resampling
            while len(self._resample_output_buffer) < frames * AudioConfig.CHANNELS:
                try:
                    audio_data = self._output_buffer.get_nowait()
                    # 24kHz -> Device sample rate resampling
                    resampled_data = self.output_resampler.resample_chunk(
                        audio_data, last=False
                    )
                    if len(resampled_data) > 0:
                        self._resample_output_buffer.extend(
                            resampled_data.astype(np.int16)
                        )
                except asyncio.QueueEmpty:
                    break

            need = frames * AudioConfig.CHANNELS
            if len(self._resample_output_buffer) >= need:
                frame_data = [self._resample_output_buffer.popleft() for _ in range(need)]
                output_array = np.array(frame_data, dtype=np.int16)
                outdata[:] = output_array.reshape(-1, AudioConfig.CHANNELS)
            else:
                # Output silence when data is insufficient
                outdata.fill(0)

        except Exception as e:
            logger.warning(f"Resampled output failed: {e}")
            outdata.fill(0)

    def _input_finished_callback(self):
        """
        Input stream finished.
        """
        logger.info("Input stream ended")

    def _reference_finished_callback(self):
        """
        Reference signal stream finished.
        """
        logger.info("Reference signal stream ended")

    def _output_finished_callback(self):
        """
        Output stream finished.
        """
        logger.info("Output stream ended")

    async def reinitialize_stream(self, is_input=True):
        """
        Reinitialize audio streams.
        """
        if self._is_closing:
            return False if is_input else None

        try:
            if is_input:
                if self.input_stream:
                    self.input_stream.stop()
                    self.input_stream.close()

                self.input_stream = sd.InputStream(
                    device=self.mic_device_id,  # <- Fix: Bring device index to avoid falling back to potentially unstable default endpoints
                    samplerate=self.device_input_sample_rate,
                    channels=AudioConfig.CHANNELS,
                    dtype=np.int16,
                    blocksize=self._device_input_frame_size,
                    callback=self._input_callback,
                    finished_callback=self._input_finished_callback,
                    latency="low",
                )
                self.input_stream.start()
                logger.info("Input stream reinitialized successfully")
                return True
            else:
                if self.output_stream:
                    self.output_stream.stop()
                    self.output_stream.close()

                # Select output sample rate based on device support
                if self.device_output_sample_rate == AudioConfig.OUTPUT_SAMPLE_RATE:
                    # Device supports 24kHz, use directly
                    output_sample_rate = AudioConfig.OUTPUT_SAMPLE_RATE
                    device_output_frame_size = AudioConfig.OUTPUT_FRAME_SIZE
                else:
                    # Device doesn't support 24kHz, use device default sample rate and enable resampling
                    output_sample_rate = self.device_output_sample_rate
                    device_output_frame_size = int(
                        self.device_output_sample_rate
                        * (AudioConfig.FRAME_DURATION / 1000)
                    )

                self.output_stream = sd.OutputStream(
                    device=self.speaker_device_id,  # Specify speaker device ID
                    samplerate=output_sample_rate,
                    channels=AudioConfig.CHANNELS,
                    dtype=np.int16,
                    blocksize=device_output_frame_size,
                    callback=self._output_callback,
                    finished_callback=self._output_finished_callback,
                    latency="low",
                )
                self.output_stream.start()
                logger.info("Output stream reinitialized successfully")
                return None
        except Exception as e:
            stream_type = "Input" if is_input else "Output"
            logger.error(f"{stream_type} stream reinitialization failed: {e}")
            if is_input:
                return False
            else:
                raise

    async def get_raw_audio_for_detection(self) -> Optional[bytes]:
        """
        Get wake word audio data.
        """
        try:
            if self._wakeword_buffer.empty():
                return None

            audio_data = self._wakeword_buffer.get_nowait()

            if hasattr(audio_data, "tobytes"):
                return audio_data.tobytes()
            elif hasattr(audio_data, "astype"):
                return audio_data.astype("int16").tobytes()
            else:
                return audio_data

        except asyncio.QueueEmpty:
            return None
        except Exception as e:
            logger.error(f"Failed to get wake word audio data: {e}")
            return None

    def set_encoded_audio_callback(self, callback):
        """
        Set encoding callback.
        """
        self._encoded_audio_callback = callback

        if callback:
            logger.info("Real-time encoding enabled")
        else:
            logger.info("Encoding callback disabled")

    def is_aec_enabled(self) -> bool:
        """
        Check if AEC is enabled.
        """
        return self._aec_enabled

    def get_aec_status(self) -> dict:
        """
        Get AEC status information.
        """
        if not self._aec_enabled or not self.aec_processor:
            return {"enabled": False, "reason": "AEC not enabled or initialization failed"}
        
        try:
            return {
                "enabled": True,
                **self.aec_processor.get_status()
            }
        except Exception as e:
            return {"enabled": False, "reason": f"Failed to get status: {e}"}

    def toggle_aec(self, enabled: bool) -> bool:
        """
        Toggle AEC enabled state.
        
        Args:
            enabled: Whether to enable AEC
            
        Returns:
            Actual AEC state
        """
        if not self.aec_processor:
            logger.warning("AEC processor not initialized, cannot toggle state")
            return False
        
        self._aec_enabled = enabled and self.aec_processor._is_initialized
        
        if enabled and not self._aec_enabled:
            logger.warning("Cannot enable AEC, processor not properly initialized")
        
        logger.info(f"AEC status: {'Enabled' if self._aec_enabled else 'Disabled'}")
        return self._aec_enabled

    async def write_audio(self, opus_data: bytes):
        """
        Decode audio and play. Network received Opus data -> Decode to 24kHz -> Playback queue.
        """
        try:
            # Opus decode to 24kHz PCM data
            pcm_data = self.opus_decoder.decode(
                opus_data, AudioConfig.OUTPUT_FRAME_SIZE
            )

            audio_array = np.frombuffer(pcm_data, dtype=np.int16)

            expected_length = AudioConfig.OUTPUT_FRAME_SIZE * AudioConfig.CHANNELS
            if len(audio_array) != expected_length:
                logger.warning(
                    f"Decoded audio length abnormal: {len(audio_array)}, expected: {expected_length}"
                )
                return

            # Put into playback queue
            self._put_audio_data_safe(self._output_buffer, audio_array)

        except opuslib.OpusError as e:
            logger.warning(f"Opus decoding failed, discarding this frame: {e}")
        except Exception as e:
            logger.warning(f"Audio write failed, discarding this frame: {e}")

    async def wait_for_audio_complete(self, timeout=10.0):
        """
        Wait for playback to complete.
        """
        start = time.time()

        while not self._output_buffer.empty() and time.time() - start < timeout:
            await asyncio.sleep(0.05)

        await asyncio.sleep(0.3)

        if not self._output_buffer.empty():
            output_remaining = self._output_buffer.qsize()
            logger.warning(f"Audio playback timeout, remaining queue - output: {output_remaining} frames")

    async def clear_audio_queue(self):
        """
        Clear audio queues.
        """
        cleared_count = 0

        queues_to_clear = [
            self._wakeword_buffer,
            self._output_buffer,
        ]

        for queue in queues_to_clear:
            while not queue.empty():
                try:
                    queue.get_nowait()
                    cleared_count += 1
                except asyncio.QueueEmpty:
                    break

        if self._resample_input_buffer:
            cleared_count += len(self._resample_input_buffer)
            self._resample_input_buffer.clear()

        if self._resample_output_buffer:
            cleared_count += len(self._resample_output_buffer)
            self._resample_output_buffer.clear()

        if cleared_count > 0:
            logger.info(f"Cleared audio queues, discarded {cleared_count} frames of audio data")

        if cleared_count > 100:
            gc.collect()
            logger.debug("Executed garbage collection to free memory")

    async def start_streams(self):
        """
        Start audio streams.
        """
        try:
            if self.input_stream and not self.input_stream.active:
                try:
                    self.input_stream.start()
                except Exception as e:
                    logger.warning(f"Error starting input stream: {e}")
                    await self.reinitialize_stream(is_input=True)

            if self.output_stream and not self.output_stream.active:
                try:
                    self.output_stream.start()
                except Exception as e:
                    logger.warning(f"Error starting output stream: {e}")
                    await self.reinitialize_stream(is_input=False)

            logger.info("Audio streams started")
        except Exception as e:
            logger.error(f"Failed to start audio streams: {e}")

    async def stop_streams(self):
        """
        Stop audio streams.
        """
        try:
            if self.input_stream and self.input_stream.active:
                self.input_stream.stop()
        except Exception as e:
            logger.warning(f"Failed to stop input stream: {e}")

        try:
            if self.output_stream and self.output_stream.active:
                self.output_stream.stop()
        except Exception as e:
            logger.warning(f"Failed to stop output stream: {e}")

    async def _cleanup_resampler(self, resampler, name):
        """
        Clean up resampler.
        """
        if resampler:
            try:
                if hasattr(resampler, "resample_chunk"):
                    empty_array = np.array([], dtype=np.int16)
                    resampler.resample_chunk(empty_array, last=True)
            except Exception as e:
                logger.warning(f"Failed to clean up {name} resampler: {e}")

    async def close(self):
        """
        Close audio codec.
        """
        if self._is_closing:
            return

        self._is_closing = True
        logger.info("Starting to close audio codec...")

        try:
            await self.clear_audio_queue()

            if self.input_stream:
                try:
                    self.input_stream.stop()
                    self.input_stream.close()
                except Exception as e:
                    logger.warning(f"Failed to close input stream: {e}")
                finally:
                    self.input_stream = None

            if self.output_stream:
                try:
                    self.output_stream.stop()
                    self.output_stream.close()
                except Exception as e:
                    logger.warning(f"Failed to close output stream: {e}")
                finally:
                    self.output_stream = None

            await self._cleanup_resampler(self.input_resampler, "input")
            await self._cleanup_resampler(self.output_resampler, "output")
            self.input_resampler = None
            self.output_resampler = None

            self._resample_input_buffer.clear()
            self._resample_output_buffer.clear()

            # Close AEC processor
            if self.aec_processor:
                try:
                    await self.aec_processor.close()
                except Exception as e:
                    logger.warning(f"Failed to close AEC processor: {e}")
                finally:
                    self.aec_processor = None

            self.opus_encoder = None
            self.opus_decoder = None

            gc.collect()

            logger.info("Audio resources fully released")
        except Exception as e:
            logger.error(f"Error occurred while closing audio codec: {e}")
        finally:
            self._is_closing = True

    def __del__(self):
        """
        Destructor.
        """
        if not self._is_closing:
            logger.warning("AudioCodec not properly closed, please call close()")
