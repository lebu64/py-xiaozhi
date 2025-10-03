# 12306 Query Tools (Railway Tools)

Railway ticket query tool is an MCP toolset based on the 12306 system, providing train ticket queries, station information queries, transfer solution queries, and other functions. The tool provides two layers of interfaces: **Smart Tools** (user-friendly natural language interface) and **Atomic Tools** (technical development interface).

## Smart Tools (Recommended for Use)

Smart tools can understand natural language input, automatically handle complex query logic, and are the preferred method for daily use.

### Common Usage Scenarios

**Smart Train Ticket Queries:**
- "Query train tickets from Beijing to Shanghai for tomorrow"
- "I want to see high-speed trains from Guangzhou to Shenzhen for the day after tomorrow"
- "Help me check tickets from Hangzhou to Nanjing for this Saturday"
- "Query bullet trains from Beijing South to Tianjin for January 15, 2025"
- "What high-speed trains depart in the morning to Shanghai"

**Smart Station Queries:**
- "What train stations are in Beijing"
- "What is the main train station in Shanghai"  
- "Query the station code for Beijing South Station"
- "Detailed information about Hongqiao Station"

**Smart Transfer Queries:**
- "What to do if there are no direct trains from Beijing to Guangzhou"
- "Query transfer solutions from Harbin to Kunming"
- "I need to transfer in Zhengzhou, help me check tickets"

**Smart Travel Suggestions:**
- "What's the best way to travel from Beijing to Shanghai"
- "Recommend travel options from Guangzhou to Shenzhen"
- "I want the fastest option to Hangzhou"
- "Recommend economical train tickets"

### Usage Tips

1. **Use Common City Names**: Such as "Beijing", "Shanghai", "Guangzhou", etc., the system will automatically match the main stations
2. **Provide Specific Dates**: Supports relative times like "tomorrow", "day after tomorrow", "this Saturday", etc.
3. **Specify Train Type Preferences**: You can indicate preferences for high-speed trains, bullet trains, or regular trains
4. **Consider Travel Time**: You can specify departure time periods, such as "morning", "afternoon", etc.
5. **Express Preferences**: You can indicate preferences like "fastest", "cheapest", "comfortable", etc.

The AI assistant will automatically call the smart tools based on your needs and provide you with accurate ticket information and travel suggestions.

## Smart Tools Detailed Introduction

### 1. smart_ticket_query - Smart Train Ticket Query
Automatically processes natural language train ticket queries, supports relative dates, train type preferences, time period filtering, etc.

**Features:**
- Automatically converts city names to station codes
- Supports relative dates (tomorrow, day after tomorrow, this Saturday, etc.)
- Intelligently recognizes train type preferences (high-speed trains, bullet trains, direct trains, etc.)
- Filters by time periods (morning, afternoon, evening)
- Formatted output, easy to read

**Usage Examples:**
- "Query train tickets from Beijing to Shanghai for tomorrow"
- "I want to see high-speed trains from Guangzhou to Shenzhen for the day after tomorrow"
- "What bullet trains depart in the morning to Nanjing"

### 2. smart_transfer_query - Smart Transfer Query
When there are no direct trains, automatically finds optimal transfer solutions, providing detailed transfer information.

**Features:**
- Automatically calculates optimal transfer routes
- Displays transfer waiting times
- Supports specifying transfer cities
- Analyzes same-station transfers and cross-station transfers
- Provides complete itinerary information

**Usage Examples:**
- "What to do if there are no direct trains from Beijing to Guangzhou"
- "Query transfer solutions from Harbin to Kunming"
- "I need to transfer in Zhengzhou, help me check tickets"

### 3. smart_station_query - Smart Station Query
Handles various station-related queries, automatically identifies query intent and provides corresponding information.

**Features:**
- Automatically identifies query types (station lists, main stations, codes, etc.)
- Supports city station queries
- Provides detailed station information
- Intelligently parses query intent

