# PowerShell deployment script for Google Cloud Run
# Usage: .\deploy-cloud-run.ps1 -ProjectId "your-project-id" -Region "us-central1"

param(
    [string]$ProjectId = $env:GOOGLE_CLOUD_PROJECT,
    [string]$Region = "us-central1"
)

$ErrorActionPreference = "Stop"

$ServiceName = "langchain-agent-mcp-server"
$ImageName = "gcr.io/$ProjectId/$ServiceName"

Write-Host "Deploying LangChain Agent MCP Server to Google Cloud Run" -ForegroundColor Green
Write-Host ""

# Check if PROJECT_ID is set
if ([string]::IsNullOrEmpty($ProjectId)) {
    Write-Host "Error: PROJECT_ID not set" -ForegroundColor Red
    Write-Host "Usage: .\deploy-cloud-run.ps1 -ProjectId 'your-project-id' -Region 'us-central1'"
    Write-Host "Or set GOOGLE_CLOUD_PROJECT environment variable"
    exit 1
}

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Project ID: $ProjectId"
Write-Host "  Region: $Region"
Write-Host "  Service Name: $ServiceName"
Write-Host ""

# Check if gcloud is installed
try {
    $null = Get-Command gcloud -ErrorAction Stop
} catch {
    Write-Host "Error: gcloud CLI not found" -ForegroundColor Red
    Write-Host "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
}

# Check if docker is installed
try {
    $null = Get-Command docker -ErrorAction Stop
} catch {
    Write-Host "Error: Docker not found" -ForegroundColor Red
    Write-Host "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
}

# Set the project
Write-Host "Setting GCP project..." -ForegroundColor Yellow
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t $ImageName .

# Push the image to Container Registry
Write-Host "Pushing image to Container Registry..." -ForegroundColor Yellow
docker push $ImageName

# Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --image $ImageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --set-env-vars "OPENAI_MODEL=gpt-4o-mini,MAX_ITERATIONS=10,VERBOSE=false" `
    --port 8000

# Get the service URL
$ServiceUrl = gcloud run services describe $ServiceName --platform managed --region $Region --format "value(status.url)"

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URL: $ServiceUrl" -ForegroundColor Green
Write-Host ""
Write-Host "Important: Set your OPENAI_API_KEY as a secret:" -ForegroundColor Yellow
Write-Host "  gcloud run services update $ServiceName \"
Write-Host "    --update-secrets=OPENAI_API_KEY=openai-api-key:latest \"
Write-Host "    --region $Region"
Write-Host ""
Write-Host "Or set it as an environment variable:" -ForegroundColor Yellow
Write-Host "  gcloud run services update $ServiceName \"
Write-Host "    --set-env-vars OPENAI_API_KEY=your-key-here \"
Write-Host "    --region $Region"
Write-Host ""
Write-Host "Test your deployment:" -ForegroundColor Green
Write-Host "  Health: $ServiceUrl/health"
Write-Host "  Manifest: $ServiceUrl/mcp/manifest"
