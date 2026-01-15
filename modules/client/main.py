"""
Main SmartThingsMCP Client class that combines all modules
"""
from .base import BaseClient
from .cache import CacheMixin
from .devices import DevicesMixin
from .locations import LocationsMixin
from .rooms import RoomsMixin
from .modes import ModesMixin
from .rules import RulesMixin
from .scenes import ScenesMixin


class SmartThingsMCPClient(
    CacheMixin,  # Cache must be first for proper MRO
    BaseClient,
    DevicesMixin,
    LocationsMixin,
    RoomsMixin,
    ModesMixin,
    RulesMixin,
    ScenesMixin
):
    """
    SmartThings MCP Client with all capabilities including caching.
    
    Combines the base client with all mixins to provide a complete
    client for interacting with SmartThingsMCPServer.
    
    Features:
    - Automatic caching of read-only operations (5 min TTL)
    - Cache invalidation on write operations
    - LRU eviction when cache is full
    - Cache statistics tracking
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, 
                auth_token: str = None, transport: str = "stdio",
                enable_cache: bool = True, cache_ttl: int = 300,
                max_cache_size: int = 1000):
        """
        Initialize the SmartThings MCP Client with caching.
        
        Args:
            host: Host where the MCP server is running
            port: Port where the MCP server is running
            auth_token: Authentication token for SmartThings API (OAuth 2.0 bearer token)
            transport: Transport to use (stdio, http, or sse)
            enable_cache: Enable caching (default: True)
            cache_ttl: Cache time-to-live in seconds (default: 300 = 5 min)
            max_cache_size: Maximum cache size (default: 1000 entries)
        """
        # Initialize the base client with cache settings
        super().__init__(host, port, auth_token, transport,
                        enable_cache=enable_cache,
                        cache_ttl=cache_ttl,
                        max_cache_size=max_cache_size)
