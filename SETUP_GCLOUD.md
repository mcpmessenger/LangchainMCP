# Setting Up Google Cloud CLI in Cursor/VS Code

## Current Status

❌ **gcloud CLI is not found in your PATH**

## Quick Fix Options

### Option 1: Install Google Cloud SDK (If Not Installed)

1. **Download the installer:**
   - Go to: https://cloud.google.com/sdk/docs/install
   - Click "Download SDK" for Windows
   - Download `GoogleCloudSDKInstaller.exe`

2. **Run the installer:**
   - Run the downloaded file
   - ✅ Make sure "Add Cloud SDK to PATH" is checked
   - Complete the installation

3. **Restart Cursor/VS Code:**
   - Close Cursor completely
   - Reopen Cursor
   - Open a new terminal (Terminal → New Terminal)

4. **Verify:**
   ```powershell
   gcloud --version
   ```

### Option 2: Add gcloud to PATH Manually (If Already Installed)

If gcloud is installed but not in PATH:

```powershell
# Check common installation locations
Test-Path "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
Test-Path "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

# If found, add to PATH for current session
$gcloudPath = "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin"
if (Test-Path "$gcloudPath\gcloud.cmd") {
    $env:PATH += ";$gcloudPath"
    Write-Host "Added gcloud to PATH for this session" -ForegroundColor Green
    gcloud --version
}
```

**To make it permanent:**
1. Search "Environment Variables" in Windows
2. Edit "Path" variable
3. Add: `C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin`
4. Restart Cursor

### Option 3: Use Full Path (Temporary Solution)

If gcloud is installed but not in PATH, you can use the full path:

```powershell
# Try common paths
& "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" --version

# Or if in user directory
& "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" --version
```

## After Installation

Once gcloud is working:

1. **Set your project:**
   ```powershell
   gcloud config set project slashmcp
   ```

2. **Verify:**
   ```powershell
   gcloud config get-value project
   # Should show: slashmcp
   ```

3. **Login (if needed):**
   ```powershell
   gcloud auth login
   ```

4. **Enable required APIs:**
   ```powershell
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```

## Next Steps

After gcloud is set up, you can deploy:

```powershell
.\deploy-cloud-run.ps1 -ProjectId "slashmcp" -Region "us-central1"
```

## Troubleshooting

### "gcloud not found" after installation
- **Solution:** Restart Cursor/VS Code completely
- Or manually add to PATH (see Option 2 above)

### "Permission denied" errors
- **Solution:** Run Cursor as Administrator, or check file permissions

### Installation fails
- **Solution:** Check Windows Defender/Antivirus isn't blocking
- Try installing as Administrator

---

**Right now:** Install Google Cloud SDK from https://cloud.google.com/sdk/docs/install if you haven't already!

