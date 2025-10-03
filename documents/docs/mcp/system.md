# System Tools

System Tools is a comprehensive MCP system management toolset that provides system status monitoring, volume control, device management, and other functions.

### Common Usage Scenarios

**System Status Query:**
- "View system status"
- "How is the system running now"
- "Check device status"
- "Are there any system issues"

**Volume Control:**
- "Set volume to 50"
- "Increase volume a bit"
- "Set volume to 80"
- "What is the current volume"

**Device Management:**
- "How many IoT devices are connected"
- "What is the device connection status"
- "View device list"
- "Are devices working normally"

**Application Status:**
- "What is the application status now"
- "Is the system busy"
- "What is the current working mode"
- "Is the application running normally"

### Usage Tips

1. **System Monitoring**: Regularly check system status to understand device health
2. **Volume Adjustment**: Can precisely set volume values or use relative adjustments
3. **Device Check**: Pay attention to IoT device connection status and quantity
4. **Status Understanding**: Understand the meaning of different device states

AI assistant will automatically call system tools based on your needs to provide system management and monitoring services.

## Feature Overview

### System Status Monitoring
- **Complete Status**: Get complete system running status
- **Audio Status**: Monitor audio devices and volume status
- **Application Status**: View application running status
- **Device Statistics**: Count IoT device connections

### Volume Control Function
- **Volume Setting**: Precisely set system volume
- **Volume Query**: Get current volume level
- **Mute Detection**: Detect if system is muted
- **Audio Devices**: Check audio device availability

### Device Management Function
- **Device Status**: Monitor device running status
- **IoT Devices**: Manage IoT device connections
- **Device Count**: Count connected devices
- **Status Tracking**: Track device status changes

### Application Monitoring Function
- **Application Status**: Monitor application status
- **Working Mode**: Identify current working mode
- **Resource Usage**: Monitor resource usage
- **Error Handling**: Detect and report system errors

## Tool List

### 1. System Status Tool

#### get_system_status - Get System Status
Get complete system running status information.

**Parameters:**
None

**Usage Scenarios:**
- System health check
- Fault diagnosis
- Status monitoring
- Performance evaluation

**Return Information:**
- Audio device status
- Application status
- IoT device statistics
- System error information

### 2. Volume Control Tool

#### set_volume - Set Volume
Set system volume to specified level.

**Parameters:**
- `volume` (Required): Volume level, range 0-100

**Usage Scenarios:**
- Volume adjustment
- Audio control
- Environment adaptation
- User preference settings

**Features:**
- Volume range validation
- Dependency checking
- Asynchronous execution
- Error handling

## Usage Examples

### System Status Query Example

```python
# Get complete system status
result = await mcp_server.call_tool("get_system_status", {})
```

### Volume Control Example

```python
# Set volume to 50
result = await mcp_server.call_tool("set_volume", {
    "volume": 50
})

# Set volume to maximum
result = await mcp_server.call_tool("set_volume", {
    "volume": 100
})

# Set volume to minimum (mute)
result = await mcp_server.call_tool("set_volume", {
    "volume": 0
})
```

## Data Structures

