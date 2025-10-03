# Voice Interaction Mode Explanation

![Image](./images/系统界面.png)

## Project Overview

py-xiaozhi is an AI voice assistant client developed based on Python, using modern asynchronous architecture design, supporting rich multimodal interaction functions. The system integrates advanced technologies such as speech recognition, natural language processing, visual recognition, IoT device control, providing users with intelligent interaction experience.

### Core Features
- **Multi-protocol Support**: WebSocket/MQTT dual-protocol communication
- **MCP Tool Ecosystem**: Integrates 10+ professional tool modules
- **IoT Device Integration**: Thing-based architecture device management
- **Visual Recognition**: Multimodal understanding based on GLM-4V
- **Audio Processing**: Opus encoding + WebRTC enhancement
- **Global Shortcuts**: System-level interaction control

## Voice Interaction Modes

The system provides multiple voice interaction methods, supporting flexible interaction control and intelligent voice detection:

### 1. Manual Press Mode

- **Operation Method**: Record during shortcut key hold, automatically send when released
- **Default Shortcut**: `Ctrl+J` (can be modified in configuration)
- **Applicable Scenarios**: Precise control of recording time, avoiding environmental noise interference
- **Advantages**: 
  - Avoid accidental recording triggers
  - Complete control over recording duration
  - Suitable for noisy environments

### 2. Turn-based Conversation Mode (AUTO_STOP)

- **Operation Method**: Press shortcut key to toggle/click GUI bottom right manual conversation mode to switch auto conversation
- **Default Shortcut**: `Ctrl+K` (can be modified in configuration)
- **Applicable Scenarios**: Quiet environments, traditional conversation interaction, when AEC function is disabled
- **Working Principle**: 
  - User speaks → AI replies → User speaks again
  - Each conversation requires waiting for AI reply completion
  - Avoids echo and simultaneous speaking conflicts
  - System automatically disables microphone input when AI is speaking
- **Technical Features**: 
  - Default mode when AEC is disabled
  - Suitable for unidirectional audio devices or environments with echo issues
  - More stable conversation experience, avoiding audio conflicts

### 3. Real-time Conversation Mode (REALTIME)

- **Operation Method**: Automatically activated when AEC echo cancellation is enabled
- **Configuration Requirement**: `"AEC_OPTIONS.ENABLED": true`
- **Applicable Scenarios**: Natural conversation, bidirectional interaction, complex environments, scenarios requiring AI interruption
- **Working Principle**:
  - Supports user interruption while AI is speaking
  - Real-time bidirectional audio stream processing
  - Intelligent echo cancellation, avoiding speaker sound interference with microphone
  - Microphone and speaker can work simultaneously
- **Technical Features**: 
  - Acoustic echo cancellation algorithm based on SpeexDSP
  - Real-time noise suppression and audio preprocessing
  - Low-latency audio processing pipeline (typically <50ms)
  - Reference signal buffering and adaptive filtering
  - Supports full-duplex audio communication

### 4. Wake Word Mode

- **Operation Method**: Activate system by speaking preset wake words
- **Default Wake Words**: "小智", "小美" (can be customized in configuration)
- **Model Support**: Based on Vosk offline speech recognition
- **Configuration Requirement**: Need to download corresponding speech recognition model

### AEC Automatic Mode Selection

The system automatically selects appropriate conversation mode based on AEC configuration:

```json
// When AEC enabled - automatically switch to real-time conversation mode
{
  "AEC_OPTIONS": {
    "ENABLED": true   // → ListeningMode.REALTIME
  }
}

// When AEC disabled - use turn-based conversation mode  
{
  "AEC_OPTIONS": {
    "ENABLED": false  // → ListeningMode.AUTO_STOP
  }
}
```

**Mode Selection Logic**:
- Read AEC configuration status in `src/application.py:99`
- Determine default `listening_mode` based on AEC status
- AEC enabled = supports real-time bidirectional conversation
- AEC disabled = uses traditional turn-based conversation

### Mode Switching and Configuration

```json
// Configure shortcuts in config/config.json
{
  "SHORTCUTS": {
    "ENABLED": true,
    "MANUAL_PRESS": {"modifier": "ctrl", "key": "j"},
    "AUTO_TOGGLE": {"modifier": "ctrl", "key": "k"},
    "MODE_TOGGLE": {"modifier": "ctrl", "key": "m"}
  }
}
```

- **Interface Display**: GUI bottom right displays current interaction mode in real-time
- **Quick Switching**: Use `Ctrl+M` to quickly switch between different modes
- **Status Indication**: System tray icon color reflects current status
- **Automatic Adaptation**: System automatically selects optimal conversation mode based on AEC configuration

## Conversation Control and System Status

### Intelligent Interruption Function

When AI is replying with voice, users can interrupt the conversation at any time:

- **Shortcut Interruption**: `Ctrl+Q` - Immediately stop current AI reply
- **GUI Operation**: Click "Interrupt" button on interface
- **Intelligent Detection**: System automatically interrupts reply when new voice input is detected

### System Status Management

The system uses event-driven state machine architecture with the following running states:

