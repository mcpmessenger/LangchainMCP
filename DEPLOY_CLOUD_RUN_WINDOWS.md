# Google Cloud Run Deployment Guide - Windows

Complete Windows-focused guide for deploying the LangChain Agent MCP Server to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK (gcloud)** installed
   - Download: https://cloud.google.com/sdk/docs/install
   - Run the installer (it will add gcloud to PATH)
   - Restart PowerShell after installation
3. **Docker Desktop** installed and running
   - Download: https://www.docker.com/products/docker-desktop
   - Make sure Docker Desktop is running (whale icon in system tray)
4. **OpenAI API Key** ready to configure
5. **PowerShell** (comes with Windows)

> **Note:** If you don't have `winget`, use the manual download links above.

## Quick Start (Windows)

### Step 1: Install Prerequisites

**Install Google Cloud SDK:**
```powershell
# Using winget (Windows 11/10 with App Installer)
winget install Google.CloudSDK

# Or download from: https://cloud.google.com/sdk/docs/install
```

**Install Docker Desktop:**
```powershell
winget install Docker.DockerDesktop
```

**Verify installations:**
```powershell
gcloud --version
docker --version
```

### Step 2: Authenticate with Google Cloud

```powershell
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config list
```

### Step 3: Enable Required APIs

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 4: Deploy Using PowerShell Script

```powershell
# Navigate to project directory
cd "C:\Users\senti\OneDrive\Desktop\Langchain MCP\restful-data-gateway-main"

# Run deployment script
.\deploy-cloud-run.ps1 -ProjectId "your-project-id" -Region "us-central1"
```

The script will:
- ✅ Build the Docker image
- ✅ Push to Google Container Registry
- ✅ Deploy to Cloud Run
- ✅ Show you the service URL

### Step 5: Configure OpenAI API Key

**Option A: Using Secret Manager (Recommended)**

```powershell
# Create the secret
$apiKey = "your-openai-api-key-here"
$apiKey | gcloud secrets create openai-api-key --data-file=-

# Get project number
$projectNumber = (gcloud projects describe $env:GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding openai-api-key `
    --member="serviceAccount:$projectNumber-compute@developer.gserviceaccount.com" `
    --role="roles/secretmanager.secretAccessor"

# Update the service to use the secret
gcloud run services update langchain-agent-mcp-server `
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest `
    --region us-central1
```

**Option B: Using Environment Variable (Quick but less secure)**

```powershell
gcloud run services update langchain-agent-mcp-server `
    --set-env-vars OPENAI_API_KEY=your-key-here `
    --region us-central1
```

### Step 6: Test Your Deployment

```powershell
# Get the service URL
$serviceUrl = gcloud run services describe langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --format "value(status.url)"

# Test health endpoint
Invoke-WebRequest -Uri "$serviceUrl/health" | Select-Object -ExpandProperty Content

# Test manifest endpoint
Invoke-WebRequest -Uri "$serviceUrl/mcp/manifest" | Select-Object -ExpandProperty Content
```

## Manual Deployment (Step-by-Step)

If you prefer to run commands manually:

### 1. Set Environment Variables

```powershell
$env:GOOGLE_CLOUD_PROJECT = "your-project-id"
$env:REGION = "us-central1"
$env:SERVICE_NAME = "langchain-agent-mcp-server"
$env:IMAGE_NAME = "gcr.io/$env:GOOGLE_CLOUD_PROJECT/$env:SERVICE_NAME"
```

### 2. Build Docker Image

```powershell
docker build -t $env:IMAGE_NAME .
```

### 3. Push to Container Registry

```powershell
docker push $env:IMAGE_NAME
```

### 4. Deploy to Cloud Run

```powershell
gcloud run deploy $env:SERVICE_NAME `
    --image $env:IMAGE_NAME `
    --platform managed `
    --region $env:REGION `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --set-env-vars "OPENAI_MODEL=gpt-4o-mini,MAX_ITERATIONS=10,VERBOSE=false" `
    --port 8000
