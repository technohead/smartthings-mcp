"""
Locations module for SmartThings MCP server.
Exposes SmartThings location endpoints as MCP tools.
"""
from typing import Dict, List, Optional, Any
from .common import (
    make_request, 
    build_url, 
    filter_none_params,
    BASE_URL
)

def build_location_url(location_id: str, *path_params) -> str:
    """
    Build a SmartThings API URL for a specific location.
    
    Args:
        location_id: The location ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete location URL string
    """
    return build_url('locations', location_id, *path_params)

def register_tools(server_instance):
    """
    Register all location tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    print(f"Registering SmartThings location tools with server: {server_instance}")
    
    @server_instance.tool()
    def list_locations(auth: str) -> Dict[str, Any]:
        """
        Get a list of all locations.
        
        Args:
            auth: OAuth 2.0 bearer token
            
        Returns:
            List of locations
        """
        return make_request(auth, "GET", build_url("locations"))
    
    @server_instance.tool()
    def get_location(auth: str, location_id: str) -> Dict[str, Any]:
        """
        Get a specific location by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to retrieve
            
        Returns:
            Location details
        """
        return make_request(auth, "GET", build_location_url(location_id))
    
    @server_instance.tool()
    def create_location(auth: str, name: str, country_code: str, 
                       latitude: Optional[float] = None, 
                       longitude: Optional[float] = None, 
                       region_code: Optional[str] = None, 
                       locality: Optional[str] = None, 
                       address_lines: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new location.
        
        Args:
            auth: OAuth 2.0 bearer token
            name: Name of the location
            country_code: Country code (ISO 3166-1 alpha-2 code format)
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            region_code: Region code (state/province)
            locality: City/locality
            address_lines: Address lines
            
        Returns:
            Created location details
        """
        data = {
            "name": name,
            "countryCode": country_code
        }
        
        # Add optional parameters
        if latitude is not None and longitude is not None:
            data["latitude"] = latitude
            data["longitude"] = longitude
            
        if region_code:
            data["regionCode"] = region_code
            
        if locality:
            data["locality"] = locality
            
        if address_lines:
            data["addressLines"] = address_lines
            
        return make_request(auth, "POST", build_url("locations"), data=data)
    
    @server_instance.tool()
    def update_location(auth: str, location_id: str, name: str, 
                       country_code: Optional[str] = None, 
                       latitude: Optional[float] = None, 
                       longitude: Optional[float] = None, 
                       region_code: Optional[str] = None, 
                       locality: Optional[str] = None, 
                       address_lines: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update an existing location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to update
            name: Name of the location
            country_code: Country code (ISO 3166-1 alpha-2 code format)
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            region_code: Region code (state/province)
            locality: City/locality
            address_lines: Address lines
            
        Returns:
            Updated location details
        """
        data = {"name": name}
        
        # Add optional parameters
        if country_code:
            data["countryCode"] = country_code
            
        if latitude is not None and longitude is not None:
            data["latitude"] = latitude
            data["longitude"] = longitude
            
        if region_code:
            data["regionCode"] = region_code
            
        if locality:
            data["locality"] = locality
            
        if address_lines:
            data["addressLines"] = address_lines
            
        return make_request(auth, "PUT", build_location_url(location_id), data=data)
    
    @server_instance.tool()
    def delete_location(auth: str, location_id: str) -> Dict[str, Any]:
        """
        Delete a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to delete
            
        Returns:
            Delete operation result
        """
        return make_request(auth, "DELETE", build_location_url(location_id))
    
    @server_instance.tool()
    def get_location_rooms(auth: str, location_id: str) -> Dict[str, Any]:
        """
        Get rooms in a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to get rooms for
            
        Returns:
            List of rooms in the location
        """
        return make_request(auth, "GET", build_location_url(location_id, "rooms"))
    
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
        return make_request(auth, "POST", build_location_url(location_id, "rooms"), data=data)
    
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
        return make_request(auth, "PUT", build_location_url(location_id, "rooms", room_id), data=data)
    
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
        return make_request(auth, "DELETE", build_location_url(location_id, "rooms", room_id))
