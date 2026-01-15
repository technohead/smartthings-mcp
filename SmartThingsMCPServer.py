#!/usr/bin/env python3
"""
SmartThings MCP Server
A FastMCP 2.0 server that exposes SmartThings API endpoints as MCP tools.
"""
import sys
import argparse
import os

# Import both FastMCP and fastmcp module for compatibility
import importlib.util
fastmcp = None

# Import FastMCP from the expected location for mcp dev
try:
    # This is the import path expected by mcp dev
    from mcp.server.fastmcp.server import FastMCP
    print("Imported FastMCP from mcp.server.fastmcp.server")
except ImportError:
    try:
        # Fallback to direct fastmcp import for standalone mode
        from fastmcp.server.server import FastMCP
        print("Imported FastMCP from fastmcp.server.server")
    except ImportError:
        print("Error: Failed to import FastMCP from any known location")
        import sys
        sys.exit(1)

# This is critical: Check for MCP_DEV environment variable which is set by mcp dev command
IS_MCP_DEV = os.environ.get('MCP_DEV') == '1'
print(f"Running in MCP dev mode: {IS_MCP_DEV}")

# Try both import paths
try:
    from SmartThingsMCP.modules.server.devices import register_tools as register_devices_tools
    from SmartThingsMCP.modules.server.locations import register_tools as register_locations_tools
    from SmartThingsMCP.modules.server.rooms import register_tools as register_rooms_tools
    from SmartThingsMCP.modules.server.modes import register_tools as register_modes_tools
    from SmartThingsMCP.modules.server.rules import register_tools as register_rules_tools
    from SmartThingsMCP.modules.server.scenes import register_tools as register_scenes_tools
    from SmartThingsMCP.modules.server.structure_tools import register_tools as register_structure_tools
except ImportError:
    # When using mcp dev, the path structure is different
    from modules.server.devices import register_tools as register_devices_tools
    from modules.server.locations import register_tools as register_locations_tools
    from modules.server.rooms import register_tools as register_rooms_tools
    from modules.server.modes import register_tools as register_modes_tools
    from modules.server.rules import register_tools as register_rules_tools
    from modules.server.scenes import register_tools as register_scenes_tools
    from modules.server.structure_tools import register_tools as register_structure_tools

# Global authentication token override
AUTH_TOKEN_OVERRIDE = None

# Global server instance - REQUIRED for mcp dev to work properly
# When running with mcp dev, this variable must be set at the module level
# and must be named 'server'
print("Creating global server instance at module level")
server = FastMCP(name="SmartThingsMCP")
print(f"Server initialized: {server}")
print(f"Server type: {type(server)}")

# Explicitly check for the expected server type
expected_type = "mcp.server.fastmcp.server.FastMCP"
actual_type = str(type(server))
print(f"Expected type: <class '{expected_type}'>, Actual type: {actual_type}")

# Register tools at the module level to ensure they're available
# This is crucial for mcp dev mode
print("Registering tools at the module level")
register_devices_tools(server)
register_locations_tools(server)
register_rooms_tools(server)
register_modes_tools(server)
register_rules_tools(server)
register_scenes_tools(server)
register_structure_tools(server)  # Structure generation tools for LLM

# Just check if the server has tools methods
print(f"Server has list_tools method: {hasattr(server, 'list_tools')}")
print(f"Server has get_tools method: {hasattr(server, 'get_tools')}")
print(f"Server has tool decorator: {hasattr(server, 'tool')}")
print(f"Registered test tool and standard device tools")
# Don't try to call list_tools() directly as it's a coroutine

class SmartThingsMCPServer:
    """
    SmartThings MCP Server implementation using FastMCP 2.0.
    Exposes SmartThings API endpoints as MCP tools.
    """
    def __init__(self, port: int = 8000, auth: str = None):
        """
        Initialize the SmartThings MCP Server.
        
        Args:
            port: Port to run the MCP server on
            auth: Authentication token override
        """
        global AUTH_TOKEN_OVERRIDE
        AUTH_TOKEN_OVERRIDE = auth
        self.port = port
        
        # Note: No need to recreate the server or register tools here
        # Tools are already registered at the module level
        # This is necessary for mcp dev compatibility
        print(f"SmartThingsMCPServer initialized with port {port}")
        print(f"Global server: {server}")
        
        # List existing tools
        try:
            tools = server.list_tools()
            print(f"Current registered tools: {tools}")
        except Exception as e:
            print(f"Error listing tools: {e}")
        
    def start_server(self, transport: str = "http"):
        """
        Start the MCP server with the specified transport.
        
        Args:
            transport: Transport to use (stdio, http, or sse)
        """
        global server
        print(f"Starting server (type: {type(server)}) with transport {transport}")
        
        # When running with mcp dev, the environment is already set up
        # We just need to keep the process alive
        # Try to import fastmcp dynamically if not already imported
        global fastmcp
        if fastmcp is None:
            try:
                import fastmcp as fastmcp_module
                fastmcp = fastmcp_module
            except ImportError:
                print("fastmcp module not found, running in standalone mode")
                
        # Check if we're in MCP Inspector environment
        if fastmcp and hasattr(fastmcp, 'current'):
            print("Running in MCP Inspector environment")
            print(f"MCP current server: {fastmcp.current}")
            print(f"Our server instance: {server}")
            
            # Just keep the process alive - don't run the server
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Exiting due to keyboard interrupt")
        else:
            # For standalone mode
            if transport == "stdio":
                print("Running server with stdio transport")
                server.run(transport="stdio")
            elif transport == "sse":
                print(f"Running server with sse transport on port {self.port}")
                server.run(transport="sse")
            elif transport == "http":
                print(f"Running server with http transport on port {self.port}")
                # The FastMCP.run() method doesn't take a port parameter directly
                # For http transport we need to configure it to use the specified port
                import uvicorn
                app = server.streamable_http_app
                uvicorn.run(app, host="0.0.0.0", port=self.port)
            else:
                print(f"Unknown transport: {transport}")
                sys.exit(1)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="SmartThings MCP Server")
    parser.add_argument("-port", type=int, default=8000, 
                      help="Port to run the MCP server on (default: 8000)")
    parser.add_argument("-auth", type=str, help="Authentication token override")
    parser.add_argument("-transport", type=str, default="http",
                      choices=["stdio", "sse", "http"], 
                      help="Transport to use (default: http)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    server_instance = SmartThingsMCPServer(port=args.port, auth=args.auth)
    server_instance.start_server(transport=args.transport)
