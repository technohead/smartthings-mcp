"""
Utility functions for SmartThingsMCP client
"""
import json
from typing import Dict, Any, List


def convert_tool_to_dict(obj: Any) -> Any:
    """
    Convert Tool objects and other non-serializable objects to dictionaries.
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON serializable version of the object
    """
    if hasattr(obj, '__dict__'):
        # For custom objects with __dict__
        return {key: convert_tool_to_dict(value) for key, value in obj.__dict__.items() 
                if not key.startswith('_') and not callable(value)}
    elif isinstance(obj, list):
        return [convert_tool_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_tool_to_dict(value) for key, value in obj.items()}
    else:
        # Try to use the object as is, let JSON handle basic types
        try:
            # Test if it's JSON serializable
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            # If not serializable, convert to string representation
            return str(obj)


async def run_action(client, action: str, params: Dict[str, Any]) -> Any:
    """
    Run the specified action on the client with the given parameters.
    
    Args:
        client: SmartThingsMCPClient instance
        action: Action name to run
        params: Parameters for the action
        
    Returns:
        Action result
    """
    # Ensure auth token is included in all calls
    if hasattr(client, 'auth_token') and client.auth_token and 'auth' not in params:
        params['auth'] = client.auth_token
    
    # Handle list_tools action specially
    if action == "list_tools":
        return await client.list_tools()
    
    # For all other actions, use call_tool
    return await client.call_tool(action, **params)
