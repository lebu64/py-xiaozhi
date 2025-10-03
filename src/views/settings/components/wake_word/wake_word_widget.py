from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_project_root, resource_finder


class WakeWordWidget(QWidget):
    """
    Wake word settings component.
    """
    
    # Signal definitions
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()
        
        # UI control references
        self.ui_controls = {}
        
        # Initialize UI
        self._setup_ui()
        self._connect_events()
        self._load_config_values()
    
    def _setup_ui(self):
        """
        Setup UI interface.
        """
        try:
            from PyQt5 import uic
            
            ui_path = Path(__file__).parent / "wake_word_widget.ui"
            uic.loadUi(str(ui_path), self)
            
            # Get UI control references
            self._get_ui_controls()
            
        except Exception as e:
            self.logger.error(f"Failed to setup wake word UI: {e}", exc_info=True)
            raise
    
    def _get_ui_controls(self):
        """
        Get UI control references.
        """
        self.ui_controls.update({
            "use_wake_word_check": self.findChild(QCheckBox, "use_wake_word_check"),
            "model_path_edit": self.findChild(QLineEdit, "model_path_edit"),
            "model_path_btn": self.findChild(QPushButton, "model_path_btn"),
            "wake_words_edit": self.findChild(QTextEdit, "wake_words_edit"),
        })
    
    def _connect_events(self):
        """
        Connect event handlers.
        """
        if self.ui_controls["use_wake_word_check"]:
            self.ui_controls["use_wake_word_check"].toggled.connect(self.settings_changed.emit)
        
        if self.ui_controls["model_path_edit"]:
            self.ui_controls["model_path_edit"].textChanged.connect(self.settings_changed.emit)
        
        if self.ui_controls["model_path_btn"]:
            self.ui_controls["model_path_btn"].clicked.connect(self._on_model_path_browse)
        
        if self.ui_controls["wake_words_edit"]:
            self.ui_controls["wake_words_edit"].textChanged.connect(self.settings_changed.emit)
    
    def _load_config_values(self):
        """
        Load values from configuration file to UI controls.
        """
        try:
            # Wake word configuration
            use_wake_word = self.config_manager.get_config("WAKE_WORD_OPTIONS.USE_WAKE_WORD", False)
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(use_wake_word)
            
            model_path = self.config_manager.get_config("WAKE_WORD_OPTIONS.MODEL_PATH", "")
            self._set_text_value("model_path_edit", model_path)
            
            # Read wake words from keywords.txt file
            wake_words_text = self._load_keywords_from_file()
            if self.ui_controls["wake_words_edit"]:
                self.ui_controls["wake_words_edit"].setPlainText(wake_words_text)
            
        except Exception as e:
            self.logger.error(f"Failed to load wake word configuration values: {e}", exc_info=True)
    
    def _set_text_value(self, control_name: str, value: str):
        """
        Set text control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setText"):
            control.setText(str(value) if value is not None else "")
    
    def _get_text_value(self, control_name: str) -> str:
        """
        Get text control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "text"):
            return control.text().strip()
        return ""
    
    def _on_model_path_browse(self):
        """
        Browse model path.
        """
        try:
            current_path = self._get_text_value("model_path_edit")
            if not current_path:
                # Use resource_finder to find default models directory
                models_dir = resource_finder.find_models_dir()
                if models_dir:
                    current_path = str(models_dir)
                else:
                    # If not found, use models under project root
                    project_root = resource_finder.get_project_root()
                    current_path = str(project_root / "models")
            
            selected_path = QFileDialog.getExistingDirectory(
                self, "Select Model Directory", current_path
            )
            
            if selected_path:
                # Convert to relative path (if applicable)
                relative_path = self._convert_to_relative_path(selected_path)
                self._set_text_value("model_path_edit", relative_path)
                self.logger.info(f"Selected model path: {selected_path}, stored as: {relative_path}")
        
        except Exception as e:
            self.logger.error(f"Failed to browse model path: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Error while browsing model path: {str(e)}")
    
    def _convert_to_relative_path(self, model_path: str) -> str:
        """
        Convert absolute path to relative path relative to project root (if on same drive).
        """
        try:
            import os
            
            # Get project root
            project_root = get_project_root()
            
            # Check if on same drive (only applicable on Windows)
            if os.name == 'nt':  # Windows system
                model_path_drive = os.path.splitdrive(model_path)[0]
                project_root_drive = os.path.splitdrive(str(project_root))[0]
                
                # If on same drive, calculate relative path
                if model_path_drive.lower() == project_root_drive.lower():
                    relative_path = os.path.relpath(model_path, project_root)
                    return relative_path
                else:
                    # Not on same drive, use absolute path
                    return model_path
            else:
                # Non-Windows system, directly calculate relative path
                try:
                    relative_path = os.path.relpath(model_path, project_root)
                    # Only use relative path if it doesn't contain ".."+os.sep
                    if not relative_path.startswith(".." + os.sep) and not relative_path.startswith("/"):
                        return relative_path
                    else:
                        # Relative path contains upward navigation, use absolute path
                        return model_path
                except ValueError:
                    # Cannot calculate relative path (different volume), use absolute path
                    return model_path
        except Exception as e:
            self.logger.warning(f"Error calculating relative path, using original path: {e}")
            return model_path
    
    def _load_keywords_from_file(self) -> str:
        """
        Load wake words from keywords.txt file, display in full format.
        """
        try:
            # Get configured model path
            model_path = self.config_manager.get_config("WAKE_WORD_OPTIONS.MODEL_PATH", "")
            if not model_path:
                # If no model path configured, use default models directory
                keywords_file = get_project_root() / "models" / "keywords.txt"
            else:
                # Use configured model path
                keywords_file = Path(model_path) / "keywords.txt"
            
            if not keywords_file.exists():
                self.logger.warning(f"Keywords file does not exist: {keywords_file}")
                return ""
            
            keywords = []
            with open(keywords_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "@" in line and not line.startswith("#"):
                        # Keep full format: pinyin @chinese
                        keywords.append(line)
            
            return "\n".join(keywords)
        
        except Exception as e:
            self.logger.error(f"Failed to read keywords file: {e}")
            return ""
    
    def _save_keywords_to_file(self, keywords_text: str):
        """
        Save wake words to keywords.txt file, support full format.
        """
        try:
            # Get configured model path
            model_path = self.config_manager.get_config("WAKE_WORD_OPTIONS.MODEL_PATH", "")
            if not model_path:
                # If no model path configured, use default models directory
                keywords_file = get_project_root() / "models" / "keywords.txt"
            else:
                # Use configured model path
                keywords_file = Path(model_path) / "keywords.txt"
            
            # Process input keywords text
            lines = [line.strip() for line in keywords_text.split("\n") if line.strip()]
            
            processed_lines = []
            has_invalid_lines = False
            
            for line in lines:
                if "@" in line:
                    # Full format: pinyin @chinese
                    processed_lines.append(line)
                else:
                    # Only Chinese, no pinyin - mark as invalid
                    processed_lines.append(f"# Invalid: Missing pinyin format - {line}")
                    has_invalid_lines = True
                    self.logger.warning(f"Keyword '{line}' missing pinyin, required format: pinyin @chinese")
            
            # Write to file
            with open(keywords_file, "w", encoding="utf-8") as f:
                f.write("\n".join(processed_lines) + "\n")
            
            self.logger.info(f"Successfully saved keywords to {keywords_file}")
            
            # If there are invalid formats, notify user
            if has_invalid_lines:
                QMessageBox.warning(
                    self,
                    "Format Error",
                    "Invalid keyword format detected!\n\n"
                    "Correct format: pinyin @chinese\n"
                    "Example: x iǎo ài t óng x ué @小爱同学\n\n"
                    "Invalid lines have been commented, please manually correct and save again.",
                )
        
        except Exception as e:
            self.logger.error(f"Failed to save keywords file: {e}")
            QMessageBox.warning(self, "Error", f"Failed to save keywords: {str(e)}")
    
    def get_config_data(self) -> dict:
        """
        Get current configuration data.
        """
        config_data = {}
        
        try:
            # Wake word configuration
            if self.ui_controls["use_wake_word_check"]:
                use_wake_word = self.ui_controls["use_wake_word_check"].isChecked()
                config_data["WAKE_WORD_OPTIONS.USE_WAKE_WORD"] = use_wake_word
            
            model_path = self._get_text_value("model_path_edit")
            if model_path:
                # Convert to relative path (if applicable)
                relative_path = self._convert_to_relative_path(model_path)
                config_data["WAKE_WORD_OPTIONS.MODEL_PATH"] = relative_path
            
        except Exception as e:
            self.logger.error(f"Failed to get wake word configuration data: {e}", exc_info=True)
        
        return config_data
    
    def save_keywords(self):
        """
        Save wake words to file.
        """
        if self.ui_controls["wake_words_edit"]:
            wake_words_text = self.ui_controls["wake_words_edit"].toPlainText().strip()
            self._save_keywords_to_file(wake_words_text)
    
    def reset_to_defaults(self):
        """
        Reset to default values.
        """
        try:
            # Get default configuration
            default_config = ConfigManager.DEFAULT_CONFIG
            
            # Wake word configuration
            wake_word_config = default_config["WAKE_WORD_OPTIONS"]
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(
                    wake_word_config["USE_WAKE_WORD"]
                )
            
            self._set_text_value("model_path_edit", wake_word_config["MODEL_PATH"])
            
            if self.ui_controls["wake_words_edit"]:
                # Use default keywords for reset
                default_keywords = self._get_default_keywords()
                self.ui_controls["wake_words_edit"].setPlainText(default_keywords)
            
            self.logger.info("Wake word configuration reset to default values")
            
        except Exception as e:
            self.logger.error(f"Failed to reset wake word configuration: {e}", exc_info=True)
    
    def _get_default_keywords(self) -> str:
        """
        Get default keyword list, full format.
        """
        default_keywords = [
            "x iǎo ài t óng x ué @小爱同学",
            "n ǐ h ǎo w èn w èn @你好问问",
            "x iǎo y ì x iǎo y ì @小艺小艺",
            "x iǎo m ǐ x iǎo m ǐ @小米小米",
            "n ǐ h ǎo x iǎo zh ì @你好小智",
            "j iā w éi s ī @贾维斯",
        ]
        return "\n".join(default_keywords)
