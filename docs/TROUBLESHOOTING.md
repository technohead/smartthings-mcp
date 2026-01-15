# Troubleshooting SmartThingsMCP

This document provides guidance for resolving common issues encountered when using SmartThingsMCP.

## Authentication Issues

### 401 Unauthorized Error

If you're seeing a `401 Unauthorized` error when making API requests:

1. **Verify your token is valid and not expired**
   - SmartThings personal access tokens expire after 30 days by default
   - Generate a new token at https://account.smartthings.com/tokens

2. **Check token permissions**
   - For Modes API: The token requires `r:locations:*` scope for read operations and `w:locations:*` for write operations
   - For Device API: The token requires `r:devices:*` for read and `w:devices:*` for write operations
   - When creating a token, select all required scopes for the operations you need

3. **Confirm token format**
   - The token should be passed as a bearer token without the "Bearer " prefix (the library adds this automatically)
   - Do not include additional quotation marks or spaces

### 403 Forbidden Error

If you're seeing a `403 Forbidden` error:

1. **Check resource access**
   - Your SmartThings account might not have access to the requested location or device
   - Verify the location/device IDs are correct and belong to your account

2. **Scopes limitation**
   - Your token might have limited scopes that don't include the particular resource you're trying to access
   - Consider creating a new token with broader permissions

## Modes API Specific Issues

### Common Modes API issues

1. **Token Permission Requirements**
   - The Modes API requires specific permission scopes beyond the base SmartThings API
   - Ensure your token has `r:locations:*` and `w:locations:*` scopes

2. **Location ID Validity**
   - Confirm your location ID is valid by first listing all locations with `list_locations`
   - Use the obtained location IDs for mode-related operations

3. **API Limitations**
   - Some locations might not support the Modes API or have limited functionality
   - Enterprise or special installations might have different requirements

## Debugging Tips

1. **Enable Debug Logging**
   - The SmartThingsMCP modules have built-in logging that can be enabled to see detailed request/response information
   - Set logging level to DEBUG for more verbose output

2. **Verify API Access with curl**
   - Test your token using curl to make direct API calls:
   ```bash
   curl -X GET "https://api.smartthings.com/v1/locations" \
   -H "Authorization: Bearer YOUR_TOKEN_HERE" \
   -H "Accept: application/json"
   ```

3. **Check Rate Limiting**
   - SmartThings API has rate limiting that may cause temporary failures
   - Add delays between requests if you're making multiple calls in succession
