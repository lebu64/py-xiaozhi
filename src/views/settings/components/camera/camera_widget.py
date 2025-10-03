from pathlib import Path

import cv2
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger


class CameraWidget(QWidget):
    """
    Camera settings component.
    """
    
    # Signal definitions
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()
        
        # UI control references
        self.ui_controls = {}
        
        # Preview related
        self.camera = None
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self._update_preview_frame)
        self.is_previewing = False
        
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
            
            ui_path = Path(__file__).parent / "camera_widget.ui"
            uic.loadUi(str(ui_path), self)
            
            # Get UI control references
            self._get_ui_controls()
            
        except Exception as e:
            self.logger.error(f"Failed to setup camera UI: {e}", exc_info=True)
            raise
    
    def _get_ui_controls(self):
        """
        Get UI control references.
        """
        self.ui_controls.update({
            "camera_index_spin": self.findChild(QSpinBox, "camera_index_spin"),
            "frame_width_spin": self.findChild(QSpinBox, "frame_width_spin"),
            "frame_height_spin": self.findChild(QSpinBox, "frame_height_spin"),
            "fps_spin": self.findChild(QSpinBox, "fps_spin"),
            "local_vl_url_edit": self.findChild(QLineEdit, "local_vl_url_edit"),
            "vl_api_key_edit": self.findChild(QLineEdit, "vl_api_key_edit"),
            "models_edit": self.findChild(QLineEdit, "models_edit"),
            "scan_camera_btn": self.findChild(QPushButton, "scan_camera_btn"),
            # Preview related controls
            "preview_label": self.findChild(QLabel, "preview_label"),
            "start_preview_btn": self.findChild(QPushButton, "start_preview_btn"),
            "stop_preview_btn": self.findChild(QPushButton, "stop_preview_btn"),
        })
    
    def _connect_events(self):
        """
        Connect event handlers.
        """
        # Connect change signals for all input controls
        for control in self.ui_controls.values():
            if isinstance(control, QLineEdit):
                control.textChanged.connect(self.settings_changed.emit)
            elif isinstance(control, QSpinBox):
                if control == self.ui_controls.get("camera_index_spin"):
                    # When camera index changes, automatically update preview
                    control.valueChanged.connect(self._on_camera_index_changed)
                else:
                    control.valueChanged.connect(self.settings_changed.emit)
            elif isinstance(control, QPushButton):
                continue
        
        # Camera scan button
        if self.ui_controls["scan_camera_btn"]:
            self.ui_controls["scan_camera_btn"].clicked.connect(self._on_scan_camera)
        
        # Preview control buttons
        if self.ui_controls["start_preview_btn"]:
            self.ui_controls["start_preview_btn"].clicked.connect(self._start_preview)
        
        if self.ui_controls["stop_preview_btn"]:
            self.ui_controls["stop_preview_btn"].clicked.connect(self._stop_preview)
    
    def _load_config_values(self):
        """
        Load values from configuration file to UI controls.
        """
        try:
            # Camera configuration
            camera_config = self.config_manager.get_config("CAMERA", {})
            self._set_spin_value("camera_index_spin", camera_config.get("camera_index", 0))
            self._set_spin_value("frame_width_spin", camera_config.get("frame_width", 640))
            self._set_spin_value("frame_height_spin", camera_config.get("frame_height", 480))
            self._set_spin_value("fps_spin", camera_config.get("fps", 30))
            self._set_text_value("local_vl_url_edit", camera_config.get("Local_VL_url", ""))
            self._set_text_value("vl_api_key_edit", camera_config.get("VLapi_key", ""))
            self._set_text_value("models_edit", camera_config.get("models", ""))
            
        except Exception as e:
            self.logger.error(f"Failed to load camera configuration values: {e}", exc_info=True)
    
    def _set_text_value(self, control_name: str, value: str):
        """
        Set text control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setText"):
            control.setText(str(value) if value is not None else "")
    
    def _set_spin_value(self, control_name: str, value: int):
        """
        Set numeric control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setValue"):
            control.setValue(int(value) if value is not None else 0)
    
    def _get_text_value(self, control_name: str) -> str:
        """
        Get text control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "text"):
            return control.text().strip()
        return ""
    
    def _get_spin_value(self, control_name: str) -> int:
        """
        Get numeric control value.
        """
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "value"):
            return control.value()
        return 0
    
    def _on_scan_camera(self):
        """
        Camera scan button click event.
        """
        try:
            # Stop current preview (to avoid camera occupation)
            was_previewing = self.is_previewing
            if self.is_previewing:
                self._stop_preview()
            
            # Scan available cameras
            available_cameras = self._scan_available_cameras()
            
            if not available_cameras:
                QMessageBox.information(
                    self, "Scan Result", 
                    "No available camera devices detected.\n"
                    "Please ensure the camera is connected and not occupied by other programs."
                )
                return
            
            # If only one camera, use it directly
            if len(available_cameras) == 1:
                camera = available_cameras[0]
                self._apply_camera_settings(camera)
                QMessageBox.information(
                    self, "Setup Complete", 
                    f"Detected 1 camera, automatically set:\n"
                    f"Index: {camera[0]}, Resolution: {camera[1]}x{camera[2]}"
                )
            else:
                # Show selection dialog when multiple cameras
                selected_camera = self._show_camera_selection_dialog(available_cameras)
                if selected_camera:
                    self._apply_camera_settings(selected_camera)
                    QMessageBox.information(
                        self, "Setup Complete", 
                        f"Camera set:\n"
                        f"Index: {selected_camera[0]}, Resolution: {selected_camera[1]}x{selected_camera[2]}"
                    )
            
            # Restore preview state
            if was_previewing:
                QTimer.singleShot(500, self._start_preview)
                
        except Exception as e:
            self.logger.error(f"Failed to scan cameras: {e}", exc_info=True)
            QMessageBox.warning(
                self, "Error", f"Error occurred while scanning cameras: {str(e)}"
            )
    
    def _scan_available_cameras(self, max_devices: int = 5):
        """
        Scan available camera devices.
        """
        available_cameras = []
        
        try:
            for i in range(max_devices):
                try:
                    # Try to open camera
                    cap = cv2.VideoCapture(i)
                    
                    if cap.isOpened():
                        # Try to read one frame to verify camera works
                        ret, _ = cap.read()
                        if ret:
                            # Get default resolution
                            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            available_cameras.append((i, width, height))
                            
                            self.logger.info(f"Detected camera {i}: {width}x{height}")
                    
                    cap.release()
                    
                except Exception as e:
                    self.logger.debug(f"Error detecting camera {i}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error in camera scanning process: {e}", exc_info=True)
        
        return available_cameras
    
    def _show_camera_selection_dialog(self, available_cameras):
        """
        Show camera selection dialog.
        """
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Select Camera")
            dialog.setFixedSize(400, 300)
            
            layout = QVBoxLayout(dialog)
            
            # Title label
            title_label = QLabel(f"Detected {len(available_cameras)} available cameras, please select one:")
            title_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
            layout.addWidget(title_label)
            
            # Camera list
            camera_list = QListWidget()
            for idx, width, height in available_cameras:
                item_text = f"Index {idx}: Resolution {width}x{height}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, (idx, width, height))  # Store camera data
                camera_list.addItem(item)
            
            # Default select first
            if camera_list.count() > 0:
                camera_list.setCurrentRow(0)
            
            layout.addWidget(camera_list)
            
            # Buttons
            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            # Show dialog
            if dialog.exec_() == QDialog.Accepted:
                current_item = camera_list.currentItem()
                if current_item:
                    return current_item.data(Qt.UserRole)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to show camera selection dialog: {e}", exc_info=True)
            return None
    
    def _apply_camera_settings(self, camera_data):
        """
        Apply camera settings.
        """
        try:
            idx, width, height = camera_data
            self._set_spin_value("camera_index_spin", idx)
            self._set_spin_value("frame_width_spin", width)
            self._set_spin_value("frame_height_spin", height)
            
            self.logger.info(f"Applied camera settings: index {idx}, {width}x{height}")
            
        except Exception as e:
            self.logger.error(f"Failed to apply camera settings: {e}", exc_info=True)
    
    def get_config_data(self) -> dict:
        """
        Get current configuration data.
        """
        config_data = {}
        
        try:
            # Camera configuration
            camera_config = {}
            camera_config["camera_index"] = self._get_spin_value("camera_index_spin")
            camera_config["frame_width"] = self._get_spin_value("frame_width_spin")
            camera_config["frame_height"] = self._get_spin_value("frame_height_spin")
            camera_config["fps"] = self._get_spin_value("fps_spin")
            
            local_vl_url = self._get_text_value("local_vl_url_edit")
            if local_vl_url:
                camera_config["Local_VL_url"] = local_vl_url
            
            vl_api_key = self._get_text_value("vl_api_key_edit")
            if vl_api_key:
                camera_config["VLapi_key"] = vl_api_key
            
            models = self._get_text_value("models_edit")
            if models:
                camera_config["models"] = models
            
            # Get existing camera configuration and update
            existing_camera = self.config_manager.get_config("CAMERA", {})
            existing_camera.update(camera_config)
            config_data["CAMERA"] = existing_camera
            
        except Exception as e:
            self.logger.error(f"Failed to get camera configuration data: {e}", exc_info=True)
        
        return config_data
    
    def reset_to_defaults(self):
        """
        Reset to default values.
        """
        try:
            # Get default configuration
            default_config = ConfigManager.DEFAULT_CONFIG
            
            # Camera configuration
            camera_config = default_config["CAMERA"]
            self._set_spin_value("camera_index_spin", camera_config["camera_index"])
            self._set_spin_value("frame_width_spin", camera_config["frame_width"])
            self._set_spin_value("frame_height_spin", camera_config["frame_height"])
            self._set_spin_value("fps_spin", camera_config["fps"])
            self._set_text_value("local_vl_url_edit", camera_config["Local_VL_url"])
            self._set_text_value("vl_api_key_edit", camera_config["VLapi_key"])
            self._set_text_value("models_edit", camera_config["models"])
            
            self.logger.info("Camera configuration reset to default values")
            
        except Exception as e:
            self.logger.error(f"Failed to reset camera configuration: {e}", exc_info=True)
    
    def _on_camera_index_changed(self):
        """
        Camera index change event handler.
        """
        try:
            # Emit settings change signal
            self.settings_changed.emit()
            
            # If currently previewing, restart preview
            if self.is_previewing:
                self._restart_preview()
                
        except Exception as e:
            self.logger.error(f"Failed to handle camera index change: {e}", exc_info=True)
    
    def _start_preview(self):
        """
        Start camera preview.
        """
        try:
            if self.is_previewing:
                self._stop_preview()
            
            # Get camera parameters
            camera_index = self._get_spin_value("camera_index_spin")
            width = self._get_spin_value("frame_width_spin")
            height = self._get_spin_value("frame_height_spin")
            fps = self._get_spin_value("fps_spin")
            
            # Initialize camera
            self.camera = cv2.VideoCapture(camera_index)
            
            if not self.camera.isOpened():
                self._show_preview_error(f"Cannot open camera index {camera_index}")
                return
            
            # Set camera parameters
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            
            # Verify camera can read normally
            ret, _ = self.camera.read()
            if not ret:
                self._show_preview_error("Camera cannot read frame")
                self.camera.release()
                self.camera = None
                return
            
            # Start preview
            self.is_previewing = True
            self.preview_timer.start(max(1, int(1000 / fps)))
            
            # Update button state
            self._update_preview_buttons(True)
            
            self.logger.info(f"Started previewing camera {camera_index}")
            
        except Exception as e:
            self.logger.error(f"Failed to start camera preview: {e}", exc_info=True)
            self._show_preview_error(f"Error occurred while starting preview: {str(e)}")
            self._cleanup_camera()
    
    def _stop_preview(self):
        """
        Stop camera preview.
        """
        try:
            if not self.is_previewing:
                return
            
            # Stop timer
            self.preview_timer.stop()
            self.is_previewing = False
            
            # Release camera
            self._cleanup_camera()
            
            # Clear preview display
            if self.ui_controls["preview_label"]:
                self.ui_controls["preview_label"].setText(
                    "Camera Preview Area\nClick Start Preview to view camera feed"
                )
                self.ui_controls["preview_label"].setPixmap(QPixmap())
            
            # Update button state
            self._update_preview_buttons(False)
            
            self.logger.info("Stopped camera preview")
            
        except Exception as e:
            self.logger.error(f"Failed to stop camera preview: {e}", exc_info=True)
    
    def _restart_preview(self):
        """
        Restart preview (called when camera parameters change).
        """
        if self.is_previewing:
            self._stop_preview()
            # Restart after slight delay to ensure camera resources are released
            QTimer.singleShot(100, self._start_preview)
    
    def _update_preview_frame(self):
        """
        Update preview frame.
        """
        try:
            if not self.camera or not self.camera.isOpened():
                return
            
            ret, frame = self.camera.read()
            if not ret:
                self._show_preview_error("Cannot read camera frame")
                return
            
            # Convert color space BGR -> RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get frame dimensions
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            
            # Convert to QImage
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to preview label size
            if self.ui_controls["preview_label"]:
                label_size = self.ui_controls["preview_label"].size()
                scaled_image = qt_image.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Convert to QPixmap and display
                pixmap = QPixmap.fromImage(scaled_image)
                self.ui_controls["preview_label"].setPixmap(pixmap)
            
        except Exception as e:
            self.logger.error(f"Failed to update preview frame: {e}", exc_info=True)
            self._show_preview_error(f"Error displaying frame: {str(e)}")
    
    def _update_preview_buttons(self, is_previewing: bool):
        """
        Update preview button state.
        """
        try:
            if self.ui_controls["start_preview_btn"]:
                self.ui_controls["start_preview_btn"].setEnabled(not is_previewing)
            
            if self.ui_controls["stop_preview_btn"]:
                self.ui_controls["stop_preview_btn"].setEnabled(is_previewing)
                
        except Exception as e:
            self.logger.error(f"Failed to update preview button state: {e}", exc_info=True)
    
    def _show_preview_error(self, message: str):
        """
        Show error message in preview area.
        """
        try:
            if self.ui_controls["preview_label"]:
                self.ui_controls["preview_label"].setText(f"Preview Error:\n{message}")
                self.ui_controls["preview_label"].setPixmap(QPixmap())
        except Exception as e:
            self.logger.error(f"Failed to show preview error: {e}", exc_info=True)
    
    def _cleanup_camera(self):
        """
        Clean up camera resources.
        """
        try:
            if self.camera:
                self.camera.release()
                self.camera = None
        except Exception as e:
            self.logger.error(f"Failed to clean up camera resources: {e}", exc_info=True)
    
    def closeEvent(self, event):
        """
        Clean up resources when component closes.
        """
        try:
            self._stop_preview()
        except Exception as e:
            self.logger.error(f"Failed to close camera component: {e}", exc_info=True)
        super().closeEvent(event)