### System Status (SystemStatus)
```python
{
    "audio_speaker": {
        "volume": 75,
        "muted": false,
        "available": true
    },
    "application": {
        "device_state": "IDLE",
        "iot_devices": 3
    },
    "cpu_usage": 25.5,
    "memory_usage": 60.2,
    "disk_usage": 45.8,
    "network_status": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Audio Status (AudioStatus)
```python
{
    "volume": 75,
    "muted": false,
    "available": true,
    "device_name": "Default Speaker",
    "sample_rate": 44100,
    "channels": 2
}
```

### Application Status (ApplicationStatus)
```python
{
    "device_state": "IDLE",
    "iot_devices": 3,
    "uptime": "2 hours 30 minutes",
    "last_activity": "2024-01-15T10:28:00Z",
    "active_tasks": 2
}
```

### Error Status (ErrorStatus)
```python
{
    "error": "Volume control dependencies incomplete",
    "audio_speaker": {
        "volume": 50,
        "muted": false,
        "available": false,
        "reason": "Dependencies not available"
    },
    "application": {
        "device_state": "unknown",
        "iot_devices": 0
    }
}
```

## Device Status Description

### Application Status Types
- **IDLE**: Idle state, waiting for user input
- **LISTENING**: Listening to voice input
- **SPEAKING**: Playing voice output
- **CONNECTING**: Connecting to services
- **PROCESSING**: Processing requests
- **ERROR**: Error state occurred

### Audio Device Status
- **available**: Audio device available
- **volume**: Current volume level (0-100)
- **muted**: Whether muted
- **device_name**: Audio device name

### IoT Device Status
- **connected**: Number of connected devices
- **device_types**: Device type statistics
- **last_update**: Last update time
- **health_status**: Device health status

## System Monitoring Metrics

### Performance Metrics
- **CPU Usage**: System CPU usage percentage
- **Memory Usage**: System memory usage percentage
- **Disk Usage**: Disk space usage percentage
- **Network Status**: Network connection status

### Application Metrics
- **Uptime**: Application running duration
- **Active Tasks**: Current active task count
- **Last Activity**: Last activity time
- **Error Count**: Error occurrence count

### Device Metrics
- **Connected Devices**: Number of connected IoT devices
- **Device Types**: Different type device statistics
- **Device Health**: Device health status assessment
- **Connection Quality**: Device connection quality assessment

## Volume Control Mechanism

### Volume Setting Process
1. **Parameter Validation**: Validate volume value range (0-100)
2. **Dependency Check**: Check if volume control dependencies are available
3. **Asynchronous Execution**: Execute volume setting in thread pool
4. **Status Update**: Update system volume status
5. **Result Return**: Return setting result

### Cross-platform Support
- **Windows**: Use WASAPI interface
- **macOS**: Use CoreAudio framework
- **Linux**: Use ALSA/PulseAudio
- **Dependency Management**: Automatically detect and load platform dependencies

### Error Handling
- **Missing Dependencies**: Detect and report missing dependencies
- **Permission Issues**: Handle insufficient permissions
- **Device Unavailable**: Handle audio device unavailable situations
- **Parameter Errors**: Validate and handle parameter errors

## Best Practices

### 1. System Monitoring
- Regularly check system status
- Monitor performance metric changes
- Timely handle error states
- Monitor device connection status

### 2. Volume Management
- Set appropriate volume levels
- Consider usage environment and time
- Regularly check audio device status
- Handle audio device failures

### 3. Device Management
- Monitor IoT device connections
- Regularly check device health status
- Handle device connection issues
- Optimize device performance

### 4. Error Handling
- Timely respond to error states
- Analyze error causes
- Implement recovery measures
- Record error logs

## Troubleshooting

### Common Issues
1. **Volume Setting Failed**: Check audio devices and dependencies
2. **System Status Abnormal**: Check application status
3. **Device Connection Issues**: Check IoT device connections
4. **Insufficient Permissions**: Check system permission settings

### Debugging Methods
1. View system status for detailed information
2. Check error logs and error information
3. Verify dependencies and permission settings
4. Test audio device functionality

### Performance Optimization
1. Regularly clean system cache
2. Optimize IoT device connections
3. Monitor resource usage
4. Adjust system parameter settings

## Security Considerations

### Permission Management
- Volume control requires appropriate permissions
- System status access permission control
- Device management permission verification
- User operation permission checking

### Data Protection
- System status information sensitivity
- Device information privacy protection
- Operation log secure storage
- Error information desensitization processing

### Access Control
- Limit system function access
- Verify user identity
- Control operation permissions
- Audit operation records

Through system tools, you can effectively monitor and manage system status, ensuring device normal operation and optimal performance.
