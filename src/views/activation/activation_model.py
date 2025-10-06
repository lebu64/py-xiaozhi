# -*- coding: utf-8 -*-
"""
Activation window data model - used for QML data binding
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class ActivationModel(QObject):
    """
    Activation window data model, used for data binding between Python and QML.
    """

    # Property change signals
    serialNumberChanged = pyqtSignal()
    macAddressChanged = pyqtSignal()
    activationStatusChanged = pyqtSignal()
    activationCodeChanged = pyqtSignal()
    statusColorChanged = pyqtSignal()

    # User action signals
    copyCodeClicked = pyqtSignal()
    retryClicked = pyqtSignal()
    closeClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Private properties
        self._serial_number = "--"
        self._mac_address = "--"
        self._activation_status = "Checking..."
        self._activation_code = "--"
        self._status_color = "#6c757d"

    # Serial number property
    @pyqtProperty(str, notify=serialNumberChanged)
    def serialNumber(self):
        return self._serial_number

    @serialNumber.setter
    def serialNumber(self, value):
        if self._serial_number != value:
            self._serial_number = value
            self.serialNumberChanged.emit()

    # MAC address property
    @pyqtProperty(str, notify=macAddressChanged)
    def macAddress(self):
        return self._mac_address

    @macAddress.setter
    def macAddress(self, value):
        if self._mac_address != value:
            self._mac_address = value
            self.macAddressChanged.emit()

    # Activation status property
    @pyqtProperty(str, notify=activationStatusChanged)
    def activationStatus(self):
        return self._activation_status

    @activationStatus.setter
    def activationStatus(self, value):
        if self._activation_status != value:
            self._activation_status = value
            self.activationStatusChanged.emit()

    # Activation code property
    @pyqtProperty(str, notify=activationCodeChanged)
    def activationCode(self):
        return self._activation_code

    @activationCode.setter
    def activationCode(self, value):
        if self._activation_code != value:
            self._activation_code = value
            self.activationCodeChanged.emit()

    # Status color property
    @pyqtProperty(str, notify=statusColorChanged)
    def statusColor(self):
        return self._status_color

    @statusColor.setter
    def statusColor(self, value):
        if self._status_color != value:
            self._status_color = value
            self.statusColorChanged.emit()

    # Convenience methods
    def update_device_info(self, serial_number=None, mac_address=None):
        """Update device information"""
        if serial_number is not None:
            self.serialNumber = serial_number
        if mac_address is not None:
            self.macAddress = mac_address

    def update_activation_status(self, status, color="#6c757d"):
        """Update activation status"""
        self.activationStatus = status
        self.statusColor = color

    def update_activation_code(self, code):
        """Update activation code"""
        self.activationCode = code

    def reset_activation_code(self):
        """Reset activation code"""
        self.activationCode = "--"

    def set_status_activated(self):
        """Set to activated status"""
        self.update_activation_status("Activated", "#28a745")
        self.reset_activation_code()

    def set_status_not_activated(self):
        """Set to not activated status"""
        self.update_activation_status("Not Activated", "#dc3545")

    def set_status_inconsistent(self, local_activated=False, server_activated=False):
        """Set status inconsistent"""
        if local_activated and not server_activated:
            self.update_activation_status("Status Inconsistent (Needs Reactivation)", "#ff9900")
        else:
            self.update_activation_status("Status Inconsistent (Fixed)", "#28a745")
