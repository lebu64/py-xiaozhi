import platform

from src.utils.config_manager import ConfigManager

config = ConfigManager.get_instance()


class ListeningMode:
    """
    Listening mode.
    """

    REALTIME = "realtime"
    AUTO_STOP = "auto_stop"
    MANUAL = "manual"


class AbortReason:
    """
    Abort reason.
    """

    NONE = "none"
    WAKE_WORD_DETECTED = "wake_word_detected"
    USER_INTERRUPTION = "user_interruption"


class DeviceState:
    """
    Device state.
    """

    IDLE = "idle"
    CONNECTING = "connecting"
    LISTENING = "listening"
    SPEAKING = "speaking"


class EventType:
    """
    Event type.
    """

    SCHEDULE_EVENT = "schedule_event"
    AUDIO_INPUT_READY_EVENT = "audio_input_ready_event"
    AUDIO_OUTPUT_READY_EVENT = "audio_output_ready_event"


def is_official_server(ws_addr: str) -> bool:
    """Check if it's the official XiaoZhi server address.

    Args:
        ws_addr (str): WebSocket address

    Returns:
        bool: Whether it's the official XiaoZhi server address
    """
    return "api.tenclass.net" in ws_addr


def get_frame_duration() -> int:
    """Get device frame duration.

    Returns:
        int: Frame duration (milliseconds)
    """
    try:
        # Check if it's the official server
        ota_url = config.get_config("SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL")
        if not is_official_server(ota_url):
            return 60

        # Detect ARM architecture devices (like Raspberry Pi)
        machine = platform.machine().lower()
        arm_archs = ["arm", "aarch64", "armv7l", "armv6l"]
        is_arm_device = any(arch in machine for arch in arm_archs)

        if is_arm_device:
            # ARM devices (like Raspberry Pi) use larger frame duration to reduce CPU load
            return 60
        else:
            # Other devices (Windows/macOS/Linux x86) have sufficient performance, use low latency
            return 20

    except Exception:
        # If acquisition fails, return default value 20ms (suitable for most modern devices)
        return 20


class AudioConfig:
    """
    Audio configuration class.
    """

    # Fixed configuration
    INPUT_SAMPLE_RATE = 16000  # Input sample rate 16kHz
    # Output sample rate: official server uses 24kHz, others use 16kHz
    _ota_url = config.get_config("SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL")
    OUTPUT_SAMPLE_RATE = 24000 if is_official_server(_ota_url) else 16000
    CHANNELS = 1

    # Dynamically get frame duration
    FRAME_DURATION = get_frame_duration()

    # Calculate frame size based on different sample rates
    INPUT_FRAME_SIZE = int(INPUT_SAMPLE_RATE * (FRAME_DURATION / 1000))
    # Linux system uses fixed frame size to reduce PCM printing, other systems calculate dynamically
    OUTPUT_FRAME_SIZE = int(OUTPUT_SAMPLE_RATE * (FRAME_DURATION / 1000))