```

## Windows-Specific Tips

### Using PowerShell vs Command Prompt

**PowerShell (Recommended):**
- Better error handling
- More modern syntax
- Better integration with gcloud

**Command Prompt:**
- Use `set` instead of `$env:`
- Use `^` for line continuation instead of backtick

### Docker Desktop on Windows

Make sure Docker Desktop is running before building:
```powershell
# Check if Docker is running
docker ps

# If not running, start Docker Desktop from Start Menu
```

### Path Issues

If you get "command not found" errors:
```powershell
# Add gcloud to PATH (usually done automatically, but verify)
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Or restart PowerShell after installing gcloud
```

### Line Continuation in PowerShell

Use backtick (`) for line continuation:
```powershell
gcloud run deploy langchain-agent-mcp-server `
    --image gcr.io/project/image `
    --region us-central1
```

## Troubleshooting (Windows)

### Docker Build Fails

**Issue:** "Cannot connect to Docker daemon"
```powershell
# Solution: Make sure Docker Desktop is running
# Check Docker status
docker info
```

**Issue:** "Build context is too large"
```powershell
# Solution: Check .dockerignore file
# Make sure large files are excluded
```

### gcloud Command Not Found

**Issue:** PowerShell can't find gcloud
```powershell
# Solution 1: Restart PowerShell after installation
# Solution 2: Add to PATH manually
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Solution 3: Use full path
& "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" --version
```

### Authentication Issues

**Issue:** "You do not currently have an active account selected"
```powershell
# Solution: Re-authenticate
gcloud auth login
gcloud auth application-default login
```

### Permission Denied Errors

**Issue:** "Permission denied" when pushing images
```powershell
# Solution: Configure Docker to use gcloud as credential helper
gcloud auth configure-docker
```

### PowerShell Execution Policy

**Issue:** "Cannot run script because execution policy"
```powershell
# Solution: Allow script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run script with bypass
powershell -ExecutionPolicy Bypass -File .\deploy-cloud-run.ps1
```

## Viewing Logs (Windows)

```powershell
# View recent logs
gcloud run services logs read langchain-agent-mcp-server `
    --platform managed `
    --region us-central1

# Follow logs in real-time
gcloud run services logs tail langchain-agent-mcp-server `
    --platform managed `
    --region us-central1
```

## Updating the Service

```powershell
# Update environment variables
gcloud run services update langchain-agent-mcp-server `
    --set-env-vars "OPENAI_MODEL=gpt-4,MAX_ITERATIONS=15" `
    --region us-central1

# Update resources
gcloud run services update langchain-agent-mcp-server `
    --memory 4Gi `
    --cpu 4 `
    --region us-central1

# Update image (after rebuilding)
gcloud run services update langchain-agent-mcp-server `
    --image gcr.io/$env:GOOGLE_CLOUD_PROJECT/langchain-agent-mcp-server:latest `
    --region us-central1
```

## Cost Optimization

### Scale to Zero (Save Money When Not in Use)

```powershell
gcloud run services update langchain-agent-mcp-server `
    --min-instances 0 `
    --region us-central1
```

### Set Maximum Instances

```powershell
gcloud run services update langchain-agent-mcp-server `
    --max-instances 5 `
    --region us-central1
```

## Quick Reference Commands

```powershell
# Get service URL
gcloud run services describe langchain-agent-mcp-server --region us-central1 --format "value(status.url)"

# List all services
gcloud run services list --region us-central1

# Delete service
gcloud run services delete langchain-agent-mcp-server --region us-central1

# View service details
gcloud run services describe langchain-agent-mcp-server --region us-central1
```

## Next Steps

1. ✅ Set up monitoring in Cloud Console
2. ✅ Configure custom domain (optional)
3. ✅ Set up CI/CD with Cloud Build (optional)
4. ✅ Review cost estimates in Cloud Console

## Getting Help

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **gcloud CLI Reference**: https://cloud.google.com/sdk/gcloud/reference
- **View logs in Console**: https://console.cloud.google.com/run

---

**Ready to deploy?** Run: `.\deploy-cloud-run.ps1 -ProjectId "your-project-id"`

