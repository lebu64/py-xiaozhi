# IoT Device Development Guide

## Overview

py-xiaozhi project adopts Thing Pattern-based IoT device architecture, providing unified device abstraction and management interfaces. All devices inherit from the Thing base class and are centrally managed through ThingManager. This architecture supports asynchronous operations, type-safe parameter processing, and state management.

**Important Note**: The current project is migrating from IoT device mode to MCP (Model Context Protocol) tool mode, some device functions have been migrated to MCP tool system.

## Core Architecture

### Directory Structure

```
src/iot/
├── thing.py                 # Core base classes and utility classes
│   ├── Thing               # Device abstract base class
│   ├── Property            # Device property class
│   ├── Method              # Device method class
│   ├── Parameter           # Method parameter class
│   └── ValueType           # Parameter type enumeration
├── thing_manager.py        # Device manager
│   └── ThingManager        # Singleton device manager
└── things/                 # Device implementations
    ├── lamp.py            # Lighting device
    ├── speaker.py         # Audio device
    ├── music_player.py    # Music player
    ├── countdown_timer.py # Countdown timer
    └── CameraVL/          # Camera device
        ├── Camera.py
        └── VL.py
```

### Core Components

#### 1. Thing Base Class

Thing is the abstract base class for all IoT devices, providing unified interface specifications:

```python
from src.iot.thing import Thing, Parameter, ValueType

class Thing:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.properties = {}
        self.methods = {}
    
    def add_property(self, name: str, description: str, getter: Callable)
    def add_method(self, name: str, description: str, parameters: List[Parameter], callback: Callable)
    async def get_descriptor_json(self) -> str
    async def get_state_json(self) -> str
    async def invoke(self, command: dict) -> dict
```

**Key Requirements:**

- All property getter functions must be asynchronous (`async def`)
- All method callback functions must be asynchronous
- Device names must be globally unique

#### 2. Property System

Property is used to define device readable states, supporting automatic type inference:

```python
class Property:
    def __init__(self, name: str, description: str, getter: Callable):
        # Force getter must be async function
        if not inspect.iscoroutinefunction(getter):
            raise TypeError(f"Property getter for '{name}' must be an async function.")
```

**Supported Property Types:**

- `boolean`: Boolean value
- `number`: Integer
- `string`: String
- `float`: Floating point number
- `array`: Array
- `object`: Object

#### 3. Method System

Method is used to define device executable operations:

```python
class Method:
    def __init__(self, name: str, description: str, parameters: List[Parameter], callback: Callable):
        # Force callback must be async function
        if not inspect.iscoroutinefunction(callback):
            raise TypeError(f"Method callback for '{name}' must be an async function.")
```

#### 4. Parameter System

Parameter defines method parameter specifications:

```python
class Parameter:
    def __init__(self, name: str, description: str, type_: str, required: bool = True):
        self.name = name
        self.description = description
        self.type = type_
        self.required = required
    
    def get_value(self):
        return self.value
```

**Supported Parameter Types:**

- `ValueType.BOOLEAN`: Boolean value
- `ValueType.NUMBER`: Integer
- `ValueType.STRING`: String
- `ValueType.FLOAT`: Floating point number
- `ValueType.ARRAY`: Array
- `ValueType.OBJECT`: Object

#### 5. ThingManager Manager

ThingManager uses singleton pattern, responsible for device registration, state management, and method invocation:

```python
from src.iot.thing_manager import ThingManager

class ThingManager:
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThingManager()
        return cls._instance
    
    def add_thing(self, thing: Thing)
    async def get_states_json(self, delta: bool = False) -> Tuple[bool, str]
    async def get_descriptors_json(self) -> str
    async def invoke(self, command: dict) -> dict
```

**Core Functions:**

- Device registration and management
- State caching and incremental updates
- Method invocation distribution
- Device description information query

## Device Implementation Patterns

### 1. Basic Device - Lamp

Simplest device implementation pattern:

