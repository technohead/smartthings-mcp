#!/bin/bash
# Script to restart the SmartThingsMCPServer

# Define terminal colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SmartThingsMCP Server Manager ===${NC}"

# Default port and transport
PORT=8000
TRANSPORT="http"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--port)
      PORT="$2"
      shift 2
      ;;
    -t|--transport)
      TRANSPORT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo -e "${BLUE}Using port: ${PORT} and transport: ${TRANSPORT}${NC}"

# Check if server is running
echo "Checking if SmartThingsMCPServer is running..."

if nc -z localhost 8000 2>/dev/null; then
    echo -e "${YELLOW}SmartThingsMCPServer detected on port 8000${NC}"
    read -p "Stop existing MCP server (y/n)? " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo "Stopping SmartThingsMCPServer..."
        pkill -f "python.*SmartThingsMCPServer\.py" || true
        sleep 1
    fi
else
    echo -e "${YELLOW}No SmartThingsMCPServer detected on port 8000${NC}"
fi

# Ask to start server
read -p "Start a new SmartThingsMCPServer instance (y/n)? " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then
    echo "Starting SmartThingsMCPServer in a new terminal window..."
    # Use the appropriate command for macOS to open a new terminal with specified transport and port
    osascript -e 'tell app "Terminal" to do script "cd '$PWD' && python SmartThingsMCPServer.py -port '$PORT' -transport '$TRANSPORT'"'
    echo "Waiting for server to start..."
    sleep 3
    
    # Check if server started
    if nc -z localhost $PORT 2>/dev/null; then
        echo -e "${GREEN}SmartThingsMCPServer started successfully on port $PORT using $TRANSPORT transport${NC}"
        echo "Testing server connectivity..."
        
        # Test with SmartThingsMCPClient
        echo -e "${BLUE}Testing with SmartThingsMCPClient...${NC}"
        python SmartThingsMCPClient.py --transport $TRANSPORT --port $PORT --action list_tools
        
        # Give useful information for using the client
        echo -e "\n${GREEN}Server is ready!${NC}"
        echo -e "${YELLOW}To list devices, use:${NC}"
        echo "python SmartThingsMCPClient.py --auth YOUR_TOKEN --transport $TRANSPORT --action list_devices"
    else
        echo -e "${RED}Failed to detect SmartThingsMCPServer on port $PORT${NC}"
        echo "Check the terminal window for error messages"
    fi
fi

echo -e "${GREEN}Done.${NC}"

echo -e "${BLUE}Usage examples:${NC}"
echo "./restart_mcp_server.sh                     # Use default port 8000 and http transport"
echo "./restart_mcp_server.sh -p 9000           # Use port 9000 with http transport"
echo "./restart_mcp_server.sh -t sse            # Use Server-Sent Events transport"
echo "./restart_mcp_server.sh -p 8080 -t http   # Custom port with specified transport"

