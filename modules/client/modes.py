"""
Modes module for SmartThingsMCP Client
"""
from typing import Dict, Any


class ModesMixin:
    """
    Mixin class for mode-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def list_modes(self, location_id: str) -> Dict[str, Any]:
        """
        List all modes for a location.
        
        Args:
            location_id: Location ID to get modes for
            
        Returns:
            List of modes for the location
        """
        return await self.call_tool("list_modes", location_id=location_id)
    
    async def get_mode(self, location_id: str, mode_id: str) -> Dict[str, Any]:
        """
        Get a specific mode by ID.
        
        Args:
            location_id: Location ID containing the mode
            mode_id: Mode ID to retrieve
            
        Returns:
            Mode details
        """
        return await self.call_tool("get_mode", location_id=location_id, mode_id=mode_id)
    
    async def get_current_mode(self, location_id: str) -> Dict[str, Any]:
        """
        Get the current mode for a location.
        
        Args:
            location_id: Location ID to get current mode for
            
        Returns:
            Current mode details
        """
        return await self.call_tool("get_current_mode", location_id=location_id)
    
    async def set_mode(self, location_id: str, mode_id: str) -> Dict[str, Any]:
        """
        Set the current mode for a location.
        
        Args:
            location_id: Location ID to set mode for
            mode_id: Mode ID to set as current
            
        Returns:
            Mode change result
        """
        return await self.call_tool("set_mode", location_id=location_id, mode_id=mode_id)
