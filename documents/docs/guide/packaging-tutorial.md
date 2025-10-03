# Project Packaging Tutorial

## Overview

UnifyPy 2.0 is an enterprise-level cross-platform Python application packaging solution that supports packaging Python projects into native installation packages for Windows, macOS, and Linux platforms. Compared to version 1.0, version 2.0 introduces new features such as parallel building, intelligent path processing, and enterprise-level rollback system. The Xiaozhi client has been configured with corresponding packaging configuration files, and this tutorial will guide you on how to use UnifyPy 2.0 for packaging.

### ✨ UnifyPy 2.0 New Features

- **🔄 Cross-platform Support**: Windows (EXE), macOS (DMG), Linux (DEB)
- **🛡️ Enterprise Features**: Automatic rollback, session management, intelligent error handling
- **🎨 Excellent Experience**: Rich progress bars, phased display, detailed logs
- **📊 Intelligent Path Processing**: Relative paths automatically resolved to absolute paths
- **🍎 macOS Permission Management**: Automatic permission file generation, code signing support

## Preparation

### 1. Install py-xiaozhi Project Dependencies

First ensure you have activated the Python environment for the py-xiaozhi project and installed all project dependencies:

```bash
# Enter py-xiaozhi project directory
cd /path/to/py-xiaozhi

# Install project dependencies based on platform
pip install -r requirements.txt        # Windows/Linux
# or
pip install -r requirements_mac.txt    # macOS
```

### 2. Install UnifyPy Dependencies in Project Environment

Install UnifyPy required dependencies in the same environment:

- Theoretically, the environment where py-xiaozhi is installed comes with these by default, if not, re-execute:

```bash
# One-click installation of all dependencies required by UnifyPy
pip install pyinstaller==6.15.0 rich==14.1.0 requests==2.32.3 packaging==25.0 pillow==11.3.0
```

### 3. Get UnifyPy 2.0

```bash
# Clone UnifyPy repository (recommended to place in same level directory as py-xiaozhi)
git clone https://github.com/huangjunsen0406/UnifyPy.git
```

### 4. Verify Environment Configuration

Verify all dependencies work properly in the current environment:

```bash
# Verify UnifyPy dependencies
python -c "import pyinstaller, rich, requests, packaging, pillow; print('✅ UnifyPy dependencies installed successfully')"

# Verify py-xiaozhi project dependencies (adjust according to actual situation)
python -c "import numpy, PyQt5; print('✅ py-xiaozhi project dependencies available')"

# Display current environment information
echo "Current environment: $(which python)"
echo "Python version: $(python --version)"
```

### Why Install in the Same Environment?

UnifyPy uses PyInstaller for packaging, which needs to access all Python packages in the current environment for dependency analysis. If dependencies are scattered across different environments, PyInstaller cannot package correctly.

### 3. Install Platform Specific Tools

#### Windows Platform

