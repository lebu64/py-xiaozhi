import os
from abc import ABCMeta
from pathlib import Path
from typing import Callable, Optional

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QFont, QKeySequence, QMovie, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from src.display.base_display import BaseDisplay
from src.utils.resource_finder import find_assets_dir


# Create compatible metaclass
class CombinedMeta(type(QObject), ABCMeta):
    pass


class GuiDisplay(BaseDisplay, QObject, metaclass=CombinedMeta):
    def __init__(self):
        super().__init__()
        QObject.__init__(self)
        self.app = None
        self.root = None

        # UI controls
        self.status_label = None
        self.emotion_label = None
        self.tts_text_label = None
        self.manual_btn = None
        self.abort_btn = None
        self.auto_btn = None
        self.mode_btn = None
        self.text_input = None
        self.send_btn = None

        # Emotion management
        self.emotion_movie = None
        self._emotion_cache = {}
        self._last_emotion_name = None

        # State management
        self.auto_mode = False
        self._running = True
        self.current_status = ""
        self.is_connected = True

        # Callback functions
        self.button_press_callback = None
        self.button_release_callback = None
        self.mode_callback = None
        self.auto_callback = None
        self.abort_callback = None
        self.send_text_callback = None

        # System tray component
        self.system_tray = None

    async def set_callbacks(
        self,
        press_callback: Optional[Callable] = None,
        release_callback: Optional[Callable] = None,
        mode_callback: Optional[Callable] = None,
        auto_callback: Optional[Callable] = None,
        abort_callback: Optional[Callable] = None,
        send_text_callback: Optional[Callable] = None,
    ):
        """
        Set callback functions.
        """
        self.button_press_callback = press_callback
        self.button_release_callback = release_callback
        self.mode_callback = mode_callback
        self.auto_callback = auto_callback
        self.abort_callback = abort_callback
        self.send_text_callback = send_text_callback

        # No longer register status listener callbacks, update_status handles all logic directly

    def _on_manual_button_press(self):
        """
        Manual mode button press event handling.
        """
        if self.manual_btn and self.manual_btn.isVisible():
            self.manual_btn.setText("Release to stop")
        if self.button_press_callback:
            self.button_press_callback()

    def _on_manual_button_release(self):
        """
        Manual mode button release event handling.
        """
        if self.manual_btn and self.manual_btn.isVisible():
            self.manual_btn.setText("Press and hold to speak")
        if self.button_release_callback:
            self.button_release_callback()

    def _on_auto_button_click(self):
        """
        Auto mode button click event handling.
        """
        if self.auto_callback:
            self.auto_callback()

    def _on_abort_button_click(self):
        """
        Handle abort button click event.
        """
        if self.abort_callback:
            self.abort_callback()

    def _on_mode_button_click(self):
        """
        Conversation mode toggle button click event.
        """
        if self.mode_callback:
            if not self.mode_callback():
                return

        self.auto_mode = not self.auto_mode

        if self.auto_mode:
            self._update_mode_button_status("Auto Conversation")
            self._switch_to_auto_mode()
        else:
            self._update_mode_button_status("Manual Conversation")
            self._switch_to_manual_mode()

    def _switch_to_auto_mode(self):
        """
        UI update when switching to auto mode.
        """
        if self.manual_btn and self.auto_btn:
            self.manual_btn.hide()
            self.auto_btn.show()

    def _switch_to_manual_mode(self):
        """
        UI update when switching to manual mode.
        """
        if self.manual_btn and self.auto_btn:
            self.auto_btn.hide()
            self.manual_btn.show()

    async def update_status(self, status: str, connected: bool):
        """
        Update status text and handle related logic.
        """
        full_status_text = f"Status: {status}"
        self._safe_update_label(self.status_label, full_status_text)

        # Track both status text changes and connection status changes
        new_connected = bool(connected)
        status_changed = status != self.current_status
        connected_changed = new_connected != self.is_connected

        if status_changed:
            self.current_status = status
        if connected_changed:
            self.is_connected = new_connected

        # Update system tray on any change
        if status_changed or connected_changed:
            self._update_system_tray(status)

    async def update_text(self, text: str):
        """
        Update TTS text.
        """
        self._safe_update_label(self.tts_text_label, text)

    async def update_emotion(self, emotion_name: str):
        """
        Update emotion display.
        """
        if emotion_name == self._last_emotion_name:
            return

        self._last_emotion_name = emotion_name
        asset_path = self._get_emotion_asset_path(emotion_name)

        if self.emotion_label:
            try:
                self._set_emotion_asset(self.emotion_label, asset_path)
            except Exception as e:
                self.logger.error(f"Error setting emotion GIF: {str(e)}")

    def _get_emotion_asset_path(self, emotion_name: str) -> str:
        """
        Get emotion asset file path, automatically match common extensions.
        """
        if emotion_name in self._emotion_cache:
            return self._emotion_cache[emotion_name]

        assets_dir = find_assets_dir()
        if not assets_dir:
            path = "😊"
        else:
            emotion_dir = assets_dir / "emojis"
            # Supported extension priority: gif > png > jpg > jpeg > webp
            candidates = [
                emotion_dir / f"{emotion_name}.gif",
                emotion_dir / f"{emotion_name}.png",
                emotion_dir / f"{emotion_name}.jpg",
                emotion_dir / f"{emotion_name}.jpeg",
                emotion_dir / f"{emotion_name}.webp",
            ]
            # Match in order
            found = next((p for p in candidates if p.exists()), None)

            # Fallback to neutral with same rules
            if not found:
                neutral_candidates = [
                    emotion_dir / "neutral.gif",
                    emotion_dir / "neutral.png",
                    emotion_dir / "neutral.jpg",
                    emotion_dir / "neutral.jpeg",
                    emotion_dir / "neutral.webp",
                ]
                found = next((p for p in neutral_candidates if p.exists()), None)

            path = str(found) if found else "😊"

        self._emotion_cache[emotion_name] = path
        return path

    def _set_emotion_asset(self, label, asset_path: str):
        """
        Set emotion asset (GIF animation or static image).
        """
        if not label:
            return

        # If it's an emoji string, set text directly
        if not isinstance(asset_path, str) or "." not in asset_path:
            label.setText(asset_path or "😊")
            return

        try:
            if asset_path.lower().endswith(".gif"):
                # GIF animation
                if hasattr(self, "_gif_movies") and asset_path in self._gif_movies:
                    movie = self._gif_movies[asset_path]
                else:
                    movie = QMovie(asset_path)
                    if not movie.isValid():
                        label.setText("😊")
                        return
                    movie.setCacheMode(QMovie.CacheAll)
                    if not hasattr(self, "_gif_movies"):
                        self._gif_movies = {}
                    self._gif_movies[asset_path] = movie

                # If switching to new movie, stop old one to avoid CPU usage
                if (
                    getattr(self, "emotion_movie", None) is not None
                    and self.emotion_movie is not movie
                ):
                    try:
                        self.emotion_movie.stop()
                    except Exception:
                        pass

                self.emotion_movie = movie
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setAlignment(Qt.AlignCenter)
                label.setMovie(movie)
                movie.setSpeed(105)
                movie.start()
            else:
                # Static image: stop old GIF if playing
                if getattr(self, "emotion_movie", None) is not None:
                    try:
                        self.emotion_movie.stop()
                    except Exception:
                        pass
                    self.emotion_movie = None

                pixmap = QPixmap(asset_path)
                if pixmap.isNull():
                    label.setText("😊")
                    return
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setAlignment(Qt.AlignCenter)
                label.setPixmap(pixmap)

        except Exception as e:
            self.logger.error(f"Failed to set GIF animation: {e}")
            label.setText("😊")

    def _safe_update_label(self, label, text):
        """
        Safely update label text.
        """
        if label:
            try:
                label.setText(text)
            except RuntimeError as e:
                self.logger.error(f"Failed to update label: {e}")

    async def close(self):
        """
        Close window handling.
        """
        self._running = False
        # Stop and clean up GIF resources to avoid resource leaks
        try:
            if getattr(self, "emotion_movie", None) is not None:
                try:
                    self.emotion_movie.stop()
                except Exception:
                    pass
                self.emotion_movie = None
            if hasattr(self, "_gif_movies") and isinstance(self._gif_movies, dict):
                for _m in list(self._gif_movies.values()):
                    try:
                        _m.stop()
                    except Exception:
                        pass
                self._gif_movies.clear()
        except Exception:
            pass
        if self.system_tray:
            self.system_tray.hide()
        if self.root:
            self.root.close()

    async def start(self):
        """
        Start GUI.
        """
        try:
            # Set Qt environment variables
            os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.fonts.debug=false")

            self.app = QApplication.instance()
            if self.app is None:
                raise RuntimeError("QApplication not found, please ensure running in qasync environment")

            # Disable automatic app exit when last window is closed, ensure tray stays
            try:
                self.app.setQuitOnLastWindowClosed(False)
            except Exception:
                pass

            # Install application-level event filter: support window restoration when clicking Dock icon
            try:
                self.app.installEventFilter(self)
            except Exception:
                pass

            # Set default font
            default_font = QFont()
            default_font.setPointSize(12)
            self.app.setFont(default_font)

            # Load UI
            from PyQt5 import uic

            self.root = QWidget()
            ui_path = Path(__file__).parent / "gui_display.ui"
            uic.loadUi(str(ui_path), self.root)

            # Get controls and connect events
            self._init_ui_controls()
            self._connect_events()

            # Initialize system tray
            self._setup_system_tray()

            # Set default emotion
            await self._set_default_emotion()

            # Show window
            self.root.show()

        except Exception as e:
            self.logger.error(f"GUI startup failed: {e}", exc_info=True)
            raise

    def eventFilter(self, obj, event):
        """Application-level event filtering:

        - macOS clicking Dock icon triggers ApplicationActivate event
        - When main window is hidden/minimized, automatically restore display
        """
        try:
            # Delayed import to avoid top-level circular dependency
            from PyQt5.QtCore import QEvent

            if event and event.type() == QEvent.ApplicationActivate:
                if self.root and not self.root.isVisible():
                    self._show_main_window()
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.error(f"Failed to handle application activation event: {e}")
        return False

    def _init_ui_controls(self):
        """
        Initialize UI controls.
        """
        self.status_label = self.root.findChild(QLabel, "status_label")
        self.emotion_label = self.root.findChild(QLabel, "emotion_label")
        self.tts_text_label = self.root.findChild(QLabel, "tts_text_label")
        self.manual_btn = self.root.findChild(QPushButton, "manual_btn")
        self.abort_btn = self.root.findChild(QPushButton, "abort_btn")
        self.auto_btn = self.root.findChild(QPushButton, "auto_btn")
        self.mode_btn = self.root.findChild(QPushButton, "mode_btn")
        self.settings_btn = self.root.findChild(QPushButton, "settings_btn")
        self.text_input = self.root.findChild(QLineEdit, "text_input")
        self.send_btn = self.root.findChild(QPushButton, "send_btn")

    def _connect_events(self):
        """
        Connect events.
        """
        if self.manual_btn:
            self.manual_btn.pressed.connect(self._on_manual_button_press)
            self.manual_btn.released.connect(self._on_manual_button_release)
        if self.abort_btn:
            self.abort_btn.clicked.connect(self._on_abort_button_click)
        if self.auto_btn:
            self.auto_btn.clicked.connect(self._on_auto_button_click)
            self.auto_btn.hide()
        if self.mode_btn:
            self.mode_btn.clicked.connect(self._on_mode_button_click)
        if self.text_input and self.send_btn:
            self.send_btn.clicked.connect(self._on_send_button_click)
            self.text_input.returnPressed.connect(self._on_send_button_click)
        if self.settings_btn:
            self.settings_btn.clicked.connect(self._on_settings_button_click)

        # Set window close event
        self.root.closeEvent = self._closeEvent

        # Shortcuts: Ctrl+, and Cmd+, to open settings
        try:
            from PyQt5.QtWidgets import QShortcut

            QShortcut(
                QKeySequence("Ctrl+,"),
                self.root,
                activated=self._on_settings_button_click,
            )
            QShortcut(
                QKeySequence("Meta+,"),
                self.root,
                activated=self._on_settings_button_click,
            )
        except Exception:
            pass

    def _setup_system_tray(self):
        """
        Set up system tray.
        """
        try:
            # Allow disabling system tray via environment variable for troubleshooting
            if os.getenv("XIAOZHI_DISABLE_TRAY") == "1":
                self.logger.warning(
                    "System tray disabled via environment variable (XIAOZHI_DISABLE_TRAY=1)"
                )
                return
            from src.views.components.system_tray import SystemTray

            self.system_tray = SystemTray(self.root)
            self.system_tray.show_window_requested.connect(self._show_main_window)
            self.system_tray.settings_requested.connect(self._on_settings_button_click)
            self.system_tray.quit_requested.connect(self._quit_application)

        except Exception as e:
            self.logger.error(f"Failed to initialize system tray component: {e}", exc_info=True)

    async def _set_default_emotion(self):
        """
        Set default emotion.
        """
        try:
            await self.update_emotion("neutral")
        except Exception as e:
            self.logger.error(f"Failed to set default emotion: {e}", exc_info=True)

    def _update_system_tray(self, status):
        """
        Update system tray status.
        """
        if self.system_tray:
            self.system_tray.update_status(status, self.is_connected)

    def _show_main_window(self):
        """
        Show main window.
        """
        if self.root:
            if self.root.isMinimized():
                self.root.showNormal()
            if not self.root.isVisible():
                self.root.show()
            self.root.activateWindow()
            self.root.raise_()

    def _quit_application(self):
        """
        Quit application.
        """
        self.logger.info("Starting application quit...")
        self._running = False

        if self.system_tray:
            self.system_tray.hide()

        try:
            from src.application import Application

            app = Application.get_instance()
            if app:
                # Asynchronously start shutdown process but set timeout
                import asyncio

                from PyQt5.QtCore import QTimer

                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create shutdown task but don't wait
                    shutdown_task = asyncio.create_task(app.shutdown())

                    # Force quit after timeout
                    def force_quit():
                        if not shutdown_task.done():
                            self.logger.warning("Shutdown timeout, forcing quit")
                            shutdown_task.cancel()
                        QApplication.quit()

                    # Force quit after 3 seconds
                    QTimer.singleShot(3000, force_quit)

                    # Normal quit when shutdown completes
                    def on_shutdown_complete(task):
                        if not task.cancelled():
                            if task.exception():
                                self.logger.error(
                                    f"Application shutdown exception: {task.exception()}"
                                )
                            else:
                                self.logger.info("Application shutdown completed normally")
                        QApplication.quit()

                    shutdown_task.add_done_callback(on_shutdown_complete)
                else:
                    # If event loop not running, quit directly
                    QApplication.quit()
            else:
                QApplication.quit()

        except Exception as e:
            self.logger.error(f"Failed to quit application: {e}")
            # Quit directly in case of exception
            QApplication.quit()

    def _closeEvent(self, event):
        """
        Handle window close event.
        """
        # Minimize to tray as long as system tray is available
        if self.system_tray and (
            getattr(self.system_tray, "is_available", lambda: False)()
            or getattr(self.system_tray, "is_visible", lambda: False)()
        ):
            self.logger.info("Closing window: minimizing to tray")
            # Delay hiding to avoid macOS graphics stack instability when directly operating window in closeEvent
            try:
                from PyQt5.QtCore import QTimer

                QTimer.singleShot(0, self.root.hide)
            except Exception:
                try:
                    self.root.hide()
                except Exception:
                    pass
            # Stop GIF animation to avoid potential crashes when hiding
            try:
                if getattr(self, "emotion_movie", None) is not None:
                    self.emotion_movie.stop()
            except Exception:
                pass
            event.ignore()
        else:
            self._quit_application()
            event.accept()

    def _update_mode_button_status(self, text: str):
        """
        Update mode button status.
        """
        if self.mode_btn:
            self.mode_btn.setText(text)

    async def update_button_status(self, text: str):
        """
        Update button status.
        """
        if self.auto_mode and self.auto_btn:
            self.auto_btn.setText(text)

    def _on_send_button_click(self):
        """
        Handle send text button click event.
        """
        if not self.text_input or not self.send_text_callback:
            return

        text = self.text_input.text().strip()
        if not text:
            return

        self.text_input.clear()

        try:
            import asyncio

            task = asyncio.create_task(self.send_text_callback(text))

            def _on_done(t):
                if not t.cancelled() and t.exception():
                    self.logger.error(
                        f"Send text task exception: {t.exception()}", exc_info=True
                    )

            task.add_done_callback(_on_done)
        except Exception as e:
            self.logger.error(f"Error sending text: {e}")

    def _on_settings_button_click(self):
        """
        Handle settings button click event.
        """
        try:
            from src.views.settings import SettingsWindow

            settings_window = SettingsWindow(self.root)
            settings_window.exec_()

        except Exception as e:
            self.logger.error(f"Failed to open settings window: {e}", exc_info=True)

    async def toggle_mode(self):
        """
        Toggle mode.
        """
        # Call existing mode switching function
        if hasattr(self, "mode_callback") and self.mode_callback:
            self._on_mode_button_click()
            self.logger.debug("Conversation mode toggled via shortcut")

    async def toggle_window_visibility(self):
        """
        Toggle window visibility.
        """
        if self.root:
            if self.root.isVisible():
                self.logger.debug("Window hidden via shortcut")
                self.root.hide()
            else:
                self.logger.debug("Window shown via shortcut")
                self.root.show()
                self.root.activateWindow()
                self.root.raise_()
