# Echo Cancellation (AEC) Configuration Guide

## Overview

Echo Cancellation (Acoustic Echo Cancellation, AEC) is a key technology in voice interaction, used to eliminate echo interference generated when speakers are playing. When the system plays audio, the microphone simultaneously captures the playback content, causing degradation in speech recognition accuracy.

**AEC Working Principle:**

- Capture microphone input audio signal (contains user voice + echo)
- Obtain speaker playback reference signal
- Use algorithm to subtract predicted echo components from microphone signal
- Output clean user voice signal

## Platform Support Architecture

py-xiaozhi adopts cross-platform adaptive strategy, selecting optimal solutions based on different operating system characteristics:

```text
                    ┌─────────────────┐
                    │   py-xiaozhi    │
                    │  AEC Processor  │
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │  Platform Check │
                    └─┬─────┬─────┬───┘
            ┌─────────▼─┐ ┌─▼───┐ ┌▼──────────┐
            │  Windows  │ │Linux│ │   macOS   │
            │ System AEC│ │PA-AEC│ │WebRTC+BH │
            └───────────┘ └─────┘ └───────────┘
                 │           │         │
            ┌────▼────┐ ┌────▼───┐ ┌───▼────┐
            │Out of   │ │One-time│ │Requires│
            │the box  │ │Config  │ │Config  │
            └─────────┘ └────────┘ └────────┘
```

### 🪟 Windows Platform

- **Solution**: System-level driver layer AEC
- **Advantage**: Zero configuration, works out of the box
- **Principle**: Audio driver already handles echo cancellation
- **Performance**: Lowest latency, no additional overhead

### 🐧 Linux Platform

- **Solution**: PulseAudio modular AEC
- **Advantage**: System-level processing, application transparent
- **Principle**: module-echo-cancel + WebRTC algorithm
- **Configuration**: One-time configuration, persistent effect

### 🍎 macOS Platform

- **Solution**: WebRTC + BlackHole virtual device
- **Advantage**: Real-time processing, controllable effect
- **Principle**: Application layer real-time algorithm processing
- **Configuration**: Need to install virtual audio device

---

# 🐧 Linux Platform Configuration

## System Requirements

| Item | Requirement |
|------|-------------|
| **Operating System** | PulseAudio based Linux distribution |
| **Test Environment** | Ubuntu 20.04+ / Fedora 35+ |
| **Hardware Recommendation** | External USB microphone + independent speakers |

> ⚠️ **Hardware Suggestion**: Laptop built-in microphone+speaker combination has limited AEC effect due to physical vibration coupling

## Technical Architecture

```text
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│ Physical    │───▶│  module-echo-   │───▶│ Virtual      │
│ Microphone  │    │  cancel         │    │ Device       │
│             │    │                 │    │ echoCancel_  │
└─────────────┘    └─────────────────┘    │ source       │
                           ▲               └──────┬───────┘
┌─────────────┐           │                      │
│ Speaker     │───────────┘                      ▼
│ Output      │                          ┌──────────────┐
└─────────────┘                          │ py-xiaozhi   │
                                         │ Audio Input  │
                                         └──────────────┘
```

## One-click Configuration Script

### Download and Install

```bash
# Download configuration script
git clone https://github.com/W-E-A/PulseAudio-AEC-Script.git
cd PulseAudio-AEC-Script

# Set execution permissions
chmod +x setup_aec.sh uninstall_aec.sh
```

### Run Configuration

```bash
# Run installation script (do not use sudo)
./setup_aec.sh
```

**Configuration Process:**

1. **Device Detection** - Script scans all available microphone devices
2. **Device Selection** - Select target microphone (recommended USB external microphone)
3. **Module Configuration** - Automatically configure PulseAudio echo cancellation module
4. **Service Restart** - Restart audio service to make configuration effective

### System Settings

After configuration:

1. Open system "Sound" settings
2. **Input Device**: Select virtual microphone containing `echo cancellation`
3. **Output Device**: Select virtual speaker containing `echo cancellation`

### Effect Verification

