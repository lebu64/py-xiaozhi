import platform
import re
import shutil
import subprocess
from functools import wraps
from typing import Any, Callable, List, Optional

from src.utils.logging_config import get_logger


class VolumeController:
    """
    Cross-platform volume controller.
    """

    # Default volume constant
    DEFAULT_VOLUME = 70

    # Platform-specific method mapping
    PLATFORM_INIT = {
        "Windows": "_init_windows",
        "Darwin": "_init_macos",
        "Linux": "_init_linux",
    }

    VOLUME_METHODS = {
        "Windows": ("_get_windows_volume", "_set_windows_volume"),
        "Darwin": ("_get_macos_volume", "_set_macos_volume"),
        "Linux": ("_get_linux_volume", "_set_linux_volume"),
    }

    LINUX_VOLUME_METHODS = {
        "pactl": ("_get_pactl_volume", "_set_pactl_volume"),
        "wpctl": ("_get_wpctl_volume", "_set_wpctl_volume"),
        "amixer": ("_get_amixer_volume", "_set_amixer_volume"),
        "alsamixer": (None, "_set_alsamixer_volume"),
    }

    # Platform-specific module dependencies
    PLATFORM_MODULES = {
        "Windows": {
            "pycaw": "pycaw.pycaw",
            "comtypes": "comtypes",
            "ctypes": "ctypes",
        },
        "Darwin": {
            "applescript": "applescript",
        },
        "Linux": {},
    }

    def __init__(self):
        """
        Initialize volume controller.
        """
        self.logger = get_logger("VolumeController")
        self.system = platform.system()
        self.is_arm = platform.machine().startswith(("arm", "aarch"))
        self.linux_tool = None
        self._module_cache = {}  # Module cache

        # Initialize platform-specific controller
        init_method_name = self.PLATFORM_INIT.get(self.system)
        if init_method_name:
            init_method = getattr(self, init_method_name)
            init_method()
        else:
            self.logger.warning(f"Unsupported operating system: {self.system}")
            raise NotImplementedError(f"Unsupported operating system: {self.system}")

    def _lazy_import(self, module_name: str, attr: str = None) -> Any:
        """Lazy load module, support caching and attribute import.

        Args:
            module_name: Module name
            attr: Optional, attribute name in module

        Returns:
            Imported module or attribute
        """
        if module_name in self._module_cache:
            module = self._module_cache[module_name]
        else:
            try:
                module = __import__(
                    module_name, fromlist=["*"] if "." in module_name else []
                )
                self._module_cache[module_name] = module
            except ImportError as e:
                self.logger.warning(f"Failed to import module {module_name}: {e}")
                raise

        if attr:
            return getattr(module, attr)
        return module

    def _safe_execute(self, func_name: str, default_return: Any = None) -> Callable:
        """
        Decorator for safe function execution.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.warning(f"{func_name} failed: {e}")
                    return default_return

            return wrapper

        return decorator

    def _run_command(
        self, cmd: List[str], check: bool = False
    ) -> Optional[subprocess.CompletedProcess]:
        """
        Generic command execution method.
        """
        try:
            return subprocess.run(cmd, capture_output=True, text=True, check=check)
        except Exception as e:
            self.logger.debug(f"Failed to execute command {' '.join(cmd)}: {e}")
            return None

    def _init_windows(self) -> None:
        """
        Initialize Windows volume control.
        """
        try:
            # Use lazy loading to import required modules
            POINTER = self._lazy_import("ctypes", "POINTER")
            cast = self._lazy_import("ctypes", "cast")
            CLSCTX_ALL = self._lazy_import("comtypes", "CLSCTX_ALL")
            AudioUtilities = self._lazy_import("pycaw.pycaw", "AudioUtilities")
            IAudioEndpointVolume = self._lazy_import(
                "pycaw.pycaw", "IAudioEndpointVolume"
            )

            self.devices = AudioUtilities.GetSpeakers()
            interface = self.devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
            self.logger.debug("Windows volume control initialized successfully")
        except Exception as e:
            self.logger.error(f"Windows volume control initialization failed: {e}")
            raise

    def _init_macos(self) -> None:
        """
        Initialize macOS volume control.
        """
        try:
            applescript = self._lazy_import("applescript")

            # Test if volume control can be accessed
            result = applescript.run("get volume settings")
            if not result or result.code != 0:
                raise Exception("Cannot access macOS volume control")
            self.logger.debug("macOS volume control initialized successfully")
        except Exception as e:
            self.logger.error(f"macOS volume control initialization failed: {e}")
            raise

    def _init_linux(self) -> None:
        """
        Initialize Linux volume control.
        """
        # Check tools by priority
        linux_tools = ["pactl", "wpctl", "amixer"]
        for tool in linux_tools:
            if shutil.which(tool):
                self.linux_tool = tool
                break

        # Check alsamixer as alternative
        if not self.linux_tool and shutil.which("alsamixer") and shutil.which("expect"):
            self.linux_tool = "alsamixer"

        if not self.linux_tool:
            self.logger.error("No available Linux volume control tools found")
            raise Exception("No available Linux volume control tools found")

        self.logger.debug(f"Linux volume control initialized successfully, using: {self.linux_tool}")

    def get_volume(self) -> int:
        """
        Get current volume (0-100)
        """
        get_method_name, _ = self.VOLUME_METHODS.get(self.system, (None, None))
        if not get_method_name:
            return self.DEFAULT_VOLUME

        get_method = getattr(self, get_method_name)
        return get_method()

    def set_volume(self, volume: int) -> None:
        """
        Set volume (0-100)
        """
        # Ensure volume is within valid range
        volume = max(0, min(100, volume))

        _, set_method_name = self.VOLUME_METHODS.get(self.system, (None, None))
        if set_method_name:
            set_method = getattr(self, set_method_name)
            set_method(volume)

    @property
    def _get_windows_volume(self) -> Callable[[], int]:
        @self._safe_execute("Get Windows volume", self.DEFAULT_VOLUME)
        def get_volume():
            volume_scalar = self.volume_control.GetMasterVolumeLevelScalar()
            return int(volume_scalar * 100)

        return get_volume

    @property
    def _set_windows_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set Windows volume")
        def set_volume(volume):
            self.volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)

        return set_volume

    @property
    def _get_macos_volume(self) -> Callable[[], int]:
        @self._safe_execute("Get macOS volume", self.DEFAULT_VOLUME)
        def get_volume():
            applescript = self._lazy_import("applescript")
            result = applescript.run("output volume of (get volume settings)")
            if result and result.out:
                return int(result.out.strip())
            return self.DEFAULT_VOLUME

        return get_volume

    @property
    def _set_macos_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set macOS volume")
        def set_volume(volume):
            applescript = self._lazy_import("applescript")
            applescript.run(f"set volume output volume {volume}")

        return set_volume

    def _get_linux_volume(self) -> int:
        """
        Get Linux volume.
        """
        get_method_name, _ = self.LINUX_VOLUME_METHODS.get(
            self.linux_tool, (None, None)
        )
        if not get_method_name:
            return self.DEFAULT_VOLUME

        get_method = getattr(self, get_method_name)
        return get_method()

    def _set_linux_volume(self, volume: int) -> None:
        """
        Set Linux volume.
        """
        _, set_method_name = self.LINUX_VOLUME_METHODS.get(
            self.linux_tool, (None, None)
        )
        if set_method_name:
            set_method = getattr(self, set_method_name)
            set_method(volume)

    @property
    def _get_pactl_volume(self) -> Callable[[], int]:
        @self._safe_execute("Get volume via pactl", self.DEFAULT_VOLUME)
        def get_volume():
            result = self._run_command(["pactl", "list", "sinks"])
            if result and result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "Volume:" in line and "front-left:" in line:
                        match = re.search(r"(\d+)%", line)
                        if match:
                            return int(match.group(1))
            return self.DEFAULT_VOLUME

        return get_volume

    @property
    def _set_pactl_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set volume via pactl")
        def set_volume(volume):
            self._run_command(
                ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume}%"]
            )

        return set_volume

    @property
    def _get_wpctl_volume(self) -> Callable[[], int]:
        @self._safe_execute("Get volume via wpctl", self.DEFAULT_VOLUME)
        def get_volume():
            result = self._run_command(
                ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], check=True
            )
            if result:
                return int(float(result.stdout.split(" ")[1]) * 100)
            return self.DEFAULT_VOLUME

        return get_volume

    @property
    def _set_wpctl_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set volume via wpctl")
        def set_volume(volume):
            self._run_command(
                ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{volume}%"],
                check=True,
            )

        return set_volume

    @property
    def _get_amixer_volume(self) -> Callable[[], int]:
        @self._safe_execute("Get volume via amixer", self.DEFAULT_VOLUME)
        def get_volume():
            result = self._run_command(["amixer", "get", "Master"])
            if result and result.returncode == 0:
                match = re.search(r"(\d+)%", result.stdout)
                if match:
                    return int(match.group(1))
            return self.DEFAULT_VOLUME

        return get_volume

    @property
    def _set_amixer_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set volume via amixer")
        def set_volume(volume):
            self._run_command(["amixer", "sset", "Master", f"{volume}%"])

        return set_volume

    @property
    def _set_alsamixer_volume(self) -> Callable[[int], None]:
        @self._safe_execute("Set volume via alsamixer")
        def set_volume(volume):
            script = f"""
            spawn alsamixer
            send "m"
            send "{volume}"
            send "%"
            send "q"
            expect eof
            """
            self._run_command(["expect", "-c", script])

        return set_volume

    @staticmethod
    def check_dependencies() -> bool:
        """
        Check and report missing dependencies.
        """
        system = platform.system()
        missing = []

        # Check Python module dependencies
        VolumeController._check_python_modules(system, missing)

        # Check Linux tool dependencies
        if system == "Linux":
            VolumeController._check_linux_tools(missing)

        # Report missing dependencies
        return VolumeController._report_missing_dependencies(system, missing)

    @staticmethod
    def _check_python_modules(system: str, missing: List[str]) -> None:
        """
        Check Python module dependencies.
        """
        if system == "Windows":
            for module in ["pycaw", "comtypes"]:
                try:
                    __import__(module)
                except ImportError:
                    missing.append(module)
        elif system == "Darwin":  # macOS
            try:
                __import__("applescript")
            except ImportError:
                missing.append("applescript")

    @staticmethod
    def _check_linux_tools(missing: List[str]) -> None:
        """
        Check Linux tool dependencies.
        """
        tools = ["pactl", "wpctl", "amixer", "alsamixer"]
        found = any(shutil.which(tool) for tool in tools)
        if not found:
            missing.append("pulseaudio-utils, wireplumber or alsa-utils")

    @staticmethod
    def _report_missing_dependencies(system: str, missing: List[str]) -> bool:
        """
        Report missing dependencies.
        """
        if missing:
            print(f"Warning: Volume control requires the following dependencies but they were not found: {', '.join(missing)}")
            print("Please use the following command to install missing dependencies:")
            if system in ["Windows", "Darwin"]:
                print("pip install " + " ".join(missing))
            elif system == "Linux":
                print("sudo apt-get install " + " ".join(missing))
            return False
        return True
