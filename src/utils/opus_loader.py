# Handle opus dynamic library before importing opuslib
import ctypes
import os
import platform
import shutil
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Union, cast

# Get logger
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


# Platform constant definitions
class PLATFORM(Enum):
    WINDOWS = "windows"
    MACOS = "darwin"
    LINUX = "linux"


# Architecture constant definitions
class ARCH(Enum):
    WINDOWS = {"arm": "x64", "intel": "x64"}
    MACOS = {"arm": "arm64", "intel": "x64"}
    LINUX = {"arm": "arm64", "intel": "x64"}


# Dynamic library path constant definitions
class LIB_PATH(Enum):
    WINDOWS = "libs/libopus/win/x64"
    MACOS = "libs/libopus/mac/{arch}"
    LINUX = "libs/libopus/linux/{arch}"


# Dynamic library name constant definitions
class LIB_INFO(Enum):
    WINDOWS = {"name": "opus.dll", "system_name": ["opus"]}
    MACOS = {"name": "libopus.dylib", "system_name": ["libopus.dylib"]}
    LINUX = {"name": "libopus.so", "system_name": ["libopus.so.0", "libopus.so"]}


def get_platform() -> str:
    system = platform.system().lower()
    if system == "windows" or system.startswith("win"):
        system = PLATFORM.WINDOWS
    elif system == "darwin":
        system = PLATFORM.MACOS
    else:
        system = PLATFORM.LINUX
    return system


def get_arch(system: PLATFORM) -> str:
    architecture = platform.machine().lower()
    is_arm = "arm" in architecture or "aarch64" in architecture
    if system == PLATFORM.WINDOWS:
        arch_name = ARCH.WINDOWS.value["arm" if is_arm else "intel"]
    elif system == PLATFORM.MACOS:
        arch_name = ARCH.MACOS.value["arm" if is_arm else "intel"]
    else:
        arch_name = ARCH.LINUX.value["arm" if is_arm else "intel"]
    return architecture, arch_name


def get_lib_path(system: PLATFORM, arch_name: str):
    if system == PLATFORM.WINDOWS:
        lib_name = LIB_PATH.WINDOWS.value
    elif system == PLATFORM.MACOS:
        lib_name = LIB_PATH.MACOS.value.format(arch=arch_name)
    else:
        lib_name = LIB_PATH.LINUX.value.format(arch=arch_name)
    return lib_name


def get_lib_name(system: PLATFORM, local: bool = True) -> Union[str, List[str]]:
    """Get library name.

    Args:
        system (PLATFORM): Platform
        local (bool, optional): Whether to get local name (str), defaults to True. If False, get system name list (List).

    Returns:
        str | List: Library name
    """
    key = "name" if local else "system_name"
    if system == PLATFORM.WINDOWS:
        lib_name = LIB_INFO.WINDOWS.value[key]
    elif system == PLATFORM.MACOS:
        lib_name = LIB_INFO.MACOS.value[key]
    else:
        lib_name = LIB_INFO.LINUX.value[key]
    return lib_name


def get_system_info() -> Tuple[str, str]:
    """
    Get current system information.
    """
    # Standardize system name
    system = get_platform()

    # Standardize architecture name
    _, arch_name = get_arch(system)
    logger.info(f"Detected system: {system}, architecture: {arch_name}")

    return system, arch_name


def get_search_paths(system: PLATFORM, arch_name: str) -> List[Tuple[Path, str]]:
    """
    Get library file search paths list (using unified resource finder)
    """
    from .resource_finder import find_libs_dir, get_project_root

    lib_name = cast(str, get_lib_name(system))

    search_paths: List[Tuple[Path, str]] = []

    # Map system names to directory names
    system_dir_map = {
        PLATFORM.WINDOWS: "win",
        PLATFORM.MACOS: "mac",
        PLATFORM.LINUX: "linux",
    }

    system_dir = system_dir_map.get(system)

    # First try to find specific platform and architecture libs directory
    if system_dir:
        specific_libs_dir = find_libs_dir(f"libopus/{system_dir}", arch_name)
        if specific_libs_dir:
            search_paths.append((specific_libs_dir, lib_name))
            logger.debug(f"Found specific platform architecture libs directory: {specific_libs_dir}")

    # Then find specific platform libs directory
    if system_dir:
        platform_libs_dir = find_libs_dir(f"libopus/{system_dir}")
        if platform_libs_dir:
            search_paths.append((platform_libs_dir, lib_name))
            logger.debug(f"Found specific platform libs directory: {platform_libs_dir}")

    # Find general libs directory
    general_libs_dir = find_libs_dir()
    if general_libs_dir:
        search_paths.append((general_libs_dir, lib_name))
        logger.debug(f"Added general libs directory: {general_libs_dir}")

    # Add project root directory as final fallback
    project_root = get_project_root()
    search_paths.append((project_root, lib_name))

    # Print all search paths for debugging
    for dir_path, filename in search_paths:
        full_path = dir_path / filename
        logger.debug(f"Search path: {full_path} (exists: {full_path.exists()})")
    return search_paths