![AEC Effect Comparison](https://github.com/W-E-A/PulseAudio-AEC-Script/raw/main/assets/images/AEC_audio_effect.png)

### Uninstall Configuration

```bash
# Restore original configuration
./uninstall_aec.sh
```

## Troubleshooting

### Common Issues

**Q1: Cannot find echo cancellation device after script runs**

Solution:

```bash
# Check PulseAudio status
pactl list sources short
pactl list sinks short

# Restart audio service
pulseaudio -k
```

**Q2: Poor AEC effect with built-in microphone**

Cause Analysis:

- Physical vibration coupling: Speaker vibration transmitted to built-in microphone
- Device compatibility: Some built-in devices don't support AEC module

Recommended Solution:

- Use external USB microphone + independent speakers
- Physically isolate vibration source

**Q3: Increased audio latency after configuration**

Tuning Solution:

```bash
# Check buffer settings
pactl list sources | grep -A10 "echo-cancel"

# Adjust latency parameters (optional)
# Edit ~/.config/pulse/default.pa
# Add: load-module module-echo-cancel aec_args='"frame_size_ms=8"'
```

---

# 🍎 macOS Platform Configuration

## System Requirements

| Item | Requirement |
|------|-------------|
| **Operating System** | macOS 10.15+ |
| **Virtual Audio** | BlackHole 2ch |
| **Python Dependency** | webrtc-audio-processing |

## Technical Architecture

```text
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│ Physical    │───▶│  WebRTC AEC     │───▶│ py-xiaozhi   │
│ Microphone  │    │  Real-time      │    │ Audio Input  │
│             │    │  Processing     │    │              │
└─────────────┘    └─────────┬───────┘    └──────────────┘
                             ▲
              ┌──────────────▼───────────────┐
              │    Aggregate Device/         │
              │    Multi-Output              │
              └──┬─────────────────────┬─────┘
┌─────────────▼─┐                    ┌▼──────────────┐
│ Physical      │                    │ BlackHole 2ch │
│ Speaker       │                    │ (Reference    │
│ (User Audio)  │                    │ Signal)       │
└───────────────┘                    └───────────────┘
```

## Install BlackHole

### Method 1: Homebrew Installation (Recommended)

```bash
# Install BlackHole
brew install blackhole-2ch
```

### Method 2: Manual Installation

1. Visit [BlackHole Official Page](https://github.com/ExistentialAudio/BlackHole)
2. Download BlackHole 2ch installation package
3. Run installer and authorize

## Audio Device Configuration

### Step 1: Create Aggregate Device

> If not working, create multi-output device, still check speaker and blackhole, according to documentation and AI recommendations, creating aggregate device is recommended, but actual testing shows creating multi-output device is needed for correct WebRTC echo cancellation

1. Open "Applications" → "Utilities" → "Audio MIDI Setup"
2. Click "+" at bottom left → "Create Aggregate Device"
3. Configure aggregate device:
   - ✅ MacBook Air Speaker (main device)
   - ✅ BlackHole 2ch
   - Sample Rate: 48.0 kHz

![Aggregate Device Configuration](./images/聚合设备.png)
![Multi-output Device Configuration](./images/多设备.png)

> 💡 **Configuration Note**: Aggregate device ensures audio synchronously outputs to speaker and BlackHole, providing precise time alignment for AEC

### Step 2: System Audio Settings

1. Open "System Preferences" → "Sound"
2. **Output**: Select newly created aggregate device
3. **Input**: Keep default microphone device

![System Audio Settings](./images/系统扬声器选择.png)

> ⚠️ **Volume Control Limitation**: Aggregate device cannot directly adjust system volume, can adjust sub-device volumes in Audio MIDI Setup

### Step 3: Verify Device Availability

```bash
# Check if BlackHole device is recognized
python3 -c "
import sounddevice as sd
devices = sd.query_devices()
for i, device in enumerate(devices):
    if 'blackhole' in device['name'].lower():
        print(f'[{i}] {device[\"name\"]} - {device[\"max_input_channels\"]}ch input')
"
```

## Application Automatic Configuration

py-xiaozhi automatically executes when starting:

1. **Device Detection** - Scan and identify BlackHole 2ch device
2. **AEC Initialization** - Create WebRTC audio processing instance
3. **Reference Signal Stream** - Establish BlackHole audio capture stream
4. **Real-time Processing** - Start echo cancellation processing for microphone audio

### Configuration Verification

```python
# Check AEC status
from src.audio_codecs.audio_codec import AudioCodec

codec = AudioCodec()
await codec.initialize()

# Get AEC status
status = codec.get_aec_status()
print(f"AEC Enabled: {status['enabled']}")
print(f"Reference Signal Available: {status['reference_available']}")
```

## Troubleshooting

### Common Issues

#### Q1: BlackHole Device Not Found

Solution:

```bash
# Reinstall BlackHole
brew reinstall blackhole-2ch

# Restart CoreAudio service
sudo launchctl kickstart -kp system/com.apple.audio.coreaudiod
```

#### Q2: Cannot Create Aggregate Device

Check Items:

- Confirm BlackHole correctly installed
- Restart "Audio MIDI Setup" application
- Check system audio permission settings

#### Q3: Poor AEC Effect

Optimization Suggestions:

- Ensure using aggregate device instead of multi-output device
- Adjust physical distance between microphone and speakers
- Check environmental noise level

#### Q4: High Audio Latency

Tuning Solutions:

- Reduce audio buffer size
- Use wired audio devices instead of Bluetooth
- Close other audio processing software

---

# 🧪 Configuration Verification and Testing

## Status Check

### General Status Verification

```python
# Check AEC status after starting py-xiaozhi
from src.audio_codecs.audio_codec import AudioCodec

codec = AudioCodec()
await codec.initialize()

# Get detailed status information
status = codec.get_aec_status()
print(f"AEC Enabled Status: {status['enabled']}")
print(f"Platform Type: {status.get('aec_type', 'unknown')}")
print(f"Description: {status.get('description', 'N/A')}")
```

### Platform Specific Checks

#### Windows

```bash
# Check audio driver AEC support
# View audio device properties in Device Manager
```

#### Linux

```bash
# Verify PulseAudio AEC module
pactl list sources | grep -i "echo"
pactl list sinks | grep -i "echo"

# Check module loading status
pactl list modules | grep echo-cancel
```

#### macOS

```bash
# Verify BlackHole device
system_profiler SPAudioDataType | grep -i blackhole

# Check aggregate device
# Confirm device status in Audio MIDI Setup
```

## Function Testing

- Theoretically, after enabling AEC in config.json, selecting auto conversation, if it doesn't talk to itself, it's normal. Linux and macOS need configuration, Windows has been tested by several people and works normally as system bottom layer already handles it.

## Reference Resources

### Official Documentation

- [PulseAudio AEC Script](https://github.com/W-E-A/PulseAudio-AEC-Script) - Linux automatic configuration script
- [BlackHole Official Repository](https://github.com/ExistentialAudio/BlackHole) - macOS virtual audio device
- [WebRTC Audio Processing](https://webrtc.googlesource.com/src/+/refs/heads/master/modules/audio_processing/) - Algorithm implementation documentation
