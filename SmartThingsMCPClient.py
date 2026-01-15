#!/usr/bin/env python3
"""
SmartThings MCP Client
A client for interacting with the SmartThingsMCPServer using FastMCP 2.0.
"""
import argparse
import json
import sys
import asyncio
from typing import Dict, Any, List

# Import modular client components
try:
    from modules.client.main import SmartThingsMCPClient
    from modules.client.utils import convert_tool_to_dict, run_action
except ImportError:
    # If running from package instead of direct
    try:
        from SmartThingsMCP.modules.client.main import SmartThingsMCPClient
        from SmartThingsMCP.modules.client.utils import convert_tool_to_dict, run_action
    except ImportError:
        print("Error: Cannot import SmartThingsMCP client modules.")
        print("Make sure you are running from the correct directory.")
        sys.exit(1)


async def main():
    """Main entry point for the SmartThingsMCP client."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SmartThings MCP Client")
    parser.add_argument("--host", type=str, default="localhost", help="MCP server host")
    parser.add_argument("--port", type=int, default=8000, help="MCP server port")
    parser.add_argument("--auth", type=str, help="SmartThings API authentication token")
    parser.add_argument("--transport", type=str, default="http", 
                        choices=["stdio", "http", "sse"], help="Transport to use")
    parser.add_argument("--action", type=str, required=True, 
                        help="Action to perform (e.g., list_devices, get_device)")
    parser.add_argument("--params", type=str, default="{}", 
                        help="Parameters for the action (JSON string)")
    parser.add_argument("--pretty", action="store_true", 
                        help="Pretty-print the JSON output")
    
    args = parser.parse_args()
    
    # Parse parameters from JSON string
    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(f"Error parsing parameters: {e}")
        print("Parameters must be a valid JSON string")
        sys.exit(1)
    
    # Create client
    client = SmartThingsMCPClient(args.host, args.port, args.auth, args.transport)
    
    # Run the action
    try:
        result = await run_action(client, args.action, params)
        
        # Convert result to serializable format
        result = convert_tool_to_dict(result)
        
        # Output result
        if args.pretty:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))
    except Exception as e:
        print(f"Error executing action: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