def find_system_opus() -> str:
    """
    Find opus library from system path.
    """
    system, _ = get_system_info()
    lib_path = ""

    try:
        # Get opus library names on the system
        lib_names = cast(List[str], get_lib_name(system, False))

        # Try to load each possible name
        for lib_name in lib_names:
            try:
                # Import ctypes.util to use find_library function
                import ctypes.util

                system_lib_path = ctypes.util.find_library(lib_name)

                if system_lib_path:
                    lib_path = system_lib_path
                    logger.info(f"Found opus library in system path: {lib_path}")
                    break
                else:
                    # Directly try to load library name
                    ctypes.cdll.LoadLibrary(lib_name)
                    lib_path = lib_name
                    logger.info(f"Directly loaded system opus library: {lib_name}")
                    break
            except Exception as e:
                logger.debug(f"Failed to load system library {lib_name}: {e}")
                continue

    except Exception as e:
        logger.error(f"Failed to find system opus library: {e}")

    return lib_path


def copy_opus_to_project(system_lib_path):
    """
    Copy system library to project directory.
    """
    from .resource_finder import get_project_root

    system, arch_name = get_system_info()

    if not system_lib_path:
        logger.error("Cannot copy opus library: system library path is empty")
        return None

    try:
        # Use resource_finder to get project root directory
        project_root = get_project_root()

        # Get target directory path - use actual directory structure
        target_path = get_lib_path(system, arch_name)
        target_dir = project_root / target_path

        # Create target directory (if it doesn't exist)
        target_dir.mkdir(parents=True, exist_ok=True)

        # Determine target filename
        lib_name = cast(str, get_lib_name(system))
        target_file = target_dir / lib_name

        # Copy file
        shutil.copy2(system_lib_path, target_file)
        logger.info(f"Copied opus library from {system_lib_path} to {target_file}")

        return str(target_file)

    except Exception as e:
        logger.error(f"Failed to copy opus library to project directory: {e}")
        return None


def setup_opus() -> bool:
    """
    Setup opus dynamic library.
    """
    # Check if already loaded by runtime_hook
    if hasattr(sys, "_opus_loaded"):
        logger.info("opus library already loaded by runtime hook")
        return True

    # Get current system information
    system, arch_name = get_system_info()
    logger.info(f"Current system: {system}, architecture: {arch_name}")

    # Build search paths
    search_paths = get_search_paths(system, arch_name)

    # Find local library file
    lib_path = ""
    lib_dir = ""

    for dir_path, file_name in search_paths:
        full_path = dir_path / file_name
        if full_path.exists():
            lib_path = str(full_path)
            lib_dir = str(dir_path)
            logger.info(f"Found opus library file: {lib_path}")
            break

    # If not found locally, try to find from system
    if not lib_path:
        logger.warning("opus library file not found locally, trying to load from system path")
        system_lib_path = find_system_opus()

        if system_lib_path:
            # First try to use system library directly
            try:
                _ = ctypes.cdll.LoadLibrary(system_lib_path)
                logger.info(f"Loaded opus library from system path: {system_lib_path}")
                sys._opus_loaded = True
                return True
            except Exception as e:
                logger.warning(f"Failed to load system opus library: {e}, trying to copy to project directory")

            # If direct loading fails, try copying to project directory
            lib_path = copy_opus_to_project(system_lib_path)
            if lib_path:
                lib_dir = str(Path(lib_path).parent)
            else:
                logger.error("Cannot find or copy opus library file")
                return False
        else:
            logger.error("opus library file not found in system either")
            return False

    # Windows platform special handling
    if system == PLATFORM.WINDOWS and lib_dir:
        # Add DLL search path
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(lib_dir)
                logger.debug(f"Added DLL search path: {lib_dir}")
            except Exception as e:
                logger.warning(f"Failed to add DLL search path: {e}")

        # Set environment variable
        os.environ["PATH"] = lib_dir + os.pathsep + os.environ.get("PATH", "")

    # Patch library path
    _patch_find_library("opus", lib_path)

    # Try to load library
    try:
        # Load DLL and store reference to prevent garbage collection
        _ = ctypes.CDLL(lib_path)
        logger.info(f"Successfully loaded opus library: {lib_path}")
        sys._opus_loaded = True
        return True
    except Exception as e:
        logger.error(f"Failed to load opus library: {e}")
        return False


def _patch_find_library(lib_name: str, lib_path: str):
    """
    Patch ctypes.util.find_library function.
    """
    import ctypes.util

    original_find_library = ctypes.util.find_library

    def patched_find_library(name):
        if name == lib_name:
            return lib_path
        return original_find_library(name)

    ctypes.util.find_library = patched_find_library
