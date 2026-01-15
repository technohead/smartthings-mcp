"""
Pytest configuration and shared fixtures for SmartThingsMCP tests.
"""
import pytest
from unittest.mock import Mock, MagicMock
import os
import sys

# Add parent directory to Python path so SmartThingsMCP can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture
def mock_auth_token():
    """Provide a mock authentication token."""
    return "test-auth-token-12345"


@pytest.fixture
def mock_location():
    """Provide a mock location object."""
    return {
        "id": "loc-1",
        "name": "Home",
        "countryCode": "US",
        "timeZoneId": "America/New_York",
        "latitude": 40.7128,
        "longitude": -74.0060
    }


@pytest.fixture
def mock_device():
    """Provide a mock device object."""
    return {
        "id": "device-1",
        "name": "Living Room Light",
        "label": "Light",
        "locationId": "loc-1",
        "roomId": "room-1",
        "status": "online",
        "components": [
            {
                "id": "main",
                "capabilities": [
                    {
                        "id": "switch",
                        "values": [{"key": "switch", "value": "on"}]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_devices_list(mock_device):
    """Provide a mock list of devices."""
    return {
        "items": [
            mock_device,
            {
                "id": "device-2",
                "name": "Kitchen Light",
                "label": "Light",
                "locationId": "loc-1",
                "roomId": "room-2",
                "status": "online"
            },
            {
                "id": "device-3",
                "name": "Front Door Lock",
                "label": "Lock",
                "locationId": "loc-1",
                "roomId": "room-3",
                "status": "offline"
            }
        ]
    }


@pytest.fixture
def mock_room():
    """Provide a mock room object."""
    return {
        "id": "room-1",
        "name": "Living Room",
        "locationId": "loc-1"
    }


@pytest.fixture
def mock_rooms_list(mock_room):
    """Provide a mock list of rooms."""
    return {
        "items": [
            mock_room,
            {
                "id": "room-2",
                "name": "Bedroom",
                "locationId": "loc-1"
            },
            {
                "id": "room-3",
                "name": "Kitchen",
                "locationId": "loc-1"
            }
        ]
    }


@pytest.fixture
def mock_rule():
    """Provide a mock rule object."""
    return {
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
                "type": "deviceCommand",
                "devices": ["device-1"],
                "capability": "switch",
                "command": "on"
            }
        ]
    }


@pytest.fixture
def mock_rules_list(mock_rule):
    """Provide a mock list of rules."""
    return {
        "items": [
            mock_rule,
            {
                "id": "rule-2",
                "name": "Morning Coffee",
                "description": "Start coffee maker in the morning",
                "enabled": True,
                "locationId": "loc-1",
                "triggers": [
                    {
                        "type": "time",
                        "at": "06:30:00"
                    }
                ],
                "conditions": [],
                "actions": []
            }
        ]
    }


@pytest.fixture
def mock_mode():
    """Provide a mock mode object."""
    return {
        "id": "mode-1",
        "name": "Home",
        "label": "Home Mode"
    }


@pytest.fixture
def mock_modes_list(mock_mode):
    """Provide a mock list of modes."""
    return {
        "locationId": "loc-1",
        "currentMode": mock_mode,
        "modes": [
            mock_mode,
            {
                "id": "mode-2",
                "name": "Away",
                "label": "Away Mode"
            }
        ]
    }


@pytest.fixture
def mock_scene():
    """Provide a mock scene object."""
    return {
        "id": "scene-1",
        "name": "Movie Night",
        "description": "Dim lights and close blinds",
        "locationId": "loc-1",
        "enabled": True
    }


@pytest.fixture
def mock_scenes_list(mock_scene):
    """Provide a mock list of scenes."""
    return {
        "items": [
            mock_scene,
            {
                "id": "scene-2",
                "name": "Good Morning",
                "description": "Open blinds and turn on coffee",
                "locationId": "loc-1",
                "enabled": True
            }
        ]
    }


@pytest.fixture
def mock_http_client():
    """Provide a mock HTTP client."""
    client = Mock()
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client


@pytest.fixture
def mock_server():
    """Provide a mock MCP server instance."""
    server = Mock()
    server.tool = Mock(return_value=lambda f: f)
    server.add_tool = Mock()
    server.list_tools = Mock()
    return server


@pytest.fixture
def api_error_response():
    """Provide a mock API error response."""
    return {
        "error": {
            "code": "INVALID_REQUEST",
            "message": "Request validation failed"
        }
    }


@pytest.fixture
def api_success_response():
    """Provide a mock successful API response."""
    return {
        "status": "success",
        "data": {}
    }


@pytest.fixture
def mock_api_url():
    """Provide the mock API base URL."""
    return "https://api.smartthings.com/v1"


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "requires_auth: marks tests that require authentication"
    )
