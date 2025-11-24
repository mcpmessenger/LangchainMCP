# Windows Setup Guide

Complete Windows setup guide for the LangChain Agent MCP Server.

## Prerequisites Installation

> **Note:** If `winget` is not available on your system, use the manual download options below.

### 1. Install Python

**Option A: Manual Download (Recommended if winget not available)**
1. Visit: https://www.python.org/downloads/
2. Download Python 3.11 or higher (Windows installer)
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Run the installer and complete setup

**Option B: Using winget (if available)**
```powershell
winget install Python.Python.3.11
```

**Verify installation:**
```powershell
py --version
# Should show: Python 3.11.x or higher

# If py doesn't work, try:
python --version
```

### 2. Install Google Cloud SDK

**Option A: Manual Download (Recommended)**
1. Visit: https://cloud.google.com/sdk/docs/install
2. Download the Windows installer
3. Run the installer (it will add gcloud to PATH)
4. Restart PowerShell after installation

**Option B: Using winget (if available)**
```powershell
winget install Google.CloudSDK
```

**Verify installation:**
```powershell
gcloud --version
```

**If gcloud is not found:**
```powershell
# Add to PATH manually (adjust path if different)
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
# Or restart PowerShell
```

**Initial setup:**
```powershell
gcloud init
gcloud auth login
```

### 3. Install Docker Desktop

**Option A: Manual Download (Recommended)**
1. Visit: https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Windows
3. Run the installer
4. Restart your computer if prompted
5. Start Docker Desktop from Start Menu

**Option B: Using winget (if available)**
```powershell
winget install Docker.DockerDesktop
```

**Important:** 
- Make sure Docker Desktop is running before building images
- You'll see a whale icon in the system tray when it's running

**Verify installation:**
```powershell
docker --version
docker ps
```

### 4. Install Git (if not already installed)

**Option A: Manual Download**
1. Visit: https://git-scm.com/download/win
2. Download and run the installer
3. Use default settings (Git will be added to PATH)

**Option B: Using winget (if available)**
```powershell
winget install Git.Git
```

**Verify installation:**
```powershell
git --version
```

## Project Setup

### 1. Clone or Navigate to Project

```powershell
cd "C:\Users\senti\OneDrive\Desktop\Langchain MCP\restful-data-gateway-main"
```

### 2. Install Python Dependencies

```powershell
py -m pip install -r requirements.txt
```

**If you get "pip not found":**
```powershell
# Use py launcher instead
py -m pip install -r requirements.txt

# Or add Python to PATH manually
```

### 3. Create .env File

```powershell
# Create .env file with your OpenAI API key
@"
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
PORT=8000
HOST=0.0.0.0
"@ | Out-File -FilePath .env -Encoding utf8
```

**Or manually create `.env` file:**
```
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
PORT=8000
HOST=0.0.0.0
```

### 4. Test Local Server

```powershell
py run_server.py
```

You should see:
```
Loaded environment variables from .env
Starting LangChain Agent MCP Server on 0.0.0.0:8000
API Documentation: http://0.0.0.0:8000/docs
```

## Installing winget (Optional)

If you want to use `winget` for easier package management:

**For Windows 10:**
1. Install App Installer from Microsoft Store: https://www.microsoft.com/store/productId/9NBLGGH4NNS1
2. Or update Windows to get the latest App Installer

**For Windows 11:**
- `winget` should be pre-installed

**Verify winget:**
```powershell
winget --version
```

## Common Windows Issues & Solutions

### Issue: "winget is not recognized"

**Solution:** Use manual download methods (see above) or install App Installer from Microsoft Store.

### Issue: "py is not recognized"

**Solution:**
```powershell
# Use full path or reinstall Python with "Add to PATH" checked
# Or use: python instead of py
python --version
```

### Issue: "pip is not recognized"

**Solution:**
```powershell
# Always use: py -m pip (Windows Python launcher)
py -m pip install -r requirements.txt

# Or: python -m pip
python -m pip install -r requirements.txt
```

### Issue: "gcloud is not recognized"

**Solution:**
```powershell
# Restart PowerShell after installing gcloud
# Or add to PATH manually:
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
```

### Issue: "Docker daemon not running"

**Solution:**
1. Start Docker Desktop from Start Menu
2. Wait for Docker to fully start (whale icon in system tray)
3. Verify: `docker ps`

### Issue: PowerShell Execution Policy

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run script with bypass:
powershell -ExecutionPolicy Bypass -File .\deploy-cloud-run.ps1
```

### Issue: Line Continuation in PowerShell

**Use backtick (`) for line continuation:**
```powershell
gcloud run deploy service-name `
    --image gcr.io/project/image `
    --region us-central1
```

### Issue: Path with Spaces

**Use quotes:**
```powershell
cd "C:\Users\senti\OneDrive\Desktop\Langchain MCP\restful-data-gateway-main"
```

## Testing Commands

### Test Local Server
```powershell
# Start server
py run_server.py

# In another terminal, test endpoints
Invoke-WebRequest -Uri "http://localhost:8000/health"
Invoke-WebRequest -Uri "http://localhost:8000/mcp/manifest"
```

### Test Docker Build
```powershell
docker build -t langchain-mcp-test .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key langchain-mcp-test
```

### Test Cloud Run Deployment
```powershell
# Get service URL
$url = gcloud run services describe langchain-agent-mcp-server `
    --region us-central1 `
    --format "value(status.url)"

# Test
Invoke-WebRequest -Uri "$url/health"
```

## Next Steps

1. ✅ **Local Development**: Test with `py run_server.py`
2. ✅ **Cloud Run Deployment**: See [DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)
3. ✅ **Production Setup**: Configure secrets and monitoring

## Getting Help

- **Python Issues**: https://www.python.org/about/help/
- **gcloud CLI**: https://cloud.google.com/sdk/gcloud/reference
- **Docker Desktop**: https://docs.docker.com/desktop/windows/
- **PowerShell**: https://docs.microsoft.com/powershell/

---

**Ready to deploy?** See [DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)

