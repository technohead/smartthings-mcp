"""
Scenes module for SmartThingsMCP Client
"""
from typing import Dict, Any, Optional, List


class ScenesMixin:
    """
    Mixin class for scene-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def list_scenes(self, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List all scenes.
        
        Args:
            location_id: Optional location ID to filter scenes
            
        Returns:
            List of scenes matching the filters
        """
        params = {}
        if location_id:
            params["location_id"] = location_id
            
        return await self.call_tool("list_scenes", **params)
    
    async def get_scene(self, scene_id: str) -> Dict[str, Any]:
        """
        Get a specific scene by ID.
        
        Args:
            scene_id: Scene ID to retrieve
            
        Returns:
            Scene details
        """
        return await self.call_tool("get_scene", scene_id=scene_id)
    
    async def execute_scene(self, scene_id: str) -> Dict[str, Any]:
        """
        Execute a scene.
        
        Args:
            scene_id: Scene ID to execute
            
        Returns:
            Scene execution result
        """
        return await self.call_tool("execute_scene", scene_id=scene_id)
    
    async def create_scene(self, location_id: str, name: str, 
                        icon: Optional[str] = None, 
                        colors: Optional[Dict[str, Any]] = None, 
                        actions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new scene.
        
        Args:
            location_id: Location ID where the scene will be created
            name: Name of the scene
            icon: Optional icon for the scene
            colors: Optional colors for the scene UI
            actions: Optional list of actions for the scene
            
        Returns:
            Created scene details
        """
        params = {
            "location_id": location_id,
            "name": name
        }
        
        if icon:
            params["icon"] = icon
        
        if colors:
            params["colors"] = colors
            
        if actions:
            params["actions"] = actions
            
        return await self.call_tool("create_scene", **params)
    
    async def update_scene(self, scene_id: str, name: Optional[str] = None, 
                        icon: Optional[str] = None, 
                        colors: Optional[Dict[str, Any]] = None, 
                        actions: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Update an existing scene.
        
        Args:
            scene_id: Scene ID to update
            name: Optional new name for the scene
            icon: Optional new icon for the scene
            colors: Optional new colors for the scene UI
            actions: Optional new list of actions for the scene
            
        Returns:
            Updated scene details
        """
        params = {"scene_id": scene_id}
        
        if name:
            params["name"] = name
            
        if icon:
            params["icon"] = icon
            
        if colors:
            params["colors"] = colors
            
        if actions:
            params["actions"] = actions
            
        return await self.call_tool("update_scene", **params)
    
    async def delete_scene(self, scene_id: str) -> Dict[str, Any]:
        """
        Delete a scene.
        
        Args:
            scene_id: Scene ID to delete
            
        Returns:
            Delete operation result
        """
        return await self.call_tool("delete_scene", scene_id=scene_id)