**Usage Examples:**
- "What train stations are in Beijing"
- "What is the main train station in Shanghai"
- "Query the station code for Beijing South Station"

### 4. smart_travel_suggestion - Smart Travel Suggestions
Comprehensively analyzes direct and transfer solutions, providing personalized travel suggestions based on user preferences.

**Features:**
- Comprehensive analysis of multiple travel options
- Recommends optimal solutions based on preferences
- Provides detailed pros and cons analysis
- Supports time and price optimization
- Personalized recommendation reasons

**Usage Examples:**
- "What's the best way to travel from Beijing to Shanghai"
- "Recommend travel options from Guangzhou to Shenzhen"
- "I want the fastest option to Hangzhou"

## Feature Overview

### Station Information Query
- **City Station Query**: Query all train stations in a specified city
- **Station Code Query**: Get the 12306 code for a station
- **Station Name Query**: Get detailed information based on station name
- **Main Station Identification**: Automatically identifies the main stations of a city

### Train Ticket Query
- **Direct Ticket Query**: Query direct trains between two locations
- **Fare Information**: Display prices and seat availability for various seat types
- **Train Filtering**: Supports filtering by train type, time, etc.
- **Sorting Function**: Supports sorting by departure time, price, etc.

### Transfer Solution Query
- **Smart Transfer**: Automatically calculates optimal transfer solutions
- **Transfer Time**: Displays transfer waiting times
- **Transfer Stations**: Supports specifying transfer stations
- **Total Duration**: Calculates total travel time including transfers

### Practical Functions
- **Date Management**: Get current date, supports relative time queries
- **Ticket Availability Status**: Real-time display of seat availability
- **Special Markers**: Display train features (such as sleeper, dining car, etc.)

## Atomic Tools (Developer Interface)

Atomic tools provide underlying technical interfaces suitable for system integration and secondary development. Each atomic tool implements a single function and requires precise parameter input.

### Basic Information Tools

#### get_current_date - Get Current Date
Get current date (Shanghai timezone).

**Parameters:**
None

**Usage Scenarios:**
- Confirm current date
- Relative time calculation
- Date validation

#### get_stations_in_city - Get City Stations
Get all train station information for a specified city.

**Parameters:**
- `city` (required): City name

**Usage Scenarios:**
- View all stations in a city
- Select specific stations
- Understand station distribution

#### get_city_station_code - Get City Main Station Codes
Get code information for the main stations of a city.

**Parameters:**
- `cities` (required): City names, multiple cities separated by "|"

**Usage Scenarios:**
- Quickly get main stations
- Batch query city stations
- System integration

#### get_station_by_name - Query by Station Name
Get detailed information based on station name.

**Parameters:**
- `station_names` (required): Station names, multiple stations separated by "|"

**Usage Scenarios:**
- Verify station names
- Get detailed station information
- Station information confirmation

#### get_station_by_code - Query by Station Code
Get station information based on station code.

**Parameters:**
- `station_code` (required): Station code

**Usage Scenarios:**
- Reverse lookup station from code
- System data validation
- Technical integration

### 2. Train Ticket Query Tools

#### query_train_tickets - Query Train Tickets
Query train ticket information for specified dates and routes.

**Parameters:**
- `date` (required): Departure date, format "YYYY-MM-DD"
- `from_station` (required): Departure station
- `to_station` (required): Arrival station
- `train_filters` (optional): Train filtering conditions
- `sort_by` (optional): Sorting method
- `reverse` (optional): Whether to reverse order
- `limit` (optional): Result quantity limit

**Usage Scenarios:**
- Daily travel ticket checking
- Fare comparison
- Travel planning

#### query_transfer_tickets - Query Transfer Tickets
Query train ticket solutions requiring transfers.

