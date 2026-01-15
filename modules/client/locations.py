"""
Locations module for SmartThingsMCP Client
"""
from typing import Dict, Any, Optional, List


class LocationsMixin:
    """
    Mixin class for location-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def list_locations(self) -> Dict[str, Any]:
        """
        Get a list of all locations.
        
        Returns:
            List of locations
        """
        return await self.call_tool("list_locations")
    
    async def get_location(self, location_id: str) -> Dict[str, Any]:
        """
        Get a specific location by ID.
        
        Args:
            location_id: Location ID to retrieve
            
        Returns:
            Location details
        """
        return await self.call_tool("get_location", location_id=location_id)
    
    async def create_location(self, name: str, country_code: str, 
                           latitude: Optional[float] = None, 
                           longitude: Optional[float] = None, 
                           region_code: Optional[str] = None, 
                           locality: Optional[str] = None, 
                           address_lines: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new location.
        
        Args:
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
        args = {
            "name": name,
            "country_code": country_code
        }
        
        if latitude is not None and longitude is not None:
            args["latitude"] = latitude
            args["longitude"] = longitude
            
        if region_code:
            args["region_code"] = region_code
            
        if locality:
            args["locality"] = locality
            
        if address_lines:
            args["address_lines"] = address_lines
            
        return await self.call_tool("create_location", **args)
    
    async def update_location(self, location_id: str, name: str, 
                           country_code: Optional[str] = None, 
                           latitude: Optional[float] = None, 
                           longitude: Optional[float] = None, 
                           region_code: Optional[str] = None, 
                           locality: Optional[str] = None, 
                           address_lines: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update an existing location.
        
        Args:
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
        args = {
            "location_id": location_id,
            "name": name
        }
        
        if country_code:
            args["country_code"] = country_code
            
        if latitude is not None and longitude is not None:
            args["latitude"] = latitude
            args["longitude"] = longitude
            
        if region_code:
            args["region_code"] = region_code
            
        if locality:
            args["locality"] = locality
            
        if address_lines:
            args["address_lines"] = address_lines
            
        return await self.call_tool("update_location", **args)
    
    async def delete_location(self, location_id: str) -> Dict[str, Any]:
        """
        Delete a location.
        
        Args:
            location_id: Location ID to delete
            
        Returns:
            Delete operation result
        """
        return await self.call_tool("delete_location", location_id=location_id)
