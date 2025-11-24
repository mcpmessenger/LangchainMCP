# Quick Deployment Guide

## Google Cloud Run - One Command Deploy

### Prerequisites
- Google Cloud SDK installed (`gcloud`)
- Docker Desktop installed and running
- GCP project with billing enabled

### Quick Deploy (Windows)

**1. Set your project:**
```powershell
$env:GOOGLE_CLOUD_PROJECT="your-project-id"
```

**2. Run deployment script:**
```powershell
.\deploy-cloud-run.ps1 -ProjectId "your-project-id" -Region "us-central1"
```

**3. Set your OpenAI API key:**
```powershell
# Create secret
"your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Grant access
$projectNumber = (gcloud projects describe $env:GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key `
    --member="serviceAccount:$projectNumber-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"

# Update service
gcloud run services update langchain-agent-mcp-server `
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest `
    --region us-central1
```

**4. Get your service URL:**
```powershell
gcloud run services describe langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --format "value(status.url)"
```

### Quick Deploy (Linux/Mac)

**1. Set your project:**
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

**2. Run deployment script:**
```bash
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh
```

**3. Set your OpenAI API key:**
```bash
# Create secret
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Grant access
PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Update service
gcloud run services update langchain-agent-mcp-server \
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest \
    --region us-central1
```

**4. Get your service URL:**
```bash
gcloud run services describe langchain-agent-mcp-server \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

That's it! Your service is now live on Cloud Run.

For detailed instructions, see [DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md).

