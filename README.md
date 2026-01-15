# SmartThingsMCP Server and Client

A comprehensive FastMCP 2.0 server and client for interacting with SmartThings devices, locations, rooms, modes, scenes, and automation rules through the SmartThings API.

## Overview

SmartThingsMCP provides:
- **FastMCP 2.0 Server**: Exposes SmartThings API functionality as MCP tools
- **Smart Client**: Python client with intelligent caching, async support, and multiple transport options
- **Modular Architecture**: Organized by functionality (devices, locations, rooms, modes, scenes, rules)
- **Two-Level Caching**: Both client and server-side caching for optimal performance
- **Multiple Transports**: HTTP, SSE (Server-Sent Events), and STDIO support
- **OAuth 2.0 Authentication**: Secure token-based authentication with SmartThings API

## Components

### Server
- **SmartThingsMCPServer.py**: FastMCP 2.0 server exposing SmartThings API as MCP tools
- **modules/server/**: Server tool implementations
  - `devices.py`: Device management tools (list, get, update, delete, execute commands, etc.)
  - `locations.py`: Location management tools (create, read, update, delete locations and rooms)
  - `rooms.py`: Room management tools (list, create, update, delete rooms)
  - `modes.py`: Mode management tools (list, get, set location modes)
  - `scenes.py`: Scene management tools (list, get, execute, create, update, delete scenes)
  - `rules.py`: Automation rule tools (list, get, create, update, delete, execute rules)
  - `structure_tools.py`: Structure generation tools for LLM integration
  - `common.py`: Shared utilities for API requests, URL building, and parameter filtering

### Client
- **SmartThingsMCPClient.py**: CLI for interacting with the MCP server
- **modules/client/**: Client implementation
  - `main.py`: Main SmartThingsMCPClient class combining all mixins
  - `base.py`: BaseClient with transport handling and tool invocation
  - `cache.py`: CacheMixin with LRU caching, TTL management, and cache statistics
  - `devices.py`: DevicesMixin with device operation methods
  - `locations.py`: LocationsMixin with location and room methods
  - `rooms.py`: RoomsMixin with room-specific methods
  - `modes.py`: ModesMixin with mode management methods
  - `rules.py`: RulesMixin with rule management methods
  - `scenes.py`: ScenesMixin with scene management methods
  - `utils.py`: Utility functions for tool conversion and action execution
  - `utils_ext.py`: Extended utilities (note: currently unused)

## API Endpoints

SmartThingsMCP exposes the following API endpoints as MCP tools:

### Device Management

- **list_devices**: Get a list of all devices (supports filtering by capability, location, room, or device ID)
- **get_device**: Get details of a specific device
- **update_device**: Update a device's label
- **delete_device**: Delete a device
- **execute_command**: Execute a command on a device component
- **get_device_status**: Get the current status of a device
- **get_device_components**: Get all components of a device
- **get_device_capabilities**: Get capabilities of a device component
- **get_device_health**: Get the health/connectivity status of a device
- **get_device_presentation**: Get the UI presentation details of a device

### Location Management

- **list_locations**: Get a list of all locations
- **get_location**: Get details of a specific location
- **create_location**: Create a new location with coordinates and address information
- **update_location**: Update location details (name, coordinates, address)
- **delete_location**: Delete a location
- **get_location_rooms**: Get all rooms in a location (convenience method)

### Room Management

- **list_rooms**: Get all rooms in a location
- **get_room**: Get details of a specific room
- **create_room**: Create a new room in a location
- **update_room**: Update a room's name
- **delete_room**: Delete a room from a location

### Mode Management

- **list_modes**: Get all available modes for a location
- **get_mode**: Get details of a specific mode
- **get_current_mode**: Get the currently active mode for a location
- **set_mode**: Change the current mode for a location

### Scene Management

- **list_scenes**: Get all scenes (optionally filtered by location)
- **get_scene**: Get details of a specific scene
- **execute_scene**: Execute/run a scene
- **create_scene**: Create a new scene with actions and visual properties
- **update_scene**: Update an existing scene (name, icon, colors, actions)
- **delete_scene**: Delete a scene

### Rule Management

- **list_rules**: Get all automation rules (optionally filtered by location)
- **get_rule**: Get details of a specific rule
- **create_rule**: Create a new automation rule with conditions and actions
- **update_rule**: Update an existing rule (name, triggers, actions, enabled state)
- **delete_rule**: Delete an automation rule
- **execute_rule**: Manually trigger execution of a rule

## Features

### Intelligent Caching

Both the SmartThingsMCPClient and SmartThingsMCPServer include comprehensive caching to improve performance:

#### Client-Side Caching
The SmartThingsMCPClient provides:
- **Automatic caching** of read-only operations (list_devices, list_locations, etc.)
- **TTL-based expiration** (default: 5 minutes, configurable)
- **Smart cache invalidation** on write operations (execute_command, update_device, etc.)
- **LRU eviction** when cache is full
- **Cache statistics** tracking (hits, misses, hit rate)
- **Green visual feedback**: `✓ Cache hit: list_locations`

See [CACHING.md](./CACHING.md) for detailed documentation.

#### Server-Side Caching
The SmartThingsMCPServer provides:
- **Automatic caching** of all GET requests to SmartThings API
- **TTL-based expiration** (default: 5 minutes)
- **Full cache invalidation** on write operations (POST, PUT, DELETE)
- **LRU eviction** when cache is full
- **Cache statistics** tracking
- **Green visual feedback**: `✓ Server cache hit: GET devices`

See [SERVER_CACHING.md](./SERVER_CACHING.md) for detailed documentation.

**Two-Level Caching:**
When both client and server caching are active, you get maximum performance with two layers of caching!

**Performance Benefits:**
- 60-80% reduction in API calls
- 5-10x faster response times for cached data
- Lower rate limit usage

### Rule Management

The server provides comprehensive rule management capabilities:

- **list_rules**: List all automation rules for a location
- **get_rule**: Get details of a specific rule
- **create_rule**: Create a new automation rule with conditions and actions
- **update_rule**: Update an existing rule (name, triggers, actions, or enabled state)
- **delete_rule**: Delete a rule
- **execute_rule**: Manually execute a rule

**Enable/Disable Rules:**
```python
# Disable a rule
client.update_rule(auth=token, rule_id="abc-123", enabled=False)

# Enable a rule
client.update_rule(auth=token, rule_id="abc-123", enabled=True)
```

The `enabled` parameter was added in December 2025 to support toggling rule state without deleting the rule.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or another Python package manager

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Required packages:**
- `fastmcp>=2.0.0`: FastMCP 2.0 framework for MCP server/client
- `requests>=2.28.0`: HTTP library for SmartThings API calls

2. Obtain a SmartThings API Token:
   - Visit [SmartThings Developer Portal](https://developer.smartthings.com/)
   - Create a new API token with the following scopes:
     - `r:devices:*` (read devices)
     - `w:devices:*` (control devices)
     - `r:locations:*` (read locations)
     - `w:locations:*` (create/update locations)
     - `r:rules:*` (read rules, requires Enterprise account)
     - `w:rules:*` (write rules, requires Enterprise account)
     - `r:scenes:*` (read scenes)
     - `x:scenes:*` (execute scenes)

## Authentication

SmartThingsMCP uses OAuth 2.0 bearer tokens for authentication with the SmartThings API.

### Token Requirements
- Must be a valid SmartThings API token (OAuth 2.0 bearer token)
- Token must have appropriate scopes for the operations you want to perform
- Token never expires when obtained from the SmartThings Developer Portal
- Keep your token secure and never commit it to version control

### Common Authentication Issues

**401 Unauthorized:**
```
Error calling tool list_devices: 401 Unauthorized
```
- Verify the token is valid and not expired
- Check that the token has been generated from SmartThings Developer Portal
- Ensure you're passing the token with the `--auth` flag

**403 Forbidden:**
```
Error calling tool list_devices: 403 Forbidden
```
- The token exists but lacks required scopes
- Some features (like Rules) require an Enterprise SmartThings account
- Grant additional scopes to the token in SmartThings Developer Portal

### Scopes Required by Feature

| Feature | Required Scopes |
|---------|-----------------|
| List/Get Devices | `r:devices:*` |
| Control Devices | `w:devices:*` |
| List/Get Locations | `r:locations:*` |
| Create/Update/Delete Locations | `w:locations:*` |
| List/Get Scenes | `r:scenes:*` |
| Execute Scenes | `x:scenes:*` |
| Create/Update/Delete Scenes | `w:scenes:*` |
| List/Get Rules | `r:rules:*` |
| Create/Update/Delete Rules | `w:rules:*` |
| List/Get/Set Modes | `r:locations:*` |

## Getting Started

### Starting the Server

1. Start the SmartThingsMCP server:

```bash
# Start with HTTP transport (default) on port 8000
python SmartThingsMCPServer.py

# Custom port
python SmartThingsMCPServer.py -port 9000

# Using SSE transport
python SmartThingsMCPServer.py -transport sse

# Using STDIO transport
python SmartThingsMCPServer.py -transport stdio

# With auth token override (if needed)
python SmartThingsMCPServer.py -auth YOUR_TOKEN
```

### Using the Command-Line Client

The SmartThingsMCPClient.py provides a CLI interface:

```bash
# List available tools
python SmartThingsMCPClient.py --transport http --port 8000 --action list_tools

# List all devices (requires auth token)
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_devices

# List devices with pretty-printed output
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_devices --pretty

# Get a specific device
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action get_device --params '{"device_id": "DEVICE_ID"}'

# Get device status
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action get_device_status --params '{"device_id": "DEVICE_ID"}'

# Execute a device command
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action execute_command --params '{
  "device_id": "DEVICE_ID",
  "component": "main",
  "capability": "switch",
  "command": "on"
}'

# List all locations
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_locations

# List all scenes
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_scenes

# Execute a scene
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action execute_scene --params '{"scene_id": "SCENE_ID"}'

# Create a new location
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action create_location --params '{
  "name": "Office",
  "country_code": "US",
  "region_code": "CA",
  "locality": "San Francisco"
}'

# List all modes for a location
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_modes --params '{"location_id": "LOCATION_ID"}'

# Set mode for a location
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action set_mode --params '{
  "location_id": "LOCATION_ID",
  "mode_id": "MODE_ID"
}'

# List all rules
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action list_rules

# Enable/disable a rule
python SmartThingsMCPClient.py --auth YOUR_TOKEN --action update_rule --params '{
  "rule_id": "RULE_ID",
  "enabled": false
}'
```

### Client Options

```
--host: MCP server host (default: localhost)
--port: MCP server port (default: 8000)
--auth: SmartThings API authentication token (required for most operations)
--transport: Transport type - http, sse, or stdio (default: http)
--action: Action/tool to execute (required)
--params: JSON string of parameters for the action (default: {})
--pretty: Pretty-print JSON output (flag)
```

### Using Python Client Programmatically

```python
import asyncio
from modules.client.main import SmartThingsMCPClient

async def main():
    # Create client with caching enabled (default)
    client = SmartThingsMCPClient(
        host="localhost",
        port=8000,
        auth_token="YOUR_TOKEN",
        transport="http",
        enable_cache=True,        # Enable automatic caching
        cache_ttl=300,            # Cache for 5 minutes
        max_cache_size=1000       # Store up to 1000 cache entries
    )
    
    # List all devices
    devices = await client.list_devices(auth="YOUR_TOKEN")
    print(f"Found {len(devices['items'])} devices")
    
    # Get specific device
    device = await client.get_device(auth="YOUR_TOKEN", device_id="DEVICE_ID")
    print(f"Device: {device['label']}")
    
    # Execute device command
    result = await client.execute_command(
        auth="YOUR_TOKEN",
        device_id="DEVICE_ID",
        component="main",
        capability="switch",
        command="on"
    )
    
    # List locations
    locations = await client.list_locations(auth="YOUR_TOKEN")
    for loc in locations['items']:
        print(f"Location: {loc['name']}")
    
    # List and execute scenes
    scenes = await client.list_scenes(auth="YOUR_TOKEN")
    if scenes['items']:
        scene_id = scenes['items'][0]['sceneId']
        await client.execute_scene(auth="YOUR_TOKEN", scene_id=scene_id)
    
    # Manage rules
    rules = await client.list_rules(auth="YOUR_TOKEN")
    for rule in rules['items']:
        print(f"Rule: {rule['name']} - Enabled: {rule.get('enabled', True)}")
    
    # Check cache statistics (when caching is enabled)
    if hasattr(client, 'get_cache_stats'):
        stats = client.get_cache_stats()
        print(f"Cache hits: {stats['hits']}, misses: {stats['misses']}")

if __name__ == "__main__":
    asyncio.run(main())
```

# Troubleshooting

## Transport Configuration

SmartThingsMCP supports three transport mechanisms for client-server communication:

### HTTP Transport (Recommended for most use cases)
- **Default port**: 8000
- **URL pattern**: `http://localhost:8000/mcp`
- **Best for**: External integrations, LLM tools, web services
- **Advantages**: 
  - Simple HTTP/REST interface
  - Easy to debug with standard tools
  - Compatible with most firewalls
  - Stateless connections

```bash
# Server
python SmartThingsMCPServer.py -transport http -port 8000

# Client
python SmartThingsMCPClient.py --transport http --port 8000
```

### SSE Transport (Server-Sent Events)
- **Default port**: 8000
- **URL pattern**: `http://localhost:8000/sse`
- **Best for**: Real-time updates, event streaming, server push
- **Advantages**:
  - Bidirectional communication
  - Event-driven architecture
  - Lower latency for updates

```bash
# Server
python SmartThingsMCPServer.py -transport sse -port 8000

# Client
python SmartThingsMCPClient.py --transport sse --port 8000
```

### STDIO Transport (Direct integration)
- **No network overhead**
- **Best for**: Direct Python integration, embedded systems
- **Advantages**:
  - No port/network configuration needed
  - Direct process communication
  - Lowest latency

```bash
# Server (runs in foreground)
python SmartThingsMCPServer.py -transport stdio

# Client
python SmartThingsMCPClient.py --transport stdio
```

## Client Configuration

### Cache Configuration

The SmartThingsMCPClient includes intelligent caching with full control:

```python
client = SmartThingsMCPClient(
    host="localhost",
    port=8000,
    auth_token="YOUR_TOKEN",
    enable_cache=True,        # Enable caching
    cache_ttl=300,            # TTL in seconds (default: 5 min)
    max_cache_size=1000       # Max entries (default: 1000)
)

# Get cache statistics
stats = client.get_cache_stats()
print(f"Hit rate: {stats['hit_rate']:.2%}")

# Clear cache manually
client.clear_cache()
```

**Cacheable Operations** (automatic caching):
- list_devices
- get_device
- list_locations
- get_location
- list_rooms
- get_room
- list_modes
- get_mode
- get_current_mode
- list_scenes
- get_scene
- list_rules
- get_rule

**Cache-Invalidating Operations** (automatic cache clearing):
- update_device
- delete_device
- execute_command
- create_location
- update_location
- delete_location
- create_room
- update_room
- delete_room
- set_mode
- create_scene
- update_scene
- delete_scene
- create_rule
- update_rule
- delete_rule
- execute_rule
- execute_scene

### Logging

SmartThingsMCP uses Python's standard logging module:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('smartthings_mcp')

# Create client - will now output detailed logs
client = SmartThingsMCPClient(...)
```

**Log levels:**
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

## Common Errors and Solutions

## Common Errors and Solutions

### Connection Errors

**Error: `Client failed to connect: Session terminated`**

```
Error calling tool list_devices: Client failed to connect: Session terminated
```

**Causes and solutions:**
- Server is not running: Start the server with `python SmartThingsMCPServer.py`
- Wrong transport type: Ensure client and server use same transport (http, sse, or stdio)
- Wrong port: Verify port matches between client and server
- Wrong host: Check hostname/IP address is correct
- Network/firewall: Ensure port is open and accessible

**Debugging:**
```bash
# Check if server is running on expected port
netstat -tuln | grep 8000

# Test HTTP connectivity
curl http://localhost:8000/mcp

# View server logs
python SmartThingsMCPServer.py 2>&1 | head -20
```

### Authentication Errors

**Error: `1 validation error for list_devicesArguments: auth: Field required`**

```
Error executing tool list_devices: 1 validation error for list_devicesArguments
auth: Field required
```

**Solutions:**
- Provide auth token with `--auth YOUR_TOKEN` flag
- Ensure token is valid: verify in SmartThings Developer Portal
- Check token has not expired
- Verify token has required scopes

**Example:**
```bash
python SmartThingsMCPClient.py --auth "YOUR_VALID_TOKEN" --action list_devices
```

**Error: `401 Unauthorized`**

```
Error calling tool list_devices: 401 Unauthorized
```

**Solutions:**
- Token is invalid or expired
- Token format is incorrect (must be OAuth 2.0 bearer token)
- Generate new token from SmartThings Developer Portal

**Error: `403 Forbidden`**

```
Error calling tool create_rule: 403 Forbidden - Access Denied
```

**Solutions:**
- Token lacks required scopes for the operation
- SmartThings account doesn't have access to feature (e.g., Rules API requires Enterprise)
- Grant additional scopes in SmartThings Developer Portal

### API Response Errors

**Error: `Device not found`**

```json
{
  "error": "Device not found",
  "message": "No device found with ID: invalid-id"
}
```

**Solutions:**
- Device ID doesn't exist
- Device has been deleted
- List devices first to get valid IDs: `list_devices` action

**Error: `Invalid component or capability`**

```json
{
  "error": "Component not found",
  "message": "Component 'main' not found on device"
}
```

**Solutions:**
- Check valid components: Use `get_device_components` to list available components
- Check valid capabilities: Use `get_device_capabilities` with correct component_id
- Device doesn't support the command you're trying to execute

### Rate Limiting

**Error: `429 Too Many Requests`**

```
Error calling tool list_devices: 429 Too Many Requests
```

**Solutions:**
- SmartThings API rate limit exceeded
- **Enable caching** to reduce API calls (enabled by default)
- Increase cache TTL to keep data longer
- Implement request throttling in your code

**Check cache effectiveness:**
```python
stats = client.get_cache_stats()
print(f"Cache hits: {stats['hits']}")
print(f"Cache misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']:.2%}")
```

### Cache Issues

**Problem: Stale data in cache**

**Solutions:**
- Reduce cache TTL: `cache_ttl=60` (1 minute)
- Manually clear cache: `client.clear_cache()`
- Disable cache if data must be real-time: `enable_cache=False`

**Problem: Cache causing high memory usage**

**Solutions:**
- Reduce max cache size: `max_cache_size=100`
- Reduce cache TTL to expire entries sooner
- Periodically clear cache: `client.clear_cache()`

## Advanced Usage

### Custom Tool Implementation

You can extend SmartThingsMCP with custom tools by modifying the server modules:

```python
# In modules/server/devices.py, add:
@server_instance.tool()
def custom_device_operation(auth: str, device_id: str) -> Dict[str, Any]:
    """Your custom operation description"""
    # Your implementation here
    return make_request(auth, "GET", build_device_url(device_id))
```

### Integration with LLMs

SmartThingsMCP tools are designed to work with Language Models:

```python
# Get formatted tool descriptions for LLM
tools = await client.list_tools()
tool_descriptions = [
    {
        "name": tool["name"],
        "description": tool["description"],
        "params": tool["parameters"]
    }
    for tool in tools
]
```

### Error Handling

```python
import asyncio

async def safe_device_operation():
    client = SmartThingsMCPClient(
        host="localhost",
        port=8000,
        auth_token="YOUR_TOKEN"
    )
    
    try:
        result = await client.get_device(
            auth="YOUR_TOKEN",
            device_id="DEVICE_ID"
        )
        return result
    except ValueError as e:
        print(f"Invalid input: {e}")
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        
asyncio.run(safe_device_operation())
```

### Performance Optimization

1. **Enable caching** (default: enabled):
   ```python
   # Already enabled by default
   client = SmartThingsMCPClient(enable_cache=True)
   ```

2. **Adjust cache TTL** for your use case:
   ```python
   # More frequent updates needed
   client = SmartThingsMCPClient(cache_ttl=60)  # 1 minute
   
   # Stable data, longer TTL
   client = SmartThingsMCPClient(cache_ttl=900)  # 15 minutes
   ```

3. **Use appropriate transport**:
   - HTTP: Best for most scenarios
   - STDIO: Best latency for local integration
   - SSE: Best for real-time updates

4. **Batch operations**:
   ```python
   # Get all data at once rather than in loops
   devices = await client.list_devices(auth=token)
   for device in devices['items']:
       # Use data from the single list_devices call
       # Don't call get_device for each one if not needed
   ```

### API Response Format

All API responses follow a consistent structure:

**Success response:**
```json
{
  "items": [...],
  "pageProperties": {
    "currentPage": 1,
    "pageSize": 50,
    "totalCount": 100
  }
}
```

**Single item response:**
```json
{
  "id": "unique-id",
  "label": "Device Name",
  "deviceTypeId": "type-id"
}
```

**Error response:**
```json
{
  "requestId": "request-id",
  "errors": [
    {
      "code": "INVALID_PARAMETER",
      "message": "Detailed error message"
    }
  ]
}
```

## Example Scripts

### Monitor Device Status

```python
import asyncio
from modules.client.main import SmartThingsMCPClient

async def monitor_devices(token):
    client = SmartThingsMCPClient(auth_token=token)
    
    # Get all devices
    devices = await client.list_devices(auth=token)
    
    for device in devices['items']:
        try:
            status = await client.get_device_status(
                auth=token,
                device_id=device['deviceId']
            )
            print(f"{device['label']}: {status}")
        except Exception as e:
            print(f"Error getting status for {device['label']}: {e}")

asyncio.run(monitor_devices("YOUR_TOKEN"))
```

### Control Multiple Devices

```python
import asyncio
from modules.client.main import SmartThingsMCPClient

async def control_devices(token, device_ids, command):
    client = SmartThingsMCPClient(auth_token=token)
    
    for device_id in device_ids:
        try:
            result = await client.execute_command(
                auth=token,
                device_id=device_id,
                component="main",
                capability="switch",
                command=command
            )
            print(f"Device {device_id}: {result}")
        except Exception as e:
            print(f"Error controlling {device_id}: {e}")

asyncio.run(control_devices("YOUR_TOKEN", ["device1", "device2"], "on"))
```

### Scene Execution

```python
import asyncio
from modules.client.main import SmartThingsMCPClient

async def execute_morning_routine(token):
    client = SmartThingsMCPClient(auth_token=token)
    
    # Get morning scene
    scenes = await client.list_scenes(auth=token)
    morning_scene = next(
        (s for s in scenes['items'] if 'morning' in s.get('sceneName', '').lower()),
        None
    )
    
    if morning_scene:
        result = await client.execute_scene(
            auth=token,
            scene_id=morning_scene['sceneId']
        )
        print(f"Executed scene: {result}")

asyncio.run(execute_morning_routine("YOUR_TOKEN"))
```

## Environment Variables

You can optionally use environment variables for common settings:

```bash
export SMARTTHINGS_TOKEN="your-token-here"
export MCP_SERVER_HOST="localhost"
export MCP_SERVER_PORT="8000"
export MCP_TRANSPORT="http"
```

## API Reference

Complete API reference is available through the MCP tools system. List all available tools:

```bash
python SmartThingsMCPClient.py --action list_tools --pretty
```

This will display all available tools with their parameters and descriptions.

## Contributing

When extending SmartThingsMCP:

1. Follow the existing module structure
2. Add tools to appropriate module (devices.py, locations.py, etc.)
3. Include proper docstrings with parameter and return descriptions
4. Test with the client
5. Update README.md with new tool documentation

## License

See LICENSE file for license information.
