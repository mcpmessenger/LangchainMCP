# Setting Up OpenAI API Key

## Current Status

❌ **OPENAI_API_KEY is NOT configured**

The service is running but won't be able to execute agent requests without the API key.

## Option 1: Using Secret Manager (Recommended)

**More secure** - API key is stored encrypted in Google Secret Manager.

### Step 1: Create the Secret

```powershell
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Replace with your actual API key
"sk-proj-your-actual-api-key-here" | gcloud secrets create openai-api-key --data-file=-
```

### Step 2: Grant Cloud Run Access

```powershell
$projectNumber = (gcloud projects describe slashmcp --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key `
    --member="serviceAccount:$projectNumber-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"
```

### Step 3: Update the Service

```powershell
gcloud run services update langchain-agent-mcp-server `
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest `
    --region us-central1
```

## Option 2: Using Environment Variable (Quick)

**Less secure** - API key is visible in service configuration.

```powershell
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Replace with your actual API key
gcloud run services update langchain-agent-mcp-server `
    --set-env-vars OPENAI_API_KEY=sk-proj-your-actual-api-key-here `
    --region us-central1
```

## Option 3: Using Google Cloud Console (GUI)

1. Go to: https://console.cloud.google.com/run/detail/us-central1/langchain-agent-mcp-server?project=slashmcp
2. Click **"EDIT & DEPLOY NEW REVISION"**
3. Go to **"Variables & Secrets"** tab
4. Click **"ADD VARIABLE"** or **"REFERENCE A SECRET"**
5. For environment variable:
   - Name: `OPENAI_API_KEY`
   - Value: Your API key
6. For secret (recommended):
   - Click **"REFERENCE A SECRET"**
   - Create new secret or select existing
   - Name: `OPENAI_API_KEY`
   - Secret: `openai-api-key:latest`
7. Click **"DEPLOY"**

## Verify It's Set

After setting the key, test it:

```powershell
$serviceUrl = "https://langchain-agent-mcp-server-554655392699.us-central1.run.app"

$body = @{
    tool = "agent_executor"
    arguments = @{
        query = "What is 2+2?"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "$serviceUrl/mcp/invoke" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

If it works, you'll get a response. If not, check the logs:

```powershell
gcloud run services logs read langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --project slashmcp `
    --limit 20
```

---

**Recommendation:** Use Secret Manager (Option 1) for production deployments.