- Install [Inno Setup](https://jrsoftware.org/isdl.php) (for creating installers)
- After installation, configure Inno Setup path in build.json, or set environment variable INNO_SETUP_PATH
- Copy ChineseSimplified.isl from UnifyPy to inno setup installation directory language folder (Windows)

#### macOS Platform

- UnifyPy 2.0 has built-in create-dmg tool, no need to install separately

#### Linux Platform

Install DEB packaging tools:

```bash
# DEB format (Debian/Ubuntu)
sudo apt-get install dpkg-dev fakeroot
```

**Linux Compilation Environment Preparation** (Important):

```bash
# Install necessary development tools and libraries
sudo apt update
sudo apt install -y build-essential python3-dev python3-pip python3-setuptools \
    libopenblas-dev liblapack-dev gfortran patchelf autoconf automake \
    libtool cmake libssl-dev libatlas-base-dev

# Install modern build system
pip install meson ninja
sudo apt install -y meson ninja-build
```

## Packaging Configuration Details

The Xiaozhi client already provides pre-configured `build.json` file. UnifyPy 2.0 supports richer configuration options and intelligent path processing. Here are detailed explanations of each configuration item:

### Intelligent Path Processing

UnifyPy 2.0 introduces intelligent path processing functionality, relative paths in configuration files are automatically resolved to absolute paths relative to **target project directory**:

- ✅ `"icon": "assets/icon.png"` → `/path/to/project/assets/icon.png`  
- ✅ `"add_data": ["data:data"]` → `/path/to/project/data:data`
- ✅ Supports nested configuration and platform specific paths

### Basic Configuration

```json
{
    "name": "xiaozhi",                  // Application name, will be used for executable file and installer name
    "version": "1.0.0",                 // Application version number
    "publisher": "Junsen",              // Publisher name
    "entry": "main.py",                 // Program entry file
    "icon": "assets/xiaozhi_icon.ico",  // Application icon path
    "hooks": "hooks",                   // PyInstaller hooks directory
    "onefile": false,                   // Whether to generate single file mode executable
    
    // PyInstaller general parameters, applicable to all platforms
    "additional_pyinstaller_args": "--add-data assets;assets --add-data libs;libs --add-data src;src --add-data models;models --hidden-import=PyQt5",
    
    // Inno Setup path (Windows platform needs)
    "inno_setup_path": "E:\\application\\Inno Setup 6\\ISCC.exe",
    
    // Other configuration...
}
```

> **Note**: JSON files do not support comments, the comments in the above code are for explanation only, actual configuration files should not contain comments.

### Platform Specific Configuration

#### Windows Platform Configuration

```json
"windows": {
    "format": "exe",                  // Output format
    "additional_pyinstaller_args": "--add-data assets;assets --add-data libs;libs --add-data src;src --add-data models;models --hidden-import=PyQt5 --noconsole",
    "desktop_entry": true,            // Whether to create desktop shortcut
    "installer_options": {
        "languages": ["ChineseSimplified", "English"],  // Installer supported languages
        "license_file": "LICENSE",                      // License file
        "readme_file": "README.md",                     // Readme file
        "create_desktop_icon": true,                    // Whether to create desktop icon
        "allow_run_after_install": true                 // Whether to allow immediate run after installation
    }
}
```

#### Linux Platform Configuration

```json
"linux": {
    "format": "deb",                  // Output format: deb
    "desktop_entry": true,            // Whether to create desktop shortcut
    "categories": "Utility;Development;",  // Application categories
    "description": "Xiaozhi Ai Client",          // Application description
    "requires": "libc6,libgtk-3-0,libx11-6,libopenblas-dev",  // Dependencies
    "additional_pyinstaller_args": "--add-data assets:assets --add-data libs:libs --add-data src:src --add-data models:models --hidden-import=PyQt5"
}
```

#### macOS Platform Configuration

```json
"macos": {
    "format": "app",                  // Output format, options: app, dmg
    "additional_pyinstaller_args": "--add-data assets:assets --add-data libs:libs --add-data src:src --add-data models:models --hidden-import=PyQt5 --windowed",
    "app_bundle_name": "XiaoZhi.app", // Application bundle name
    "bundle_identifier": "com.junsen.xiaozhi",  // Application identifier
    "sign_bundle": false,             // Whether to sign application bundle
    "create_dmg": true,               // Whether to create DMG image
    "installer_options": {
        "license_file": "LICENSE",    // License file
        "readme_file": "README.md"    // Readme file
    }
}
```

### Other Important Configuration Items

```json
"build_installer": true  // Whether to build installer, set to false to only generate executable file
```

> **Tip**: The `.unifypy` folder automatically generated by UnifyPy contains packaging configurations for all platforms, no need for manual maintenance. If customization is needed, directly edit the corresponding platform configuration files.

### Windows Application Identifier (AppId) Management

UnifyPy 2.0 automatically manages Windows installer AppId, no need to manually modify template files.

#### Automatic Generation Mechanism

When packaging for the first time, UnifyPy automatically creates `.unifypy` folder in project root directory, containing platform configuration files:

```
Project Directory/
├── .unifypy/
│   ├── cache/             # Build cache
│   ├── linux/
│   │   ├── app.desktop    # Linux desktop file
│   │   └── control        # DEB package control file
│   ├── macos/
│   │   ├── dmg_config.json # DMG configuration
│   │   └── Info.plist     # macOS application information
│   ├── windows/
│   │   └── setup.iss      # Inno Setup script (contains AppId)
│   ├── .gitignore         # Git ignore rules
│   └── metadata.json      # Project metadata
├── build.json
└── main.py
```

#### Custom AppId (Optional)

If enterprise-specific AppId is needed, manually edit `.unifypy/windows/setup.iss` file before first packaging:

```ini
[Setup]
AppId={{{Your Enterprise GUID}}}  ; Replace with enterprise custom GUID
AppName=XiaoZhi
AppVersion=1.0.0
; ...(Other configuration)
```

**Or configure in `metadata.json`**:

```json
{
  "project_name": "xiaozhi",
  "app_id": "{Your Enterprise GUID}",
  "created_date": "2024-01-01T00:00:00Z",
  "last_modified": "2024-01-01T00:00:00Z"
}
```

**Ways to get Enterprise GUID**:

- Online generation tool: [Online GUID Generator](https://www.guidgenerator.com/)
- Visual Studio command: `Tools > Create GUID`
- PowerShell command: `[System.Guid]::NewGuid()`

#### File Management Suggestions

1. **Version Control**: Add `.unifypy` folder to Git version control, but exclude cache directory:

   ```gitignore
   # Add in project root directory .gitignore
   .unifypy/cache/
   ```

2. **AppId Management**: Once AppId is generated, it's recommended not to change it arbitrarily to avoid upgrade conflicts in installer

3. **Team Collaboration**: Ensure all team members use same UnifyPy configuration, especially Windows AppId

## Execute Packaging

### Environment Preparation

**Important**: Before packaging, ensure UnifyPy and target project are in same environment:

```bash
# Activate unified environment
conda activate packaging-env  # or source build_env/bin/activate

# Verify environment
which python
python -c "import rich, requests, numpy, PyQt5; print('Environment ready')"
```

### UnifyPy 2.0 Basic Packaging Commands

Recommended to place UnifyPy in same level directory as py-xiaozhi project:

```bash
# Basic packaging (recommended)
python ../UnifyPy/main.py . --config build.json

# Verbose output mode
python ../UnifyPy/main.py . --config build.json --verbose

# Clean rebuild
python ../UnifyPy/main.py . --config build.json --clean --verbose

# Only generate executable file, skip installer
python ../UnifyPy/main.py . --config build.json --skip-installer

# Specify specific format
python ../UnifyPy/main.py . --config build.json --format exe   # Windows
python ../UnifyPy/main.py . --config build.json --format dmg   # macOS  
python ../UnifyPy/main.py . --config build.json --format deb   # Linux
```

### Main Command Line Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--clean` | Clean previous build files | `--clean` |
| `--skip-exe` | Skip executable file build | `--skip-exe` |
| `--skip-installer` | Skip installer build | `--skip-installer` |
| `--format FORMAT` | Specify output format(exe/dmg/deb) | `--format deb` |
| `--development` | macOS development mode (automatic permission configuration) | `--development` |
| `--list-rollback` | List available rollback sessions | `--list-rollback` |
| `--rollback SESSION_ID` | Execute specified session rollback | `--rollback abc123` |

### Packaging Commands for Different Platforms

#### Windows Platform

```bash
python C:\path\to\UnifyPy\main.py . --config build.json
```

#### macOS Platform

```bash
python /path/to/UnifyPy/main.py . --config build.json
```

#### Linux Platform (DEB Format)

1. **Prepare Environment**

   ```bash
   # Update system and install necessary dependencies
   sudo apt update
   sudo apt install -y build-essential python3-dev python3-pip python3-setuptools libopenblas-dev liblapack-dev gfortran patchelf autoconf automake libtool cmake libssl-dev libatlas-base-dev
   ```

2. **Execute Packaging**

   Ensure linux.format in build.json is set to "deb", then execute:

   ```bash
   python3 /path/to/UnifyPy/main.py . --config build.json
   ```

### Linux Platform Dependency Processing Notes

**NumPy Compilation Environment Configuration (Important)**

**⚠️ Important Reminder**: Do not delete NumPy! The correct approach is to ensure compilation environment is configured correctly.

```bash
# Option 1: Recommended solution - Ensure NumPy dependencies compile correctly
# Set environment variables
export BLAS=openblas
export LAPACK=openblas
export NPY_NUM_BUILD_JOBS=$(nproc)  # Use all CPU cores to accelerate compilation

# Verify current NumPy availability
python -c "import numpy; print('NumPy version:', numpy.__version__); print('BLAS info:', numpy.show_config())"

# If above command succeeds, no need to recompile
```

**Alternative Solution**: Use conda to manage dependencies (recommended for complex environments):

```bash
# Install conda/miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Create environment and install dependencies
conda create -n build_env python=3.9
conda activate build_env
conda install numpy scipy openblas-devel
pip install -r requirements.txt
```

## Packaging Output

After successful packaging, packaged applications will be found in `dist` folder under project root directory:

- **Windows**:
  - Executable file (.exe) located in `dist/xiaozhi` directory
  - Installer located in `dist/installer` directory, named `xiaozhi-1.0.0-setup.exe`

- **macOS**:
  - Application bundle (.app) located in `dist/xiaozhi` directory
  - Disk image (.dmg) located in `dist/installer` directory, named `xiaozhi-1.0.0.dmg`

- **Linux**:
  - Executable file located in `dist/xiaozhi` directory
  - DEB installation package located in `dist/installer` directory: `xiaozhi-1.0.0.deb`

## Advanced Configuration Options

### PyInstaller Parameters

In `additional_pyinstaller_args` field, you can add any PyInstaller supported parameters. Here are some commonly used parameters:

- `--noconsole`: Do not display console window (only for GUI programs)
- `--windowed`: Equivalent to `--noconsole`
- `--hidden-import=MODULE`: Add implicitly imported modules
- `--add-data SRC;DEST`: Add data files (Windows platform uses semicolon separator)
- `--add-data SRC:DEST`: Add data files (macOS/Linux platform uses colon separator)
- `--icon=FILE.ico`: Set application icon

### Handling Special Dependencies

Some Python libraries may require special handling to package correctly, can be resolved through following methods:

1. **Use Hook Files**: Create custom hooks in `hooks` directory to handle special import situations
2. **Add Implicit Imports**: Use `--hidden-import` parameter to explicitly include implicitly imported modules
3. **Add Data Files**: Use `--add-data` parameter to include data files required for program operation

## UnifyPy 2.0 New Features Detailed Explanation

### 🔄 Rollback System

UnifyPy 2.0 introduces enterprise-level rollback system, automatically tracking build operations:

```bash
# List available rollback sessions
python ../UnifyPy/main.py . --list-rollback

# Execute rollback to specified session
python ../UnifyPy/main.py . --rollback SESSION_ID

# Disable automatic rollback (improve performance)
python ../UnifyPy/main.py . --config build.json --no-rollback
```

### 🍎 macOS Automatic Permission Management

UnifyPy 2.0 provides complete permission management solution for macOS applications:

```bash
# Development mode - Automatically generate permission files, suitable for development and testing
python ../UnifyPy/main.py . --config build.json --development

# Production mode - For already signed applications
python ../UnifyPy/main.py . --config build.json --production
```

**Automation Features**:

- ✅ Automatically generate entitlements.plist
- ✅ Automatically update Info.plist permission descriptions  
- ✅ Automatically ad-hoc code signing
- ✅ Automatically convert icon formats (PNG → ICNS)

## Common Issues and Solutions

### Windows Platform Common Issues

1. **Cannot Find Inno Setup**

   Solution
