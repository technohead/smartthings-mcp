"""
Test cache invalidation on write operations.

Verifies that DELETE operations properly clear the cache.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.server import common


class TestCacheInvalidation:
    """Test cache clearing on write operations"""
    
    def setup_method(self):
        """Clear cache before each test"""
        common._clear_cache()
    
    def test_get_request_caches_response(self):
        """Test that GET requests are cached"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # First request - should hit API
            result1 = common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/test")
            
            # Second request - should hit cache
            result2 = common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/test")
            
            # API should only be called once
            assert mock_request.call_count == 1
            assert result1 == result2
    
    def test_delete_clears_cache(self):
        """Test that DELETE operation clears all cache"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # First: Cache some GET requests
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/devices")
            
            # Verify cache has entries
            stats = common.get_cache_stats()
            assert stats['size'] == 2
            
            # Now perform DELETE operation
            common.make_request("Bearer token", "DELETE", "https://api.smartthings.com/v1/rules/123")
            
            # Verify cache is empty
            stats_after = common.get_cache_stats()
            assert stats_after['size'] == 0
    
    def test_post_clears_cache(self):
        """Test that POST operation clears cache"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # Cache a GET request
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            
            # POST operation
            common.make_request("Bearer token", "POST", "https://api.smartthings.com/v1/rules", 
                              data={"name": "test"})
            
            # Cache should be cleared
            assert common.get_cache_stats()['size'] == 0
    
    def test_put_clears_cache(self):
        """Test that PUT operation clears cache"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # Cache a GET request
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            
            # PUT operation
            common.make_request("Bearer token", "PUT", "https://api.smartthings.com/v1/rules/123",
                              data={"name": "updated"})
            
            # Cache should be cleared
            assert common.get_cache_stats()['size'] == 0
    
    def test_delete_rule_clears_cache(self):
        """Test that delete_rule properly clears cache"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "deleted"}'
            mock_response.json.return_value = {"result": "deleted"}
            mock_request.return_value = mock_response
            
            # Cache a list_rules result
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            
            # Delete a rule (simulating the delete_rule function behavior)
            common.make_request("Bearer token", "DELETE", "https://api.smartthings.com/v1/rules/rule123",
                              params={"locationId": "location123"})
            
            # Cache should be cleared
            assert common.get_cache_stats()['size'] == 0
    
    def test_failed_delete_still_clears_cache(self):
        """Test that cache is cleared even if DELETE fails"""
        with patch('modules.server.common.requests.request') as mock_request:
            # Setup: Cache a GET request
            mock_response_get = Mock()
            mock_response_get.status_code = 200
            mock_response_get.content = b'{"result": "test"}'
            mock_response_get.json.return_value = {"result": "test"}
            
            # DELETE will fail
            mock_response_delete = Mock()
            mock_response_delete.status_code = 404
            mock_response_delete.raise_for_status.side_effect = Exception("Not found")
            
            mock_request.side_effect = [mock_response_get, mock_response_delete]
            
            # Cache a GET
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            
            # Try to DELETE (will fail)
            with pytest.raises(Exception):
                common.make_request("Bearer token", "DELETE", "https://api.smartthings.com/v1/rules/123")
            
            # Cache should still be cleared (happens before the request)
            assert common.get_cache_stats()['size'] == 0
    
    def test_cache_refills_after_clear(self):
        """Test that cache refills correctly after being cleared"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # Cache initial GET
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            assert mock_request.call_count == 1
            
            # Clear cache with DELETE
            common.make_request("Bearer token", "DELETE", "https://api.smartthings.com/v1/rules/123")
            assert common.get_cache_stats()['size'] == 0
            assert mock_request.call_count == 2
            
            # GET again - should refill cache
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            assert mock_request.call_count == 3
            
            # GET again - should hit cache (no new API call)
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/rules")
            assert common.get_cache_stats()['size'] == 1
            assert mock_request.call_count == 3  # Still 3, used cache


class TestCacheStats:
    """Test cache statistics"""
    
    def setup_method(self):
        """Clear cache before each test"""
        common._clear_cache()
    
    def test_cache_stats_structure(self):
        """Test that cache stats returns expected structure"""
        stats = common.get_cache_stats()
        
        assert 'enabled' in stats
        assert 'size' in stats
        assert 'max_size' in stats
        assert 'ttl_seconds' in stats
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'total_requests' in stats
        assert 'hit_rate_percent' in stats
    
    def test_cache_hit_rate(self):
        """Test cache hit rate calculation"""
        with patch('modules.server.common.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b'{"result": "test"}'
            mock_response.json.return_value = {"result": "test"}
            mock_request.return_value = mock_response
            
            # First request - miss
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/test")
            
            # Second request - hit
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/test")
            
            # Third request - hit
            common.make_request("Bearer token", "GET", "https://api.smartthings.com/v1/test")
            
            stats = common.get_cache_stats()
            assert stats['hits'] == 2
            assert stats['misses'] == 1
            assert stats['total_requests'] == 3
            assert stats['hit_rate_percent'] == pytest.approx(66.67, abs=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
