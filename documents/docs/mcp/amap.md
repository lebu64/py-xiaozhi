# Amap Tools

Amap Tools is an MCP toolset based on Amap Web API, providing rich geographic location service functionality.

## Natural Language Usage Methods

### Route Planning
- "How to get from Yunsheng Science Park to Science City Metro Station"
- "Route to Tianhe City"
- "How long does it take to drive from A to B"

### Nearest Location Query
- "How to get to the nearest milk tea shop"
- "Where is the nearest restaurant"
- "Nearest metro station"
- "Nearest bank"

### Nearby Location Search
- "What milk tea shops are nearby"
- "Nearby restaurants"
- "Surrounding supermarkets"
- "Banks within 2 kilometers nearby"

### Smart Navigation
- "Go to Tianhe City"
- "Navigate to Canton Tower"
- "How to get to Baiyun Airport"

### Travel Mode Comparison
- "From A to B, which is faster, driving or taking metro"
- "Compare various ways to get to the airport"
- "Which method is the fastest"

## MCP Tool Introduction

### Smart Tools (Recommended Use)

#### 1. route_planning - Smart Route Planning
Supports natural language address input for route planning, automatically handles address conversion and coordinate parsing.

**Parameters:**
- `origin` (required): Starting point address name
- `destination` (required): Destination address name
- `city` (optional): City location, default Guangzhou
- `travel_mode` (optional): Travel mode, walking (walking), driving (driving), bicycling (cycling), transit (public transport), default walking

#### 2. find_nearest - Find Nearest Location
Find the nearest location of a certain type and provide detailed walking route.

**Parameters:**
- `keywords` (required): Search keywords, such as "milk tea shop", "restaurant", "metro station", "bank"
- `radius` (optional): Search radius (meters), default 5000 meters
- `user_location` (optional): User location, if not provided, automatically locates

#### 3. find_nearby - Nearby Location Search
Search for multiple nearby locations, displayed sorted by distance.

**Parameters:**
- `keywords` (required): Search keywords, such as "milk tea shop", "restaurant", "supermarket"
- `radius` (optional): Search radius (meters), default 2000 meters
- `user_location` (optional): User location, if not provided, automatically locates

#### 4. navigation - Smart Navigation
Provide comparison and recommendations for multiple travel modes to destination.

**Parameters:**
- `destination` (required): Destination name
- `city` (optional): City location, default Guangzhou
- `user_location` (optional): User location, if not provided, automatically locates

#### 5. get_location - Current Location Acquisition
Smart location service based on IP address.

**Parameters:**
- `user_ip` (optional): User IP address, if not provided, automatically obtains

#### 6. compare_routes - Route Comparison
Compare time, distance, and applicability of different travel modes.

**Parameters:**
- `origin` (required): Starting point address name
- `destination` (required): Destination address name
- `city` (optional): City location, default Guangzhou

### Basic Tools (For Secondary Development)

#### Geocoding Tools
- `maps_geo` - Address to coordinates
- `maps_regeocode` - Coordinates to address
- `maps_ip_location` - IP location

#### Route Planning Tools
- `maps_direction_walking` - Walking route planning
- `maps_direction_driving` - Driving route planning
- `maps_bicycling` - Cycling route planning
- `maps_direction_transit_integrated` - Public transport route planning

#### Search Tools
- `maps_text_search` - Keyword search
- `maps_around_search` - Surrounding search
- `maps_search_detail` - POI detail query

#### Other Tools
- `maps_weather` - Weather query
- `maps_distance` - Distance measurement

## Usage Examples

### Smart Tool Examples

```python
# Smart route planning
result = await mcp_server.call_tool("route_planning", {
    "origin": "Yunsheng Science Park",
    "destination": "Science City Metro Station",
    "travel_mode": "walking"
})

# Find nearest location
result = await mcp_server.call_tool("find_nearest", {
    "keywords": "milk tea shop",
    "radius": "5000"
})

# Nearby location search
result = await mcp_server.call_tool("find_nearby", {
    "keywords": "restaurant",
    "radius": "2000"
})
```

