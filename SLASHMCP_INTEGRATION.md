# SlashMCP Integration Guide

## Correct Service URL

**✅ Correct URL:**
```
https://langchain-agent-mcp-server-554655392699.us-central1.run.app
```

**❌ Incorrect URL (has typo):**
```
https://langchain-agent-mcp-server-554655392699.us-centrall.run.app
```

## Register in SlashMCP

### Step 1: Remove the Incorrect Registration

In SlashMCP, run:
```
/slashmcp remove langchain-agent
```

### Step 2: Add with Correct URL

```
/slashmcp add langchain-agent https://langchain-agent-mcp-server-554655392699.us-central1.run.app
```

### Step 3: Verify Registration

```
/slashmcp list
```

You should see:
- `langchain-agent (srv_xxxxx)` - active, auth: no auth

## Using the Agent

Once registered correctly, invoke the agent:

```
/srv_xxxxx agent_executor query="What is the capital of France?"
```

Or using the server ID directly:
```
/slashmcp invoke srv_xxxxx agent_executor query="Your question here"
```

## MCP Endpoints

The service exposes these MCP-compliant endpoints:

1. **GET /mcp/manifest** - Returns tool definitions
2. **POST /mcp/invoke** - Executes the agent

### Expected Request Format

```json
{
  "tool": "agent_executor",
  "arguments": {
    "query": "Your question here"
  }
}
```

### Expected Response Format

```json
{
  "content": [
    {
      "type": "text",
      "text": "Agent response here..."
    }
  ],
  "isError": false
}
```

## Troubleshooting

### 404 Errors

If you get 404 errors:
1. ✅ Verify the URL is correct (no typos)
2. ✅ Check the service is running: `https://langchain-agent-mcp-server-554655392699.us-central1.run.app/health`
3. ✅ Verify manifest endpoint: `https://langchain-agent-mcp-server-554655392699.us-central1.run.app/mcp/manifest`

### Gateway Request Failed

If "MCP gateway request failed":
- The SlashMCP gateway might be trying to access a different endpoint
- Verify the service URL is accessible from the internet
- Check if there are any CORS issues (should be configured to allow all origins)

### Agent Not Responding

If the agent doesn't respond:
1. Check service logs:
   ```powershell
   gcloud run services logs read langchain-agent-mcp-server `
       --platform managed `
       --region us-central1 `
       --project slashmcp
   ```
2. Verify API key is set correctly
3. Test the endpoint directly:
   ```powershell
   $body = @{
       tool = "agent_executor"
       arguments = @{
           query = "test"
       }
   } | ConvertTo-Json
   
   Invoke-WebRequest -Uri "https://langchain-agent-mcp-server-554655392699.us-central1.run.app/mcp/invoke" `
       -Method POST `
       -ContentType "application/json" `
       -Body $body
   ```

## Service Status

- **Status:** ✅ Running
- **URL:** https://langchain-agent-mcp-server-554655392699.us-central1.run.app
- **API Key:** ✅ Configured
- **Endpoints:** ✅ Working

---

**Fix the typo in the URL and re-register to resolve the 404 errors!**

