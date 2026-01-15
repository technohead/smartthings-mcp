"""
Devices module for SmartThingsMCP Client
"""
from typing import Dict, Any, Optional, List


class DevicesMixin:
    """
    Mixin class for device-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def list_devices(self, capability: Optional[str] = None, device_id: Optional[str] = None,
                    location_id: Optional[str] = None, room_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of devices.
        
        Args:
            capability: Filter by capability
            device_id: Filter by device ID
            location_id: Filter by location ID
            room_id: Filter by room ID
            
        Returns:
            List of devices matching the filters
        """
        args = {}
        if capability:
            args["capability"] = capability
        if device_id:
            args["device_id"] = device_id
        if location_id:
            args["location_id"] = location_id
        if room_id:
            args["room_id"] = room_id
            
        return await self.call_tool("list_devices", **args)
    
    async def get_device(self, device_id: str) -> Dict[str, Any]:
        """
        Get a specific device by ID.
        
        Args:
            device_id: Device ID to retrieve
            
        Returns:
            Device details
        """
        return await self.call_tool("get_device", device_id=device_id)
    
    async def delete_device(self, device_id: str) -> Dict[str, Any]:
        """
        Delete a device.
        
        Args:
            device_id: Device ID to delete
            
        Returns:
            Delete operation result
        """
        return await self.call_tool("delete_device", device_id=device_id)
    
    async def update_device(self, device_id: str, label: str) -> Dict[str, Any]:
        """
        Update a device.
        
        Args:
            device_id: Device ID to update
            label: New label for the device
            
        Returns:
            Updated device details
        """
        return await self.call_tool("update_device", device_id=device_id, label=label)
    
    async def execute_command(self, device_id: str, component: str, capability: str, 
                     command: str, arguments: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Execute a command on a device.
        
        Args:
            device_id: Device ID to execute command on
            component: Component ID
            capability: Capability ID
            command: Command name
            arguments: Command arguments
            
        Returns:
            Command execution result
        """
        return await self.call_tool("execute_command", device_id=device_id, component=component,
                            capability=capability, command=command, arguments=arguments or [])
    
    async def get_device_status(self, device_id: str, component_id: Optional[str] = None,
                       capability_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the status of a device.
        
        Args:
            device_id: Device ID to get status for
            component_id: Filter by component ID
            capability_id: Filter by capability ID
            
        Returns:
            Device status
        """
        args = {"device_id": device_id}
        if component_id:
            args["component_id"] = component_id
        if capability_id:
            args["capability_id"] = capability_id
            
        return await self.call_tool("get_device_status", **args)
    
    async def get_device_components(self, device_id: str) -> Dict[str, Any]:
        """
        Get the components of a device.
        
        Args:
            device_id: Device ID to get components for
            
        Returns:
            Device components
        """
        return await self.call_tool("get_device_components", device_id=device_id)
    
    async def get_device_capabilities(self, device_id: str, component_id: str) -> Dict[str, Any]:
        """
        Get the capabilities of a device component.
        
        Args:
            device_id: Device ID
            component_id: Component ID to get capabilities for
            
        Returns:
            Component capabilities
        """
        return await self.call_tool("get_device_capabilities", device_id=device_id, component_id=component_id)
    
    async def get_device_health(self, device_id: str) -> Dict[str, Any]:
        """
        Get the health status of a device.
        
        Args:
            device_id: Device ID to get health status for
            
        Returns:
            Device health status
        """
        return await self.call_tool("get_device_health", device_id=device_id)
