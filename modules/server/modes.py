"""
Modes module for SmartThings MCP server.
Exposes SmartThings modes endpoints as MCP tools.

Authentication Requirements:
- Requires a valid OAuth 2.0 bearer token with appropriate permissions.
- The token must have the following scopes: 'r:locations:*' for read operations and 'w:locations:*' for write operations.
- For location-specific operations like mode management, the token must have access to the specific location.

Common Authentication Issues:
- 401 Unauthorized: Token is missing, invalid, expired, or lacks required permissions.
- 403 Forbidden: Token doesn't have access to the specified location or resource.

See https://developer.smartthings.com/docs/api/public#section/Authentication for more details on authentication.
"""
import sys
import logging
from typing import Dict, Any
from .common import (
    make_request, 
    build_url, 
    filter_none_params,
    BASE_URL
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_mode_url(location_id: str, *path_params) -> str:
    """
    Build a SmartThings API URL for location modes.
    
    Args:
        location_id: The location ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete mode URL string
    """
    return build_url('locations', location_id, 'modes', *path_params)

def register_tools(server_instance):
    """
    Register all mode tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    print(f"Registering SmartThings Mode tools with server: {server_instance}")
    
    @server_instance.tool()
    def list_modes(auth: str, location_id: str) -> Dict[str, Any]:
        """
        List all modes for a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to get modes for
            
        Returns:
            List of modes for the location
        """
        logger.info(f"Listing modes for location: {location_id}")
        logger.info(f"Auth token prefix: {auth[:10]}...")
        url = build_mode_url(location_id)
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url)
            logger.info("Successfully retrieved modes")
            return result
        except Exception as e:
            logger.error(f"Error listing modes: {e}")
            raise
    
    @server_instance.tool()
    def get_mode(auth: str, location_id: str, mode_id: str) -> Dict[str, Any]:
        """
        Get a specific mode by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID containing the mode
            mode_id: Mode ID to retrieve
            
        Returns:
            Mode details
        """
        logger.info(f"Getting mode {mode_id} for location: {location_id}")
        url = build_mode_url(location_id, mode_id)
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url)
            logger.info("Successfully retrieved mode")
            return result
        except Exception as e:
            logger.error(f"Error getting mode: {e}")
            raise
    
    @server_instance.tool()
    def get_current_mode(auth: str, location_id: str) -> Dict[str, Any]:
        """
        Get the current mode for a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to get current mode for
            
        Returns:
            Current mode details
        """
        logger.info(f"Getting current mode for location: {location_id}")
        url = build_url('locations', location_id, 'modes', 'current')
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url)
            logger.info("Successfully retrieved current mode")
            return result
        except Exception as e:
            logger.error(f"Error getting current mode: {e}")
            raise
    
    @server_instance.tool()
    def set_mode(auth: str, location_id: str, mode_id: str) -> Dict[str, Any]:
        """
        Set the current mode for a location.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID to set mode for
            mode_id: Mode ID to set as current
            
        Returns:
            Mode change result
        """
        logger.info(f"Setting mode {mode_id} for location: {location_id}")
        url = build_url('locations', location_id, 'modes/current')
        data = {"modeId": mode_id}
        logger.info(f"Request URL: {url}")
        logger.info(f"Request data: {data}")
        try:
            result = make_request(auth, "PUT", url, data=data)
            logger.info("Successfully set mode")
            return result
        except Exception as e:
            logger.error(f"Error setting mode: {e}")
            raise
