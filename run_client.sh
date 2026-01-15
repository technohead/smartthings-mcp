#!/bin/bash

# Check for required parameters
if [ $# -lt 2 ]; then
    echo "Usage: $0 <auth_token> <tool_name> [tool_params...]"
    echo "Example: $0 my-auth-token list_devices"
    exit 1
 fi

AUTH_TOKEN="$1"
TOOL_NAME="$2"
shift 2

# Convert remaining parameters to tool parameters string
PARAMS=""
while [ $# -gt 0 ]; do
    PARAMS="$PARAMS --param $1"
    shift
done

python SmartThingsMCPClient.py --transport http --auth "$AUTH_TOKEN" --action "$TOOL_NAME" $PARAMS
