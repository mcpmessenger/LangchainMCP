# Installing Prerequisites on Windows

Quick guide for installing all required software on Windows (without winget).

## Required Software

1. ✅ Python 3.11+
2. ✅ Google Cloud SDK
3. ✅ Docker Desktop
4. ✅ Git (optional, but recommended)

## Step-by-Step Installation

### 1. Install Python

**Download and Install:**
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.11.x" (or latest version)
3. Run the downloaded installer
4. ✅ **CRITICAL:** Check the box "Add Python to PATH" at the bottom
5. Click "Install Now"
6. Wait for installation to complete

**Verify:**
```powershell
py --version
# Should show: Python 3.11.x or higher
```

**If `py` doesn't work:**
```powershell
python --version
```

### 2. Install Google Cloud SDK

**Download and Install:**
1. Go to: https://cloud.google.com/sdk/docs/install
2. Click "Download SDK" for Windows
3. Run the installer (`GoogleCloudSDKInstaller.exe`)
4. Follow the installation wizard
5. ✅ Make sure "Add Cloud SDK to PATH" is checked
6. Restart PowerShell after installation

**Verify:**
```powershell
gcloud --version
```

**If gcloud is not found:**
```powershell
# Restart PowerShell first, then try:
gcloud --version

# If still not found, add manually:
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
```

**Initial Setup:**
```powershell
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### 3. Install Docker Desktop

**Download and Install:**
1. Go to: https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer (`Docker Desktop Installer.exe`)
4. Follow the installation wizard
5. Restart your computer if prompted
6. Start Docker Desktop from Start Menu
7. Wait for Docker to fully start (you'll see a whale icon in system tray)

**Verify:**
```powershell
docker --version
docker ps
```

**Important:** Docker Desktop must be running before you can build images!

### 4. Install Git (Optional but Recommended)

**Download and Install:**
1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer
4. Use default settings (Git will be added to PATH automatically)

**Verify:**
```powershell
git --version
```

## Verify All Installations

Run this in PowerShell to check everything:

```powershell
Write-Host "Checking prerequisites..." -ForegroundColor Green

Write-Host "`nPython:" -ForegroundColor Yellow
py --version
if ($LASTEXITCODE -ne 0) { python --version }

Write-Host "`nGoogle Cloud SDK:" -ForegroundColor Yellow
gcloud --version

Write-Host "`nDocker:" -ForegroundColor Yellow
docker --version

Write-Host "`nGit:" -ForegroundColor Yellow
git --version

Write-Host "`n✅ All prerequisites installed!" -ForegroundColor Green
```

## Troubleshooting

### Python not found after installation

**Solution:**
1. Reinstall Python and make sure "Add Python to PATH" is checked
2. Or manually add to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts`
   - Restart PowerShell

### gcloud not found after installation

**Solution:**
1. Restart PowerShell (required after installation)
2. If still not found, add manually:
   ```powershell
   $env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
   ```
3. Or reinstall and make sure "Add Cloud SDK to PATH" is checked

### Docker Desktop won't start

**Solution:**
1. Make sure virtualization is enabled in BIOS
2. Check Windows features: Enable "Hyper-V" or "Windows Subsystem for Linux"
3. Restart computer
4. Try running Docker Desktop as Administrator

### PowerShell Execution Policy

If you get "execution policy" errors:

```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

Once all prerequisites are installed:

1. ✅ Navigate to project directory
2. ✅ Install Python dependencies: `py -m pip install -r requirements.txt`
3. ✅ Create `.env` file with your OpenAI API key
4. ✅ Test locally: `py run_server.py`
5. ✅ Deploy to Cloud Run: See [DEPLOY_CLOUD_RUN_WINDOWS.md](DEPLOY_CLOUD_RUN_WINDOWS.md)

## Quick Links

- **Python**: https://www.python.org/downloads/
- **Google Cloud SDK**: https://cloud.google.com/sdk/docs/install
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Git**: https://git-scm.com/download/win

---

**Ready?** Continue to [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for project setup!