**Parameters:**
- `date` (required): Departure date
- `from_station` (required): Departure station
- `to_station` (required): Arrival station
- `middle_station` (optional): Specified transfer station
- `show_wz` (optional): Whether to show standing tickets
- `train_filters` (optional): Train filtering conditions
- `sort_by` (optional): Sorting method
- `reverse` (optional): Whether to reverse order
- `limit` (optional): Result quantity limit, default 10

**Usage Scenarios:**
- Query transfers when no direct trains available
- Compare transfer solutions
- Complex travel planning

#### query_train_route - Query Train Route Stops
Query stop information for specified train numbers.

**Parameters:**
- `train_code` (required): Train number

**Usage Scenarios:**
- Understand train routes
- Select intermediate stops
- Travel route planning

Note: This feature is under development

## Usage Examples

### Basic Information Query Examples

```python
# Get current date
result = await mcp_server.call_tool("get_current_date", {})

# Query all stations in Beijing
result = await mcp_server.call_tool("get_stations_in_city", {
    "city": "Beijing"
})

# Get main stations for multiple cities
result = await mcp_server.call_tool("get_city_station_code", {
    "cities": "Beijing|Shanghai|Guangzhou"
})

# Query by station name
result = await mcp_server.call_tool("get_station_by_name", {
    "station_names": "Beijing South|Shanghai Hongqiao"
})

# Query by station code
result = await mcp_server.call_tool("get_station_by_code", {
    "station_code": "VNP"
})
```

### Train Ticket Query Examples

```python
# Basic train ticket query
result = await mcp_server.call_tool("query_train_tickets", {
    "date": "2025-07-15",
    "from_station": "Beijing",
    "to_station": "Shanghai"
})

# Query with filtering conditions
result = await mcp_server.call_tool("query_train_tickets", {
    "date": "2025-07-15",
    "from_station": "Beijing",
    "to_station": "Shanghai",
    "train_filters": "G,D",  # Only query high-speed and bullet trains
    "sort_by": "departure_time",
    "limit": 10
})

# Transfer ticket query
result = await mcp_server.call_tool("query_transfer_tickets", {
    "date": "2025-07-15",
    "from_station": "Beijing",
    "to_station": "Guangzhou",
    "limit": 5
})

# Query with specified transfer station
result = await mcp_server.call_tool("query_transfer_tickets", {
    "date": "2025-07-15",
    "from_station": "Beijing",
    "to_station": "Guangzhou",
    "middle_station": "Zhengzhou",
    "limit": 5
})
```

## Data Structure

### Station Information (Station)
```python
{
    "station_code": "VNP",
    "station_name": "Beijing South",
    "station_pinyin": "beijingnan",
    "city": "Beijing",
    "code": "VNP"
}
```

### Train Ticket Information (Ticket)
```python
{
    "start_train_code": "G1",
    "from_station": "Beijing South",
    "to_station": "Shanghai Hongqiao",
    "start_time": "09:00",
    "arrive_time": "14:28",
    "duration": "5:28",
    "prices": [
        {
            "seat_name": "Business Class",
            "price": "1748",
            "num": "3"
        },
        {
            "seat_name": "First Class",
            "price": "933",
            "num": "Available"
        }
    ],
    "features": ["WiFi", "Charging Sockets"]
}
```

### Transfer Solution (Transfer)
```python
{
    "start_date": "2025-07-15",
    "start_time": "08:00",
    "arrive_date": "2025-07-15",
    "arrive_time": "20:30",
    "from_station_name": "Beijing South",
    "middle_station_name": "Zhengzhou East",
    "end_station_name": "Guangzhou South",
    "same_train": false,
    "same_station": true,
    "wait_time": "2 hours 15 minutes",
    "duration": "12 hours 30 minutes",
    "ticket_list": [
        {
            "start_train_code": "G79",
            "from_station": "Beijing South",
            "to_station": "Zhengzhou East",
            "start_time": "08:00",
            "arrive_time": "11:15",
            "duration": "3:15",
            "prices": [...]
        }
    ]
}
```

