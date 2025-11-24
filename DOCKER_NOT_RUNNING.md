# Docker Desktop Not Running

## Issue

The deployment script failed because **Docker Desktop is not running**.

Error message:
```
ERROR: error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

## Solution

### Step 1: Start Docker Desktop

1. **Open Start Menu**
2. **Search for "Docker Desktop"**
3. **Click to launch Docker Desktop**
4. **Wait for Docker to fully start** - You'll see a whale icon in your system tray when it's ready

### Step 2: Verify Docker is Running

Open a new PowerShell terminal and run:

```powershell
docker ps
```

You should see output like:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you get an error, Docker is still starting. Wait a bit longer.

### Step 3: Run Deployment Again

Once Docker is running:

```powershell
# Make sure gcloud is in PATH
$env:PATH += ";C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

# Run deployment
.\deploy-cloud-run.ps1 -ProjectId "slashmcp" -Region "us-central1"
```

## Troubleshooting

### Docker Desktop Won't Start

1. **Check if virtualization is enabled** in BIOS
2. **Run as Administrator** - Right-click Docker Desktop → Run as Administrator
3. **Restart your computer** if Docker was just installed
4. **Check Windows features** - Enable "Hyper-V" or "Windows Subsystem for Linux"

### Docker Starts But Commands Fail

1. **Restart PowerShell** after Docker starts
2. **Check Docker status**: Look for whale icon in system tray
3. **Verify Docker**: `docker --version` should work

---

**Once Docker is running, the deployment will proceed!** 🐳

