# Configuration Guide

## Configuration System Overview

### Configuration File Structure
py-xiaozhi uses a layered configuration system supporting multiple configuration management methods:

```
config/
├── config.json          # Main configuration file (runtime configuration)
└── efuse.json           # Device identity file (automatically generated)
```

### Configuration Hierarchy Structure

1. **Default Configuration Template**
   - Location: `DEFAULT_CONFIG` in `src/utils/config_manager.py`
   - Purpose: Provides system default configuration values
   - Usage: Template for automatically generating configuration files on first run

2. **Runtime Configuration File**
   - Location: `config/config.json`
   - Purpose: Stores user custom configurations
   - Usage: Actual configuration read during system runtime

3. **Device Identity File**
   - Location: `config/efuse.json`
   - Purpose: Stores device unique identifier and activation status
   - Usage: Device activation and identity verification

### Configuration Access Methods

The configuration system supports dot-separated path access for easy retrieval and modification of nested configurations:

```python
# Configuration retrieval example
from src.utils.config_manager import ConfigManager
config = ConfigManager.get_instance()

# Get network configuration
websocket_url = config.get_config("SYSTEM_OPTIONS.NETWORK.WEBSOCKET_URL")

# Get wake word configuration
wake_words = config.get_config("WAKE_WORD_OPTIONS.WAKE_WORDS")

# Update configuration
config.update_config("WAKE_WORD_OPTIONS.USE_WAKE_WORD", True)
config.update_config("CAMERA.VLapi_key", "your_api_key_here")

# Reload configuration
config.reload_config()
```

## System Configuration (SYSTEM_OPTIONS)

### Basic System Configuration

```json
{
  "SYSTEM_OPTIONS": {
    "CLIENT_ID": "Automatically generated client ID",
    "DEVICE_ID": "Device MAC address",
    "NETWORK": {
      "OTA_VERSION_URL": "https://api.tenclass.net/xiaozhi/ota/",
      "WEBSOCKET_URL": "wss://api.tenclass.net/xiaozhi/v1/",
      "WEBSOCKET_ACCESS_TOKEN": "Access token",
      "MQTT_INFO": {
        "endpoint": "mqtt.server.com",
        "client_id": "xiaozhi_client",
        "username": "your_username",
        "password": "your_password",
        "publish_topic": "xiaozhi/commands",
        "subscribe_topic": "xiaozhi/responses"
      },
      "ACTIVATION_VERSION": "v2",
      "AUTHORIZATION_URL": "https://xiaozhi.me/"
    }
  }
}
```

### Configuration Item Description

| Configuration Item | Type | Default Value | Description |
|-------------------|------|---------------|-------------|
| `CLIENT_ID` | String | Auto-generated | Client unique identifier |
| `DEVICE_ID` | String | MAC address | Device unique identifier |
| `OTA_VERSION_URL` | String | Official OTA address | OTA configuration retrieval address |
| `WEBSOCKET_URL` | String | Provided by OTA | WebSocket server address |
| `WEBSOCKET_ACCESS_TOKEN` | String | Provided by OTA | WebSocket access token |
| `ACTIVATION_VERSION` | String | "v2" | Activation protocol version (v1/v2) |
| `AUTHORIZATION_URL` | String | "https://xiaozhi.me/" | Device authorization address |

## Server Configuration Replacement

### Replace with Self-Deployed Server

To use a self-deployed server, simply modify the OTA interface address, the system will automatically retrieve WebSocket connection information from the OTA server:

```json
{
  "SYSTEM_OPTIONS": {
    "NETWORK": {
      "OTA_VERSION_URL": "https://your-server.com/xiaozhi/ota/"
    }
  }
}
```

### Configuration Auto-Update Mechanism

The system automatically updates configuration during startup through the following process:

1. **OTA Configuration Retrieval**: Send POST request to `OTA_VERSION_URL`
2. **Configuration Auto-Update**: System automatically updates MQTT and WebSocket configurations
3. **Connection Establishment**: Establish connections using updated configurations