```
┌─────────────────────────────────────────────────────────┐
│                    System State Flow Chart               │
└─────────────────────────────────────────────────────────┘

     IDLE              CONNECTING           LISTENING
  ┌─────────┐    Wake word/Button  ┌─────────┐  Connection  ┌─────────┐
  │  Idle   │  ─────────────> │ Connecting │ ────────> │ Listening │
  │ Standby │                │  Server   │   Success  │ Recording │
  └─────────┘                └─────────┘           └─────────┘
       ↑                           │                     │
       │                         Connection              │ Speech
       │                          Failure                │ Recognition
       │                           │                     │ Complete/Timeout
       │                           ↓                     │
       │                     ┌─────────┐                 │
       └──── Playback/Interrupt ──── │ Replying │ <──────────────┘
                             │ AI Speaking │
                             └─────────┘
```

### Status Indication Description

**System Tray Icon Colors**:
- **Green**: System running normally, in standby state
- **Yellow**: Listening to user voice input
- **Blue**: AI is replying with voice
- **Red**: System error or connection exception
- **Gray**: Not connected to server

## Shortcut System

The system provides rich global shortcut support, detailed description please refer to: [Shortcut Explanation](./shortcut-explanation.md)

### Common Shortcuts

| Shortcut | Function Description | Notes |
|----------|---------------------|-------|
| `Ctrl+J` | Hold to speak mode | Record during hold, send when released |
| `Ctrl+K` | Auto conversation mode | Toggle automatic voice detection |
| `Ctrl+Q` | Interrupt conversation | Immediately stop AI reply |
| `Ctrl+M` | Switch interaction mode | Switch between manual/auto modes |
| `Ctrl+W` | Show/hide window | Window minimize/restore |

## Intelligent Voice Command System

### Basic Interaction Commands
- **Greetings**: "Hello", "Who are you", "Good morning"
- **Polite Expressions**: "Thank you", "Goodbye", "Please help me"
- **Status Inquiry**: "How is the system status", "Is connection normal"

### Visual Recognition Commands

Integrated GLM-4V multimodal understanding capability:

```bash
# Visual recognition analysis
"Recognize the scene"             # Analyze current camera view
"What's in front of the camera"   # Describe what is seen
"What is this thing"              # Object recognition
```

### MCP Tool Invocation Commands

Utilize rich MCP tool ecosystem:

```bash
# Calendar management
"Create meeting reminder for tomorrow 3 PM"
"Check today's schedule"

# Timer function  
"Play Chrysanthemum Terrace in one minute"

# System operations
"View system information"
"Adjust volume to 80%"

# Web search
"Search for today's weather"
"Find recent hot topics"

# Map navigation
"Find nearby coffee shops"
"Navigate to Beijing Tiananmen"

# Food recipes
"Recommend dinner recipe for today"
"Teach me how to make Kung Pao Chicken"

# Bazi fortune telling (optional)
"Analyze my birth date and time"
"How is today's fortune"
```

## Running Modes and Deployment

### GUI Mode (Default)

Graphical user interface mode, providing intuitive interaction experience:

```bash
# Standard startup
python main.py

# Use MQTT protocol
python main.py --protocol mqtt
```

**GUI Mode Features**:
- Visual operation interface
- Real-time status display
- Audio waveform visualization
- System tray support
- Graphical settings interface

### CLI Mode

Command line interface mode, suitable for server deployment:

```bash
# CLI mode startup
python main.py --mode cli

# CLI + MQTT protocol
python main.py --mode cli --protocol mqtt
```

**CLI Mode Features**:
- Low resource usage
- Server friendly
- Detailed log output
- Keyboard shortcut support
- Scripted deployment

**Build Features**:
- Cross-platform support
- Single file mode
- Dependency packaging
- Automated configuration

## Platform Compatibility

### Windows Platform
- **Fully Compatible**: All functions normally supported
- **Audio Enhancement**: Supports Windows Audio API
- **Volume Control**: Integrated pycaw volume management
- **System Tray**: Complete tray function support
- **Global Hotkeys**: Complete shortcut function

### macOS Platform  
- **Fully Compatible**: Core functions completely supported
- **Status Bar**: Tray icon displayed in top status bar
- **Permission Management**: May require microphone/camera permissions authorization
- **Shortcuts**: Some shortcuts require system permissions
- **Audio**: Native CoreAudio support

### Linux Platform
- **Compatibility**: Supports mainstream distributions (Ubuntu/CentOS/Debian)
- **Desktop Environment**: 
  - GNOME: Complete support
  - KDE: Complete support  
  - Xfce: Requires additional tray support
- **Audio System**:
  - PulseAudio: Recommended (automatic detection)
  - ALSA: Alternative solution
- **Dependencies**: May need to install system tray support packages

```bash
# Ubuntu/Debian tray support
sudo apt-get install libappindicator3-1

# CentOS/RHEL tray support  
sudo yum install libappindicator-gtk3
```

## Troubleshooting Guide

### Common Issues

**1. Speech Recognition Not Working**
- Use simple recognition wake words like 小美, 小明

**2. Camera Cannot Be Used** 
```bash
# Test camera
python scripts/camera_scanner.py

# Check camera permissions and device index
```

**3. Shortcuts Not Responding**
- Check if other programs are using the same shortcuts
- Try running with administrator privileges (Windows)
- Check system security software blocking

**4. Network Connection Issues**
- Check firewall settings
- Verify WebSocket/MQTT server addresses
- Test network connectivity
