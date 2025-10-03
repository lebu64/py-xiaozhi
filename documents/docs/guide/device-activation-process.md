# Device Activation Process

## Overview

The device activation process is responsible for verifying device identity and obtaining necessary configuration information. The system supports v1 and v2 activation protocols, with the v2 protocol using HMAC-SHA256 based security verification mechanism.

## System Initialization Phase

### Phase Division

System initialization is divided into three main phases:

1. **Device Fingerprint Phase**: Prepare device identity information
2. **Configuration Management Phase**: Initialize configuration manager
3. **OTA Configuration Phase**: Obtain server configuration information

### Phase 1: Device Fingerprint

Collect and manage device identity information through the `DeviceFingerprint` class:

- Generate or load device serial number
- Create or obtain HMAC key
- Manage local activation status
- Obtain standardized MAC address

Device fingerprint file is stored in `config/efuse.json`, containing:
```json
{
  "serial_number": "SN-xxxxxxxxxxxxxxxx",
  "hmac_key": "64-bit hexadecimal string",
  "mac_address": "xx:xx:xx:xx:xx:xx",
  "activated": false
}
```

### Phase 2: Configuration Management

Initialize configuration manager and ensure key configuration items:

- Initialize CLIENT_ID (UUID format)
- Set DEVICE_ID from device fingerprint (MAC address)
- Verify configuration integrity

### Phase 3: OTA Configuration

Request configuration information from OTA server:

**Request URL**: `SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL`

**Request Headers**:
```
Device-Id: MAC address
Client-Id: Client UUID
Content-Type: application/json
User-Agent: board_type/app_name-version
Accept-Language: zh-CN
Activation-Version: version (v2 protocol only)
```

**Request Body**:
```json
{
  "application": {
    "version": "Application version",
    "elf_sha256": "HMAC key"
  },
  "board": {
    "type": "Device type",
    "name": "Application name",
    "ip": "Local IP",
    "mac": "MAC address"
  }
}
```

## Activation Status Analysis

System analyzes status based on local activation status and server response:

### Status Combination Processing

1. **Local not activated + Server returns activation data**: Need activation process
2. **Local activated + Server no activation data**: Device already activated
3. **Local not activated + Server no activation data**: Automatically repair local status
4. **Local activated + Server returns activation data**: Status inconsistent, may need reactivation

### Server Response Format

Response when successfully obtaining configuration:
```json
{
  "mqtt": {
    "endpoint": "MQTT server address",
    "client_id": "MQTT client ID",
    "username": "Username",
    "password": "Password",
    "publish_topic": "Publish topic"
  },
  "websocket": {
    "url": "WebSocket server URL",
    "token": "Access token"
  }
}
```

Response when activation is needed:
```json
{
  "activation": {
    "message": "Activation prompt message",
    "code": "6-digit verification code",
    "challenge": "Random string for HMAC signature",
    "timeout_ms": 30000
  }
}
```

## v2 Protocol Activation Process

### Activation Trigger Conditions

When system analysis finds activation is needed, start activation process:

1. Check device serial number and HMAC key
2. Display verification code to user
3. Play voice prompt
4. Execute HMAC signature verification

### HMAC Signature Calculation

Use HMAC-SHA256 algorithm to sign challenge:
```python
signature = hmac.new(
    hmac_key.encode('utf-8'),
    challenge.encode('utf-8'),
    hashlib.sha256
).hexdigest()
```

### Activation Request

**Request URL**: `OTA_VERSION_URL + "activate"`

**Request Headers**:
```
Activation-Version: 2
Device-Id: MAC address
Client-Id: Client UUID
Content-Type: application/json
```

**Request Body**:
```json
{
  "Payload": {
    "algorithm": "hmac-sha256",
    "serial_number": "Device serial number",
    "challenge": "Server challenge",
    "hmac": "HMAC signature"
  }
}
```

### Response Processing

- **HTTP 200**: Activation successful, update local activation status
- **HTTP 202**: Wait for user to input verification code, continue polling
- **HTTP 4xx**: Activation failed, record error information

### Retry Mechanism

Activation request uses long polling mechanism:

- Maximum retry count: 60 times
- Retry interval: 5 seconds
- Total timeout: 5 minutes
- Replay verification code prompt on each retry

## User Interface Integration

### GUI Mode

Provide graphical interface through `ActivationWindow` class:

- Display verification code
- Provide activation status feedback
- Support cancel activation operation
- Asynchronously wait for activation completion

### CLI Mode

Provide command line interface through `CLIActivation` class:

- Console output verification code
- Voice playback verification code
- Display activation progress

## Security Mechanism

1. **Device Unique Identification**: Generate unique serial number based on hardware information
2. **HMAC-SHA256 Signature**: Prevent forged activation requests
3. **Verification Code Verification**: User manually inputs to confirm device ownership
4. **Long Polling Mechanism**: Adapt to network environment, avoid frequent requests

## Configuration Update

After successful activation, system automatically updates configuration:

- MQTT connection information
- WebSocket connection information
- Local activation status marker

After configuration update is completed, application continues normal startup process.
