#!/bin/bash
# Script to build and preview documentation
# Usage: ./build-docs.sh [serve|build|deploy]

ACTION=${1:-serve}

echo "Documentation Builder"
echo ""

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "Installing MkDocs dependencies..."
    pip install -r requirements-docs.txt
fi

case $ACTION in
    serve)
        echo "Starting MkDocs server..."
        echo "Visit: http://127.0.0.1:8000"
        mkdocs serve
        ;;
    build)
        echo "Building documentation..."
        mkdocs build
        echo "Documentation built in 'site/' directory"
        ;;
    deploy)
        echo "Deploying to GitHub Pages..."
        mkdocs gh-deploy
        echo "Documentation deployed!"
        ;;
    *)
        echo "Usage: ./build-docs.sh [serve|build|deploy]"
        ;;
esac

