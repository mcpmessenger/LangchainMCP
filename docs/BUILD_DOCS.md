# Building Documentation

## Quick Start

### Install Dependencies

```bash
pip install -r requirements-docs.txt
```

### Preview Locally

```bash
mkdocs serve
```

Visit: http://127.0.0.1:8000

### Build Static Site

```bash
mkdocs build
```

Output: `site/` directory

## GitHub Pages Setup

### Automatic Deployment

The documentation is automatically deployed via GitHub Actions when you push to `main` branch.

### Manual Deployment

```bash
mkdocs gh-deploy
```

### Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (created automatically)
4. Folder: `/ (root)`
5. Save

Your docs will be available at:
`https://mcpmessenger.github.io/LangchainMCP/`

## Structure

```
docs/
├── index.md              # Homepage
├── getting-started.md    # Setup guide
├── examples.md          # Code examples
├── deployment.md         # Deployment guide
├── api-reference.md     # API docs
└── troubleshooting.md   # Troubleshooting
```

## Customization

Edit `mkdocs.yml` to customize:
- Theme colors
- Navigation structure
- Plugins
- Site metadata

