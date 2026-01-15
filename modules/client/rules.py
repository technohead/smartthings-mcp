"""
Rules module for SmartThingsMCP Client
"""
from typing import Dict, Any, Optional, List


class RulesMixin:
    """
    Mixin class for rule-related endpoints.
    To be used with the SmartThingsMCPClient class.
    """

    async def list_rules(self, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List all rules.
        
        Args:
            location_id: Optional location ID to filter rules
            
        Returns:
            List of rules matching the filters
        """
        params = {}
        if location_id:
            params["location_id"] = location_id
            
        return await self.call_tool("list_rules", **params)
    
    async def get_rule(self, rule_id: str) -> Dict[str, Any]:
        """
        Get a specific rule by ID.
        
        Args:
            rule_id: Rule ID to retrieve
            
        Returns:
            Rule details
        """
        return await self.call_tool("get_rule", rule_id=rule_id)
    
    async def create_rule(self, name: str, actions: List[Dict[str, Any]], 
                      triggers: List[Dict[str, Any]], 
                      location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new rule.
        
        Args:
            name: Name for the rule
            actions: List of actions for the rule
            triggers: List of triggers for the rule
            location_id: Optional location ID for the rule
            
        Returns:
            Created rule details
        """
        params = {
            "name": name,
            "actions": actions,
            "triggers": triggers
        }
        
        if location_id:
            params["location_id"] = location_id
            
        return await self.call_tool("create_rule", **params)
    
    async def update_rule(self, rule_id: str, name: Optional[str] = None, 
                      actions: Optional[List[Dict[str, Any]]] = None, 
                      triggers: Optional[List[Dict[str, Any]]] = None,
                      enabled: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update an existing rule.
        
        Args:
            rule_id: Rule ID to update
            name: Optional new name for the rule
            actions: Optional new list of actions for the rule
            triggers: Optional new list of triggers for the rule
            enabled: Optional boolean to enable (True) or disable (False) the rule
            
        Returns:
            Updated rule details
        """
        params = {"rule_id": rule_id}
        
        if name:
            params["name"] = name
        if actions:
            params["actions"] = actions
        if triggers:
            params["triggers"] = triggers
        if enabled is not None:
            params["enabled"] = enabled
            
        return await self.call_tool("update_rule", **params)
    
    async def delete_rule(self, rule_id: str, location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete a rule.
        
        Args:
            rule_id: Rule ID to delete
            location_id: Optional location ID (required by SmartThings API)
            
        Returns:
            Delete operation result
        """
        params = {"rule_id": rule_id}
        if location_id:
            params["location_id"] = location_id
            
        return await self.call_tool("delete_rule", **params)
    
    async def execute_rule(self, rule_id: str) -> Dict[str, Any]:
        """
        Execute a rule.
        
        Args:
            rule_id: Rule ID to execute
            
        Returns:
            Rule execution result
        """
        return await self.call_tool("execute_rule", rule_id=rule_id)
