"""
Rooms module for SmartThingsMCP Client
"""
from typing import Dict, Any


class RoomsMixin:
    """
    Mixin class for room-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def get_location_rooms(self, location_id: str) -> Dict[str, Any]:
        """
        Get rooms in a location.
        
        Args:
            location_id: Location ID to get rooms for
            
        Returns:
            List of rooms in the location
        """
        return await self.call_tool("get_location_rooms", location_id=location_id)
        
    async def get_room(self, location_id: str, room_id: str) -> Dict[str, Any]:
        """
        Get a specific room by ID.
        
        Args:
            location_id: Location ID containing the room
            room_id: Room ID to retrieve
            
        Returns:
            Room details
        """
        return await self.call_tool("get_room", location_id=location_id, room_id=room_id)
    
    async def create_room(self, location_id: str, name: str) -> Dict[str, Any]:
        """
        Create a room in a location.
        
        Args:
            location_id: Location ID where to create room
            name: Name of the room
            
        Returns:
            Created room details
        """
        return await self.call_tool("create_room", location_id=location_id, name=name)
    
    async def update_room(self, location_id: str, room_id: str, name: str) -> Dict[str, Any]:
        """
        Update a room in a location.
        
        Args:
            location_id: Location ID containing the room
            room_id: Room ID to update
            name: New name for the room
            
        Returns:
            Updated room details
        """
        return await self.call_tool("update_room", location_id=location_id, room_id=room_id, name=name)
    
    async def delete_room(self, location_id: str, room_id: str) -> Dict[str, Any]:
        """
        Delete a room from a location.
        
        Args:
            location_id: Location ID containing the room
            room_id: Room ID to delete
            
        Returns:
            Delete operation result
        """
        return await self.call_tool("delete_room", location_id=location_id, room_id=room_id)