### Basic Tool Examples

```python
# Address to coordinates
result = await mcp_server.call_tool("maps_geo", {
    "address": "Tiananmen Square, Beijing",
    "city": "Beijing"
})

# Walking route planning
result = await mcp_server.call_tool("maps_direction_walking", {
    "origin": "116.397428,39.90923",
    "destination": "116.407428,39.91923"
})
```

## Secondary Development Instructions

### Tool Architecture

Amap Tools adopts layered architecture design:

#### 1. Smart Tool Layer (MCP Adaptation)
- **AmapToolsManager**: Manager adapted for MCP server
- **Smart Tool Registration**: Automatically registers user-friendly smart tools
- **Parameter Validation**: Complete parameter type and format validation
- **Result Formatting**: User-friendly result display

#### 2. Business Logic Layer (AmapManager)
- **Smart Route Planning**: Supports natural language address input
- **Automatic Location**: Multi-strategy IP location and city recognition
- **Combined Functions**: Combines multiple API calls into advanced functions
- **Error Handling**: Comprehensive exception handling and fault tolerance mechanism

#### 3. API Client Layer (AmapClient)
- **HTTP Client**: Asynchronous HTTP client based on aiohttp
- **API Encapsulation**: Complete encapsulation of all Amap APIs
- **Response Parsing**: Automatically parses API responses and converts to data models
- **Error Handling**: API-level error handling and retry

#### 4. Data Model Layer (Models)
- **Structured Data**: Data structures defined using dataclass
- **Type Safety**: Complete type annotations and validation
- **Format Conversion**: Automatic conversion of coordinates, addresses and other formats
- **Data Consistency**: Unified data format and naming conventions

### Smart Function Features

#### Automatic Location Strategy
1. Priority use of Amap API automatic IP recognition
2. If failed, try third-party IP service
3. Verify validity of location results
4. Fallback to city center coordinates

#### Address Smart Parsing
- Supports natural language address input: "Tiananmen Square"
- Supports coordinate format: "116.397428,39.90923"
- Supports composite addresses: "No. 1 Tiananmen Square, Dongcheng District, Beijing"

#### Result Smart Formatting
- User-friendly output format
- Comparison display of multiple travel modes
- Detailed walking route guidance

### Configuration Instructions

#### API Key Configuration
Amap Tools requires API key configuration to function properly.

**Obtain API Key:**
1. Visit [Amap Open Platform](https://lbs.amap.com/)
2. Register developer account
3. Create application, obtain API Key

**Configuration Method:**
Currently API key is hardcoded in `src/mcp/tools/amap/__init__.py`:

**Recommended Configuration Method:**
Configure API key in `config/config.json`:

### Extension Development

#### Adding New Smart Tools
1. Implement business logic in `AmapManager`
2. Register new tool in `AmapToolsManager`
3. Add tool definition in `AmapTools`
4. Update test cases

#### Adding New Basic Tools
1. Encapsulate API call in `AmapClient`
2. Implement business logic in `AmapManager`
3. Add tool definition in `AmapTools`
4. Update data models (if needed)

### Data Structures

```python
class Location:
    longitude: float  # Longitude
    latitude: float   # Latitude

class POI:
    id: str              # POI ID
    name: str            # Name
    address: str         # Address
    location: Location   # Coordinates
    type_code: str       # Type code
```

### Best Practices

1. **Prioritize Smart Tools**: Automatically handles complex logic, user-friendly
2. **Reasonable Parameter Settings**: Specify city, radius and other parameters to improve accuracy
3. **Error Handling**: Handle network exceptions and API errors
4. **Cache Strategy**: Cache results of frequent queries
5. **Asynchronous Calls**: Use asynchronous methods to improve performance

With Amap Tools, you can easily add powerful geographic location service functionality to your applications, providing better user experience.