```python
import asyncio
from src.iot.thing import Thing

class Lamp(Thing):
    def __init__(self):
        super().__init__("Lamp", "A test lamp")
        self.power = False
        
        # Register property - getter must be async function
        self.add_property("power", "Whether the lamp is on", self.get_power)
        
        # Register method - callback must be async function
        self.add_method("TurnOn", "Turn on the lamp", [], self._turn_on)
        self.add_method("TurnOff", "Turn off the lamp", [], self._turn_off)
    
    async def get_power(self):
        return self.power
    
    async def _turn_on(self, params):
        self.power = True
        return {"status": "success", "message": "Lamp turned on"}
    
    async def _turn_off(self, params):
        self.power = False
        return {"status": "success", "message": "Lamp turned off"}
```

### 2. Parameter Device - Speaker

Device implementation with parameter validation:

```python
import asyncio
from src.iot.thing import Thing, Parameter, ValueType
from src.utils.volume_controller import VolumeController

class Speaker(Thing):
    def __init__(self):
        super().__init__("Speaker", "Current AI robot speaker")
        
        # Initialize volume controller
        self.volume_controller = None
        try:
            if VolumeController.check_dependencies():
                self.volume_controller = VolumeController()
                self.volume = self.volume_controller.get_volume()
            else:
                self.volume = 70
        except Exception:
            self.volume = 70
        
        # Register property
        self.add_property("volume", "Current volume value", self.get_volume)
        
        # Register method with parameters
        self.add_method(
            "SetVolume",
            "Set volume",
            [Parameter("volume", "Integer between 0 and 100", ValueType.NUMBER, True)],
            self._set_volume,
        )
    
    async def get_volume(self):
        if self.volume_controller:
            try:
                self.volume = self.volume_controller.get_volume()
            except Exception:
                pass
        return self.volume
    
    async def _set_volume(self, params):
        # Get value from Parameter object
        volume = params["volume"].get_value()
        
        # Parameter validation
        if not (0 <= volume <= 100):
            raise ValueError("Volume must be between 0-100")
        
        self.volume = volume
        try:
            if self.volume_controller:
                # Asynchronous system API call
                await asyncio.to_thread(self.volume_controller.set_volume, volume)
            return {"success": True, "message": f"Volume set to: {volume}"}
        except Exception as e:
            return {"success": False, "message": f"Failed to set volume: {e}"}
```

### 3. Complex Device - CountdownTimer

Asynchronous task management device implementation:

```python
import asyncio
import json
from typing import Dict
from asyncio import Task
from src.iot.thing import Thing, Parameter
from src.iot.thing_manager import ThingManager

class CountdownTimer(Thing):
    def __init__(self):
        super().__init__("CountdownTimer", "A countdown timer for delayed command execution")
        
        # Task management
        self._timers: Dict[int, Task] = {}
        self._next_timer_id = 0
        self._lock = asyncio.Lock()
        
        # Register methods
        self.add_method(
            "StartCountdown",
            "Start a countdown that executes specified command after delay",
            [
                Parameter("command", "IoT command to execute (JSON format string)", "string", True),
                Parameter("delay", "Delay time (seconds), default 5 seconds", "integer", False)
            ],
            self._start_countdown,
        )
        
        self.add_method(
            "CancelCountdown",
            "Cancel specified countdown",
            [Parameter("timer_id", "Timer ID to cancel", "integer", True)],
            self._cancel_countdown,
        )
    
    async def _start_countdown(self, params_dict):
        # Process required parameters
        command_param = params_dict.get("command")
        command_str = command_param.get_value() if command_param else None
        
        if not command_str:
            return {"status": "error", "message": "Missing 'command' parameter value"}
        
        # Process optional parameters
        delay_param = params_dict.get("delay")
        delay = (
            delay_param.get_value()
            if delay_param and delay_param.get_value() is not None
            else 5
        )
        
        # Validate command format
        try:
            json.loads(command_str)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Command format error, cannot parse JSON"}
        
        # Create async task
        async with self._lock:
            timer_id = self._next_timer_id
            self._next_timer_id += 1
            task = asyncio.create_task(
                self._delayed_execution(delay, timer_id, command_str)
            )
            self._timers[timer_id] = task
        
        return {
            "status": "success",
            "message": f"Countdown {timer_id} started, will execute in {delay} seconds",
            "timer_id": timer_id
        }
    
    async def _delayed_execution(self, delay: int, timer_id: int, command_str: str):
        try:
            await asyncio.sleep(delay)
            # Execute command
            command_dict = json.loads(command_str)
            thing_manager = ThingManager.get_instance()
            result = await thing_manager.invoke(command_dict)
            print(f"Countdown {timer_id} execution result: {result}")
        except asyncio.CancelledError:
            print(f"Countdown {timer_id} cancelled")
        finally:
            async with self._lock:
                self._timers.pop(timer_id, None)
    
    async def _cancel_countdown(self, params_dict):
        timer_id_param = params_dict.get("timer_id")
        timer_id = timer_id_param.get_value() if timer_id_param else None
        
        if timer_id is None:
            return {"status": "error", "message": "Missing 'timer_id' parameter value"}
        
        async with self._lock:
            if timer_id in self._timers:
                task = self._timers.pop(timer_id)
                task.cancel()
                return {"status": "success", "message": f"Countdown {timer_id} cancelled"}
            else:
                return {"status": "error", "message": "Timer does not exist"}
```

