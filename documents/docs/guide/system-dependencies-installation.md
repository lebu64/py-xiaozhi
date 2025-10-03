# System Dependencies Installation

## Overview

This document provides complete dependency installation guidelines for the py-xiaozhi project, including system-level dependencies and Python environment configuration. Please follow the documentation order for installation.

> Compatibility range: Ubuntu **20.04 / 22.04 / 23.10 / 24.04 / 25.xx**.
> **Qt installation source unified: Only use pip or conda to install PyQt5 (do not use apt's python3-pyqt5)**. ARM Ubuntu (aarch64) strongly recommends **conda** for PyQt installation.

## System Dependencies Installation

### Windows

#### Multimedia Components

```bash
# Use Scoop to install (recommended)
scoop install ffmpeg

# Or use Conda
conda install -c conda-forge ffmpeg opus
```

#### Manual FFmpeg Installation

1. Download: [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
2. Add the `bin` directory to the system environment variable `PATH` after extraction

#### Opus Audio Codec

* The project already includes `opus.dll`, usually no additional installation needed
* If encountering issues, copy `/libs/windows/opus.dll` to:

  * Application runtime directory
  * `C:\Windows\System32`

### Linux (Debian/Ubuntu)

> Compatible with Ubuntu **20/22/23/24/25**. The following commands apply to all the above versions; if some minimal images lack packages, install them as prompted.
> **Please do not install apt's `python3-pyqt5*`, Qt should only be installed via pip/conda.**

#### Core Dependencies

```bash
# Update package manager
sudo apt-get update

# Install core dependencies (excluding Qt)
sudo apt-get install -y portaudio19-dev libportaudio2 ffmpeg libopus0 libopus-dev \
                        build-essential python3-venv python3-pip libasound2-dev \
                        libxcb-xinerama0 libxkbcommon-x11-0
```

* `libxcb-xinerama0`, `libxkbcommon-x11-0`: Runtime libraries that Qt GUI might be missing in some desktop environments; installing them provides more stability.
* **Audio System** (choose one):

  * PulseAudio tools (recommended):

    ```bash
    sudo apt-get install -y pulseaudio-utils
    ```

  * ALSA:

    ```bash
    sudo apt-get install -y alsa-utils
    ```

  * ALSA + interactive tools:

    ```bash
    sudo apt-get install -y alsa-utils expect
    ```

* Note: Ubuntu 24+ defaults to PipeWire, but `pulseaudio-utils` is still usable through the `pipewire-pulse` compatibility layer, not affecting this project.

#### Development Tools (Optional)

```bash
sudo apt-get install -y gcc g++ make cmake pkg-config
```

### macOS

```bash
# Use Homebrew to install
brew install portaudio opus ffmpeg gfortran
brew upgrade tcl-tk

# Install Xcode command line tools (if not installed)
xcode-select --install
```

## Python Environment Configuration

### Method 1: Using Miniconda (Recommended)

#### 1. Download Miniconda

| Operating System | Architecture | Download Command                                                                                                                |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Linux**        | x86_64       | `wget -O Miniconda3-latest-Linux-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`               |
| **Linux**        | ARM64        | `wget -O Miniconda3-latest-Linux-aarch64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh`             |
| **macOS**        | Intel        | `wget -O Miniconda3-latest-MacOSX-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh`             |
| **macOS**        | Apple Silicon | `wget -O Miniconda3-latest-MacOSX-arm64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh`               |
| **Windows**      | x86_64       | [Download Link](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)                                       |

#### 2. Install Miniconda

**Linux/macOS**

```bash
# Add execution permissions
chmod +x Miniconda3-latest-*.sh

# Run installer
./Miniconda3-latest-*.sh
```

Installation process choices:

1. License agreement: Press `Enter` or `q` to skip, enter `yes` to accept
2. Installation path: Use default path (recommended)
3. Initialization: Enter `yes` (recommended)

#### 3. Configure Environment (if needed)

```bash
# If environment variables not automatically configured
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Initialize conda
conda init
```

#### 4. Verify Installation

```bash
conda --version
```

#### 5. Optimize Configuration

```bash
# Disable automatic base environment activation
conda config --set auto_activate_base false

# Add conda-forge channel
conda config --add channels conda-forge
```

### Method 2: Using System Python + venv

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

## (Unified) Qt Installation via pip/conda

> Only use pip or conda to install PyQt5, do not use apt's PyQt.
> **ARM Ubuntu (aarch64) strongly recommends: Conda for PyQt installation**; x86_64 can use pip or conda. Do not mix the two.

### Route B1: Conda Install PyQt (Recommended for ARM Ubuntu)

```bash
# Recommended minimal system dependencies (skip if already installed in "Core Dependencies")
sudo apt-get update
sudo apt-get install -y libportaudio2 portaudio19-dev ffmpeg libopus0 \
                        libasound2-dev libxcb-xinerama0 libxkbcommon-x11-0

# Create and enter environment
conda create -n py-xiaozhi python=3.10 -y
conda activate py-xiaozhi

# Use conda to install PyQt and C++ runtime libraries (avoid GLIBCXX issues)
conda install -c conda-forge -y pyqt=5.15 libstdcxx-ng>=13 libgcc-ng>=13

# PortAudio binding (choose one)
# A) Use system libportaudio (already installed via apt)
pip install sounddevice
# B) Let conda handle everything (no system dependency)
# conda install -c conda-forge -y portaudio jack python-sounddevice

# Other dependencies
pip install -r requirements.txt   # Ensure requirements.txt doesn't contain PyQt5
```

### Route B2: pip Install PyQt (More stable for x86_64; ARM may lack wheels, not recommended)

```bash
# Dev dependencies needed if fallback to source build (install only if failed)
sudo apt-get install -y build-essential python3-dev \
                        qtbase5-dev qtchooser qt5-qmake qtmultimedia5-dev

# venv
python3 -m venv .venv
source .venv/bin/activate

# Install PyQt (ARM will attempt native build if no manylinux wheels, use conda if fails)
pip install "PyQt5==5.15.*" PyQt5-Qt5 PyQt5-sip

# Other dependencies
pip install -r requirements.txt   # Similarly, don't install PyQt5 again
```

> **Do not mix**:
>
> * If you choose **pip/conda** for PyQt, **do not** `apt install python3-pyqt5*`.
> * If you choose **apt** for PyQt (this file has removed this option), **do not** install PyQt via pip/conda.

## Package Manager Optimization

### Source Change Tool (Recommended)

```bash
# Windows (PowerShell administrator privileges)
winget install RubyMetric.chsrc --source winget

# Linux/macOS
wget -O- aslant.top/chsrc.sh | sudo bash

# Configure pip source
chsrc set pip
```

### Manual pip Source Configuration

```bash
# Use Alibaba Cloud mirror source
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
```

## Project Dependencies Installation

### 1. Create Project Environment

```bash
# Use Conda (recommended)
conda create -n py-xiaozhi python=3.10 -y
conda activate py-xiaozhi

# Or use venv
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### 2. Install Python Dependencies

```bash
# Linux/Windows
pip install -r requirements.txt

# macOS
pip install -r requirements_mac.txt
```

### 3. Verify Installation

```bash
# Check key dependencies (depending on your chosen route, PyQt provided by conda or pip)
python -c "import sounddevice; print('SoundDevice OK')"
python -c "import opuslib; print('Opus OK')"
python -c "import PyQt5.QtCore as q; print('PyQt5 OK, Qt', q.QT_VERSION_STR)"
```

## Troubleshooting

### Common Issues

#### SoundDevice Installation Failed

```bash
# Ubuntu/Debian
sudo apt-get install -y portaudio19-dev libasound2-dev libportaudio2

# macOS
brew install portaudio

# Windows
pip install sounddevice
```

#### PyQt5 Installation Failed

* **Conda route (recommended for ARM)**:

```bash
conda install -c conda-forge -y pyqt=5.15 libstdcxx-ng>=13 libgcc-ng>=13
```

* **pip route (mainly for x86_64)**: Confirm if manylinux wheels are available; if ARM source build fails, use conda instead.

#### Opus Library Missing

* macOS users prefer conda installation (otherwise need to handle dynamic library paths):

```bash
conda install -c conda-forge opus
# If really needed:
# nano ~/.zshrc
# export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
# source ~/.zshrc
```

* Linux

```bash
sudo apt-get install -y libopus0 libopus-dev
```

* macOS

```bash
brew install opus
```

#### Permission Issues (Linux)

```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Takes effect after re-login
```

## Version Requirements

* **Python**: 3.9.13+ (recommended 3.10, maximum 3.11)
* **PyQt5**: 5.15+
* **SoundDevice**: 0.4.4+
* **FFmpeg**: 4.0+
* **Opus**: 1.3+
* **PortAudio**: 19.0+

## Notes

1. Recommend using Conda environment for dependency management (**ARM Ubuntu strongly recommends conda for PyQt installation**)
2. Do not share Conda environment with esp32-server
3. macOS users must use `requirements_mac.txt`
4. Windows users don't need to manually install `opus.dll`
5. Project uses SoundDevice instead of PyAudio, uses PyQt5 as GUI framework
6. Ensure system dependencies are installed before Python dependencies
7. Using domestic mirror sources can improve download speed
8. **Do not mix PyQt installation sources**: Only use **pip or conda**, **do not use apt's python3-pyqt5**\*
