# Shortcut Explanation

## Overview

py-xiaozhi provides complete global shortcut support, allowing quick operations even when running in the background. The shortcut system is implemented based on the pynput library and supports cross-platform usage.

## Default Shortcuts

| Function Category | Shortcut | Function Description | Usage Scenario |
|------------------|----------|---------------------|----------------|
| **Voice Interaction** | `Ctrl+J` | Hold to speak mode | Record during hold, send when released |
| | `Ctrl+K` | Auto conversation mode | Toggle automatic voice detection |
| | `Ctrl+Q` | Interrupt conversation | Immediately stop AI reply |
| **Mode Control** | `Ctrl+M` | Switch interaction mode | Switch between manual/auto modes |
| | `Ctrl+W` | Show/hide window | Window minimize/restore |

## Shortcut Detailed Explanation

### Voice Interaction Shortcuts

#### Ctrl+J - Hold to Speak
- **Function**: Manual press mode, record during hold
- **Usage Method**: 
  1. Hold `Ctrl+J`
  2. Speak into microphone
  3. Release key to automatically send voice
- **Applicable Scenarios**: Precise control of recording time, avoid environmental noise interference

#### Ctrl+K - Auto Conversation
- **Function**: Toggle auto conversation mode
- **Usage Method**: Press `Ctrl+K` to toggle auto conversation state
- **Applicable Scenarios**: Continuous conversation, long-term interaction

#### Ctrl+Q - Interrupt Conversation
- **Function**: Immediately stop current AI voice reply
- **Usage Method**: Press `Ctrl+Q` during AI reply process
- **Applicable Scenarios**: When urgent interruption of AI reply is needed

### Mode Control Shortcuts

#### Ctrl+M - Switch Interaction Mode
- **Function**: Switch between different voice interaction modes
- **Usage Method**: Press `Ctrl+M` to cycle through modes
- **Mode Types**: Manual press mode ↔ Auto conversation mode

#### Ctrl+W - Show/Hide Window
- **Function**: Control main window display state
- **Usage Method**: Press `Ctrl+W` to toggle window visibility
- **Applicable Scenarios**: Quickly hide/show main interface

## Shortcut Configuration

### Configuration File Location

Shortcut configuration is stored in `config/config.json` file:

```json
{
  "SHORTCUTS": {
    "ENABLED": true,
    "MANUAL_PRESS": {
      "modifier": "ctrl",
      "key": "j",
      "description": "Hold to speak"
    },
    "AUTO_TOGGLE": {
      "modifier": "ctrl",
      "key": "k",
      "description": "Auto conversation"
    },
    "ABORT": {
      "modifier": "ctrl",
      "key": "q",
      "description": "Interrupt conversation"
    },
    "MODE_TOGGLE": {
      "modifier": "ctrl",
      "key": "m",
      "description": "Switch mode"
    },
    "WINDOW_TOGGLE": {
      "modifier": "ctrl",
      "key": "w",
      "description": "Show/hide window"
    }
  }
}
```

### Custom Shortcuts

#### Supported Modifier Keys

- `ctrl` - Ctrl key
- `alt` - Alt key  
- `shift` - Shift key
- `ctrl+alt` - Ctrl+Alt combination
- `ctrl+shift` - Ctrl+Shift combination

#### Supported Main Keys

- **Letter keys**: a-z
- **Number keys**: 0-9
- **Function keys**: f1-f12
- **Special keys**: space, enter, tab, esc

#### Configuration Example

```json
{
  "SHORTCUTS": {
    "ENABLED": true,
    "MANUAL_PRESS": {
      "modifier": "alt",
      "key": "space",
      "description": "Hold to speak"
    },
    "AUTO_TOGGLE": {
      "modifier": "ctrl+shift",
      "key": "a",
      "description": "Auto conversation"
    }
  }
}
```

## Platform Compatibility

### Windows
- **Full Support**: All shortcut functions work normally
- **Permission Requirements**: May require administrator privileges in some cases
- **Notes**: Avoid conflicts with system shortcuts

### macOS
- **Permission Configuration**: Need to grant accessibility permissions
- **Configuration Path**: System Preferences → Security & Privacy → Privacy → Accessibility
- **Terminal Permissions**: If running through terminal, need to authorize terminal

### Linux
- **User Group**: Need to add user to input group
- **Configuration Command**: `sudo usermod -a -G input $USER`
- **Desktop Environment**: Supports X11 and Wayland

## Troubleshooting

### Shortcuts Not Responding

#### Check Configuration
1. Confirm `SHORTCUTS.ENABLED` is `true` in configuration file
2. Check if shortcut configuration format is correct
3. Verify validity of modifier keys and main keys

#### Permission Issues
```bash
# macOS: Check accessibility permissions
System Preferences → Security & Privacy → Privacy → Accessibility

# Linux: Add user to audio group
sudo usermod -a -G input $USER

# Windows: Run with administrator privileges
Right-click application → Run as administrator
```

#### Conflict Detection
1. Check if other programs are using same shortcuts
2. Try changing to less commonly used shortcut combinations
3. Close potentially conflicting applications

### Common Error Handling

#### ImportError: No module named 'pynput'
```bash
# Install pynput library
pip install pynput
```

#### macOS Permission Denied
```bash
# Check and re-authorize
System Preferences → Security & Privacy → Privacy → Accessibility
# Remove and re-add application
```

#### Linux Keyboard Listening Failure
```bash
# Re-login to apply user group changes
sudo usermod -a -G input $USER
# Log out and log back in
```

## Advanced Configuration

### Error Recovery Mechanism

System built-in shortcut error recovery functionality:

- **Health Check**: Check listener status every 30 seconds
- **Auto Restart**: Automatically restart when failure detected
- **Error Counting**: Trigger recovery when consecutive errors exceed limit
- **Status Cleanup**: Clean key states when restarting

### Debug Mode

Enable detailed log output:

```python
# Enable debug logging in configuration
import logging
logging.getLogger('pynput').setLevel(logging.DEBUG)
```

### Performance Optimization

- **Key Cache**: Reduce duplicate key detection
- **Asynchronous Processing**: Non-blocking key event processing
- **Resource Management**: Automatically clean listener resources

## Code Reference

Shortcut system implementation locations:

- **Main Implementation**: `src/views/components/shortcut_manager.py`
- **Configuration Management**: `src/utils/config_manager.py`
- **Application Integration**: `src/application.py`

### Core Methods

```python
# Start shortcut listening
from src.views.components.shortcut_manager import start_global_shortcuts_async
shortcut_manager = await start_global_shortcuts_async()

# Manually stop listening
await shortcut_manager.stop()
