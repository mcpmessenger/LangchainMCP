# Google Cloud Run Deployment Guide

Complete guide for deploying the LangChain Agent MCP Server to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK (gcloud)** installed and configured
3. **Docker** installed and running
4. **OpenAI API Key** ready to configure

## Quick Start

### Option 1: Using Deployment Scripts (Recommended)

**Windows PowerShell (Recommended for Windows users):**
```powershell
.\deploy-cloud-run.ps1 -ProjectId "your-project-id" -Region "us-central1"
```
📖 **For detailed Windows instructions, see [DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)**

**Linux/Mac:**
```bash
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh your-project-id us-central1
```

### Option 2: Manual Deployment

Follow the step-by-step instructions below.

## Step-by-Step Deployment

### 1. Install and Configure Google Cloud SDK

```bash
# Install gcloud CLI (if not already installed)
# See: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Build and Push Docker Image

```bash
# Set variables
PROJECT_ID="your-project-id"
SERVICE_NAME="langchain-agent-mcp-server"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Build the image
docker build -t $IMAGE_NAME .

# Push to Container Registry
docker push $IMAGE_NAME
```

### 4. Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars "OPENAI_MODEL=gpt-4o-mini,MAX_ITERATIONS=10,VERBOSE=false" \
    --port 8000
```

### 5. Configure OpenAI API Key

**Option A: Using Environment Variable (Quick but less secure)**
```bash
gcloud run services update $SERVICE_NAME \
    --set-env-vars OPENAI_API_KEY=your-key-here \
    --region us-central1
```

**Option B: Using Secret Manager (Recommended for production)**

1. Create a secret:
```bash
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key \
    --data-file=- \
    --replication-policy="automatic"
```

2. Grant Cloud Run access to the secret:
```bash
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

3. Update the service to use the secret:
```bash
gcloud run services update $SERVICE_NAME \
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest \
    --region us-central1
```

### 6. Verify Deployment

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test manifest endpoint
curl $SERVICE_URL/mcp/manifest
```

## Configuration Options

### Resource Allocation

Adjust based on your needs:

```bash
# For higher traffic or complex queries
--memory 4Gi \
--cpu 4 \
--max-instances 20

# For cost optimization
--memory 1Gi \
--cpu 1 \
--max-instances 5 \
--min-instances 0  # Scale to zero when not in use
```

### Timeout Settings

Cloud Run has a maximum timeout of 300 seconds (5 minutes). For longer-running agent tasks:

```bash
--timeout 300  # Maximum allowed
```

### Environment Variables

Set additional environment variables:

```bash
gcloud run services update $SERVICE_NAME \
    --set-env-vars "OPENAI_MODEL=gpt-4,MAX_ITERATIONS=15,VERBOSE=true,API_KEY=your-api-key" \
    --region us-central1
```

### CORS Configuration

If you need to allow specific origins:

```bash
gcloud run services update $SERVICE_NAME \
    --set-env-vars "CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com" \
    --region us-central1
```

## Using Cloud Build (CI/CD)

### 1. Create cloudbuild.yaml

The `cloudbuild.yaml` file is already included in the repository. It:
- Builds the Docker image
- Pushes to Container Registry
- Deploys to Cloud Run

### 2. Set up Cloud Build Trigger

```bash
# Create a trigger for GitHub
gcloud builds triggers create github \
    --name="deploy-langchain-mcp" \
    --repo-name="LangchainMCP" \
    --repo-owner="mcpmessenger" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild.yaml"
```

### 3. Set Secrets in Cloud Build

```bash
# Store OpenAI API key as a secret
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key \
    --data-file=-

# Grant Cloud Build access
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding openai-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 4. Update cloudbuild.yaml to use secrets

Add this step before the deploy step:

```yaml
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      gcloud run services update langchain-agent-mcp-server \
        --update-secrets=OPENAI_API_KEY=openai-api-key:latest \
        --region us-central1
```

## Monitoring and Logging

### View Logs

```bash
# View recent logs
gcloud run services logs read $SERVICE_NAME \
    --platform managed \
    --region us-central1

# Follow logs in real-time
gcloud run services logs tail $SERVICE_NAME \
    --platform managed \
    --region us-central1
```

### Set up Monitoring

1. Go to Cloud Console → Cloud Run → Your Service
2. Click on "Monitoring" tab
3. Set up alerts for:
   - Request latency
   - Error rate
   - Memory usage
   - CPU usage

## Cost Optimization

### 1. Scale to Zero

```bash
--min-instances 0  # Scales down when not in use
```

### 2. Use Appropriate Resources

Start with minimal resources and scale up as needed:
- **Development**: 1 CPU, 1Gi memory
- **Production**: 2 CPU, 2Gi memory
- **High Traffic**: 4 CPU, 4Gi memory

### 3. Set Request Limits

```bash
--max-instances 10  # Limit concurrent instances
```

### 4. Use Cloud Run Pricing Calculator

Estimate costs: https://cloud.google.com/run/pricing

## Troubleshooting

### Service Won't Start

1. Check logs:
```bash
gcloud run services logs read $SERVICE_NAME --region us-central1
```

2. Verify environment variables:
```bash
gcloud run services describe $SERVICE_NAME --region us-central1
```

3. Test locally with Docker:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key gcr.io/$PROJECT_ID/$SERVICE_NAME
```

### High Latency

1. Increase memory/CPU:
```bash
gcloud run services update $SERVICE_NAME \
    --memory 4Gi --cpu 4 --region us-central1
```

2. Check agent iteration limits:
```bash
gcloud run services update $SERVICE_NAME \
    --set-env-vars MAX_ITERATIONS=5 --region us-central1
```

### Authentication Issues

If you need to restrict access:

```bash
# Remove --allow-unauthenticated and use IAM
gcloud run services update $SERVICE_NAME \
    --no-allow-unauthenticated \
    --region us-central1

# Grant access to specific users
gcloud run services add-iam-policy-binding $SERVICE_NAME \
    --member="user:email@example.com" \
    --role="roles/run.invoker" \
    --region us-central1
```

## Security Best Practices

1. **Use Secret Manager** for API keys (not environment variables)
2. **Enable VPC** if accessing private resources
3. **Set up IAM** policies for service access
4. **Enable Cloud Armor** for DDoS protection
5. **Use HTTPS only** (enabled by default)
6. **Set up API key authentication** in the application

## Next Steps

- Set up custom domain: https://cloud.google.com/run/docs/mapping-custom-domains
- Configure CDN: Use Cloud CDN with Cloud Run
- Set up monitoring: Configure alerts in Cloud Monitoring
- Enable tracing: Use Cloud Trace for request tracing

## Support

For issues or questions:
- Check Cloud Run logs
- Review [Cloud Run documentation](https://cloud.google.com/run/docs)
- Check application logs in Cloud Console

