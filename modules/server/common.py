"""
Common module for SmartThings MCP server.
Contains utility functions used across the server modules.
"""
import requests
import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional, List
from collections import OrderedDict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL for SmartThings API
BASE_URL = "https://api.smartthings.com/v1"

# Server-side cache
_server_cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
_cache_ttl = 300  # 5 minutes default
_cache_max_size = 1000
_cache_enabled = True
_cache_hits = 0
_cache_misses = 0


def _generate_cache_key(method: str, url: str, params: Optional[Dict[str, Any]]) -> str:
    """Generate cache key for a request."""
    cache_data = {
        'method': method,
        'url': url,
        'params': params or {}
    }
    cache_string = json.dumps(cache_data, sort_keys=True)
    cache_hash = hashlib.md5(cache_string.encode()).hexdigest()[:12]
    return f"{method}:{cache_hash}"


def _is_cache_valid(timestamp: float) -> bool:
    """Check if cached entry is still valid."""
    return (time.time() - timestamp) < _cache_ttl


def _get_from_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get value from cache if valid."""
    global _cache_hits, _cache_misses
    
    if not _cache_enabled:
        return None
    
    if cache_key in _server_cache:
        result, timestamp = _server_cache[cache_key]
        
        if _is_cache_valid(timestamp):
            # Move to end (LRU)
            _server_cache.move_to_end(cache_key)
            _cache_hits += 1
            return result
        else:
            # Expired - remove from cache
            del _server_cache[cache_key]
    
    _cache_misses += 1
    return None


def _put_in_cache(cache_key: str, result: Dict[str, Any]) -> None:
    """Store value in cache."""
    if not _cache_enabled:
        return
    
    # Add to cache with current timestamp
    _server_cache[cache_key] = (result, time.time())
    
    # Move to end (most recently used)
    _server_cache.move_to_end(cache_key)
    
    # Evict oldest entries if cache is full (LRU)
    while len(_server_cache) > _cache_max_size:
        _server_cache.popitem(last=False)


def _clear_cache() -> None:
    """Clear all cache entries."""
    global _cache_hits, _cache_misses
    _server_cache.clear()
    _cache_hits = 0
    _cache_misses = 0


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    total = _cache_hits + _cache_misses
    hit_rate = (_cache_hits / total * 100) if total > 0 else 0
    
    return {
        'enabled': _cache_enabled,
        'size': len(_server_cache),
        'max_size': _cache_max_size,
        'ttl_seconds': _cache_ttl,
        'hits': _cache_hits,
        'misses': _cache_misses,
        'total_requests': total,
        'hit_rate_percent': round(hit_rate, 2),
    }


def make_request(auth: str, method: str, url: str, params: Optional[Dict[str, Any]] = None, 
                 data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a request to SmartThings API endpoints with caching.
    
    Args:
        auth: OAuth 2.0 bearer token for authentication
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        url: The endpoint URL
        params: Query parameters
        data: Request body data
        headers: Additional headers
        
    Returns:
        API response as dictionary
    """
    # Check cache for GET requests
    if method.upper() == 'GET':
        cache_key = _generate_cache_key(method, url, params)
        cached_result = _get_from_cache(cache_key)
        
        if cached_result is not None:
            # Display cache hit in green
            endpoint = url.replace(BASE_URL + '/', '')
            print(f"\033[92m✓ Server cache hit: {method} {endpoint}\033[0m")
            logger.info(f"Cache hit for {method} {url}")
            return cached_result
    
    # Clear cache on write operations
    if method.upper() in ['POST', 'PUT', 'DELETE', 'PATCH']:
        # Invalidate cache on write operations
        cache_size_before = len(_server_cache)
        _clear_cache()
        logger.info(f"Cache cleared due to {method} operation (cleared {cache_size_before} cached entries)")
    
    if headers is None:
        headers = {}
    
    # Add authorization header with bearer token
    auth_header = f"Bearer {auth}"
    headers["Authorization"] = auth_header
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    
    logger.info(f"Making {method} request to: {url}")
    logger.info(f"Auth header: {auth_header[:15]}...")
    
    if params:
        logger.info(f"Request params: {params}")
    if data:
        logger.info(f"Request data: {data}")
    
    try:
        logger.info("Sending request to SmartThings API...")
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=headers
        )
        
        logger.info(f"Response status code: {response.status_code}")
        
        # Add extra logging for authentication issues
        if response.status_code == 401:
            logger.error("Authentication error (401 Unauthorized)")
            logger.error("Please verify that your SmartThings token:")
            logger.error(" - Is valid and not expired")
            logger.error(" - Has the required permissions for this operation")
            logger.error(" - Is properly formatted in the authorization header")
            if hasattr(response, 'text'):
                logger.error(f"Response body: {response.text}")
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        if response.content:
            result = response.json()
            logger.info("Successfully processed API response")
            
            # Cache GET responses
            if method.upper() == 'GET':
                cache_key = _generate_cache_key(method, url, params)
                _put_in_cache(cache_key, result)
                logger.info(f"Cached response for {method} {url}")
            
            return result
        return {}
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        error_message = str(e)
        logger.error(f"Request exception: {error_message}")
        
        try:
            if hasattr(e.response, 'json'):
                error_data = e.response.json()
                if 'message' in error_data:
                    error_message = error_data['message']
                    logger.error(f"API error message: {error_message}")
        except Exception as json_error:
            logger.error(f"Error parsing error response: {str(json_error)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Raw error response: {e.response.text}")
            
        raise Exception(f"SmartThings API request failed: {error_message}")


def build_url(endpoint: str, *path_params) -> str:
    """
    Build a SmartThings API URL.
    
    Args:
        endpoint: The API endpoint path (e.g., 'devices')
        path_params: Additional path parameters to append
        
    Returns:
        Complete URL string
    """
    url_parts = [BASE_URL, endpoint]
    url_parts.extend([str(param) for param in path_params if param is not None])
    return '/'.join(url_parts)


def build_device_url(device_id: str, *path_params) -> str:
    """
    Build a SmartThings API URL for a specific device.
    
    Args:
        device_id: The device ID
        path_params: Additional path parameters to append
        
    Returns:
        Complete device URL string
    """
    return build_url('devices', device_id, *path_params)


def filter_none_params(**kwargs) -> Dict[str, Any]:
    """
    Build a parameter dictionary filtering out None values.
    
    Args:
        **kwargs: Key-value pairs where values can be None
        
    Returns:
        Dictionary with only non-None values
    """
    return {k: v for k, v in kwargs.items() if v is not None}


def build_command_payload(component: str, capability: str, command: str, 
                         arguments: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    Build a command payload for device command execution.
    
    Args:
        component: Component ID
        capability: Capability ID
        command: Command name
        arguments: Command arguments
        
    Returns:
        Command payload dictionary
    """
    return {
        "commands": [
            {
                "component": component,
                "capability": capability,
                "command": command,
                "arguments": arguments or []
            }
        ]
    }
