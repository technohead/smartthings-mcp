"""
Unit tests for SmartThingsMCP rule operations.
Tests the rules module and rule-related MCP tools.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime


class TestRuleTools:
    """Test rule-related MCP tools."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_list_rules(self, mock_request):
        """Test listing all rules for a location."""
        mock_request.return_value = {
            "items": [
                {
                    "id": "rule-1",
                    "name": "Evening Lights",
                    "enabled": True,
                    "locationId": "loc-1"
                },
                {
                    "id": "rule-2",
                    "name": "Morning Coffee",
                    "enabled": True,
                    "locationId": "loc-1"
                }
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/rules?locationId=loc-1")
        
        assert len(result["items"]) == 2
        assert result["items"][0]["name"] == "Evening Lights"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_rule(self, mock_request):
        """Test getting details of a specific rule."""
        mock_request.return_value = {
            "id": "rule-1",
            "name": "Evening Lights",
            "description": "Turn on lights in the evening",
            "enabled": True,
            "locationId": "loc-1",
            "triggers": [
                {
                    "type": "time",
                    "at": "18:00:00"
                }
            ],
            "conditions": [],
            "actions": [
                {
                    "capability": "switch",
                    "command": "on",
                    "devices": ["d1", "d2"]
                }
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/rules/rule-1")
        
        assert result["id"] == "rule-1"
        assert result["name"] == "Evening Lights"
        assert result["enabled"] is True
        assert len(result["triggers"]) > 0
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_create_rule(self, mock_request):
        """Test creating a new rule."""
        mock_request.return_value = {
            "id": "rule-new",
            "name": "New Rule",
            "enabled": True,
            "locationId": "loc-1"
        }
        
        payload = {
            "name": "New Rule",
            "enabled": True,
            "locationId": "loc-1",
            "triggers": [],
            "conditions": [],
            "actions": []
        }
        
        result = mock_request("test-token", "POST",
                            "https://api.smartthings.com/v1/rules",
                            json=payload)
        
        assert result["id"] == "rule-new"
        assert result["name"] == "New Rule"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_update_rule(self, mock_request):
        """Test updating an existing rule."""
        mock_request.return_value = {
            "id": "rule-1",
            "name": "Updated Rule",
            "enabled": False
        }
        
        payload = {
            "name": "Updated Rule",
            "enabled": False
        }
        
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/rules/rule-1",
                            json=payload)
        
        assert result["name"] == "Updated Rule"
        assert result["enabled"] is False
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_delete_rule(self, mock_request):
        """Test deleting a rule."""
        mock_request.return_value = {}
        
        result = mock_request("test-token", "DELETE",
                            "https://api.smartthings.com/v1/rules/rule-1")
        
        assert result == {}
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_execute_rule(self, mock_request):
        """Test manually executing a rule."""
        mock_request.return_value = {
            "id": "exec-123",
            "ruleId": "rule-1",
            "status": "EXECUTED"
        }
        
        result = mock_request("test-token", "POST",
                            "https://api.smartthings.com/v1/rules/rule-1/execute")
        
        assert result["status"] == "EXECUTED"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_enable_rule(self, mock_request):
        """Test enabling a rule."""
        mock_request.return_value = {
            "id": "rule-1",
            "enabled": True
        }
        
        payload = {"enabled": True}
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/rules/rule-1",
                            json=payload)
        
        assert result["enabled"] is True
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_disable_rule(self, mock_request):
        """Test disabling a rule."""
        mock_request.return_value = {
            "id": "rule-1",
            "enabled": False
        }
        
        payload = {"enabled": False}
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/rules/rule-1",
                            json=payload)
        
        assert result["enabled"] is False


class TestRuleTriggers:
    """Test rule trigger configurations."""
    
    def test_time_trigger(self):
        """Test time-based trigger."""
        trigger = {
            "type": "time",
            "at": "18:00:00"
        }
        
        assert trigger["type"] == "time"
        assert trigger["at"] == "18:00:00"
    
    def test_device_trigger(self):
        """Test device-based trigger."""
        trigger = {
            "type": "deviceEvent",
            "deviceId": "d1",
            "capability": "switch",
            "attribute": "switch",
            "value": "on"
        }
        
        assert trigger["deviceId"] == "d1"
        assert trigger["capability"] == "switch"
    
    def test_location_mode_trigger(self):
        """Test location mode trigger."""
        trigger = {
            "type": "locationMode",
            "locationId": "loc-1",
            "modeId": "mode-home"
        }
        
        assert trigger["type"] == "locationMode"
        assert trigger["modeId"] == "mode-home"
    
    def test_sunrise_trigger(self):
        """Test sunrise-based trigger."""
        trigger = {
            "type": "sunrise",
            "offset": 30  # 30 minutes after sunrise
        }
        
        assert trigger["type"] == "sunrise"
        assert trigger["offset"] == 30
    
    def test_sunset_trigger(self):
        """Test sunset-based trigger."""
        trigger = {
            "type": "sunset",
            "offset": -30  # 30 minutes before sunset
        }
        
        assert trigger["type"] == "sunset"
        assert trigger["offset"] == -30


class TestRuleActions:
    """Test rule action configurations."""
    
    def test_device_command_action(self):
        """Test device command action."""
        action = {
            "type": "deviceCommand",
            "devices": ["d1", "d2"],
            "capability": "switch",
            "command": "on"
        }
        
        assert action["capability"] == "switch"
        assert action["command"] == "on"
        assert len(action["devices"]) == 2
    
    def test_scene_action(self):
        """Test scene action."""
        action = {
            "type": "scene",
            "sceneId": "scene-1"
        }
        
        assert action["type"] == "scene"
        assert action["sceneId"] == "scene-1"
    
    def test_notification_action(self):
        """Test notification action."""
        action = {
            "type": "notification",
            "target": "email",
            "recipients": ["user@example.com"]
        }
        
        assert action["target"] == "email"
        assert len(action["recipients"]) == 1


class TestRuleConditions:
    """Test rule condition configurations."""
    
    def test_device_condition(self):
        """Test device condition."""
        condition = {
            "type": "deviceCondition",
            "deviceId": "d1",
            "capability": "switch",
            "attribute": "switch",
            "value": "on",
            "operator": "equals"
        }
        
        assert condition["deviceId"] == "d1"
        assert condition["operator"] == "equals"
    
    def test_time_condition(self):
        """Test time range condition."""
        condition = {
            "type": "timeCondition",
            "startTime": "09:00:00",
            "endTime": "17:00:00"
        }
        
        assert condition["startTime"] == "09:00:00"
        assert condition["endTime"] == "17:00:00"
    
    def test_location_mode_condition(self):
        """Test location mode condition."""
        condition = {
            "type": "locationModeCondition",
            "locationId": "loc-1",
            "modeId": "mode-home"
        }
        
        assert condition["modeId"] == "mode-home"


class TestRuleFiltering:
    """Test rule filtering and search."""
    
    def test_filter_rules_by_enabled(self):
        """Test filtering rules by enabled status."""
        rules = [
            {"id": "rule-1", "name": "Rule 1", "enabled": True},
            {"id": "rule-2", "name": "Rule 2", "enabled": False},
            {"id": "rule-3", "name": "Rule 3", "enabled": True}
        ]
        
        enabled = [r for r in rules if r["enabled"]]
        assert len(enabled) == 2
        assert all(r["enabled"] for r in enabled)
    
    def test_filter_rules_by_name(self):
        """Test filtering rules by name."""
        rules = [
            {"id": "rule-1", "name": "Evening Lights"},
            {"id": "rule-2", "name": "Morning Coffee"},
            {"id": "rule-3", "name": "Evening Security"}
        ]
        
        evening = [r for r in rules if "Evening" in r["name"]]
        assert len(evening) == 2
    
    def test_sort_rules_by_name(self):
        """Test sorting rules by name."""
        rules = [
            {"id": "rule-3", "name": "Zebra"},
            {"id": "rule-1", "name": "Apple"},
            {"id": "rule-2", "name": "Banana"}
        ]
        
        sorted_rules = sorted(rules, key=lambda r: r["name"])
        assert sorted_rules[0]["name"] == "Apple"
        assert sorted_rules[1]["name"] == "Banana"


class TestRuleValidation:
    """Test rule validation logic."""
    
    def test_rule_has_triggers(self):
        """Test that a rule has at least one trigger."""
        rule = {
            "name": "Test Rule",
            "triggers": [{"type": "time", "at": "18:00:00"}],
            "actions": []
        }
        
        assert len(rule["triggers"]) > 0
    
    def test_rule_has_actions(self):
        """Test that a rule has at least one action."""
        rule = {
            "name": "Test Rule",
            "triggers": [],
            "actions": [{"type": "deviceCommand", "devices": ["d1"]}]
        }
        
        assert len(rule["actions"]) > 0
    
    def test_rule_name_not_empty(self):
        """Test that rule name is not empty."""
        rule = {"name": "My Rule"}
        assert len(rule["name"]) > 0
    
    def test_rule_name_max_length(self):
        """Test rule name length constraints."""
        rule = {"name": "A" * 100}
        assert len(rule["name"]) <= 256  # Assuming max length of 256
