# Home Assistant MCP Integration

To improve architecture flexibility and stability, py-xiaozhi has removed the built-in Home Assistant (HA). Now you can access HA through the WSS-based Home Assistant MCP external plugin, which directly connects to Xiaozhi AI server via MCP protocol without any intermediaries. This plugin is open-source maintained by c1pher-cn and fully supports device status queries, entity control, and automation management.

Project address: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi)

## Plugin Features

### Core Capabilities

1. **Direct Connection to Xiaozhi Server**: Home Assistant acts as an MCP server, directly connecting to Xiaozhi server via WebSocket protocol without intermediaries
2. **Multi-API Group Proxy**: Simultaneously select multiple API groups in one entity (Home Assistant built-in control API, user-defined MCP Server)
3. **Multi-Entity Support**: Supports configuring multiple entity instances simultaneously
4. **HACS Integration**: One-click installation through HACS store, convenient for management and updates

### Technical Advantages

- **Low Latency**: Direct connection architecture reduces network intermediary latency
- **High Reliability**: Based on WebSocket long connections, better stability
- **Easy Expansion**: Supports proxying other MCP Servers, strong scalability
- **Easy Maintenance**: HACS management, automatic updates

## Common Usage Scenarios

**Device Status Queries:**

- "What is the current status of the living room light"
- "Check the status of all lights"
- "What temperature does the temperature sensor show"
- "Is the air conditioner currently on"

**Device Control:**

- "Turn on the living room light"
- "Turn off all lights"
- "Set the air conditioner temperature to 25 degrees"
- "Adjust living room light brightness to 80%"

**Scene Control:**

- "Activate sleep mode"
- "Activate home arrival scene"
- "Execute good night scene"
- "Start party mode"

**Advanced Control:**

- "Control TV through script"
- "Execute custom automation"
- "Control multimedia devices"
- "Manage security system"

## Installation Guide

### Prerequisites

- Home Assistant installed and running
- HACS (Home Assistant Community Store) installed
- Xiaozhi AI account and MCP access point address

### Installation Steps

#### 1. Install via HACS

1. Open HACS, search for `xiaozhi` or `ha-mcp-for-xiaozhi`

<img width="700" alt="HACS Search Interface" src="https://github.com/user-attachments/assets/fa49ee7c-b503-49fa-ad63-512499fa3885" />

2. Click download and install the plugin

<img width="500" alt="Plugin Download Interface" src="https://github.com/user-attachments/assets/1ee75d6f-e1b0-4073-a2c7-ee0d72d002ca" />

3. Restart Home Assistant

#### 2. Manual Installation

If unable to install via HACS, you can manually download:

1. Download the latest version from [GitHub Releases](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/releases)
2. Extract to `custom_components` directory
3. Restart Home Assistant

### Configuration Steps

#### 1. Add Integration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for "Mcp" or "MCP Server for Xiaozhi"

<img width="600" alt="Add Integration Interface" src="https://github.com/user-attachments/assets/07a70fe1-8c6e-4679-84df-1ea05114b271" />

3. Select and click add

#### 2. Configure Parameters

The configuration interface requires the following information:

**Basic Configuration:**

- **Xiaozhi MCP Access Point Address**: MCP access address obtained from Xiaozhi AI backend
- **Device Name**: Set an identification name for this Home Assistant instance

**API Group Selection:**

- **Assist**: Home Assistant built-in control functions
- **Other MCP Server**: If you have configured other MCP servers in Home Assistant, you can choose to proxy them to Xiaozhi

<img width="600" alt="Configuration Interface" src="https://github.com/user-attachments/assets/38e98fde-8a6c-4434-932c-840c25dc6e28" />

#### 3. Entity Exposure Settings

To allow Xiaozhi to control devices, you need to expose the corresponding entities:

1. Go to **Settings > Voice Assistant > Expose**
2. Select devices and entities that need to be controlled by Xiaozhi
3. Save settings

#### 4. Verify Connection

1. Wait about 1 minute after configuration is complete
2. Log in to Xiaozhi AI backend, go to MCP access point page
3. Click refresh, check if connection status is normal

<img width="600" alt="Connection Status Check" src="https://github.com/user-attachments/assets/ace79a44-6197-4e94-8c49-ab9048ed4502" />

## Usage Examples

### Basic Device Control

```
User: "Turn on the living room light"
Xiaozhi: "Okay, I've turned on the living room light for you"

User: "Set the air conditioner temperature to 26 degrees"  
Xiaozhi: "I've set the air conditioner temperature to 26 degrees"

User: "Turn off all lights"
Xiaozhi: "I've turned off all lights for you"
```

### Status Queries

```
User: "What is the current temperature in the living room"
Xiaozhi: "The living room temperature sensor shows the current temperature is 23.5 degrees"

User: "Which lights are currently on"
Xiaozhi: "Currently turned on lights include: living room light, bedroom bedside light"
```

### Scene Control

```
User: "Execute sleep mode"
Xiaozhi: "I've executed sleep mode scene for you, all lights are turned off, curtains are closed"

User: "Activate home arrival scene"  
Xiaozhi: "Welcome home! I've turned on the living room light and entrance light for you, air conditioner is set to comfortable temperature"
```

## Debugging Instructions

### 1. Entity Exposure Check

The number of exposed tools depends on the types of entities you expose to Home Assistant voice assistant:

- Go to **Settings > Voice Assistant > Expose**
- Ensure devices that need to be controlled are added to the exposure list

### 2. Version Requirements

It is recommended to use the latest version of Home Assistant:

- Newer versions provide more complete tools and APIs
- May version shows significant improvements in tool support compared to March version

### 3. Debugging Methods

When control effects don't meet expectations:

**Check Xiaozhi Chat Records:**

1. Check how Xiaozhi understands and processes instructions
2. Confirm if Home Assistant tools are called
3. Analyze if call parameters are correct

**Known Issues:**

- Light control may conflict with built-in screen control
- Music control may conflict with built-in music functions
- These issues will be resolved next month when Xiaozhi server supports built-in tool selection

### 4. Debug Logs

If Home Assistant function calls are correct but execution is abnormal:

1. Enable debug logs for this plugin in Home Assistant
2. Reproduce the problematic operation
3. Check detailed execution situation in the logs

## Demo Videos

To better understand plugin functionality, you can watch the following demo videos:

- [Integration Demo Video](https://www.bilibili.com/video/BV1XdjJzeEwe) - Basic installation and configuration process
- [TV Control Demo](https://www.bilibili.com/video/BV18DM8zuEYV) - TV control through custom script implementation
- [Advanced Tutorial](https://www.bilibili.com/video/BV1SruXzqEW5) - Detailed tutorial on Home Assistant, LLM, MCP, Xiaozhi

## Troubleshooting

### Common Issues

**1. Connection Failure**

- Check if Xiaozhi MCP access point address is correct
- Confirm Home Assistant network connection is normal
- Check firewall settings

**2. Device Cannot Be Controlled**

- Confirm device is exposed in voice assistant
- Check if device entity status is normal
- Verify if device supports corresponding operations

**3. Partial Function Conflicts**

- Temporarily disable built-in functions
- Adjust device naming to avoid conflicts
- Wait for Xiaozhi server tool selection function update

**4. Response Delay**

- Check network connection quality
- Optimize Home Assistant performance
- Reduce unnecessary entity exposure

### Debugging Tips

1. Enable detailed log recording
2. Gradually test basic functions
3. Compare configurations of normally working devices
4. Refer to community discussions and issues

## Community Support

### Project Links

- **GitHub Repository**: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi)
- **Issue Reporting**: [GitHub Issues](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/discussions)
