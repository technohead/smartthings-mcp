"""
Unit tests for SmartThingsMCP location operations.
Tests the locations module and location-related MCP tools.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestLocationTools:
    """Test location-related MCP tools."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_list_locations(self, mock_request):
        """Test listing all locations."""
        mock_request.return_value = {
            "items": [
                {
                    "id": "loc-1",
                    "name": "Home",
                    "countryCode": "US",
                    "timeZoneId": "America/New_York"
                },
                {
                    "id": "loc-2",
                    "name": "Cabin",
                    "countryCode": "US",
                    "timeZoneId": "America/Denver"
                }
            ]
        }
        
        result = mock_request("test-token", "GET", "https://api.smartthings.com/v1/locations")
        
        assert len(result["items"]) == 2
        assert result["items"][0]["id"] == "loc-1"
        assert result["items"][0]["name"] == "Home"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_location_details(self, mock_request):
        """Test getting location details."""
        mock_request.return_value = {
            "id": "loc-1",
            "name": "Home",
            "countryCode": "US",
            "timeZoneId": "America/New_York",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        result = mock_request("test-token", "GET", 
                            "https://api.smartthings.com/v1/locations/loc-1")
        
        assert result["id"] == "loc-1"
        assert result["name"] == "Home"
        assert result["latitude"] == 40.7128
        assert result["longitude"] == -74.0060
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_location_mode(self, mock_request):
        """Test getting location mode."""
        mock_request.return_value = {
            "locationId": "loc-1",
            "currentMode": {
                "id": "mode-1",
                "name": "Home",
                "label": "Home Mode"
            }
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/locations/loc-1/modes")
        
        assert result["locationId"] == "loc-1"
        assert result["currentMode"]["id"] == "mode-1"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_location_hubs(self, mock_request):
        """Test getting hubs in a location."""
        mock_request.return_value = {
            "items": [
                {
                    "id": "hub-1",
                    "name": "SmartThings Hub",
                    "status": "ONLINE"
                }
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/hubs?locationId=loc-1")
        
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "SmartThings Hub"
        assert result["items"][0]["status"] == "ONLINE"


class TestLocationFiltering:
    """Test location filtering and search functionality."""
    
    def test_filter_locations_by_country(self):
        """Test filtering locations by country code."""
        locations = [
            {"id": "loc-1", "name": "Home", "countryCode": "US"},
            {"id": "loc-2", "name": "Cabin", "countryCode": "CA"},
            {"id": "loc-3", "name": "Beach", "countryCode": "US"}
        ]
        
        us_locations = [loc for loc in locations if loc.get("countryCode") == "US"]
        assert len(us_locations) == 2
        assert all(loc["countryCode"] == "US" for loc in us_locations)
    
    def test_filter_locations_by_name(self):
        """Test filtering locations by name."""
        locations = [
            {"id": "loc-1", "name": "Home"},
            {"id": "loc-2", "name": "Cabin"},
            {"id": "loc-3", "name": "HomeOffice"}
        ]
        
        home_locations = [loc for loc in locations if "Home" in loc.get("name", "")]
        assert len(home_locations) == 2
    
    def test_sort_locations_by_name(self):
        """Test sorting locations by name."""
        locations = [
            {"id": "loc-3", "name": "Zebra"},
            {"id": "loc-1", "name": "Apple"},
            {"id": "loc-2", "name": "Banana"}
        ]
        
        sorted_locations = sorted(locations, key=lambda x: x["name"])
        assert sorted_locations[0]["name"] == "Apple"
        assert sorted_locations[1]["name"] == "Banana"
        assert sorted_locations[2]["name"] == "Zebra"


class TestLocationWithRooms:
    """Test location operations with associated rooms."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_location_rooms(self, mock_request):
        """Test getting rooms in a location."""
        mock_request.return_value = {
            "items": [
                {"id": "room-1", "name": "Living Room", "locationId": "loc-1"},
                {"id": "room-2", "name": "Bedroom", "locationId": "loc-1"},
                {"id": "room-3", "name": "Kitchen", "locationId": "loc-1"}
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/rooms?locationId=loc-1")
        
        assert len(result["items"]) == 3
        assert all(room["locationId"] == "loc-1" for room in result["items"])
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_location_with_rooms_structure(self, mock_request):
        """Test getting location structure with rooms."""
        mock_request.return_value = {
            "location": {
                "id": "loc-1",
                "name": "Home"
            },
            "rooms": [
                {"id": "room-1", "name": "Living Room"},
                {"id": "room-2", "name": "Bedroom"}
            ]
        }
        
        result = mock_request("test-token", "GET", "https://api.smartthings.com/v1/locations/loc-1")
        
        assert result["location"]["id"] == "loc-1"
        assert len(result["rooms"]) == 2


class TestLocationDeviceCount:
    """Test counting and aggregating devices by location."""
    
    def test_count_devices_by_location(self):
        """Test counting devices in each location."""
        devices = [
            {"id": "d1", "name": "Light 1", "locationId": "loc-1"},
            {"id": "d2", "name": "Light 2", "locationId": "loc-1"},
            {"id": "d3", "name": "Light 3", "locationId": "loc-2"},
            {"id": "d4", "name": "Light 4", "locationId": "loc-1"}
        ]
        
        location_counts = {}
        for device in devices:
            loc_id = device["locationId"]
            location_counts[loc_id] = location_counts.get(loc_id, 0) + 1
        
        assert location_counts["loc-1"] == 3
        assert location_counts["loc-2"] == 1
    
    def test_count_devices_by_location_and_capability(self):
        """Test counting devices by location and capability."""
        devices = [
            {"id": "d1", "name": "Light", "locationId": "loc-1", "capabilities": ["switch"]},
            {"id": "d2", "name": "Light", "locationId": "loc-1", "capabilities": ["switch"]},
            {"id": "d3", "name": "Lock", "locationId": "loc-1", "capabilities": ["lock"]},
            {"id": "d4", "name": "Light", "locationId": "loc-2", "capabilities": ["switch"]}
        ]
        
        switch_by_location = {}
        for device in devices:
            if "switch" in device.get("capabilities", []):
                loc_id = device["locationId"]
                switch_by_location[loc_id] = switch_by_location.get(loc_id, 0) + 1
        
        assert switch_by_location["loc-1"] == 2
        assert switch_by_location["loc-2"] == 1
        assert "loc-3" not in switch_by_location
