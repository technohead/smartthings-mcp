"""
Scenes module for SmartThings MCP server.
Exposes SmartThings scenes endpoints as MCP tools.

Authentication Requirements:
- Requires a valid OAuth 2.0 bearer token with appropriate permissions.
- The token must have the following scopes: 'r:scenes:*' for read operations and 'x:scenes:*' for executing scenes.
- For location-specific operations, the token must have access to the specific location.
"""
import logging
from typing import Dict, Any, Optional, List
from .common import (
    make_request, 
    build_url, 
    filter_none_params,
    BASE_URL
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_scene_url(scene_id: str = None, *path_params) -> str:
    """
    Build a SmartThings API URL for scenes.
    
    Args:
        scene_id: Optional scene ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete scene URL string
    """
    if scene_id:
        return build_url('scenes', scene_id, *path_params)
    else:
        return build_url('scenes', *path_params)

def register_tools(server_instance):
    """
    Register all scene tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    logger.info(f"Registering SmartThings Scene tools with server: {server_instance}")
    
    @server_instance.tool()
    def list_scenes(auth: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List all scenes.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Optional location ID to filter scenes
            
        Returns:
            List of scenes matching the filters
        """
        logger.info(f"Listing scenes" + (f" for location: {location_id}" if location_id else ""))
        params = filter_none_params(locationId=location_id)
        url = build_scene_url()
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url, params=params)
            logger.info("Successfully retrieved scenes")
            return result
        except Exception as e:
            logger.error(f"Error listing scenes: {e}")
            raise
    
    @server_instance.tool()
    def get_scene(auth: str, scene_id: str) -> Dict[str, Any]:
        """
        Get a specific scene by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            scene_id: Scene ID to retrieve
            
        Returns:
            Scene details
        """
        logger.info(f"Getting scene: {scene_id}")
        url = build_scene_url(scene_id)
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url)
            logger.info("Successfully retrieved scene")
            return result
        except Exception as e:
            logger.error(f"Error getting scene: {e}")
            raise
    
    @server_instance.tool()
    def execute_scene(auth: str, scene_id: str) -> Dict[str, Any]:
        """
        Execute a scene.
        
        Args:
            auth: OAuth 2.0 bearer token
            scene_id: Scene ID to execute
            
        Returns:
            Scene execution result
        """
        logger.info(f"Executing scene: {scene_id}")
        url = build_scene_url(scene_id, "execute")
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "POST", url)
            logger.info("Successfully executed scene")
            return result
        except Exception as e:
            logger.error(f"Error executing scene: {e}")
            raise
    
    @server_instance.tool()
    def create_scene(auth: str, location_id: str, name: str, 
                     icon: Optional[str] = None, 
                     colors: Optional[Dict[str, Any]] = None, 
                     actions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new scene.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Location ID where the scene will be created
            name: Name of the scene
            icon: Optional icon for the scene
            colors: Optional colors for the scene UI
            actions: List of actions for the scene
            
        Returns:
            Created scene details
        """
        logger.info(f"Creating scene: {name} in location: {location_id}")
        url = build_scene_url()
        
        data = {
            "locationId": location_id,
            "sceneName": name
        }
        
        if icon:
            data["icon"] = icon
        
        if colors:
            data["colors"] = colors
            
        if actions:
            data["actions"] = actions
            
        logger.info(f"Request URL: {url}")
        logger.info(f"Request data: {data}")
        try:
            result = make_request(auth, "POST", url, data=data)
            logger.info("Successfully created scene")
            return result
        except Exception as e:
            logger.error(f"Error creating scene: {e}")
            raise
    
    @server_instance.tool()
    def update_scene(auth: str, scene_id: str, name: Optional[str] = None, 
                     icon: Optional[str] = None, 
                     colors: Optional[Dict[str, Any]] = None, 
                     actions: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Update an existing scene.
        
        Args:
            auth: OAuth 2.0 bearer token
            scene_id: Scene ID to update
            name: Optional new name for the scene
            icon: Optional new icon for the scene
            colors: Optional new colors for the scene UI
            actions: Optional new list of actions for the scene
            
        Returns:
            Updated scene details
        """
        logger.info(f"Updating scene: {scene_id}")
        url = build_scene_url(scene_id)
        
        data = {}
        if name:
            data["sceneName"] = name
            
        if icon:
            data["icon"] = icon
            
        if colors:
            data["colors"] = colors
            
        if actions:
            data["actions"] = actions
            
        logger.info(f"Request URL: {url}")
        logger.info(f"Request data: {data}")
        try:
            result = make_request(auth, "PUT", url, data=data)
            logger.info("Successfully updated scene")
            return result
        except Exception as e:
            logger.error(f"Error updating scene: {e}")
            raise
    
    @server_instance.tool()
    def delete_scene(auth: str, scene_id: str) -> Dict[str, Any]:
        """
        Delete a scene.
        
        Args:
            auth: OAuth 2.0 bearer token
            scene_id: Scene ID to delete
            
        Returns:
            Delete operation result
        """
        logger.info(f"Deleting scene: {scene_id}")
        url = build_scene_url(scene_id)
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "DELETE", url)
            logger.info("Successfully deleted scene")
            return result
        except Exception as e:
            logger.error(f"Error deleting scene: {e}")
            raise
