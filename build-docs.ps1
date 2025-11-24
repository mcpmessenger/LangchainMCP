# PowerShell script to build and preview documentation
# Usage: .\build-docs.ps1 [serve|build|deploy]

param(
    [string]$Action = "serve"
)

Write-Host "Documentation Builder" -ForegroundColor Green
Write-Host ""

# Check if mkdocs is installed
try {
    $null = Get-Command mkdocs -ErrorAction Stop
} catch {
    Write-Host "Installing MkDocs dependencies..." -ForegroundColor Yellow
    pip install -r requirements-docs.txt
}

switch ($Action) {
    "serve" {
        Write-Host "Starting MkDocs server..." -ForegroundColor Yellow
        Write-Host "Visit: http://127.0.0.1:8000" -ForegroundColor Cyan
        mkdocs serve
    }
    "build" {
        Write-Host "Building documentation..." -ForegroundColor Yellow
        mkdocs build
        Write-Host "Documentation built in 'site/' directory" -ForegroundColor Green
    }
    "deploy" {
        Write-Host "Deploying to GitHub Pages..." -ForegroundColor Yellow
        mkdocs gh-deploy
        Write-Host "Documentation deployed!" -ForegroundColor Green
    }
    default {
        Write-Host "Usage: .\build-docs.ps1 [serve|build|deploy]" -ForegroundColor Yellow
    }
}

