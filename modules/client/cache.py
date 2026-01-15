"""
Caching module for SmartThingsMCP Client
Implements TTL-based caching for read-only API operations
"""
import time
import json
import hashlib
from typing import Dict, Any, Optional, Tuple
from collections import OrderedDict


class CacheMixin:
    """
    Mixin class that adds caching capabilities to SmartThingsMCPClient.
    Uses TTL-based caching with automatic invalidation for write operations.
    """
    
    # Default cache TTL in seconds (5 minutes)
    DEFAULT_CACHE_TTL = 300
    
    # Operations that should be cached (read-only operations)
    CACHEABLE_OPERATIONS = {
        'list_locations',
        'get_location',
        'list_devices',
        'get_device',
        'get_location_rooms',
        'get_room',
        'list_modes',
        'get_current_mode',
        'list_scenes',
        'get_scene',
        'list_rules',
        'get_rule',
        'get_device_components',
        'get_device_capabilities',
        'get_device_health',
    }
    
    # Operations that invalidate cache (write operations)
    CACHE_INVALIDATING_OPERATIONS = {
        'execute_command',
        'create_location',
        'update_location',
        'delete_location',
        'create_room',
        'update_room',
        'delete_room',
        'set_mode',
        'execute_scene',
        'update_device',
        'delete_device',
        'create_rule',
        'update_rule',
        'delete_rule',
        'execute_rule',
    }
    
    # Cache invalidation patterns: which operations invalidate which cached data
    INVALIDATION_PATTERNS = {
        'execute_command': ['get_device_status', 'get_device'],
        'update_device': ['list_devices', 'get_device'],
        'delete_device': ['list_devices'],
        'create_location': ['list_locations'],
        'update_location': ['list_locations', 'get_location'],
        'delete_location': ['list_locations'],
        'create_room': ['get_location_rooms'],
        'update_room': ['get_location_rooms', 'get_room'],
        'delete_room': ['get_location_rooms'],
        'set_mode': ['get_current_mode'],
        'create_rule': ['list_rules'],
        'update_rule': ['list_rules', 'get_rule'],
        'delete_rule': ['list_rules', 'get_rule'],
        'execute_rule': [],  # Executing a rule doesn't change rule list
    }
    
    def __init__(self, *args, **kwargs):
        """Initialize cache storage"""
        # Extract cache-specific kwargs before passing to parent
        cache_ttl = kwargs.pop('cache_ttl', self.DEFAULT_CACHE_TTL)
        enable_cache = kwargs.pop('enable_cache', True)
        max_cache_size = kwargs.pop('max_cache_size', 1000)
        
        # Call parent __init__ with remaining args/kwargs
        super().__init__(*args, **kwargs)
        
        # Cache storage: {cache_key: (result, timestamp)}
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        
        # Cache TTL in seconds
        self._cache_ttl = cache_ttl
        
        # Enable/disable caching
        self._cache_enabled = enable_cache
        
        # Max cache size (LRU eviction)
        self._max_cache_size = max_cache_size
        
        # Cache statistics
        self._cache_hits = 0
        self._cache_misses = 0
    
    def _generate_cache_key(self, tool_name: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key for a tool call.
        
        Args:
            tool_name: Name of the tool
            params: Parameters passed to the tool
            
        Returns:
            Cache key string
        """
        # Sort params for consistent key generation
        sorted_params = json.dumps(params, sort_keys=True)
        
        # Create hash of params for shorter key
        params_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:8]
        
        return f"{tool_name}:{params_hash}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """
        Check if cached entry is still valid based on TTL.
        
        Args:
            timestamp: Timestamp when entry was cached
            
        Returns:
            True if cache entry is still valid
        """
        return (time.time() - timestamp) < self._cache_ttl
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """
        Get value from cache if valid.
        
        Args:
            cache_key: Cache key to lookup
            
        Returns:
            Cached value if valid, None otherwise
        """
        if not self._cache_enabled:
            return None
        
        if cache_key in self._cache:
            result, timestamp = self._cache[cache_key]
            
            if self._is_cache_valid(timestamp):
                # Move to end (LRU)
                self._cache.move_to_end(cache_key)
                self._cache_hits += 1
                return result
            else:
                # Expired - remove from cache
                del self._cache[cache_key]
        
        self._cache_misses += 1
        return None
    
    def _put_in_cache(self, cache_key: str, result: Any) -> None:
        """
        Store value in cache.
        
        Args:
            cache_key: Cache key
            result: Result to cache
        """
        if not self._cache_enabled:
            return
        
        # Add to cache with current timestamp
        self._cache[cache_key] = (result, time.time())
        
        # Move to end (most recently used)
        self._cache.move_to_end(cache_key)
        
        # Evict oldest entries if cache is full (LRU)
        while len(self._cache) > self._max_cache_size:
            self._cache.popitem(last=False)
    
    def _invalidate_cache_pattern(self, pattern: str) -> None:
        """
        Invalidate all cache entries matching a pattern.
        
        Args:
            pattern: Tool name pattern to invalidate
        """
        if not self._cache_enabled:
            return
        
        # Find and remove all matching cache entries
        keys_to_remove = [
            key for key in self._cache.keys()
            if key.startswith(f"{pattern}:")
        ]
        
        for key in keys_to_remove:
            del self._cache[key]
    
    def _invalidate_cache_for_operation(self, tool_name: str) -> None:
        """
        Invalidate cache entries affected by a write operation.
        
        Args:
            tool_name: Name of the write operation
        """
        if tool_name in self.INVALIDATION_PATTERNS:
            patterns = self.INVALIDATION_PATTERNS[tool_name]
            for pattern in patterns:
                self._invalidate_cache_pattern(pattern)
    
    def clear_cache(self) -> None:
        """Clear all cached entries"""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'enabled': self._cache_enabled,
            'size': len(self._cache),
            'max_size': self._max_cache_size,
            'ttl_seconds': self._cache_ttl,
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'total_requests': total_requests,
            'hit_rate_percent': round(hit_rate, 2),
        }
    
    def set_cache_enabled(self, enabled: bool) -> None:
        """
        Enable or disable caching.
        
        Args:
            enabled: True to enable caching, False to disable
        """
        self._cache_enabled = enabled
        if not enabled:
            self.clear_cache()
    
    def set_cache_ttl(self, ttl_seconds: int) -> None:
        """
        Set cache TTL.
        
        Args:
            ttl_seconds: Time-to-live in seconds
        """
        self._cache_ttl = ttl_seconds
