# Timer Tools

Timer Tools is a powerful MCP countdown toolset that provides functions for creating, managing, and canceling scheduled tasks, supporting delayed execution of various operations.

### Common Usage Scenarios

**Timed Reminders:**
- "Remind me to attend the meeting in 5 minutes"
- "Remind me to take a break in 10 minutes"
- "Remind me to take medicine in half an hour"
- "Remind me to turn off the computer in 1 hour"

**Timed Playback:**
- "Play music in 5 minutes"
- "Play my favorite song in 10 minutes"
- "Stop playback in 15 minutes"
- "Play alarm in 20 minutes"

**Timed System Operations:**
- "Lower volume in 30 minutes"
- "Shut down system in 1 hour"
- "Check system status in 10 minutes"
- "Check weather in 5 minutes"

**Timed Queries:**
- "Check train tickets in 5 minutes"
- "Search for news in 10 minutes"
- "Check schedule in 15 minutes"
- "Look up recipes in 20 minutes"

**Task Management:**
- "View current scheduled tasks"
- "Cancel the timer just set"
- "View all active timers"
- "Cancel the reminder in 5 minutes"

### Usage Tips

1. **Time Expression**: Supports various time expressions like "in 5 minutes", "in half an hour", "in 1 hour"
2. **Task Description**: Can add task descriptions to help identify different scheduled tasks
3. **Task Management**: Can view and cancel running scheduled tasks
4. **Flexible Settings**: Supports setting various types of delayed execution tasks

AI assistant will automatically call timer tools based on your needs, providing convenient scheduled task management services.

## Feature Overview

### Countdown Functionality
- **Scheduled Execution**: Execute tasks after specified delay time
- **Task Types**: Supports various MCP tool calls
- **Time Settings**: Flexible time setting options
- **Task Description**: Can add task descriptions for easy management

### Task Management Functionality
- **Task Creation**: Create new scheduled tasks
- **Task Cancellation**: Cancel running scheduled tasks
- **Task Query**: View all active scheduled tasks
- **Status Monitoring**: Real-time monitoring of task execution status

### Execution Control Functionality
- **Delay Control**: Precise control of execution delay time
- **Task Queue**: Manage multiple concurrent scheduled tasks
- **Error Handling**: Comprehensive error handling mechanism
- **Log Recording**: Detailed task execution logs

### System Integration Functionality
- **MCP Integration**: Seamless integration with other MCP tools
- **Asynchronous Execution**: Supports asynchronous task execution
- **Resource Management**: Reasonable system resource management
- **Performance Optimization**: Optimize scheduled task performance

## Tool List

### 1. Scheduled Task Tools

#### start_countdown_timer - Start Countdown Task
Create and start a countdown task that executes the specified operation after a specified time.

**Parameters:**
- `command` (required): MCP tool call to execute, JSON format string
- `delay` (optional): Delay time (seconds), default 5 seconds
- `description` (optional): Task description

**Usage Scenarios:**
- Timed reminders
- Delayed task execution
- Timed music playback
- Timed system operations

#### cancel_countdown_timer - Cancel Countdown Task
Cancel the specified running countdown task.

**Parameters:**
- `timer_id` (required): Timer ID to cancel

**Usage Scenarios:**
- Cancel unnecessary scheduled tasks
- Modify scheduled task settings
- Clean up scheduled tasks

#### get_active_countdown_timers - Get Active Timers
Get the status of all running countdown tasks.

**Parameters:**
None

**Usage Scenarios:**
- View current scheduled tasks
- Manage scheduled tasks
- Monitor task status

## Usage Examples

### Scheduled Task Creation Examples

```python
# Create a reminder task in 5 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
    "command": '{"name": "create_event", "arguments": {"title": "Meeting Reminder", "start_time": "2024-01-15T14:00:00"}}',
    "delay": 300,
    "description": "Meeting Reminder"
})

# Create a task to play music in 10 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
    "command": '{"name": "search_and_play", "arguments": {"song_name": "Light Music"}}',
    "delay": 600,
    "description": "Play Light Music"
})

# Create a task to adjust volume in 30 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
    "command": '{"name": "set_volume", "arguments": {"volume": 30}}',
    "delay": 1800,
    "description": "Lower Volume"
})
```

### Task Management Examples

```python
# View all active scheduled tasks
result = await mcp_server.call_tool("get_active_countdown_timers", {})

# Cancel specified scheduled task
result = await mcp_server.call_tool("cancel_countdown_timer", {
    "timer_id": "timer_123"
})
```

## Data Structures

### Countdown Task (CountdownTimer)
```python
{
    "timer_id": "timer_123",
    "command": {
        "name": "create_event",
        "arguments": {
            "title": "Meeting Reminder",
            "start_time": "2024-01-15T14:00:00"
        }
    },
    "delay": 300,
    "description": "Meeting Reminder",
    "created_at": "2024-01-15T10:25:00Z",
    "execute_at": "2024-01-15T10:30:00Z",
    "status": "running",
    "remaining_time": 240
}
```

