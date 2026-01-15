"""
Rooms module for SmartThings MCP server.
Exposes SmartThings room endpoints as MCP tools.
"""
from typing import Dict, List, Optional, Any
from .common import (
    make_request, 
    build_url, 
    filter_none_params,
    BASE_URL
)

def build_room_url(location_id: str, room_id: Optional[str] = None, *path_params) -> str:
    """
    Build a SmartThings API URL for rooms in a location.
    
    Args:
        location_id: The location ID
        room_id: The optional room ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete room URL string
    """
    if room_id:
        return build_url('locations', location_id, 'rooms', room_id, *path_params)
    return build_url('locations', location_id, 'rooms', *path_params)

def register_tools(server_instance):
    """
    Register all room tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    print(f"Registering SmartThings room tools with server: {server_instance}")
    
    @server_instance.tool()
    def list_rooms(auth: str, location_id: str) -> Dict[str, Any]:
        """
        Get a list of all rooms in a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to get rooms for
            
        Returns:
            List of rooms in the location
        """
        return make_request(auth, "GET", build_room_url(location_id))
    
    @server_instance.tool()
    def get_room(auth: str, location_id: str, room_id: str) -> Dict[str, Any]:
        """
        Get a specific room by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID containing the room
            room_id: Room ID to retrieve
            
        Returns:
            Room details
        """
        return make_request(auth, "GET", build_room_url(location_id, room_id))
    
    @server_instance.tool()
    def create_room(auth: str, location_id: str, name: str) -> Dict[str, Any]:
        """
        Create a room in a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID where to create room
            name: Name of the room
            
        Returns:
            Created room details
        """
        data = {"name": name}
        return make_request(auth, "POST", build_room_url(location_id), data=data)
    
    @server_instance.tool()
    def update_room(auth: str, location_id: str, room_id: str, name: str) -> Dict[str, Any]:
        """
        Update a room in a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID containing the room
            room_id: Room ID to update
            name: New name for the room
            
        Returns:
            Updated room details
        """
        data = {"name": name}
        return make_request(auth, "PUT", build_room_url(location_id, room_id), data=data)
    
    @server_instance.tool()
    def delete_room(auth: str, location_id: str, room_id: str) -> Dict[str, Any]:
        """
        Delete a room from a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID containing the room
            room_id: Room ID to delete
            
        Returns:
            Delete operation result
        """
        return make_request(auth, "DELETE", build_room_url(location_id, room_id))