Related code locations:
- OTA configuration retrieval: `fetch_and_update_config()` method in `src/core/ota.py`
- Configuration update: `update_websocket_config()` and `update_mqtt_config()` methods in `src/core/ota.py`

### Disable Configuration Auto-Update

If configuration auto-update is not needed, you can comment out related code in the following locations:

**1. Disable OTA Configuration Retrieval**

Comment out the third stage in `src/core/system_initializer.py`:

```python
# async def stage_3_ota_config(self):
#     """
#     Third stage: OTA configuration retrieval.
#     """
#     # Comment out entire method content
```

**2. Disable WebSocket Configuration Update**

Comment out update methods in `src/core/ota.py`:

```python
async def update_websocket_config(self, response_data):
    """
    Update WebSocket configuration information.
    """
    # Comment out configuration update logic
    return None
```

**3. Manual WebSocket Connection Configuration**

Directly configure fixed connection information in `config/config.json`:

```json
{
  "SYSTEM_OPTIONS": {
    "NETWORK": {
      "WEBSOCKET_URL": "wss://your-server.com/xiaozhi/v1/",
      "WEBSOCKET_ACCESS_TOKEN": "your_fixed_token"
    }
  }
}
```

## Wake Word Configuration (WAKE_WORD_OPTIONS)

### Sherpa-ONNX Voice Wake-up Settings

```json
{
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "MODEL_PATH": "models",
    "NUM_THREADS": 4,
    "PROVIDER": "cpu",
    "MAX_ACTIVE_PATHS": 2,
    "KEYWORDS_SCORE": 1.8,
    "KEYWORDS_THRESHOLD": 0.2,
    "NUM_TRAILING_BLANKS": 1
  }
}
```

### Configuration Item Description

| Configuration Item | Type | Default Value | Description |
|-------------------|------|---------------|-------------|
| `USE_WAKE_WORD` | Boolean | true | Whether to enable voice wake-up |
| `MODEL_PATH` | String | "models" | Sherpa-ONNX model file directory |
| `NUM_THREADS` | Integer | 4 | Model inference thread count, affects response speed |
| `PROVIDER` | String | "cpu" | Inference engine (cpu/cuda/coreml) |
| `MAX_ACTIVE_PATHS` | Integer | 2 | Search path count, affects accuracy and speed |
| `KEYWORDS_SCORE` | Float | 1.8 | Keyword enhancement score, affects detection sensitivity |
| `KEYWORDS_THRESHOLD` | Float | 0.2 | Detection threshold, lower is more sensitive |
| `NUM_TRAILING_BLANKS` | Integer | 1 | Trailing blank token count |

### Model File Structure

```bash
models/
├── encoder.onnx      # Encoder model (built-in high-precision version)
├── decoder.onnx      # Decoder model
├── joiner.onnx       # Joiner model
├── tokens.txt        # Pinyin token mapping table
└── keywords.txt      # Keyword configuration file
```

### Custom Wake Words

Edit `models/keywords.txt` to add wake words:

```
# Format: pinyin decomposition @Chinese original text
n ǐ h ǎo x iǎo zh ì @Hello Xiao Zhi
j iā w éi s ī @Jarvis
x iǎo zh ù sh ǒu @Assistant
k āi sh ǐ g ōng z uò @Start Working
```

### Performance Tuning

#### Speed Priority Configuration:
```json
{
  "WAKE_WORD_OPTIONS": {
    "NUM_THREADS": 6,
    "MAX_ACTIVE_PATHS": 1,
    "KEYWORDS_THRESHOLD": 0.15,
    "KEYWORDS_SCORE": 1.5
  }
}
```

#### Accuracy Priority Configuration:
```json
{
  "WAKE_WORD_OPTIONS": {
    "NUM_THREADS": 4,
    "MAX_ACTIVE_PATHS": 3,
    "KEYWORDS_THRESHOLD": 0.25,
    "KEYWORDS_SCORE": 2.2
  }
}
```

## Camera Configuration (CAMERA)

### Visual Recognition Settings

