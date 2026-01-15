"""
Devices module for SmartThings MCP server.
Exposes SmartThings device endpoints as MCP tools.
"""
from typing import Dict, List, Optional, Any
from .common import (
    make_request, 
    build_url, 
    build_device_url, 
    filter_none_params, 
    build_command_payload,
    BASE_URL
)

def register_tools(server_instance):
    """
    Register all device tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    print(f"Registering SmartThings tools with server: {server_instance}")
    print(f"Server type: {type(server_instance)}")
    print(f"Server dir: {dir(server_instance)}")
    
    # Try direct tool registration with proper method signature
    try:
        print("Attempting direct tool registration...")
        # The add_tool method may have different signatures in different FastMCP versions
        # Try with basic signature
        server_instance.add_tool(
            name="st_test_tool", 
            fn=lambda auth: {"result": "Test successful", "auth": auth}
        )
        print("Direct tool registration succeeded")
        
        # List all tools after registration
        print("Tools registered on server:")
        try:
            # FastMCP.list_tools appears to be a coroutine, so we can't call it directly
            # Just check if the methods exist
            if hasattr(server_instance, "list_tools"):
                tools = "Server has list_tools() method (coroutine)"
            elif hasattr(server_instance, "get_tools"):
                tools = "Server has get_tools() method"
            else:
                tools = "Unable to list tools - method not found"
            print(f"Tools: {tools}")
        except Exception as e:
            print(f"Error listing tools: {e}")
    except Exception as e:
        print(f"Error registering test tool: {e}")
    
    # Register the list_devices tool
    print("Registering list_devices tool")
    @server_instance.tool()
    def list_devices(auth: str, capability: Optional[str] = None, 
                     device_id: Optional[str] = None, 
                     location_id: Optional[str] = None,
                     room_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of devices.
        
        Args:
            auth: OAuth 2.0 bearer token
            capability: Filter by capability
            device_id: Filter by device ID
            location_id: Filter by location ID
            room_id: Filter by room ID
            
        Returns:
            List of devices matching the filters
        """
        params = filter_none_params(
            capability=capability,
            deviceId=device_id,
            locationId=location_id,
            roomId=room_id
        )
            
        return make_request(auth, "GET", build_url("devices"), params=params)
    
    @server_instance.tool()
    def get_device(auth: str, device_id: str) -> Dict[str, Any]:
        """
        Get a specific device by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to retrieve
            
        Returns:
            Device details
        """
        return make_request(auth, "GET", build_device_url(device_id))
    
    @server_instance.tool()
    def delete_device(auth: str, device_id: str) -> Dict[str, Any]:
        """
        Delete a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to delete
            
        Returns:
            Delete operation result
        """
        return make_request(auth, "DELETE", build_device_url(device_id))
    
    @server_instance.tool()
    def update_device(auth: str, device_id: str, label: str) -> Dict[str, Any]:
        """
        Update a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to update
            label: New label for the device
            
        Returns:
            Updated device details
        """
        data = {"label": label}
        return make_request(auth, "PUT", build_device_url(device_id), data=data)
    
    @server_instance.tool()
    def execute_command(auth: str, device_id: str, component: str, capability: str, 
                        command: str, arguments: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Execute a command on a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to execute command on
            component: Component ID
            capability: Capability ID
            command: Command name
            arguments: Command arguments
            
        Returns:
            Command execution result
        """
        data = build_command_payload(component, capability, command, arguments)
        return make_request(auth, "POST", build_device_url(device_id, "commands"), data=data)
    
    @server_instance.tool()
    def get_device_status(auth: str, device_id: str, 
                          component_id: Optional[str] = None, 
                          capability_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the status of a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to get status for
            component_id: Filter by component ID
            capability_id: Filter by capability ID
            
        Returns:
            Device status
        """
        params = filter_none_params(
            componentId=component_id,
            capabilityId=capability_id
        )
            
        return make_request(auth, "GET", build_device_url(device_id, "status"), params=params)
    
    @server_instance.tool()
    def get_device_components(auth: str, device_id: str) -> Dict[str, Any]:
        """
        Get the components of a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to get components for
            
        Returns:
            Device components
        """
        return make_request(auth, "GET", build_device_url(device_id, "components"))
    
    @server_instance.tool()
    def get_device_capabilities(auth: str, device_id: str, component_id: str) -> Dict[str, Any]:
        """
        Get the capabilities of a device component.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID
            component_id: Component ID to get capabilities for
            
        Returns:
            Component capabilities
        """
        return make_request(auth, "GET", build_device_url(device_id, "components", component_id, "capabilities"))
    
    @server_instance.tool()
    def get_device_health(auth: str, device_id: str) -> Dict[str, Any]:
        """
        Get the health status of a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to get health status for
            
        Returns:
            Device health status
        """
        return make_request(auth, "GET", build_device_url(device_id, "health"))
    
    @server_instance.tool()
    def get_device_presentation(auth: str, device_id: str) -> Dict[str, Any]:
        """
        Get the presentation of a device.
        
        Args:
            auth: OAuth 2.0 bearer token
            device_id: Device ID to get presentation for
            
        Returns:
            Device presentation
        """
        return make_request(auth, "GET", build_device_url(device_id, "presentation"))
