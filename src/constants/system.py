# System constants definition
from enum import Enum


class InitializationStage(Enum):
    """
    Initialization stage enumeration.
    """

    DEVICE_FINGERPRINT = "Stage 1: Device identity preparation"
    CONFIG_MANAGEMENT = "Stage 2: Configuration management initialization"
    OTA_CONFIG = "Stage 3: OTA configuration acquisition"
    ACTIVATION = "Stage 4: Activation process"


class SystemConstants:
    """
    System constants.
    """

    # Application information
    APP_NAME = "py-xiaozhi"
    APP_VERSION = "2.0.0"
    BOARD_TYPE = "bread-compact-wifi"

    # Default timeout settings
    DEFAULT_TIMEOUT = 10
    ACTIVATION_MAX_RETRIES = 60
    ACTIVATION_RETRY_INTERVAL = 5

    # File name constants
    CONFIG_FILE = "config.json"
    EFUSE_FILE = "efuse.json"
