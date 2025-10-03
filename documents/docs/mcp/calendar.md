# Calendar Tools

Calendar Tools is a comprehensive MCP calendar management toolset that provides full-featured calendar management functions including event creation, query, update, deletion, and more.

### Common Usage Scenarios

**Create Events:**
- "Schedule a meeting for me tomorrow at 10 AM"
- "Remind me to attend a meeting next Tuesday at 3 PM"
- "Set up a stand-up meeting every morning at 9 AM"
- "Schedule an important meeting on July 15, 2025 at 14:30, ending at 16:00"

**Query Events:**
- "What's scheduled for today"
- "Tomorrow's schedule"
- "This week's meeting arrangements"
- "All schedules for next month"
- "What upcoming events are there recently"

**Modify Events:**
- "Change tomorrow's meeting to 2 PM"
- "Change meeting description to team discussion"
- "Extend meeting time to 3 hours"

**Delete Events:**
- "Cancel tomorrow's meeting"
- "Delete all rest reminders for today"
- "Clear all schedules for this week"

**Category Management:**
- "View all work-type schedules"
- "Create a meeting category schedule"
- "What schedule categories are there"

### Usage Tips

1. **Natural Time Description**: Supports natural language time expressions like "tomorrow", "next Tuesday", "this afternoon"
2. **Smart Duration**: If end time is not specified, system intelligently sets appropriate duration based on event type
3. **Category Management**: Can set categories for events, such as "work", "meeting", "rest", etc.
4. **Reminder Function**: Can set how many minutes in advance to remind, default 15 minutes
5. **Batch Operations**: Supports batch query and deletion of events

AI assistant will automatically select appropriate calendar management tools based on your needs, providing convenient calendar management services.

## Feature Overview

### Core Calendar Management Functions
- **Event Creation**: Create calendar events with time, description, category
- **Event Query**: Query events by date, category, time range
- **Event Update**: Modify event title, time, description and other information
- **Event Deletion**: Delete single or batch delete calendar events

### Time Management Functions
- **Smart Duration**: Automatically sets appropriate duration based on event type
- **Upcoming Events**: Query events within specified future time
- **Reminder Settings**: Configurable advance reminder time
- **Time Conflict Detection**: Prevents creation of conflicting time events

### Category Management
- **Category Statistics**: View all used calendar categories
- **Query by Category**: Filter events by category
- **Smart Categorization**: System automatically assigns appropriate categories for common activities

## Tool List

### 1. Event Creation Tools

#### create_event - Create Calendar Event
Create a new calendar event.

**Parameters:**
- `title` (required): Event title
- `start_time` (required): Start time, ISO format "2025-07-09T10:00:00"
- `end_time` (optional): End time, if not provided, intelligently set
- `description` (optional): Event description
- `category` (optional): Event category, default "default"
- `reminder_minutes` (optional): Advance reminder minutes, default 15 minutes

**Usage Scenarios:**
- Schedule meetings
- Set reminders
- Create work tasks
- Arrange personal activities

### 2. Event Query Tools

#### get_events_by_date - Query Events by Date
Query calendar events within specified date range.

**Parameters:**
- `date_type` (optional): Query type, supports "today", "tomorrow", "week", "month"
- `category` (optional): Filter by category
- `start_date` (optional): Custom start date
- `end_date` (optional): Custom end date

**Usage Scenarios:**
- View today's arrangements
- View this week's schedule
- View schedules by category
- Custom time range query

#### get_upcoming_events - Get Upcoming Events
Query events that will start within specified future time.

**Parameters:**
- `hours` (optional): Query events within how many hours in the future, default 24 hours

**Usage Scenarios:**
- View upcoming arrangements
- Event reminders
- Time planning

### 3. Event Update Tools

#### update_event - Update Calendar Event
Modify existing calendar event information.

**Parameters:**
- `event_id` (required): Calendar event ID
- `title` (optional): New event title
- `start_time` (optional): New start time
- `end_time` (optional): New end time
- `description` (optional): New event description
- `category` (optional): New event category
- `reminder_minutes` (optional): New reminder time

**Usage Scenarios:**
- Modify meeting time
- Update event description
- Adjust reminder time
- Change event category

### 4. Event Deletion Tools

#### delete_event - Delete Calendar Event
Delete specified calendar event.

**Parameters:**
- `event_id` (required): Calendar event ID to delete

**Usage Scenarios:**
- Cancel meetings
- Delete expired events
- Clean up unnecessary events

#### delete_events_batch - Batch Delete Events
Batch delete events that meet conditions.

**Parameters:**
- `date_type` (optional): Delete type, supports "today", "tomorrow", "week", "month"
- `start_date` (optional): Custom start date
- `end_date` (optional): Custom end date
- `category` (optional): Delete by category
- `delete_all` (optional): Whether to delete all events

**Usage Scenarios:**
- Clear events for a specific day
- Delete all events of a category
- Batch clean up expired events

### 5. Category Management Tools

#### get_categories - Get Calendar Categories
Get all used calendar categories.

**Parameters:**
None

**Usage Scenarios:**
- View all categories
- Category statistics
- Category management

## Usage Examples

### Event Creation Examples

