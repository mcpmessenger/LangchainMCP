# Enable GitHub Pages for Documentation

## Automatic Setup (Recommended)

The documentation will be automatically deployed when you push to the `main` branch via GitHub Actions.

## Manual Setup

### Step 1: Deploy Documentation

```bash
# Install dependencies
pip install -r requirements-docs.txt

# Deploy to GitHub Pages
mkdocs gh-deploy
```

This will:
- Build the documentation
- Create/update the `gh-pages` branch
- Push to GitHub

### Step 2: Enable GitHub Pages

1. Go to your repository: https://github.com/mcpmessenger/LangchainMCP
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
4. Click **Save**

### Step 3: Access Your Docs

Your documentation will be available at:
**https://mcpmessenger.github.io/LangchainMCP/**

(It may take a few minutes to become available)

## Verify Deployment

After enabling GitHub Pages, check:
- GitHub Actions tab shows successful deployment
- `gh-pages` branch exists
- Documentation is accessible at the URL above

## Troubleshooting

### Pages Not Showing

1. Wait 5-10 minutes after first deployment
2. Check GitHub Actions for errors
3. Verify `gh-pages` branch exists
4. Check repository Settings → Pages configuration

### Build Errors

Check the GitHub Actions logs:
- Go to **Actions** tab
- Click on the latest workflow run
- Review build logs

---

**Once enabled, documentation will auto-update on every push to `main`!**

