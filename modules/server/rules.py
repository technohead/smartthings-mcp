"""
Rules module for SmartThings MCP server.
Exposes SmartThings rules endpoints as MCP tools.

Authentication Requirements:
- Requires a valid OAuth 2.0 bearer token with specific permissions.
- The token MUST have the following scopes:
  * 'r:rules:*' for read operations (list_rules, get_rule)
  * 'w:rules:*' for write operations (create_rule, update_rule, delete_rule, execute_rule)
  * Access to rules may require additional scopes like 'r:devices:*' or 'w:devices:*' 
    if rules interact with devices
- The Rules API may require an Enterprise account or special permissions in your SmartThings account

Common Authentication Issues:
- 401 Unauthorized: Token is missing, invalid, or expired
- 403 Forbidden: Token lacks required permissions or Rules API is not enabled for your account

Important Note:
- The Rules API has restricted access and may not be available to all SmartThings users
- If you're receiving a 403 Forbidden error, ensure your SmartThings account has access to the Rules API
- You may need to contact SmartThings support or use a SmartThings Enterprise account

See https://developer.smartthings.com/docs/api/public#section/Authentication for authentication details
and https://developer.smartthings.com/docs/api/public#tag/Rules for Rules API documentation.
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

def build_rule_url(rule_id: str = None, *path_params) -> str:
    """
    Build a SmartThings API URL for rules.
    
    Args:
        rule_id: Optional rule ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete rule URL string
    """
    if rule_id:
        return build_url('rules', rule_id, *path_params)
    else:
        return build_url('rules', *path_params)

def register_tools(server_instance):
    """
    Register all rule tools with the MCP server.
    
    Args:
        server_instance: FastMCP instance to register tools with
    """
    logger.info(f"Registering SmartThings Rule tools with server: {server_instance}")
    
    @server_instance.tool()
    def list_rules(auth: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List all rules.
        
        Args:
            auth: OAuth 2.0 bearer token
            location_id: Optional location ID to filter rules
            
        Returns:
            List of rules matching the filters
        """
        logger.info(f"Listing rules" + (f" for location: {location_id}" if location_id else ""))
        params = filter_none_params(locationId=location_id)
        url = build_rule_url()
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url, params=params)
            logger.info("Successfully retrieved rules")
            return result
        except Exception as e:
            logger.error(f"Error listing rules: {e}")
            raise
    
    @server_instance.tool()
    def get_rule(auth: str, rule_id: str) -> Dict[str, Any]:
        """
        Get a specific rule by ID.
        
        Args:
            auth: OAuth 2.0 bearer token
            rule_id: Rule ID to retrieve
            
        Returns:
            Rule details
        """
        logger.info(f"Getting rule: {rule_id}")
        url = build_rule_url(rule_id)
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "GET", url)
            logger.info("Successfully retrieved rule")
            return result
        except Exception as e:
            logger.error(f"Error getting rule: {e}")
            raise
    
    @server_instance.tool()
    def create_rule(auth: str, name: str, actions: List[Dict[str, Any]], 
                  triggers: List[Dict[str, Any]] = None, 
                  location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new rule.
        
        Args:
            auth: OAuth 2.0 bearer token
            name: Name for the rule
            actions: List of actions for the rule (contains if/then structures)
            triggers: Optional list of triggers (deprecated - triggers are now in actions)
            location_id: Optional location ID for the rule (required by SmartThings API as query param)
            
        Returns:
            Created rule details
        """
        logger.info(f"Creating rule: {name}")
        url = build_rule_url()
        
        # location_id must be passed as query parameter, not in the body
        params = filter_none_params(locationId=location_id)
        
        # Build data payload - only include name and actions
        # The if/then structure is already embedded in actions
        data = {
            "name": name,
            "actions": actions
        }
        
        # Only add triggers if provided and non-empty (for backward compatibility)
        if triggers:
            data["triggers"] = triggers
        
        # Log the complete URL with query parameters for debugging
        import json as _json
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{query_string}"
            logger.info(f"Request URL with params: {full_url}")
        else:
            logger.info(f"Request URL: {url}")
        
        # Log pretty JSON body for debugging server-side parsing errors
        try:
            logger.info("Request data (JSON):\n%s", _json.dumps(data, indent=2))
        except Exception:
            logger.info(f"Request data (raw): {data}")
            
        try:
            result = make_request(auth, "POST", url, params=params, data=data)
            logger.info("Successfully created rule")
            return result
        except Exception as e:
            logger.error(f"Error creating rule: {e}")
            raise
    
    @server_instance.tool()
    def update_rule(auth: str, rule_id: str, name: Optional[str] = None, 
                  actions: Optional[List[Dict[str, Any]]] = None, 
                  triggers: Optional[List[Dict[str, Any]]] = None,
                  enabled: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update an existing rule.
        
        Args:
            auth: OAuth 2.0 bearer token
            rule_id: Rule ID to update
            name: Optional new name for the rule
            actions: Optional new list of actions for the rule
            triggers: Optional new list of triggers for the rule
            enabled: Optional boolean to enable (True) or disable (False) the rule
            
        Returns:
            Updated rule details
        """
        logger.info(f"Updating rule: {rule_id}")
        url = build_rule_url(rule_id)
        
        data = {}
        if name:
            data["name"] = name
        if actions:
            data["actions"] = actions
        if triggers:
            data["triggers"] = triggers
        if enabled is not None:
            data["enabled"] = enabled
            
        logger.info(f"Request URL: {url}")
        logger.info(f"Request data: {data}")
        try:
            result = make_request(auth, "PUT", url, data=data)
            logger.info("Successfully updated rule")
            return result
        except Exception as e:
            logger.error(f"Error updating rule: {e}")
            raise
    
    @server_instance.tool()
    def delete_rule(auth: str, rule_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete a rule.
        
        Args:
            auth: OAuth 2.0 bearer token
            rule_id: Rule ID to delete
            location_id: Optional location ID (required by SmartThings API)
            
        Returns:
            Delete operation result
        """
        logger.info(f"Deleting rule: {rule_id}" + (f" for location: {location_id}" if location_id else ""))
        params = filter_none_params(locationId=location_id)
        url = build_rule_url(rule_id)
        
        # Log the complete URL with query parameters for debugging
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{query_string}"
            logger.info(f"Request URL with params: {full_url}")
        else:
            logger.info(f"Request URL: {url}")
        
        try:
            result = make_request(auth, "DELETE", url, params=params)
            logger.info("Successfully deleted rule")
            logger.info("Note: Server cache has been cleared - next list_rules will fetch fresh data")
            return result
        except Exception as e:
            logger.error(f"Error deleting rule: {e}")
            raise
            
    @server_instance.tool()
    def execute_rule(auth: str, rule_id: str) -> Dict[str, Any]:
        """
        Execute a rule.
        
        Args:
            auth: OAuth 2.0 bearer token
            rule_id: Rule ID to execute
            
        Returns:
            Rule execution result
        """
        logger.info(f"Executing rule: {rule_id}")
        url = build_rule_url(rule_id, "execute")
        logger.info(f"Request URL: {url}")
        try:
            result = make_request(auth, "POST", url)
            logger.info("Successfully executed rule")
            return result
        except Exception as e:
            logger.error(f"Error executing rule: {e}")
            raise
