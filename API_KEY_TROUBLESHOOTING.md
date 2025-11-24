# API Key Troubleshooting

## Current Status

✅ **API Key is configured** in Cloud Run service  
❌ **OpenAI returned 401 Unauthorized** error

## Error Details

```
Error code: 401 - Incorrect API key provided
```

## Possible Causes

### 1. Invalid or Expired API Key

- Check your API key at: https://platform.openai.com/account/api-keys
- Make sure the key is active and not revoked
- Verify you're using the correct key (not a test key)

### 2. API Key Format Issue

The key should start with `sk-proj-` or `sk-` and be the full key.

### 3. Billing/Quota Issues

- Check your OpenAI account has credits/billing set up
- Verify you haven't exceeded rate limits

## Verify Your Key Works

### Test Locally

```powershell
# Test if your key works
py -c "from openai import OpenAI; client = OpenAI(api_key='sk-proj-your-key'); models = list(client.models.list()); print('✅ Key works!' if models else '❌ Key invalid')"
```

### Check in OpenAI Dashboard

1. Go to: https://platform.openai.com/account/api-keys
2. Verify your key is listed and active
3. Check usage/credits: https://platform.openai.com/usage

## Update the Key

If you need to update the key in Cloud Run:

```powershell
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Update with new key
gcloud run services update langchain-agent-mcp-server `
    --set-env-vars "OPENAI_API_KEY=sk-proj-your-new-key-here" `
    --region us-central1
```

## Alternative: Use Secret Manager

For better security, use Secret Manager:

```powershell
# Create secret
"sk-proj-your-key" | gcloud secrets create openai-api-key --data-file=-

# Grant access
$projectNumber = (gcloud projects describe slashmcp --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key `
    --member="serviceAccount:$projectNumber-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"

# Update service
gcloud run services update langchain-agent-mcp-server `
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest `
    --region us-central1
```

## Check Service Logs

```powershell
gcloud run services logs read langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --project slashmcp `
    --limit 50
```

---

**Next Step:** Verify your API key is valid at https://platform.openai.com/account/api-keys

