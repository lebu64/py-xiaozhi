from pathlib import Path
import os

from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QTabWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.views.settings.components.shortcuts_settings import ShortcutsSettingsWidget
from src.views.settings.components.system_options import SystemOptionsWidget
from src.views.settings.components.wake_word import WakeWordWidget
from src.views.settings.components.camera import CameraWidget
from src.views.settings.components.audio import AudioWidget


class SettingsWindow(QDialog):
    """
    Settings configuration window.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # Component references
        self.system_options_tab = None
        self.wake_word_tab = None
        self.camera_tab = None
        self.audio_tab = None
        self.shortcuts_tab = None
        
        # UI controls
        self.ui_controls = {}

        # Initialize UI
        self._setup_ui()
        self._connect_events()

    def _setup_ui(self):
        """
        Setup UI interface.
        """
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "settings_window.ui"
            uic.loadUi(str(ui_path), self)

            # Get UI control references
            self._get_ui_controls()

            # Add component tabs
            self._add_component_tabs()

        except Exception as e:
            self.logger.error(f"Failed to setup UI: {e}", exc_info=True)
            raise

    def _add_component_tabs(self):
        """
        Add component tabs.
        """
        try:
            # Get TabWidget
            tab_widget = self.findChild(QTabWidget, "tabWidget")
            if not tab_widget:
                self.logger.error("TabWidget control not found")
                return

            # Clear existing tabs (if any)
            tab_widget.clear()

            # Create and add system options component
            self.system_options_tab = SystemOptionsWidget()
            tab_widget.addTab(self.system_options_tab, "System Options")
            self.system_options_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add wake word component
            self.wake_word_tab = WakeWordWidget()
            tab_widget.addTab(self.wake_word_tab, "Wake Word")
            self.wake_word_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add camera component
            self.camera_tab = CameraWidget()
            tab_widget.addTab(self.camera_tab, "Camera")
            self.camera_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add audio device component
            self.audio_tab = AudioWidget()
            tab_widget.addTab(self.audio_tab, "Audio Devices")
            self.audio_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add shortcuts settings component
            self.shortcuts_tab = ShortcutsSettingsWidget()
            tab_widget.addTab(self.shortcuts_tab, "Shortcuts")
            self.shortcuts_tab.settings_changed.connect(self._on_settings_changed)

            self.logger.debug("Successfully added all component tabs")

        except Exception as e:
            self.logger.error(f"Failed to add component tabs: {e}", exc_info=True)

    def _on_settings_changed(self):
        """
        Settings change callback.
        """
        # Can add some prompts or other logic here

    def _get_ui_controls(self):
        """
        Get UI control references.
        """
        # Only need to get main button controls
        self.ui_controls.update({
            "save_btn": self.findChild(QPushButton, "save_btn"),
            "cancel_btn": self.findChild(QPushButton, "cancel_btn"),
            "reset_btn": self.findChild(QPushButton, "reset_btn"),
        })

    def _connect_events(self):
        """
        Connect event handlers.
        """
        if self.ui_controls["save_btn"]:
            self.ui_controls["save_btn"].clicked.connect(self._on_save_clicked)

        if self.ui_controls["cancel_btn"]:
            self.ui_controls["cancel_btn"].clicked.connect(self.reject)

        if self.ui_controls["reset_btn"]:
            self.ui_controls["reset_btn"].clicked.connect(self._on_reset_clicked)

    # Configuration loading is now handled by each component, no need to handle in main window

    # Removed no longer needed control operation methods, now handled by each component

    def _on_save_clicked(self):
        """
        Save button click event.
        """
        try:
            # Collect all configuration data
            success = self._save_all_config()

            if success:
                # Show save success and prompt for restart
                reply = QMessageBox.question(
                    self,
                    "Configuration Saved Successfully",
                    "Configuration saved successfully!\n\nTo make the configuration take effect, it is recommended to restart the software.\nRestart now?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
                )

                if reply == QMessageBox.Yes:
                    self._restart_application()
                else:
                    self.accept()
            else:
                QMessageBox.warning(self, "Error", "Configuration save failed, please check the input values.")

        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Error occurred while saving configuration: {str(e)}")

    def _save_all_config(self) -> bool:
        """
        Save all configurations.
        """
        try:
            # Collect configuration data from each component
            all_config_data = {}
            
            # System options configuration
            if self.system_options_tab:
                system_config = self.system_options_tab.get_config_data()
                all_config_data.update(system_config)
            
            # Wake word configuration
            if self.wake_word_tab:
                wake_word_config = self.wake_word_tab.get_config_data()
                all_config_data.update(wake_word_config)
                # Save wake word file
                self.wake_word_tab.save_keywords()
            
            # Camera configuration
            if self.camera_tab:
                camera_config = self.camera_tab.get_config_data()
                all_config_data.update(camera_config)
            
            # Audio device configuration
            if self.audio_tab:
                audio_config = self.audio_tab.get_config_data()
                all_config_data.update(audio_config)
            
            # Shortcuts configuration
            if self.shortcuts_tab:
                # Shortcuts component has its own save method
                self.shortcuts_tab.apply_settings()
            
            # Batch update configuration
            for config_path, value in all_config_data.items():
                self.config_manager.update_config(config_path, value)
            
            self.logger.info("Configuration saved successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Error occurred while saving configuration: {e}", exc_info=True)
            return False

    def _on_reset_clicked(self):
        """
        Reset button click event.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            "Are you sure you want to reset all configurations to default values?\nThis will clear all current settings.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self._reset_to_defaults()

    def _reset_to_defaults(self):
        """
        Reset to default values.
        """
        try:
            # Let each component reset to default values
            if self.system_options_tab:
                self.system_options_tab.reset_to_defaults()
            
            if self.wake_word_tab:
                self.wake_word_tab.reset_to_defaults()
            
            if self.camera_tab:
                self.camera_tab.reset_to_defaults()
            
            if self.audio_tab:
                self.audio_tab.reset_to_defaults()
            
            if self.shortcuts_tab:
                self.shortcuts_tab.reset_to_defaults()
            
            self.logger.info("All component configurations reset to default values")
        
        except Exception as e:
            self.logger.error(f"Failed to reset configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Error occurred while resetting configuration: {str(e)}")

    def _restart_application(self):
        """
        Restart application.
        """
        try:
            self.logger.info("User chose to restart application")

            # Close settings window
            self.accept()

            # Directly restart program
            self._direct_restart()

        except Exception as e:
            self.logger.error(f"Failed to restart application: {e}", exc_info=True)
            QMessageBox.warning(
                self, "Restart Failed", "Automatic restart failed, please manually restart the software for the configuration to take effect."
            )

    def _direct_restart(self):
        """
        Directly restart program.
        """
        try:
            import sys
            from PyQt5.QtWidgets import QApplication

            # Get current program path and arguments
            python = sys.executable
            script = sys.argv[0]
            args = sys.argv[1:]

            self.logger.info(f"Restart command: {python} {script} {' '.join(args)}")

            # Close current application
            QApplication.quit()

            # Start new instance
            if getattr(sys, "frozen", False):
                # Packaged environment
                os.execv(sys.executable, [sys.executable] + args)
            else:
                # Development environment
                os.execv(python, [python, script] + args)

        except Exception as e:
            self.logger.error(f"Direct restart failed: {e}", exc_info=True)

    def closeEvent(self, event):
        """
        Window close event.
        """
        self.logger.debug("Settings window closed")
        super().closeEvent(event)