### Task Creation Response (CreateResponse)
```python
{
    "success": true,
    "message": "Countdown task created successfully",
    "timer_id": "timer_123",
    "execute_at": "2024-01-15T10:30:00Z",
    "remaining_time": 300,
    "description": "Meeting Reminder"
}
```

### Task Cancellation Response (CancelResponse)
```python
{
    "success": true,
    "message": "Countdown task cancelled",
    "timer_id": "timer_123",
    "cancelled_at": "2024-01-15T10:27:00Z"
}
```

### Active Task List (ActiveTimers)
```python
{
    "success": true,
    "total_active_timers": 2,
    "timers": [
        {
            "timer_id": "timer_123",
            "description": "Meeting Reminder",
            "remaining_time": 240,
            "execute_at": "2024-01-15T10:30:00Z",
            "status": "running"
        },
        {
            "timer_id": "timer_456",
            "description": "Play Music",
            "remaining_time": 480,
            "execute_at": "2024-01-15T10:33:00Z",
            "status": "running"
        }
    ]
}
```

## Task Status Description

### Task Status Types
- **running**: Running, waiting for execution
- **executing**: Executing task
- **completed**: Execution completed
- **cancelled**: Has been cancelled
- **failed**: Execution failed

### Time-related Fields
- **created_at**: Task creation time
- **execute_at**: Task execution time
- **remaining_time**: Remaining time (seconds)
- **cancelled_at**: Task cancellation time
- **completed_at**: Task completion time

## Supported Command Types

### Calendar Management Commands
- **create_event**: Create calendar event
- **update_event**: Update calendar event
- **delete_event**: Delete calendar event

### Music Playback Commands
- **search_and_play**: Search and play music
- **play_pause**: Play/pause music
- **stop**: Stop playback
- **get_status**: Get playback status

### System Control Commands
- **set_volume**: Set volume
- **get_system_status**: Get system status

### Search Query Commands
- **search_bing**: Web search
- **query_train_tickets**: Query train tickets
- **get_recipe_by_id**: Get recipe

## Time Setting Specifications

### Time Units
- **Second**: Minimum time unit
- **Minute**: 60 seconds
- **Hour**: 3600 seconds
- **Day**: 86400 seconds

### Common Time Settings
- **5 minutes**: 300 seconds
- **10 minutes**: 600 seconds
- **15 minutes**: 900 seconds
- **30 minutes**: 1800 seconds
- **1 hour**: 3600 seconds
- **2 hours**: 7200 seconds

### Time Limits
- **Minimum delay**: 1 second
- **Maximum delay**: 24 hours (86400 seconds)
- **Recommended range**: 1 second - 4 hours

## Best Practices

### 1. Task Design
- Use clear task descriptions
- Set reasonable delay times
- Choose appropriate execution commands
- Consider task execution timing

### 2. Task Management
- Regularly check active tasks
- Promptly cancel unnecessary tasks
- Avoid creating too many concurrent tasks
- Reasonably arrange task timing

### 3. Error Handling
- Verify command format correctness
- Handle task execution failure situations
- Monitor task execution status
- Record task execution logs

### 4. Performance Optimization
- Avoid creating tasks with too short intervals
- Reasonably control concurrent task count
- Optimize task execution logic
- Regularly clean up completed tasks

## Usage Scenario Examples

### Work Efficiency Scenarios
1. **Pomodoro Technique**: Remind to rest after 25 minutes
2. **Meeting Reminder**: Remind to prepare 5 minutes before meeting
3. **Task Switching**: Switch to next task after 1 hour
4. **Timed Check**: Check email every 30 minutes

### Life Assistant Scenarios
1. **Cooking Timer**: Remind to check stove in 10 minutes
2. **Medication Reminder**: Remind to take medicine every 8 hours
3. **Exercise Reminder**: Remind to stand up and move every hour
4. **Sleep Reminder**: Remind to prepare for sleep at 10 PM

### Entertainment Scenarios
1. **Music Playback**: Play bedtime music in 30 minutes
2. **Game Reminder**: Remind to rest after 1 hour
3. **Video Timing**: Pause video after 2 hours
4. **Reading Reminder**: Remind to rest eyes after 45 minutes

## Precautions

1. **Time Accuracy**: Timer is based on system time, ensure system time is accurate
2. **Task Complexity**: Avoid executing overly complex operations in scheduled tasks
3. **Resource Management**: Reasonably control concurrent task count, avoid excessive resource occupation
4. **Error Recovery**: System automatically cleans up when task execution fails
5. **Task Persistence**: Scheduled tasks will be lost after system restart

## Troubleshooting

### Common Issues
1. **Task Creation Failure**: Check command format and parameters
2. **Task Execution Failure**: Check if target tool is available
3. **Task Cancellation Failure**: Confirm task ID is correct
4. **Time Setting Error**: Verify time parameter range

### Debugging Methods
1. Check error information returned by task creation
2. Check active task list to confirm task status
3. Verify if command format is correct
4. Test if target tool works normally

### Performance Optimization Suggestions
1. Avoid creating too many short-interval tasks
2. Reasonably set task descriptions for easy management
3. Regularly clean up unnecessary tasks
4. Monitor system resource usage

With Timer Tools, you can easily set various scheduled tasks to improve work efficiency and life convenience.
