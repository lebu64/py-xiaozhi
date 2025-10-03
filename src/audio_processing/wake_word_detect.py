import asyncio
import time
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import sherpa_onnx

from src.constants.constants import AudioConfig
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.resource_finder import resource_finder

logger = get_logger(__name__)


class WakeWordDetector:

    def __init__(self):
        # Basic properties
        self.audio_codec = None
        self.is_running_flag = False
        self.paused = False
        self.detection_task = None

        # Anti-repeat trigger mechanism - shorten cooldown time for better response
        self.last_detection_time = 0
        self.detection_cooldown = 1.5  # 1.5 second cooldown

        # Callback functions
        self.on_detected_callback: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

        # Configuration check
        config = ConfigManager.get_instance()
        if not config.get_config("WAKE_WORD_OPTIONS.USE_WAKE_WORD", False):
            logger.info("Wake word feature disabled")
            self.enabled = False
            return

        # Basic parameter initialization
        self.enabled = True
        self.sample_rate = AudioConfig.INPUT_SAMPLE_RATE

        # Sherpa-ONNX KWS components
        self.keyword_spotter = None
        self.stream = None

        # Initialize configuration
        self._load_config(config)
        self._init_kws_model()
        self._validate_config()

    def _load_config(self, config):
        """
        Load configuration parameters.
        """
        # Model path configuration
        model_path = config.get_config("WAKE_WORD_OPTIONS.MODEL_PATH", "models")
        self.model_dir = resource_finder.find_directory(model_path)

        if self.model_dir is None:
            # Fallback: try to use path directly
            self.model_dir = Path(model_path)
            logger.warning(
                f"ResourceFinder did not find model directory, using original path: {self.model_dir}"
            )

        # KWS parameter configuration - optimized for speed
        self.num_threads = config.get_config(
            "WAKE_WORD_OPTIONS.NUM_THREADS", 4
        )  # Increase thread count
        self.provider = config.get_config("WAKE_WORD_OPTIONS.PROVIDER", "cpu")
        self.max_active_paths = config.get_config(
            "WAKE_WORD_OPTIONS.MAX_ACTIVE_PATHS", 2
        )  # Reduce search paths
        self.keywords_score = config.get_config(
            "WAKE_WORD_OPTIONS.KEYWORDS_SCORE", 1.8
        )  # Lower score for faster speed
        self.keywords_threshold = config.get_config(
            "WAKE_WORD_OPTIONS.KEYWORDS_THRESHOLD", 0.2
        )  # Lower threshold for higher sensitivity
        self.num_trailing_blanks = config.get_config(
            "WAKE_WORD_OPTIONS.NUM_TRAILING_BLANKS", 1
        )

        logger.info(
            f"KWS configuration loaded - threshold: {self.keywords_threshold}, score: {self.keywords_score}"
        )

    def _init_kws_model(self):
        """
        Initialize Sherpa-ONNX KeywordSpotter model.
        """
        try:
            # Check model files
            encoder_path = self.model_dir / "encoder.onnx"
            decoder_path = self.model_dir / "decoder.onnx"
            joiner_path = self.model_dir / "joiner.onnx"
            tokens_path = self.model_dir / "tokens.txt"
            keywords_path = self.model_dir / "keywords.txt"

            required_files = [
                encoder_path,
                decoder_path,
                joiner_path,
                tokens_path,
                keywords_path,
            ]
            for file_path in required_files:
                if not file_path.exists():
                    raise FileNotFoundError(f"Model file does not exist: {file_path}")

            logger.info(f"Loading Sherpa-ONNX KeywordSpotter model: {self.model_dir}")

            # Create KeywordSpotter
            self.keyword_spotter = sherpa_onnx.KeywordSpotter(
                tokens=str(tokens_path),
                encoder=str(encoder_path),
                decoder=str(decoder_path),
                joiner=str(joiner_path),
                keywords_file=str(keywords_path),
                num_threads=self.num_threads,
                sample_rate=self.sample_rate,
                feature_dim=80,
                max_active_paths=self.max_active_paths,
                keywords_score=self.keywords_score,
                keywords_threshold=self.keywords_threshold,
                num_trailing_blanks=self.num_trailing_blanks,
                provider=self.provider,
            )

            logger.info("Sherpa-ONNX KeywordSpotter model loaded successfully")

        except Exception as e:
            logger.error(f"Sherpa-ONNX KeywordSpotter initialization failed: {e}", exc_info=True)
            self.enabled = False

    def on_detected(self, callback: Callable):
        """
        Set callback function for detected wake word.
        """
        self.on_detected_callback = callback

    async def start(self, audio_codec) -> bool:
        """
        Start wake word detector.
        """
        if not self.enabled:
            logger.warning("Wake word feature not enabled")
            return False

        if not self.keyword_spotter:
            logger.error("KeywordSpotter not initialized")
            return False

        try:
            self.audio_codec = audio_codec
            self.is_running_flag = True
            self.paused = False

            # Create detection stream
            self.stream = self.keyword_spotter.create_stream()

            # Start detection task
            self.detection_task = asyncio.create_task(self._detection_loop())

            logger.info("Sherpa-ONNX KeywordSpotter detector started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start KeywordSpotter detector: {e}")
            self.enabled = False
            return False

    async def _detection_loop(self):
        """
        Detection loop.
        """
        error_count = 0
        MAX_ERRORS = 5

        while self.is_running_flag:
            try:
                if self.paused:
                    await asyncio.sleep(0.1)
                    continue

                if not self.audio_codec:
                    await asyncio.sleep(0.5)
                    continue

                # Process audio data
                await self._process_audio()

                # Reduce delay for better response speed
                await asyncio.sleep(0.005)
                error_count = 0

            except asyncio.CancelledError:
                break
            except Exception as e:
                error_count += 1
                logger.error(f"KWS detection loop error({error_count}/{MAX_ERRORS}): {e}")

                # Call error callback
                if self.on_error:
                    try:
                        if asyncio.iscoroutinefunction(self.on_error):
                            await self.on_error(e)
                        else:
                            self.on_error(e)
                    except Exception as callback_error:
                        logger.error(f"Failed to execute error callback: {callback_error}")

                if error_count >= MAX_ERRORS:
                    logger.critical("Reached maximum error count, stopping KWS detection")
                    break
                await asyncio.sleep(1)

    async def _process_audio(self):
        """Process audio data - batch processing optimization"""
        try:
            if not self.audio_codec or not self.stream:
                return

            # Batch get multiple audio frames for efficiency
            audio_batches = []
            for _ in range(3):  # Process up to 3 frames at once
                data = await self.audio_codec.get_raw_audio_for_detection()
                if data:
                    audio_batches.append(data)

            if not audio_batches:
                return

            # Batch process audio data
            for data in audio_batches:
                # Convert audio format
                if isinstance(data, bytes):
                    samples = (
                        np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                    )
                else:
                    samples = np.array(data, dtype=np.float32)

                # Provide audio data to KeywordSpotter
                self.stream.accept_waveform(
                    sample_rate=self.sample_rate, waveform=samples
                )

            # Process detection results
            while self.keyword_spotter.is_ready(self.stream):
                self.keyword_spotter.decode_stream(self.stream)
                result = self.keyword_spotter.get_result(self.stream)

                if result:
                    await self._handle_detection_result(result)
                    # Reset stream state
                    self.keyword_spotter.reset_stream(self.stream)
                    break  # Process immediately after detection, don't continue batch processing

        except Exception as e:
            logger.debug(f"KWS audio processing error: {e}")

    async def _handle_detection_result(self, result):
        """
        Handle detection result.
        """
        # Anti-repeat trigger check
        current_time = time.time()
        if current_time - self.last_detection_time < self.detection_cooldown:
            return

        self.last_detection_time = current_time

        # Trigger callback
        if self.on_detected_callback:
            try:
                if asyncio.iscoroutinefunction(self.on_detected_callback):
                    await self.on_detected_callback(result, result)
                else:
                    self.on_detected_callback(result, result)
            except Exception as e:
                logger.error(f"Wake word callback execution failed: {e}")

    async def stop(self):
        """
        Stop detector.
        """
        self.is_running_flag = False

        if self.detection_task:
            self.detection_task.cancel()
            try:
                await self.detection_task
            except asyncio.CancelledError:
                pass

        logger.info("Sherpa-ONNX KeywordSpotter detector stopped")

    async def pause(self):
        """
        Pause detection.
        """
        self.paused = True
        logger.debug("KWS detection paused")

    async def resume(self):
        """
        Resume detection.
        """
        self.paused = False
        logger.debug("KWS detection resumed")

    def is_running(self) -> bool:
        """
        Check if running.
        """
        return self.is_running_flag and not self.paused

    def _validate_config(self):
        """
        Validate configuration parameters.
        """
        if not self.enabled:
            return

        # Validate threshold parameters
        if not 0.1 <= self.keywords_threshold <= 1.0:
            logger.warning(f"Keyword threshold {self.keywords_threshold} out of range, reset to 0.25")
            self.keywords_threshold = 0.25

        if not 0.1 <= self.keywords_score <= 10.0:
            logger.warning(f"Keyword score {self.keywords_score} out of range, reset to 2.0")
            self.keywords_score = 2.0

        logger.info(
            f"KWS configuration validation completed - threshold: {self.keywords_threshold}, score: {self.keywords_score}"
        )

    def get_performance_stats(self):
        """
        Get performance statistics.
        """
        return {
            "enabled": self.enabled,
            "engine": "sherpa-onnx-kws",
            "provider": self.provider,
            "num_threads": self.num_threads,
            "keywords_threshold": self.keywords_threshold,
            "keywords_score": self.keywords_score,
            "is_running": self.is_running(),
        }

    def clear_cache(self):
        """
        Clear cache.
        """