### 4. Multi-threaded Device - Camera

Device implementation integrating multi-threading and external services:

```python
import threading
import base64
import cv2
from src.iot.thing import Thing
from src.iot.things.CameraVL.VL import ImageAnalyzer

class Camera(Thing):
    def __init__(self):
        super().__init__("Camera", "Camera management")
        self.cap = None
        self.is_running = False
        self.camera_thread = None
        self.result = ""
        
        # Initialize VL analyzer
        self.VL = ImageAnalyzer.get_instance()
        
        # Register properties
        self.add_property("power", "Whether camera is on", self.get_power)
        self.add_property("result", "Recognized content of the image", self.get_result)
        
        # Register methods
        self.add_method("start_camera", "Start camera", [], self.start_camera)
        self.add_method("stop_camera", "Stop camera", [], self.stop_camera)
        self.add_method("capture_frame_to_base64", "Recognize image", [], self.capture_frame_to_base64)
    
    async def get_power(self):
        return self.is_running
    
    async def get_result(self):
        return self.result
    
    async def start_camera(self, params):
        if self.camera_thread and self.camera_thread.is_alive():
            return {"status": "info", "message": "Camera already running"}
        
        self.camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
        self.camera_thread.start()
        return {"status": "success", "message": "Camera started"}
    
    async def stop_camera(self, params):
        self.is_running = False
        if self.camera_thread:
            self.camera_thread.join()
            self.camera_thread = None
        return {"status": "success", "message": "Camera stopped"}
    
    async def capture_frame_to_base64(self, params):
        if not self.cap or not self.cap.isOpened():
            return {"status": "error", "message": "Camera not opened"}
        
        ret, frame = self.cap.read()
        if not ret:
            return {"status": "error", "message": "Unable to read frame"}
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Use VL analyzer to recognize image
        self.result = str(self.VL.analyze_image(frame_base64))
        
        return {"status": "success", "result": self.result}
    
    def _camera_loop(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return
        
        self.is_running = True
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_running = False
        
        self.cap.release()
        cv2.destroyAllWindows()
```

## Device Registration and Management

### 1. Device Registration

Register devices when application starts:

```python
from src.iot.thing_manager import ThingManager
from src.iot.things.lamp import Lamp
from src.iot.things.speaker import Speaker

def initialize_iot_devices():
    # Get device manager instance
    manager = ThingManager.get_instance()
    
    # Register devices
    manager.add_thing(Lamp())
    manager.add_thing(Speaker())
    
    print(f"Registered {len(manager.things)} devices")
```

### 2. Device Status Query

