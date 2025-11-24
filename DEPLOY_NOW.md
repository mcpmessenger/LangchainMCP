# Deploy Now - Quick Steps

## Step 1: Select Your Project

You're currently being prompted to select a Google Cloud project. 

**Recommended choices:**
- **Option 8: `mcp-oath`** - If this is for MCP-related work
- **Option 12: `slashmcp`** - If this is for SlashMCP integration
- **Option 17: Create a new project** - If you want a dedicated project

**Type the number and press Enter:**
```
8
```
or
```
12
```
or
```
17
```

## Step 2: After Project Selection

Once you've selected your project, run:

```powershell
# Set your project (replace with your chosen project ID)
$env:GOOGLE_CLOUD_PROJECT = "mcp-oath"  # or "slashmcp" or your new project ID

# Verify
gcloud config get-value project
```

## Step 3: Enable Required APIs

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## Step 4: Deploy

```powershell
.\deploy-cloud-run.ps1 -ProjectId "mcp-oath" -Region "us-central1"
```

(Replace `mcp-oath` with your chosen project ID)

## Step 5: Set OpenAI API Key

```powershell
# Create secret
"your-openai-api-key-here" | gcloud secrets create openai-api-key --data-file=-

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

## Step 6: Get Your Service URL

```powershell
gcloud run services describe langchain-agent-mcp-server `
    --platform managed `
    --region us-central1 `
    --format "value(status.url)"
```

---

**Right now:** Just type the number of your project choice (8, 12, or 17) and press Enter!


