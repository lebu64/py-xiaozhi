import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger


class AudioWidget(QWidget):
    """
    Audio device settings component.
    """

    # Signal definitions
    settings_changed = pyqtSignal()
    status_message = pyqtSignal(str)
    reset_input_ui = pyqtSignal()
    reset_output_ui = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # UI control references
        self.ui_controls = {}

        # Device data
        self.input_devices = []
        self.output_devices = []

        # Testing status
        self.testing_input = False
        self.testing_output = False

        # Initialize UI
        self._setup_ui()
        self._connect_events()
        self._scan_devices()
        self._load_config_values()

        # Connect thread-safe UI update signals
        try:
            self.status_message.connect(self._on_status_message)
            self.reset_input_ui.connect(self._reset_input_test_ui)
            self.reset_output_ui.connect(self._reset_output_test_ui)
        except Exception:
            pass

    def _setup_ui(self):
        """
        Setup UI interface.
        """
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "audio_widget.ui"
            uic.loadUi(str(ui_path), self)

            # Get UI control references
            self._get_ui_controls()

        except Exception as e:
            self.logger.error(f"Failed to setup audio UI: {e}", exc_info=True)
            raise

    def _get_ui_controls(self):
        """
        Get UI control references.
        """
        self.ui_controls.update({
            "input_device_combo": self.findChild(QComboBox, "input_device_combo"),
            "output_device_combo": self.findChild(QComboBox, "output_device_combo"),
            "input_info_label": self.findChild(QLabel, "input_info_label"),
            "output_info_label": self.findChild(QLabel, "output_info_label"),
            "test_input_btn": self.findChild(QPushButton, "test_input_btn"),
            "test_output_btn": self.findChild(QPushButton, "test_output_btn"),
            "scan_devices_btn": self.findChild(QPushButton, "scan_devices_btn"),
            "status_text": self.findChild(QTextEdit, "status_text"),
        })

    def _connect_events(self):
        """
        Connect event handlers.
        """
        # Device selection changes
        if self.ui_controls["input_device_combo"]:
            self.ui_controls["input_device_combo"].currentTextChanged.connect(self._on_input_device_changed)

        if self.ui_controls["output_device_combo"]:
            self.ui_controls["output_device_combo"].currentTextChanged.connect(self._on_output_device_changed)

        # Button clicks
        if self.ui_controls["test_input_btn"]:
            self.ui_controls["test_input_btn"].clicked.connect(self._test_input_device)

        if self.ui_controls["test_output_btn"]:
            self.ui_controls["test_output_btn"].clicked.connect(self._test_output_device)

        if self.ui_controls["scan_devices_btn"]:
            self.ui_controls["scan_devices_btn"].clicked.connect(self._scan_devices)

    def _on_input_device_changed(self):
        """
        Input device change event.
        """
        self.settings_changed.emit()
        self._update_device_info()

    def _on_output_device_changed(self):
        """
        Output device change event.
        """
        self.settings_changed.emit()
        self._update_device_info()

    def _update_device_info(self):
        """
        Update device information display.
        """
        try:
            # Update input device information
            input_device_id = self.ui_controls["input_device_combo"].currentData()
            if input_device_id is not None:
                input_device = next((d for d in self.input_devices if d['id'] == input_device_id), None)
                if input_device:
                    info_text = f"Sample Rate: {int(input_device['sample_rate'])}Hz, Channels: {input_device['channels']}"
                    self.ui_controls["input_info_label"].setText(info_text)
                else:
                    self.ui_controls["input_info_label"].setText("Failed to get device information")
            else:
                self.ui_controls["input_info_label"].setText("No device selected")

            # Update output device information
            output_device_id = self.ui_controls["output_device_combo"].currentData()
            if output_device_id is not None:
                output_device = next((d for d in self.output_devices if d['id'] == output_device_id), None)
                if output_device:
                    info_text = f"Sample Rate: {int(output_device['sample_rate'])}Hz, Channels: {output_device['channels']}"
                    self.ui_controls["output_info_label"].setText(info_text)
                else:
                    self.ui_controls["output_info_label"].setText("Failed to get device information")
            else:
                self.ui_controls["output_info_label"].setText("No device selected")

        except Exception as e:
            self.logger.error(f"Failed to update device information: {e}", exc_info=True)

    def _scan_devices(self):
        """
        Scan audio devices.
        """
        try:
            self._append_status("Scanning audio devices...")

            # Clear existing device lists
            self.input_devices.clear()
            self.output_devices.clear()

            # Get system default devices
            default_input = sd.default.device[0] if sd.default.device else None
            default_output = sd.default.device[1] if sd.default.device else None

            # Scan all devices
            devices = sd.query_devices()
            for i, dev_info in enumerate(devices):
                device_name = dev_info['name']

                # Add input devices
                if dev_info['max_input_channels'] > 0:
                    default_mark = " (default)" if i == default_input else ""
                    self.input_devices.append({
                        'id': i,
                        'name': device_name + default_mark,
                        'raw_name': device_name,
                        'channels': dev_info['max_input_channels'],
                        'sample_rate': dev_info['default_samplerate']
                    })

                # Add output devices
                if dev_info['max_output_channels'] > 0:
                    default_mark = " (default)" if i == default_output else ""
                    self.output_devices.append({
                        'id': i,
                        'name': device_name + default_mark,
                        'raw_name': device_name,
                        'channels': dev_info['max_output_channels'],
                        'sample_rate': dev_info['default_samplerate']
                    })

            # Update dropdowns
            self._update_device_combos()

            # Auto-select default devices
            self._select_default_devices()

            self._append_status(f"Scan completed: found {len(self.input_devices)} input devices, {len(self.output_devices)} output devices")

        except Exception as e:
            self.logger.error(f"Failed to scan audio devices: {e}", exc_info=True)
            self._append_status(f"Device scan failed: {str(e)}")

    def _update_device_combos(self):
        """
        Update device dropdowns.
        """
        try:
            # Save current selections
            current_input = self.ui_controls["input_device_combo"].currentData()
            current_output = self.ui_controls["output_device_combo"].currentData()

            # Clear and refill input devices
            self.ui_controls["input_device_combo"].clear()
            for device in self.input_devices:
                self.ui_controls["input_device_combo"].addItem(device['name'], device['id'])

            # Clear and refill output devices
            self.ui_controls["output_device_combo"].clear()
            for device in self.output_devices:
                self.ui_controls["output_device_combo"].addItem(device['name'], device['id'])

            # Try to restore previous selections
            if current_input is not None:
                index = self.ui_controls["input_device_combo"].findData(current_input)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)

            if current_output is not None:
                index = self.ui_controls["output_device_combo"].findData(current_output)
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)

        except Exception as e:
            self.logger.error(f"Failed to update device dropdowns: {e}", exc_info=True)

    def _select_default_devices(self):
        """
        Auto-select default devices (consistent with audio_codec.py logic).
        """
        try:
            # Prefer devices from configuration, otherwise use system defaults
            config_input_id = self.config_manager.get_config("AUDIO_DEVICES.input_device_id")
            config_output_id = self.config_manager.get_config("AUDIO_DEVICES.output_device_id")

            # Select input device
            if config_input_id is not None:
                # Use device from configuration
                index = self.ui_controls["input_device_combo"].findData(config_input_id)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)
            else:
                # Auto-select default input device (with "default" mark)
                for i in range(self.ui_controls["input_device_combo"].count()):
                    if "default" in self.ui_controls["input_device_combo"].itemText(i):
                        self.ui_controls["input_device_combo"].setCurrentIndex(i)
                        break

            # Select output device
            if config_output_id is not None:
                # Use device from configuration
                index = self.ui_controls["output_device_combo"].findData(config_output_id)
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)
            else:
                # Auto-select default output device (with "default" mark)
                for i in range(self.ui_controls["output_device_combo"].count()):
                    if "default" in self.ui_controls["output_device_combo"].itemText(i):
                        self.ui_controls["output_device_combo"].setCurrentIndex(i)
                        break

            # Update device information display
            self._update_device_info()

        except Exception as e:
            self.logger.error(f"Failed to select default devices: {e}", exc_info=True)

    def _test_input_device(self):
        """
        Test input device.
        """
        if self.testing_input:
            return

        try:
            device_id = self.ui_controls["input_device_combo"].currentData()
            if device_id is None:
                QMessageBox.warning(self, "Prompt", "Please select an input device first")
                return

            self.testing_input = True
            self.ui_controls["test_input_btn"].setEnabled(False)
            self.ui_controls["test_input_btn"].setText("Recording...")

            # Execute test in thread
            test_thread = threading.Thread(target=self._do_input_test, args=(device_id,))
            test_thread.daemon = True
            test_thread.start()

        except Exception as e:
            self.logger.error(f"Failed to test input device: {e}", exc_info=True)
            self._append_status(f"Input device test failed: {str(e)}")
            self._reset_input_test_ui()

    def _do_input_test(self, device_id):
        """
        Execute input device test.
        """
        try:
            # Get device information and sample rate
            input_device = next((d for d in self.input_devices if d['id'] == device_id), None)
            if not input_device:
                self._append_status_threadsafe("Error: Unable to get device information")
                return

            sample_rate = int(input_device['sample_rate'])
            duration = 3  # Recording duration 3 seconds

            self._append_status_threadsafe(f"Starting recording test (Device: {device_id}, Sample Rate: {sample_rate}Hz)")
            self._append_status_threadsafe("Please speak into the microphone, for example count numbers: 1, 2, 3...")

            # Countdown prompt
            for i in range(3, 0, -1):
                self._append_status_threadsafe(f"Starting recording in {i} seconds...")
                time.sleep(1)

            self._append_status_threadsafe("Recording, please speak... (3 seconds)")

            # Record
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                device=device_id,
                dtype=np.float32
            )
            sd.wait()

            self._append_status_threadsafe("Recording completed, analyzing...")

            # Analyze recording quality
            max_amplitude = np.max(np.abs(recording))
            rms = np.sqrt(np.mean(recording**2))

            # Detect voice activity
            frame_length = int(0.1 * sample_rate)  # 100ms frame
            frames = []
            for i in range(0, len(recording) - frame_length, frame_length):
                frame_rms = np.sqrt(np.mean(recording[i:i+frame_length]**2))
                frames.append(frame_rms)

            active_frames = sum(1 for f in frames if f > 0.01)  # Active frame count
            activity_ratio = active_frames / len(frames) if frames else 0

            # Test result analysis
            if max_amplitude < 0.001:
                self._append_status_threadsafe("[Failed] No audio signal detected")
                self._append_status_threadsafe("Please check: 1) Microphone connection 2) System volume 3) Microphone permissions")
            elif max_amplitude > 0.8:
                self._append_status_threadsafe("[Warning] Audio signal overload")
                self._append_status_threadsafe("Suggest lowering microphone gain or volume settings")
            elif activity_ratio < 0.1:
                self._append_status_threadsafe("[Warning] Audio detected but little voice activity")
                self._append_status_threadsafe("Please ensure speaking into microphone, or check microphone sensitivity")
            else:
                self._append_status_threadsafe("[Success] Recording test passed")
                self._append_status_threadsafe(f"Audio quality data: Max volume={max_amplitude:.1%}, Average volume={rms:.1%}, Activity={activity_ratio:.1%}")
                self._append_status_threadsafe("Microphone working normally")

        except Exception as e:
            self.logger.error(f"Recording test failed: {e}", exc_info=True)
            self._append_status_threadsafe(f"[Error] Recording test failed: {str(e)}")
            if "Permission denied" in str(e) or "access" in str(e).lower():
                self._append_status_threadsafe("May be a permission issue, please check system microphone permission settings")
        finally:
            # Reset UI state (switch back to main thread)
            self._reset_input_ui_threadsafe()

    def _test_output_device(self):
        """
        Test output device.
        """
        if self.testing_output:
            return

        try:
            device_id = self.ui_controls["output_device_combo"].currentData()
            if device_id is None:
                QMessageBox.warning(self, "Prompt", "Please select an output device first")
                return

            self.testing_output = True
            self.ui_controls["test_output_btn"].setEnabled(False)
            self.ui_controls["test_output_btn"].setText("Playing...")

            # Execute test in thread
            test_thread = threading.Thread(target=self._do_output_test, args=(device_id,))
            test_thread.daemon = True
            test_thread.start()

        except Exception as e:
            self.logger.error(f"Failed to test output device: {e}", exc_info=True)
            self._append_status(f"Output device test failed: {str(e)}")
            self._reset_output_test_ui()

    def _do_output_test(self, device_id):
        """
        Execute output device test.
        """
        try:
            # Get device information and sample rate
            output_device = next((d for d in self.output_devices if d['id'] == device_id), None)
            if not output_device:
                self._append_status_threadsafe("Error: Unable to get device information")
                return

            sample_rate = int(output_device['sample_rate'])
            duration = 2.0  # Playback duration
            frequency = 440  # 440Hz A tone

            self._append_status_threadsafe(f"Starting playback test (Device: {device_id}, Sample Rate: {sample_rate}Hz)")
            self._append_status_threadsafe("Please prepare headphones/speakers, test tone will play soon...")

            # Countdown prompt
            for i in range(3, 0, -1):
                self._append_status_threadsafe(f"Starting playback in {i} seconds...")
                time.sleep(1)

            self._append_status_threadsafe(f"Playing {frequency}Hz test tone ({duration} seconds)...")

            # Generate test audio (sine wave)
            t = np.linspace(0, duration, int(sample_rate * duration))
            # Add fade in/out effect to avoid clipping
            fade_samples = int(0.1 * sample_rate)  # 0.1 second fade in/out
            audio = 0.3 * np.sin(2 * np.pi * frequency * t)

            # Apply fade in/out
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

            # Play audio
            sd.play(audio, samplerate=sample_rate, device=device_id)
            sd.wait()

            self._append_status_threadsafe("Playback completed")
            self._append_status_threadsafe("Test explanation: If you hear a clear test tone, speakers/headphones are working normally")
            self._append_status_threadsafe("If no sound is heard, please check volume settings or select another output device")

        except Exception as e:
            self.logger.error(f"Playback test failed: {e}", exc_info=True)
            self._append_status_threadsafe(f"[Error] Playback test failed: {str(e)}")
        finally:
            # Reset UI state (switch back to main thread)
            self._reset_output_ui_threadsafe()

    def _reset_input_test_ui(self):
        """
        Reset input test UI state.
        """
        self.testing_input = False
        self.ui_controls["test_input_btn"].setEnabled(True)
        self.ui_controls["test_input_btn"].setText("Test Recording")

    def _reset_input_ui_threadsafe(self):
        try:
            self.reset_input_ui.emit()
        except Exception as e:
            self.logger.error(f"Thread-safe reset of input test UI failed: {e}")

    def _reset_output_test_ui(self):
        """
        Reset output test UI state.
        """
        self.testing_output = False
        self.ui_controls["test_output_btn"].setEnabled(True)
        self.ui_controls["test_output_btn"].setText("Test Playback")

    def _reset_output_ui_threadsafe(self):
        try:
            self.reset_output_ui.emit()
        except Exception as e:
            self.logger.error(f"Thread-safe reset of output test UI failed: {e}")

    def _append_status(self, message):
        """
        Add status information.
        """
        try:
            if self.ui_controls["status_text"]:
                current_time = time.strftime("%H:%M:%S")
                formatted_message = f"[{current_time}] {message}"
                self.ui_controls["status_text"].append(formatted_message)
                # Scroll to bottom
                self.ui_controls["status_text"].verticalScrollBar().setValue(
                    self.ui_controls["status_text"].verticalScrollBar().maximum()
                )
        except Exception as e:
            self.logger.error(f"Failed to add status information: {e}", exc_info=True)

    def _append_status_threadsafe(self, message):
        """
        Thread-safely append status text to QTextEdit (switch back to main thread via signal).
        """
        try:
            if not self.ui_controls.get("status_text"):
                return
            current_time = time.strftime("%H:%M:%S")
            formatted_message = f"[{current_time}] {message}"
            self.status_message.emit(formatted_message)
        except Exception as e:
            self.logger.error(f"Thread-safe status append failed: {e}", exc_info=True)

    def _on_status_message(self, formatted_message: str):
        try:
            if not self.ui_controls.get("status_text"):
                return
            self.ui_controls["status_text"].append(formatted_message)
            # Scroll to bottom
            self.ui_controls["status_text"].verticalScrollBar().setValue(
                self.ui_controls["status_text"].verticalScrollBar().maximum()
            )
        except Exception as e:
            self.logger.error(f"Status text append failed: {e}")

    def _load_config_values(self):
        """
        Load values from configuration file to UI controls.
        """
        try:
            # Get audio device configuration
            audio_config = self.config_manager.get_config("AUDIO_DEVICES", {})

            # Set input device
            input_device_id = audio_config.get("input_device_id")
            if input_device_id is not None:
                index = self.ui_controls["input_device_combo"].findData(input_device_id)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)

            # Set output device
            output_device_id = audio_config.get("output_device_id")
            if output_device_id is not None:
                index = self.ui_controls["output_device_combo"].findData(output_device_id)
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)

            # Device information automatically updates on device selection change, no manual setup needed

        except Exception as e:
            self.logger.error(f"Failed to load audio device configuration values: {e}", exc_info=True)

    def get_config_data(self) -> dict:
        """
        Get current configuration data.
        """
        config_data = {}

        try:
            audio_config = {}

            # Input device configuration
            input_device_id = self.ui_controls["input_device_combo"].currentData()
            if input_device_id is not None:
                audio_config["input_device_id"] = input_device_id
                audio_config["input_device_name"] = self.ui_controls["input_device_combo"].currentText()

            # Output device configuration
            output_device_id = self.ui_controls["output_device_combo"].currentData()
            if output_device_id is not None:
                audio_config["output_device_id"] = output_device_id
                audio_config["output_device_name"] = self.ui_controls["output_device_combo"].currentText()

            # Device sample rate information is automatically determined by the device, no user configuration needed
            # Save device default sample rate for later use
            input_device = next((d for d in self.input_devices if d['id'] == input_device_id), None)
            if input_device:
                audio_config["input_sample_rate"] = int(input_device['sample_rate'])

            output_device = next((d for d in self.output_devices if d['id'] == output_device_id), None)
            if output_device:
                audio_config["output_sample_rate"] = int(output_device['sample_rate'])

            if audio_config:
                config_data["AUDIO_DEVICES"] = audio_config

        except Exception as e:
            self.logger.error(f"Failed to get audio device configuration data: {e}", exc_info=True)

        return config_data

    def reset_to_defaults(self):
        """
        Reset to default values.
        """
        try:
            # Rescan devices
            self._scan_devices()

            # Device sample rate information automatically displays after device scan, no manual setup needed

            # Clear status display
            if self.ui_controls["status_text"]:
                self.ui_controls["status_text"].clear()

            self._append_status("Reset to default settings")
            self.logger.info("Audio device configuration reset to default values")

        except Exception as e:
            self.logger.error(f"Failed to reset audio device configuration: {e}", exc_info=True)