```python
# Get all device status
changed, states = await manager.get_states_json(delta=False)
print(f"Device status: {states}")

# Get changed status (incremental update)
changed, delta_states = await manager.get_states_json(delta=True)
if changed:
    print(f"Status changes: {delta_states}")
```

### 3. Device Method Invocation

```python
# Call device method
command = {
    "name": "Lamp",
    "method": "TurnOn",
    "parameters": {}
}
result = await manager.invoke(command)
print(f"Execution result: {result}")

# Method call with parameters
command = {
    "name": "Speaker",
    "method": "SetVolume",
    "parameters": {"volume": 80}
}
result = await manager.invoke(command)
```

## Development Best Practices

### 1. Asynchronous Programming

**All property getters and method callbacks must be async functions:**

```python
# Correct async property
async def get_power(self):
    return self.power

# Correct async method
async def turn_on(self, params):
    self.power = True
    return {"status": "success"}

# Error: sync function will throw exception
def get_power(self):  # TypeError!
    return self.power
```

### 2. Parameter Processing

**Properly handle required and optional parameters:**

```python
async def my_method(self, params):
    # Process required parameters
    required_value = params["required_param"].get_value()
    
    # Process optional parameters
    optional_value = None
    if "optional_param" in params:
        optional_value = params["optional_param"].get_value()
    
    # Parameter validation
    if not isinstance(required_value, str):
        return {"status": "error", "message": "Parameter type error"}
    
    return {"status": "success", "result": required_value}
```

### 3. Error Handling

**Implement appropriate error handling:**

```python
async def risky_operation(self, params):
    try:
        # Execute potentially failing operation
        result = await self.perform_operation()
        return {"status": "success", "result": result}
    except ValueError as e:
        return {"status": "error", "message": f"Parameter error: {e}"}
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        return {"status": "error", "message": "Operation failed"}
```

### 4. Resource Management

**Properly manage device resources:**

```python
class MyDevice(Thing):
    def __init__(self):
        super().__init__("MyDevice", "My device")
        self.resource = None
        self._lock = asyncio.Lock()
    
    async def acquire_resource(self, params):
        async with self._lock:
            if self.resource is None:
                self.resource = await self.create_resource()
            return {"status": "success"}
    
    async def cleanup(self):
        """Device cleanup method"""
        if self.resource:
            await self.resource.close()
            self.resource = None
```

### 5. Logging

**Use unified logging system:**

```python
from src.utils.logging_config import get_logger

class MyDevice(Thing):
    def __init__(self):
        super().__init__("MyDevice", "My device")
        self.logger = get_logger(self.__class__.__name__)
    
    async def my_method(self, params):
        self.logger.info("Method called")
        try:
            result = await self.perform_operation()
            self.logger.info(f"Operation successful: {result}")
            return {"status": "success", "result": result}
        except Exception as e:
            self.logger.error(f"Operation failed: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
```

## Migration Instructions

**Important Note**: Project is migrating from IoT device mode to MCP (Model Context Protocol) tool mode:

1. **Countdown Timer**: Already migrated to MCP tools, providing better AI integration
2. **Other Devices**: May migrate gradually based on complexity
3. **New Features**: Recommended to consider using MCP tool framework directly

Current IoT architecture is still stable and suitable for:

- Simple device control
- Learning and demonstration
- Rapid prototyping development

## Notes

1. **Async Requirement**: All property getters and method callbacks must be async functions
2. **Parameter Processing**: Method parameters passed through Parameter objects, need to call `get_value()` to get value
3. **Error Handling**: Implement appropriate error handling and feedback mechanisms
4. **Resource Management**: Properly manage device resources, avoid resource leaks
5. **Device Names**: Ensure device names are globally unique
6. **Return Format**: Method returns should include `status` and `message` fields

## Summary

py-xiaozhi's IoT architecture provides complete device abstraction and management framework, supporting asynchronous operations, type safety, and state management. By following the best practices in this guide, you can quickly develop stable and reliable IoT devices. As the project migrates to MCP tool mode, it's recommended to consider using MCP tool framework for new features.
