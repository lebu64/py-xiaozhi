# MCP Development Guide

MCP (Model Context Protocol) is an open standard protocol for AI tool extension. This project implements a powerful tool system based on MCP, supporting seamless integration of multiple functional modules.

## 📖 Documentation Navigation

- **[🔧 Built-in MCP Development Guide](#system-architecture)** - This document: Developing and using built-in MCP tools
- **[🔌 External MCP Integration Guide](xiaozhi-mcp.md)** - External MCP service integration and community project integration

> 💡 **Selection Guide**: If you want to develop new built-in tools, please refer to this document; if you want to integrate external MCP services or learn about community projects, please check the [External Integration Guide](xiaozhi-mcp.md).

## System Architecture

### Core Components

#### 1. MCP Server (`src/mcp/mcp_server.py`)
- **Based on JSON-RPC 2.0 Protocol**: Complies with MCP standard specifications
- **Singleton Pattern**: Global unified server instance management
- **Tool Registration System**: Supports dynamic addition and management of tools
- **Parameter Validation**: Complete type checking and parameter validation mechanism
- **Error Handling**: Standardized error response and exception handling

#### 2. Tool Property System
```python
# Property type definition
class PropertyType(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"

# Property definition
@dataclass
class Property:
    name: str
    type: PropertyType
    default_value: Optional[Any] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
```

#### 3. Tool Definition Structure
```python
@dataclass
class McpTool:
    name: str                  # Tool name
    description: str           # Tool description
    properties: PropertyList   # Parameter list
    callback: Callable         # Callback function
```

### Tool Manager Architecture

Each functional module has a corresponding manager class responsible for:
- Tool initialization and registration
- Business logic encapsulation
- Interaction with underlying services

#### Existing Tool Modules

1. **System Tools (`src/mcp/tools/system/`)**
   - Device status monitoring
   - Application management (start, terminate, scan)
   - System information query

2. **Calendar Management (`src/mcp/tools/calendar/`)**
   - Calendar CRUD operations
   - Intelligent time parsing
   - Conflict detection
   - Reminder service

3. **Timer (`src/mcp/tools/timer/`)**
   - Countdown timer management
   - Task scheduling
   - Time reminders

4. **Music Playback (`src/mcp/tools/music/`)**
   - Music playback control
   - Playlist management
   - Volume control

5. **Railway Query (`src/mcp/tools/railway/`)**
   - 12306 train query
   - Station information query
   - Fare query

6. **Search Tools (`src/mcp/tools/search/`)**
   - Web search
   - Information retrieval
   - Result filtering

7. **Recipe Tools (`src/mcp/tools/recipe/`)**
   - Recipe query
   - Recipe recommendation
   - Nutritional information

8. **Camera Tools (`src/mcp/tools/camera/`)**
   - Photo capture
   - Visual Q&A
   - Image analysis

9. **Map Tools (`src/mcp/tools/amap/`)**
   - Geocoding/Reverse geocoding
   - Route planning
   - Weather query
   - POI search

10. **Bazi Fortune Telling (`src/mcp/tools/bazi/`)**
    - Bazi calculation
    - Fortune analysis
    - Marriage compatibility analysis
    - Chinese almanac query

## Tool Development Guide

### 1. Creating New Tool Modules

Creating a new tool module requires the following steps:

#### Step 1: Create Module Directory
```bash
mkdir src/mcp/tools/your_tool_name
cd src/mcp/tools/your_tool_name
```

#### Step 2: Create Necessary Files
```bash
touch __init__.py
touch manager.py      # Manager class
touch tools.py        # Tool function implementation
touch models.py       # Data models (optional)
touch client.py       # Client class (optional)
```

#### Step 3: Implement Manager Class
```python
# manager.py
class YourToolManager:
    def __init__(self):
        # Initialization code
        pass
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        Initialize and register tools
        """
        # Define tool properties
        tool_props = PropertyList([
            Property("param1", PropertyType.STRING),
            Property("param2", PropertyType.INTEGER, default_value=0)
        ])
        
        # Register tool
        add_tool((
            "tool_name",
            "Tool description",
            tool_props,
            your_tool_function
        ))

# Global manager instance
_manager = None

def get_your_tool_manager():
    global _manager
    if _manager is None:
        _manager = YourToolManager()
    return _manager
```

#### Step 4: Implement Tool Function
```python
# tools.py
async def your_tool_function(args: dict) -> str:
    """
    Tool function implementation
    """
    param1 = args.get("param1")
    param2 = args.get("param2", 0)
    
    # Business logic
    result = perform_operation(param1, param2)
    
    return f"Operation result: {result}"
```

#### Step 5: Register to Main Server
Add in the `add_common_tools` method of `src/mcp/mcp_server.py`:
```python
# Add your tool
from src.mcp.tools.your_tool_name import get_your_tool_manager

your_tool_manager = get_your_tool_manager()
your_tool_manager.init_tools(self.add_tool, PropertyList, Property, PropertyType)
```

### 2. Best Practices

#### Tool Naming Convention
- Use `self.module.action` format
- For example: `self.calendar.create_event`, `self.music.play`

#### Parameter Design
- Required parameters without default values
- Optional parameters with reasonable default values
- Use appropriate parameter types (STRING, INTEGER, BOOLEAN)

#### Error Handling
```python
async def your_tool_function(args: dict) -> str:
    try:
        # Business logic
        result = await perform_operation(args)
        return f"Success: {result}"
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return f"Error: {str(e)}"
```

#### Asynchronous Support
- Prefer using async/await
- Support automatic wrapping of synchronous functions
- Reasonable use of asyncio tools

### 3. Tool Description Writing

Tool descriptions should include:
- Function introduction
- Usage scenarios
- Parameter description
- Return format
- Precautions

Example:
```python
description = """
Create new calendar events, supporting intelligent time settings and conflict detection.
Usage scenarios:
1. Schedule meetings or appointments
2. Set reminders
3. Time management planning

Parameters:
  title: Event title (required)
  start_time: Start time, ISO format (required)
  end_time: End time, can be automatically calculated
  description: Event description
  category: Event category
  reminder_minutes: Reminder time (minutes)

Returns: Success or failure message of creation
"""
```

## Usage Examples

### Calendar Management
```python
# Create calendar event
await mcp_server.call_tool("self.calendar.create_event", {
    "title": "Team Meeting",
    "start_time": "2024-01-01T10:00:00",
    "category": "Meeting",
    "reminder_minutes": 15
})

# Query today's calendar
await mcp_server.call_tool("self.calendar.get_events", {
    "date_type": "today"
})
```

### Map Functions
```python
# Address to coordinates
await mcp_server.call_tool("self.amap.geocode", {
    "address": "Tiananmen Square, Beijing"
})

# Route planning
await mcp_server.call_tool("self.amap.direction_walking", {
    "origin": "116.397428,39.90923",
    "destination": "116.390813,39.904368"
})
```

### Bazi Fortune Telling
```python
# Get Bazi analysis
await mcp_server.call_tool("self.bazi.get_bazi_detail", {
    "solar_datetime": "2008-03-01T13:00:00+08:00",
    "gender": 1
})

# Marriage compatibility analysis
await mcp_server.call_tool("self.bazi.analyze_marriage_compatibility", {
    "male_solar_datetime": "1990-01-01T10:00:00+08:00",
    "female_solar_datetime": "1992-05-15T14:30:00+08:00"
})
```

## Advanced Features

### 1. Parameter Validation
System provides complete parameter validation mechanism:
- Type checking
- Range validation
- Required parameter checking
- Default value handling

### 2. Tool Discovery
Supports dynamic tool discovery and list retrieval:
- Pagination support
- Size limits
- Cursor traversal

### 3. Visual Capabilities
Supports visual-related functions:
- Image analysis
- Visual Q&A
- Configure external visual services

### 4. Concurrent Processing
- Asynchronous tool execution
- Task scheduling
- Resource management

## Debugging and Testing

### Logging System
```python
from src.utils.logging_config import get_logger
logger = get_logger(__name__)

logger.info("Tool execution started")
logger.error("Execution failed", exc_info=True)
```

### Testing Tools
```python
# Test tool registration
server = McpServer.get_instance()
server.add_common_tools()

# Test tool calling
result = await server.parse_message({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "your_tool_name",
        "arguments": {"param1": "value1"}
    },
    "id": 1
})
```

## Deployment and Configuration

### Environment Requirements
- Python 3.8+
- Asynchronous support
- Related dependency libraries

### Configuration Files
Tool configuration is managed through `config/config.json`, supporting:
- API key configuration
- Service endpoint settings
- Feature switch control

### Performance Optimization
- Connection pool management
- Cache strategy
- Concurrency control
- Resource recycling

## Troubleshooting

### Common Issues
1. **Tool Registration Failure**: Check manager singleton and import paths
2. **Parameter Validation Error**: Confirm parameter types and requirements
3. **Asynchronous Call Issues**: Ensure correct use of async/await
4. **Dependency Missing**: Check module imports and dependency installation

### Debugging Tips
- Enable detailed logging
- Use debugging tools
- Unit test verification
- Performance analysis tools
