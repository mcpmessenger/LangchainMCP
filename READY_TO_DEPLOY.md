# ✅ Ready to Deploy!

## Current Status

✅ **Google Cloud CLI**: Installed and working (v548.0.0)  
✅ **Project**: Set to `slashmcp`  
✅ **Authentication**: Logged in as williamtflynn@gmail.com  
✅ **Docker**: Installed and working (v28.3.0)  
✅ **APIs**: Cloud Build, Cloud Run, Container Registry, Secret Manager enabled  

## Important Note

**gcloud PATH Issue:** gcloud is installed but not permanently in your PATH. 

**For this session:** It's been added temporarily, so commands will work.

**To make it permanent:**
1. Search "Environment Variables" in Windows
2. Edit "Path" variable  
3. Add: `C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin`
4. Restart Cursor

**Or** add this to your PowerShell profile:
```powershell
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
```

## Next Steps - Deploy!

You're ready to deploy! Run:

```powershell
.\deploy-cloud-run.ps1 -ProjectId "slashmcp" -Region "us-central1"
```

Or manually:

```powershell
# Build and push
docker build -t gcr.io/slashmcp/langchain-agent-mcp-server .
docker push gcr.io/slashmcp/langchain-agent-mcp-server

# Deploy
gcloud run deploy langchain-agent-mcp-server `
    --image gcr.io/slashmcp/langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --set-env-vars "OPENAI_MODEL=gpt-4o-mini,MAX_ITERATIONS=10,VERBOSE=false"
```

## After Deployment

Set your OpenAI API key:

```powershell
# Create secret
"your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

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

---

**You're all set! Ready to deploy?** 🚀

