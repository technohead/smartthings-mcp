# SmartThingsMCP Unit Tests

Comprehensive unit and integration tests for the SmartThingsMCP server and client.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py               # Pytest configuration and shared fixtures
├── pytest.ini                # Pytest configuration file
├── test_devices.py           # Device operations tests
├── test_locations.py         # Location operations tests
├── test_rooms.py             # Room operations tests
├── test_rules.py             # Rule operations tests
├── test_client.py            # Client operations and caching tests
└── test_integration.py       # Integration tests
```

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_devices.py -v
```

### Run Tests by Marker
```bash
# Unit tests only
pytest tests/ -m unit

# Integration tests only
pytest tests/ -m integration

# Device tests only
pytest tests/ -m devices

# Tests requiring authentication
pytest tests/ -m requires_auth
```

### Run with Coverage Report
```bash
pytest tests/ --cov=SmartThingsMCP --cov-report=html
```

### Run and Stop on First Failure
```bash
pytest tests/ -x
```

### Run Tests in Parallel
```bash
pytest tests/ -n auto
```

### Skip Slow Tests
```bash
pytest tests/ -m "not slow"
```

## Test Categories

### Unit Tests (test_devices.py, test_locations.py, etc.)
Tests for individual components and functions:
- **Common utilities**: URL building, parameter filtering, HTTP requests
- **Device tools**: Listing, filtering, commanding devices
- **Location tools**: Location queries and management
- **Room tools**: Room operations and device associations
- **Rule tools**: Rule creation, editing, execution
- **Client operations**: Caching, authentication, API calls
- **Data filtering and validation**: Sorting, filtering, searching

### Integration Tests (test_integration.py)
Tests that interact with external services:
- Real SmartThings API calls (requires auth token)
- Server startup and initialization
- Client-server communication
- Full workflow end-to-end tests

### Fixtures (conftest.py)
Reusable test data and mocks:
- `mock_auth_token`: Authentication token
- `mock_location`: Sample location object
- `mock_device`: Sample device object
- `mock_room`: Sample room object
- `mock_rule`: Sample rule object
- `mock_server`: Mock MCP server instance
- And many more...

## Test Markers

Decorate tests with markers for easy categorization:

```python
@pytest.mark.unit
@pytest.mark.devices
def test_list_devices():
    pass

@pytest.mark.integration
@pytest.mark.requires_auth
def test_list_devices_integration():
    pass

@pytest.mark.slow
def test_large_dataset():
    pass
```

## Mocking

Tests use `unittest.mock` for mocking API calls:

```python
from unittest.mock import Mock, patch

@patch('SmartThingsMCP.modules.server.common.make_request')
def test_list_devices(self, mock_request):
    mock_request.return_value = {
        "items": [{"id": "d1", "name": "Device 1"}]
    }
    # Test code here
```

## Test Coverage

To generate a coverage report:

```bash
pytest tests/ --cov=SmartThingsMCP --cov-report=html
```

Coverage reports are created in `htmlcov/index.html`

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```bash
# GitHub Actions example
pytest tests/ -v --tb=short --cov=SmartThingsMCP
```

## Environment Variables

For integration tests, set the following environment variables:

```bash
export SMARTTHINGS_AUTH_TOKEN="your-token-here"
```

## Common Test Patterns

### Testing API Calls
```python
@patch('SmartThingsMCP.modules.server.common.make_request')
def test_api_call(self, mock_request):
    mock_request.return_value = {"status": "success"}
    result = some_function()
    assert result == {"status": "success"}
```

### Testing Caching
```python
def test_cache_hit(self):
    cache = {}
    cache["key"] = "value"
    assert cache.get("key") == "value"
```

### Testing Filtering
```python
def test_filter_devices(self):
    devices = [{"id": "1", "status": "online"}, {"id": "2", "status": "offline"}]
    filtered = [d for d in devices if d["status"] == "online"]
    assert len(filtered) == 1
```

### Testing Validation
```python
def test_rule_validation(self):
    rule = {"name": "Test", "triggers": [], "actions": []}
    assert len(rule["triggers"]) >= 0
    assert len(rule["actions"]) >= 0
```

## Troubleshooting

### Test Import Errors
Make sure the SmartThingsMCP module is in the Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

### Fixture Not Found
Ensure fixtures are defined in `conftest.py` and accessible to all tests.

### Mock Not Working
Check that the mock path matches the import path:
```python
# If imported as:
from SmartThingsMCP.modules.server.common import make_request
# Then mock as:
@patch('SmartThingsMCP.modules.server.common.make_request')
```

### Tests Passing Locally but Failing in CI
- Check environment variables are set correctly
- Verify Python version compatibility
- Ensure all dependencies are installed

## Writing New Tests

### Template for Device Tests
```python
class TestNewFeature:
    """Test description."""
    
    @patch('SmartThingsMCP.modules.server.common.make_request')
    def test_something(self, mock_request):
        """Test specific functionality."""
        mock_request.return_value = {"expected": "result"}
        
        # Call function
        result = some_function()
        
        # Assert results
        assert result == {"expected": "result"}
```

### Using Fixtures
```python
def test_with_fixture(self, mock_device):
    """Test using a fixture."""
    assert mock_device["id"] == "device-1"
    assert mock_device["status"] == "online"
```

## Performance Testing

Some tests are marked as slow. Run them separately:

```bash
# Run slow tests only
pytest tests/ -m slow

# Run everything except slow tests
pytest tests/ -m "not slow"
```

## Contributing Tests

When adding new features:

1. Write unit tests for the feature
2. Add integration tests if it involves API calls
3. Use fixtures for reusable test data
4. Mark tests appropriately (@pytest.mark.devices, etc.)
5. Ensure tests pass locally before submitting
6. Include docstrings explaining what is being tested

## Reference

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Markers](https://docs.pytest.org/en/stable/marker.html)