```json
{
  "CAMERA": {
    "camera_index": 0,
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
    "Local_VL_url": "https://open.bigmodel.cn/api/paas/v4/",
    "VLapi_key": "your_zhipu_api_key",
    "models": "glm-4v-plus"
  }
}
```

### Configuration Item Description

| Configuration Item | Type | Default Value | Description |
|-------------------|------|---------------|-------------|
| `camera_index` | Integer | 0 | Camera device index |
| `frame_width` | Integer | 640 | Frame width |
| `frame_height` | Integer | 480 | Frame height |
| `fps` | Integer | 30 | Frame rate |
| `Local_VL_url` | String | Zhipu API address | Visual model API address |
| `VLapi_key` | String | "" | Zhipu API key |
| `models` | String | "glm-4v-plus" | Visual model name |

### Camera Testing

```bash
# Test camera functionality
python scripts/camera_scanner.py

# Test visual recognition in program
Voice ask: What's in front of the camera?
```

## Shortcut Configuration (SHORTCUTS)

### Global Shortcut Settings

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

### Shortcut Description

| Shortcut | Function | Description |
|----------|----------|-------------|
| `Ctrl+J` | Hold to speak | Record during hold, send after release |
| `Ctrl+K` | Auto conversation | Toggle auto conversation mode |
| `Ctrl+Q` | Interrupt conversation | Interrupt current conversation |
| `Ctrl+M` | Switch mode | Switch between different conversation modes |
| `Ctrl+W` | Show/hide window | Show or hide main window |

## Acoustic Echo Cancellation Configuration (AEC_OPTIONS)

### AEC Audio Processing Settings

```json
{
  "AEC_OPTIONS": {
    "ENABLED": true,
    "BUFFER_MAX_LENGTH": 200,
    "FRAME_DELAY": 3,
    "FILTER_LENGTH_RATIO": 0.4,
    "ENABLE_PREPROCESS": true
  }
}
```

### Configuration Item Description

| Configuration Item | Type | Default Value | Description |
|-------------------|------|---------------|-------------|
| `ENABLED` | Boolean | true | Whether to enable AEC echo cancellation function |
| `BUFFER_MAX_LENGTH` | Integer | 200 | Reference signal buffer size (frame count) |
| `FRAME_DELAY` | Integer | 3 | Delay compensation frame count (not currently used) |
| `FILTER_LENGTH_RATIO` | Float | 0.4 | Filter length ratio (seconds), affects echo cancellation strength |
| `ENABLE_PREPROCESS` | Boolean | true | Whether to enable noise suppression preprocessing |

### AEC Function Description

**Echo Cancellation**
- Eliminates echo generated by speaker playback in microphone
- Supports real-time bidirectional conversation, avoids echo interference

**Noise Suppression**
- Suppresses background noise and environmental interference
- Improves speech recognition accuracy

**Conversation Mode Impact**
```json
{
  "AEC_OPTIONS": {
    "ENABLED": true  // When enabled: real-time conversation mode (ListeningMode.REALTIME)
                     // When disabled: turn-based conversation mode (ListeningMode.AUTO_STOP)
  }
}
```

### Environment Optimization Suggestions

**Small Room/Office Environment**
```json
{
  "AEC_OPTIONS": {
    "FILTER_LENGTH_RATIO": 0.2,
    "BUFFER_MAX_LENGTH": 150
  }
}
```

**Large Room/Meeting Room Environment**
```json
{
  "AEC_OPTIONS": {
    "FILTER_LENGTH_RATIO": 0.6,
    "BUFFER_MAX_LENGTH": 300
  }
}
```

**Noisy Environment**
```json
{
  "AEC_OPTIONS": {
    "FILTER_LENGTH_RATIO": 0.8,
    "ENABLE_PREPROCESS": true,
    "BUFFER_MAX_LENGTH": 400
  }
}
```

### AEC Function Testing

```bash
# Test echo cancellation effect
# 1. Enable AEC, speak while playing music
python main.py  # No echo should be present when AEC is enabled

# 2. Compare with AEC disabled
# Modify configuration file "ENABLED": false
python main.py  # Echo may be present when AEC is disabled
```

