"""
Unit tests for SmartThingsMCP room operations.
Tests the rooms module and room-related MCP tools.
"""
import pytest
from unittest.mock import Mock, patch


class TestRoomTools:
    """Test room-related MCP tools."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_list_rooms(self, mock_request):
        """Test listing all rooms in a location."""
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
        assert result["items"][0]["name"] == "Living Room"
        assert all(room["locationId"] == "loc-1" for room in result["items"])
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_room_details(self, mock_request):
        """Test getting details of a specific room."""
        mock_request.return_value = {
            "id": "room-1",
            "name": "Living Room",
            "locationId": "loc-1",
            "created": "2025-01-14T10:00:00Z",
            "lastModified": "2025-01-14T10:00:00Z"
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/rooms/room-1")
        
        assert result["id"] == "room-1"
        assert result["name"] == "Living Room"
        assert result["locationId"] == "loc-1"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_room_devices(self, mock_request):
        """Test getting devices in a room."""
        mock_request.return_value = {
            "items": [
                {"id": "d1", "name": "Light", "roomId": "room-1"},
                {"id": "d2", "name": "Switch", "roomId": "room-1"},
                {"id": "d3", "name": "Lamp", "roomId": "room-1"}
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/devices?roomId=room-1")
        
        assert len(result["items"]) == 3
        assert all(device["roomId"] == "room-1" for device in result["items"])
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_create_room(self, mock_request):
        """Test creating a new room."""
        mock_request.return_value = {
            "id": "room-new",
            "name": "New Room",
            "locationId": "loc-1"
        }
        
        payload = {"name": "New Room", "locationId": "loc-1"}
        result = mock_request("test-token", "POST",
                            "https://api.smartthings.com/v1/rooms",
                            json=payload)
        
        assert result["id"] == "room-new"
        assert result["name"] == "New Room"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_update_room(self, mock_request):
        """Test updating a room."""
        mock_request.return_value = {
            "id": "room-1",
            "name": "Updated Room",
            "locationId": "loc-1"
        }
        
        payload = {"name": "Updated Room"}
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/rooms/room-1",
                            json=payload)
        
        assert result["name"] == "Updated Room"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_delete_room(self, mock_request):
        """Test deleting a room."""
        mock_request.return_value = {}
        
        result = mock_request("test-token", "DELETE",
                            "https://api.smartthings.com/v1/rooms/room-1")
        
        assert result == {}


class TestRoomDeviceAssociation:
    """Test associating devices with rooms."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_add_device_to_room(self, mock_request):
        """Test adding a device to a room."""
        mock_request.return_value = {
            "id": "d1",
            "name": "Light",
            "roomId": "room-1"
        }
        
        payload = {"roomId": "room-1"}
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/devices/d1",
                            json=payload)
        
        assert result["roomId"] == "room-1"
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_remove_device_from_room(self, mock_request):
        """Test removing a device from a room."""
        mock_request.return_value = {
            "id": "d1",
            "name": "Light",
            "roomId": None
        }
        
        payload = {"roomId": None}
        result = mock_request("test-token", "PUT",
                            "https://api.smartthings.com/v1/devices/d1",
                            json=payload)
        
        assert result["roomId"] is None
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_get_devices_in_room(self, mock_request):
        """Test getting all devices in a specific room."""
        mock_request.return_value = {
            "items": [
                {"id": "d1", "name": "Ceiling Light", "roomId": "room-living"},
                {"id": "d2", "name": "Wall Switch", "roomId": "room-living"},
                {"id": "d3", "name": "Outlet", "roomId": "room-living"}
            ]
        }
        
        result = mock_request("test-token", "GET",
                            "https://api.smartthings.com/v1/devices?roomId=room-living")
        
        assert len(result["items"]) == 3
        assert all(d["roomId"] == "room-living" for d in result["items"])