```python
# Create simple event
result = await mcp_server.call_tool("create_event", {
    "title": "Team Meeting",
    "start_time": "2025-07-10T10:00:00",
    "description": "Weekly team sync meeting",
    "category": "work"
})

# Create event with end time
result = await mcp_server.call_tool("create_event", {
    "title": "Project Review",
    "start_time": "2025-07-11T14:00:00",
    "end_time": "2025-07-11T16:00:00",
    "description": "Monthly project review meeting",
    "category": "meeting",
    "reminder_minutes": 30
})

# Create personal reminder
result = await mcp_server.call_tool("create_event", {
    "title": "Doctor Appointment",
    "start_time": "2025-07-12T09:30:00",
    "description": "Annual health checkup",
    "category": "personal"
})
```

### Event Query Examples

```python
# Query today's events
result = await mcp_server.call_tool("get_events_by_date", {
    "date_type": "today"
})

# Query this week's work events
result = await mcp_server.call_tool("get_events_by_date", {
    "date_type": "week",
    "category": "work"
})

# Query upcoming events in next 12 hours
result = await mcp_server.call_tool("get_upcoming_events", {
    "hours": 12
})

# Custom date range query
result = await mcp_server.call_tool("get_events_by_date", {
    "start_date": "2025-07-10",
    "end_date": "2025-07-15"
})
```

### Event Update Examples

```python
# Update event time
result = await mcp_server.call_tool("update_event", {
    "event_id": "event_123",
    "start_time": "2025-07-10T11:00:00",
    "end_time": "2025-07-10T12:00:00"
})

# Update event description
result = await mcp_server.call_tool("update_event", {
    "event_id": "event_123",
    "description": "Updated: Team sync with new agenda"
})

# Change event category
result = await mcp_server.call_tool("update_event", {
    "event_id": "event_123",
    "category": "important"
})
```

### Event Deletion Examples

```python
# Delete single event
result = await mcp_server.call_tool("delete_event", {
    "event_id": "event_123"
})

# Delete today's events
result = await mcp_server.call_tool("delete_events_batch", {
    "date_type": "today"
})

# Delete all work category events
result = await mcp_server.call_tool("delete_events_batch", {
    "category": "work"
})

# Delete all events
result = await mcp_server.call_tool("delete_events_batch", {
    "delete_all": true
})
```

### Category Management Examples

```python
# Get all categories
result = await mcp_server.call_tool("get_categories", {})
```

## Data Structures

### Calendar Event (CalendarEvent)
```python
{
    "id": "event_123",
    "title": "Team Meeting",
    "start_time": "2025-07-10T10:00:00",
    "end_time": "2025-07-10T11:00:00",
    "description": "Weekly team sync meeting",
    "category": "work",
    "reminder_minutes": 15,
    "created_at": "2025-07-09T14:30:00Z",
    "updated_at": "2025-07-09T14:30:00Z"
}
```

### Event Query Response (EventsResponse)
```python
{
    "success": true,
    "date_range": {
        "start": "2025-07-10",
        "end": "2025-07-10"
    },
    "total_events": 3,
    "events": [
        {
            "id": "event_123",
            "title": "Team Meeting",
            "start_time": "2025-07-10T10:00:00",
            "end_time": "2025-07-10T11:00:00",
            "description": "Weekly team sync meeting",
            "category": "work"
        }
    ]
}
```

### Category Response (CategoriesResponse)
```python
{
    "success": true,
    "categories": [
        "work",
        "meeting",
        "personal",
        "important",
        "default"
    ],
    "total_categories": 5
}
```

## Best Practices

### 1. Event Creation
- Use clear and descriptive titles
- Set appropriate categories for easy filtering
- Consider setting reminders for important events
- Specify end times for events with fixed durations

### 2. Event Query
- Use date types for common queries
- Filter by category for specific needs
- Use upcoming events for time-sensitive planning
- Custom date ranges for detailed analysis

### 3. Event Management
- Regularly update event information
- Delete expired or unnecessary events
- Use batch operations for efficiency
- Maintain consistent category usage

### 4. Performance Optimization
- Avoid creating too many short-duration events
- Use appropriate query ranges
- Clean up old events regularly
- Use batch operations for bulk changes

## Supported Event Types

### Work Events
- Meetings and appointments
- Project deadlines
- Team activities
- Work reminders

### Personal Events
- Appointments and reservations
- Personal reminders
- Social activities
- Health and wellness

### System Events
- Automated reminders
- System notifications
- Maintenance schedules
- Backup schedules

## Precautions

1. **Time Zone**: All times are in UTC timezone
2. **Event Limits**: Avoid creating too many concurrent events
3. **Data Persistence**: Events are stored in memory and may be lost on restart
4. **Conflict Detection**: System may warn about overlapping events
5. **Reminder Accuracy**: Reminder timing depends on system load

## Troubleshooting

### Common Issues
1. **Event Creation Failure**: Check time format and required parameters
2. **Query No Results**: Verify date range and category filters
3. **Update Failure**: Confirm event ID exists and parameters are valid
4. **Delete Failure**: Check event ID and permissions

### Debugging Methods
1. Verify parameter formats and values
2. Check event ID existence
3. Test with simple examples first
4. Use category queries to verify data

### Performance Tips
1. Use appropriate date ranges for queries
2. Batch operations for multiple changes
3. Regular cleanup of old events
4. Consistent category usage for better organization

With Calendar Tools, you can efficiently manage your schedule, set reminders, and organize your time effectively for both work and personal activities.
