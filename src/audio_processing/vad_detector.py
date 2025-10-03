import logging
import threading
import time

import numpy as np
import pyaudio
import webrtcvad

from src.constants.constants import AbortReason, DeviceState

# Configure logging
logger = logging.getLogger("VADDetector")


class VADDetector:
    """
    WebRTC VAD-based voice activity detector for detecting user interruptions.
    """

    def __init__(self, audio_codec, protocol, app_instance, loop):
        """Initialize VAD detector.

        Args:
            audio_codec: Audio codec instance
            protocol: Communication protocol instance
            app_instance: Application instance
            loop: Event loop
        """
        self.audio_codec = audio_codec
        self.protocol = protocol
        self.app = app_instance
        self.loop = loop

        # VAD settings
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)  # Set highest sensitivity

        # Parameter settings
        self.sample_rate = 16000
        self.frame_duration = 20  # milliseconds
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        self.speech_window = 5  # How many consecutive speech frames to trigger interruption
        self.energy_threshold = 300  # Energy threshold

        # State variables
        self.running = False
        self.paused = False
        self.thread = None
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False

        # Create independent PyAudio instance and stream to avoid conflicts with main audio stream
        self.pa = None
        self.stream = None

    def start(self):
        """
        Start VAD detector.
        """
        if self.thread and self.thread.is_alive():
            logger.warning("VAD detector is already running")
            return

        self.running = True
        self.paused = False

        # Initialize PyAudio and stream
        self._initialize_audio_stream()

        # Start detection thread
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        logger.info("VAD detector started")

    def stop(self):
        """
        Stop VAD detector.
        """
        self.running = False

        # Close audio stream
        self._close_audio_stream()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

        logger.info("VAD detector stopped")

    def pause(self):
        """
        Pause VAD detection.
        """
        self.paused = True
        logger.info("VAD detector paused")

    def resume(self):
        """
        Resume VAD detection.
        """
        self.paused = False
        # Reset state
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False
        logger.info("VAD detector resumed")

    def is_running(self):
        """
        Check if VAD detector is running.
        """
        return self.running and not self.paused

    def _initialize_audio_stream(self):
        """
        Initialize independent audio stream.
        """
        try:
            # Create PyAudio instance
            self.pa = pyaudio.PyAudio()

            # Get default input device
            device_index = None
            for i in range(self.pa.get_device_count()):
                device_info = self.pa.get_device_info_by_index(i)
                if device_info["maxInputChannels"] > 0:
                    device_index = i
                    break

            if device_index is None:
                logger.error("No available input device found")
                return False

            # Create input stream
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.frame_size,
                start=True,
            )

            logger.info(f"VAD detector audio stream initialized, using device index: {device_index}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize VAD audio stream: {e}")
            return False

    def _close_audio_stream(self):
        """
        Close audio stream.
        """
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            if self.pa:
                self.pa.terminate()
                self.pa = None

            logger.info("VAD detector audio stream closed")
        except Exception as e:
            logger.error(f"Failed to close VAD audio stream: {e}")

    def _detection_loop(self):
        """
        VAD detection main loop.
        """
        logger.info("VAD detection loop started")

        while self.running:
            # Skip if paused or audio stream not initialized
            if self.paused or not self.stream:
                time.sleep(0.1)
                continue

            try:
                # Only detect during speaking state
                if self.app.device_state == DeviceState.SPEAKING:
                    # Read audio frame
                    frame = self._read_audio_frame()
                    if not frame:
                        time.sleep(0.01)
                        continue

                    # Detect if it's speech
                    is_speech = self._detect_speech(frame)

                    # If speech detected and trigger condition met, handle interruption
                    if is_speech:
                        self._handle_speech_frame(frame)
                    else:
                        self._handle_silence_frame(frame)
                else:
                    # Not in speaking state, reset state
                    self._reset_state()

            except Exception as e:
                logger.error(f"VAD detection loop error: {e}")

            time.sleep(0.01)  # Small delay to reduce CPU usage

        logger.info("VAD detection loop ended")

    def _read_audio_frame(self):
        """
        Read one frame of audio data.
        """
        try:
            if not self.stream or not self.stream.is_active():
                return None

            # Read audio data
            data = self.stream.read(self.frame_size, exception_on_overflow=False)
            return data
        except Exception as e:
            logger.error(f"Failed to read audio frame: {e}")
            return None

    def _detect_speech(self, frame):
        """
        Detect if it's speech.
        """
        try:
            # Ensure frame length is correct
            if len(frame) != self.frame_size * 2:  # 16-bit audio, 2 bytes per sample
                return False

            # Use VAD detection
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            # Calculate audio energy
            audio_data = np.frombuffer(frame, dtype=np.int16)
            energy = np.mean(np.abs(audio_data))

            # Combine VAD and energy threshold
            is_valid_speech = is_speech and energy > self.energy_threshold

            if is_valid_speech:
                logger.debug(
                    f"Speech detected [energy: {energy:.2f}] [consecutive speech frames: {self.speech_count+1}]"
                )

            return is_valid_speech
        except Exception as e:
            logger.error(f"Failed to detect speech: {e}")
            return False

    def _handle_speech_frame(self, frame):
        """
        Handle speech frame.
        """
        self.speech_count += 1
        self.silence_count = 0

        # Detect enough consecutive speech frames, trigger interruption
        if self.speech_count >= self.speech_window and not self.triggered:
            self.triggered = True
            logger.info("Continuous speech detected, triggering interruption!")
            self._trigger_interrupt()

            # Immediately pause itself to prevent repeated triggering
            self.paused = True
            logger.info("VAD detector automatically paused to prevent repeated triggering")

            # Reset state
            self.speech_count = 0
            self.silence_count = 0
            self.triggered = False

    def _handle_silence_frame(self, frame):
        """
        Handle silence frame.
        """
        self.silence_count += 1
        self.speech_count = 0

    def _reset_state(self):
        """
        Reset state.
        """
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False

    def _trigger_interrupt(self):
        """
        Trigger interruption.
        """
        # Notify application to abort current speech output
        self.app.schedule(
            lambda: self.app.abort_speaking(AbortReason.WAKE_WORD_DETECTED)
        )