## Ticket Availability Status Explanation

### Seat Availability Display
- **Specific Number**: Such as "5" indicates 5 tickets remaining
- **"Available"**: Tickets available, specific quantity unknown
- **"Plentiful"**: Plenty of tickets available
- **"None"**: No tickets available
- **"--"**: This seat type not available for sale
- **"Waitlist"**: No tickets, can join waitlist

### Seat Types
- **Business Class**: Highest class seats
- **First Class**: High class seats
- **Second Class**: Standard seats
- **Standing**: Standing tickets
- **Hard Sleeper**: Hard sleeper berths
- **Soft Sleeper**: Soft sleeper berths
- **Deluxe Soft Sleeper**: Luxury sleeper berths

## Query Techniques

### 1. Station Names
- Use official station names, such as "Beijing South" instead of "Beijing South Station"
- Support city names, system will automatically match main stations
- Large cities may have multiple options, recommend specifying station names

### 2. Time Formats
- Date format: YYYY-MM-DD, such as "2025-07-15"
- Supports relative times, such as "tomorrow", "day after tomorrow"
- Pay attention to holidays and schedule adjustments

### 3. Filtering Conditions
- Train filtering: G(High-speed), D(Bullet), C(Intercity), Z(Direct), T(Express), K(Fast)
- Time filtering: Can sort by departure time or arrival time
- Price filtering: Can sort by ticket price

### 4. Transfer Queries
- Prefer using major hub stations for transfers
- Pay attention to transfer times, recommend allowing sufficient transfer time
- Consider luggage and travel convenience

## Precautions

1. **Data Real-time Nature**: Ticket information updates in real-time, query results are for reference only
2. **Ticket Purchase Channels**: Tool only provides query functionality, ticket purchase requires official channels
3. **Network Dependency**: Queries require network connection to 12306 system
4. **Query Limitations**: Avoid frequent queries, comply with 12306 usage regulations

## Troubleshooting

### Common Issues
1. **Station Name Errors**: Check if station names are correct
2. **No Query Results**: Confirm date and station information
3. **Network Timeout**: Check network connection status
4. **Data Format Errors**: Verify input parameter formats

### Debugging Methods
1. First query station information to confirm station names
2. Use get_current_date to confirm date format
3. Check network connection and firewall settings
4. Check returned error messages

## Secondary Development Guide

### MCP Tool Integration

Railway tools are based on MCP (Model Context Protocol) architecture, supporting flexible tool integration and extension.

#### Tool Manager
```python
from src.mcp.tools.railway import get_railway_tools_manager

# Get tool manager instance
manager = get_railway_tools_manager()

# Initialize tools (called in MCP server)
manager.init_tools(add_tool, PropertyList, Property, PropertyType)
```

#### Custom Smart Tools
Developers can create new smart tools based on existing atomic tools:

```python
async def custom_smart_query(self, args: Dict[str, Any]) -> str:
    """Custom smart query tool"""
    # Parse user input
    query = args.get("query", "")
    
    # Call atomic tools
    client = await get_railway_client()
    result = await client.query_tickets(...)
    
    # Format output
    return self._format_custom_result(result)
```

### Architecture Description

Railway tools use layered architecture:
- **Smart Tool Layer**: Processes natural language input, user-friendly
- **Atomic Tool Layer**: Provides basic functionality, technically precise
- **Client Layer**: Interacts with 12306 API
- **Data Model Layer**: Defines data structures

### Extension Suggestions

1. **Add New Smart Tools**: Combine new functionality based on existing atomic tools
2. **Optimize Query Logic**: Improve processing algorithms for smart tools
3. **Enhance Data Formats**: Add more output format options
4. **Integrate Other Services**: Combine with other transportation information

With railway ticket query tools, you can conveniently obtain train ticket information, plan travel routes, making it an essential practical tool for travel. Smart tools make daily use more convenient, while atomic tools provide developers with powerful integration capabilities.