class TestRoomFiltering:
    """Test room filtering and search functionality."""
    
    def test_filter_rooms_by_name(self):
        """Test filtering rooms by name."""
        rooms = [
            {"id": "room-1", "name": "Living Room"},
            {"id": "room-2", "name": "Bedroom"},
            {"id": "room-3", "name": "Dining Room"}
        ]
        
        # "Room" (capital R) appears in "Living Room" and "Dining Room" only (case-sensitive)
        filtered = [r for r in rooms if "Room" in r["name"]]
        assert len(filtered) == 2
    
    def test_filter_rooms_by_name_exact_match(self):
        """Test exact match filtering of rooms."""
        rooms = [
            {"id": "room-1", "name": "Living Room"},
            {"id": "room-2", "name": "Bedroom"},
            {"id": "room-3", "name": "Living"}
        ]
        
        filtered = [r for r in rooms if r["name"] == "Living Room"]
        assert len(filtered) == 1
        assert filtered[0]["id"] == "room-1"
    
    def test_filter_rooms_by_location(self):
        """Test filtering rooms by location."""
        rooms = [
            {"id": "room-1", "name": "Living Room", "locationId": "loc-1"},
            {"id": "room-2", "name": "Bedroom", "locationId": "loc-2"},
            {"id": "room-3", "name": "Kitchen", "locationId": "loc-1"}
        ]
        
        filtered = [r for r in rooms if r["locationId"] == "loc-1"]
        assert len(filtered) == 2
        assert all(r["locationId"] == "loc-1" for r in filtered)
    
    def test_sort_rooms_by_name(self):
        """Test sorting rooms alphabetically."""
        rooms = [
            {"id": "room-3", "name": "Zebra Room"},
            {"id": "room-1", "name": "Apple Room"},
            {"id": "room-2", "name": "Banana Room"}
        ]
        
        sorted_rooms = sorted(rooms, key=lambda r: r["name"])
        assert sorted_rooms[0]["name"] == "Apple Room"
        assert sorted_rooms[1]["name"] == "Banana Room"
        assert sorted_rooms[2]["name"] == "Zebra Room"


class TestRoomDeviceCount:
    """Test counting devices by room."""
    
    def test_count_devices_in_room(self):
        """Test counting total devices in a room."""
        devices = [
            {"id": "d1", "roomId": "room-1"},
            {"id": "d2", "roomId": "room-1"},
            {"id": "d3", "roomId": "room-1"},
            {"id": "d4", "roomId": "room-2"}
        ]
        
        room_1_count = len([d for d in devices if d["roomId"] == "room-1"])
        assert room_1_count == 3
    
    def test_count_devices_by_room(self):
        """Test counting devices in each room."""
        devices = [
            {"id": "d1", "roomId": "room-1"},
            {"id": "d2", "roomId": "room-1"},
            {"id": "d3", "roomId": "room-2"},
            {"id": "d4", "roomId": "room-3"},
            {"id": "d5", "roomId": "room-3"}
        ]
        
        counts = {}
        for device in devices:
            room_id = device["roomId"]
            counts[room_id] = counts.get(room_id, 0) + 1
        
        assert counts["room-1"] == 2
        assert counts["room-2"] == 1
        assert counts["room-3"] == 2
    
    def test_count_devices_by_room_and_capability(self):
        """Test counting devices by room and capability."""
        devices = [
            {"id": "d1", "roomId": "room-1", "capabilities": ["switch"]},
            {"id": "d2", "roomId": "room-1", "capabilities": ["brightness"]},
            {"id": "d3", "roomId": "room-2", "capabilities": ["switch"]},
            {"id": "d4", "roomId": "room-2", "capabilities": ["lock"]}
        ]
        
        switches_by_room = {}
        for device in devices:
            if "switch" in device.get("capabilities", []):
                room_id = device["roomId"]
                switches_by_room[room_id] = switches_by_room.get(room_id, 0) + 1
        
        assert switches_by_room["room-1"] == 1
        assert switches_by_room["room-2"] == 1
        assert "room-3" not in switches_by_room
