"""
Base client module for SmartThingsMCP
"""
import sys
from typing import Dict, Any, Optional, List, Union

# Import FastMCP client
try:
    from fastmcp.client import Client as FastMCPClient
except ImportError:
    print("Error: fastmcp package not found.")
    print("Please install it with: pip install fastmcp>=2.0.0")
    sys.exit(1)


class BaseClient:
    """
    Base client for SmartThings MCP API interactions.
    Handles connection and common operations.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, 
                 auth_token: str = None, transport: str = "stdio", **kwargs):
        """
        Initialize the SmartThings MCP Client.
        
        Args:
            host: Host where the MCP server is running
            port: Port where the MCP server is running
            auth_token: Authentication token for SmartThings API (OAuth 2.0 bearer token)
            transport: Transport to use (stdio, http, or sse)
            **kwargs: Additional parameters (e.g., cache settings)
        """
        self.auth_token = auth_token
        self.host = host
        self.port = port
        self.transport = transport
        self.client = None
        
        # Don't call super().__init__() here as other mixins don't have __init__
        # and it would eventually reach object.__init__() which doesn't accept kwargs
        
        self._init_client()
    
    def _init_client(self):
        """Initialize the FastMCP client with the appropriate transport"""
        if self.transport == "stdio":
            # Use stdio transport
            self.client = FastMCPClient(
                transport="stdio",
                auth=f"Bearer {self.auth_token}" if self.auth_token else None
            )
            print(f"Initialized FastMCP 2.0 client with stdio transport")
        elif self.transport == "http":
            # Use HTTP transport
            # For FastMCP HTTP transport, need to include the '/mcp' path
            server_url = f"http://{self.host}:{self.port}/mcp"
            self.client = FastMCPClient(
                server_url,
                auth=f"Bearer {self.auth_token}" if self.auth_token else None
            )
            print(f"Initialized FastMCP 2.0 client with HTTP transport at {server_url}")
        elif self.transport == "sse":
            # Use SSE transport
            server_url = f"http://{self.host}:{self.port}/sse"
            self.client = FastMCPClient(
                server_url,
                auth=f"Bearer {self.auth_token}" if self.auth_token else None
            )
            print(f"Initialized FastMCP 2.0 client with SSE transport at {server_url}")
        else:
            raise ValueError(f"Unsupported transport: {self.transport}. Must be one of: stdio, http, sse")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the MCP server.
        
        Returns:
            List of tools as dictionaries
        """
        try:
            async with self.client as client:
                tools = await client.list_tools()
                
                # Convert Tool objects to dictionaries
                from .utils import convert_tool_to_dict
                return [convert_tool_to_dict(tool) for tool in tools]
        except Exception as e:
            print(f"Error listing tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a tool on the MCP server with caching support.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool response
        """
        # Remove auth from kwargs to avoid passing it to the FastMCP client directly
        # We already set auth during client initialization
        if 'auth' in kwargs:
            # Extract and save auth for the tool parameters only
            auth_value = kwargs.pop('auth')
            # Create parameters dict with auth for the tool
            params = {"auth": auth_value}
            # Add any other parameters
            params.update(kwargs)
        else:
            params = kwargs
        
        # Check if operation is cacheable
        is_cacheable = tool_name in getattr(self, 'CACHEABLE_OPERATIONS', set())
        is_write_op = tool_name in getattr(self, 'CACHE_INVALIDATING_OPERATIONS', set())
        
        # Try to get from cache if cacheable
        if is_cacheable and hasattr(self, '_get_from_cache'):
            cache_key = self._generate_cache_key(tool_name, params)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result is not None:
                # Display cache hit in green
                print(f"\033[92m✓ Cache hit: {tool_name}\033[0m")
                return cached_result
        
        # Call the actual tool
        try:
            async with self.client as client:
                result = await client.call_tool(tool_name, params)
                
                # Cache the result if cacheable
                if is_cacheable and hasattr(self, '_put_in_cache'):
                    cache_key = self._generate_cache_key(tool_name, params)
                    self._put_in_cache(cache_key, result)
                
                # Invalidate cache if this is a write operation
                if is_write_op and hasattr(self, '_invalidate_cache_for_operation'):
                    self._invalidate_cache_for_operation(tool_name)
                
                return result
        except Exception as e:
            print(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}
