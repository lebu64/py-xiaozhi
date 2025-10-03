"""
System tray component module providing system tray icon, menu, and status indication functionality.
"""

from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon, QWidget

from src.utils.logging_config import get_logger


class SystemTray(QObject):
    """
    System tray component.
    """

    # Define signals
    show_window_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.logger = get_logger("SystemTray")
        self.parent_widget = parent

        # Tray-related components
        self.tray_icon = None
        self.tray_menu = None

        # Status-related
        self.current_status = ""
        self.is_connected = True

        # Initialize tray
        self._setup_tray()

    def _setup_tray(self):
        """
        Set up system tray icon.
        """
        try:
            # Check if system supports system tray
            if not QSystemTrayIcon.isSystemTrayAvailable():
                self.logger.warning("System does not support system tray functionality")
                return

            # Create tray menu
            self._create_tray_menu()

            # Create system tray icon (do not bind QWidget as parent to avoid window lifecycle affecting tray icon, prevent crashes on macOS when hiding/closing)
            self.tray_icon = QSystemTrayIcon()
            self.tray_icon.setContextMenu(self.tray_menu)

            # Set a placeholder icon before display to avoid QSystemTrayIcon::setVisible: No Icon set warning
            try:
                # Use a solid dot as initial placeholder
                pixmap = QPixmap(16, 16)
                pixmap.fill(QColor(0, 0, 0, 0))
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(QBrush(QColor(0, 180, 0)))
                painter.setPen(QColor(0, 0, 0, 0))
                painter.drawEllipse(2, 2, 12, 12)
                painter.end()
                self.tray_icon.setIcon(QIcon(pixmap))
            except Exception:
                pass

            # Connect tray icon events
            self.tray_icon.activated.connect(self._on_tray_activated)

            # Set initial icon (avoid crashes on some platforms during first draw, delay until event loop is idle)
            try:
                from PyQt5.QtCore import QTimer

                QTimer.singleShot(0, lambda: self.update_status("Standby", connected=True))
            except Exception:
                self.update_status("Standby", connected=True)

            # Show system tray icon
            self.tray_icon.show()
            self.logger.info("System tray icon initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize system tray icon: {e}", exc_info=True)

    def _create_tray_menu(self):
        """
        Create tray right-click menu.
        """
        self.tray_menu = QMenu()

        # Add show main window menu item
        show_action = QAction("Show Main Window", self.parent_widget)
        show_action.triggered.connect(self._on_show_window)
        self.tray_menu.addAction(show_action)

        # Add separator
        self.tray_menu.addSeparator()

        # Add settings menu item
        settings_action = QAction("Settings", self.parent_widget)
        settings_action.triggered.connect(self._on_settings)
        self.tray_menu.addAction(settings_action)

        # Add separator
        self.tray_menu.addSeparator()

        # Add quit menu item
        quit_action = QAction("Quit Program", self.parent_widget)
        quit_action.triggered.connect(self._on_quit)
        self.tray_menu.addAction(quit_action)

    def _on_tray_activated(self, reason):
        """
        Handle tray icon click events.
        """
        if reason == QSystemTrayIcon.Trigger:  # Single click
            self.show_window_requested.emit()

    def _on_show_window(self):
        """
        Handle show window menu item click.
        """
        self.show_window_requested.emit()

    def _on_settings(self):
        """
        Handle settings menu item click.
        """
        self.settings_requested.emit()

    def _on_quit(self):
        """
        Handle quit menu item click.
        """
        self.quit_requested.emit()

    def update_status(self, status: str, connected: bool = True):
        """Update tray icon status.

        Args:
            status: Status text
            connected: Connection status
        """
        if not self.tray_icon:
            return

        self.current_status = status
        self.is_connected = connected

        try:
            icon_color = self._get_status_color(status, connected)

            # Create icon with specified color
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(icon_color))
            painter.setPen(QColor(0, 0, 0, 0))  # Transparent border
            painter.drawEllipse(2, 2, 12, 12)
            painter.end()

            # Set icon
            self.tray_icon.setIcon(QIcon(pixmap))

            # Set tooltip text
            tooltip = f"XiaoZhi AI Assistant - {status}"
            self.tray_icon.setToolTip(tooltip)

        except Exception as e:
            self.logger.error(f"Failed to update system tray icon: {e}")

    def _get_status_color(self, status: str, connected: bool) -> QColor:
        """Return corresponding color based on status.

        Args:
            status: Status text
            connected: Connection status

        Returns:
            QColor: Corresponding color
        """
        if not connected:
            return QColor(128, 128, 128)  # Gray - Not connected

        if "Error" in status:
            return QColor(255, 0, 0)  # Red - Error status
        elif "Listening" in status:
            return QColor(255, 200, 0)  # Yellow - Listening status
        elif "Speaking" in status:
            return QColor(0, 120, 255)  # Blue - Speaking status
        else:
            return QColor(0, 180, 0)  # Green - Standby/Started status

    def show_message(
        self,
        title: str,
        message: str,
        icon_type=QSystemTrayIcon.Information,
        duration: int = 2000,
    ):
        """Display tray notification message.

        Args:
            title: Notification title
            message: Notification content
            icon_type: Icon type
            duration: Display time (milliseconds)
        """
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon_type, duration)

    def hide(self):
        """
        Hide tray icon.
        """
        if self.tray_icon:
            self.tray_icon.hide()

    def is_visible(self) -> bool:
        """
        Check if tray icon is visible.
        """
        return self.tray_icon and self.tray_icon.isVisible()

    def is_available(self) -> bool:
        """
        Check if system tray is available.
        """
        return QSystemTrayIcon.isSystemTrayAvailable()