### Performance Parameter Description

**Filter Length Calculation**
```
Actual filter length = Sample rate(16000Hz) × FILTER_LENGTH_RATIO
Example: FILTER_LENGTH_RATIO = 0.4 → Filter length = 6400 samples (0.4 seconds)
```

**Parameter Impact**
- **Filter length↑**: Echo cancellation effect↑, CPU consumption↑
- **Buffer length↑**: Stability↑, Memory consumption↑
- **Preprocessing enabled**: Noise suppression↑, Slight delay↑

## Protocol Configuration Details

### WebSocket Protocol Configuration

WebSocket connection information is usually automatically provided by the OTA server, no manual configuration needed:

```json
{
  "SYSTEM_OPTIONS": {
    "NETWORK": {
      "WEBSOCKET_URL": "wss://your-server.com/xiaozhi/v1/",
      "WEBSOCKET_ACCESS_TOKEN": "your_access_token"
    }
  }
}
```

**Configuration Points:**
- URL must start with `ws://` or `wss://`
- Supports IP addresses or domain names
- Default port is 8000, can be adjusted according to server configuration
- Access token used for identity verification
- Usually automatically configured by OTA server, no manual setup needed

### MQTT Protocol Configuration

```json
{
  "SYSTEM_OPTIONS": {
    "NETWORK": {
      "MQTT_INFO": {
        "endpoint": "mqtt.server.com",
        "port": 1883,
        "client_id": "xiaozhi_client_001",
        "username": "your_username",
        "password": "your_password",
        "publish_topic": "xiaozhi/commands",
        "subscribe_topic": "xiaozhi/responses",
        "qos": 1,
        "keep_alive": 60
      }
    }
  }
}
```

**Configuration Points:**
- `endpoint`: MQTT server address
- `port`: Usually 1883 (non-encrypted) or 8883 (TLS encrypted)
- `client_id`: Client unique identifier
- `qos`: Message quality level (0-2)
- `keep_alive`: Heartbeat interval (seconds)

## Device Activation Configuration

### Activation Version Description

```json
{
  "SYSTEM_OPTIONS": {
    "NETWORK": {
      "ACTIVATION_VERSION": "v2",
      "AUTHORIZATION_URL": "https://xiaozhi.me/"
    }
  }
}
```

**Version Differences:**
- **v1**: Simplified activation process, no verification code needed
- **v2**: Complete activation process, includes verification code verification

### Device Identity File (efuse.json)

```json
{
  "serial_number": "SN-E3E1F618-902e16dbe116",
  "hmac_key": "b5bf012dd518080532f928b70ed958799f34f9224e80dd4128795a70a5baca24",
  "activation_status": false,
  "mac_address": "00:11:22:33:44:55",
  "device_fingerprint": {
    "cpu_info": "...",
    "memory_info": "...",
    "disk_info": "..."
  }
}
```

**Field Description:**
- `serial_number`: Device serial number
- `hmac_key`: Device verification key
- `activation_status`: Activation status
- `mac_address`: Device MAC address
- `device_fingerprint`: Device fingerprint information

## Configuration Management Practical Tips

### 1. Configuration File Generation

```bash
# Automatically generate configuration on first run
python main.py

# Regenerate default configuration
rm config/config.json
python main.py
```

### 2. Configuration Backup and Recovery

```bash
# Backup configuration
cp config/config.json config/config.json.bak

# Recover configuration
cp config/config.json.bak config/config.json
```

## Common Configuration Issues

### 1. WebSocket Connection Failure

**Symptoms**: Unable to connect to server

**Solutions**:
1. Check if OTA_VERSION_URL is correct
2. Ensure OTA server can respond normally
3. Check network connection

### 2. Wake Word Not Working

**Symptoms**: Voice wake-up no response

**Solutions**:
```json
{
  "WAKE_WORD_OPTIONS": {
    "USE_WAKE_WORD": true,
    "MODEL_PATH": "models/vosk-model-small-cn-0.22",
    "WAKE_WORDS": ["Xiao Zhi", "
