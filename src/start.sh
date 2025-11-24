#!/bin/sh
# Startup script for Cloud Run
# Reads PORT from environment (set by Cloud Run) or defaults to 8000

PORT=${PORT:-8000}
exec uvicorn src.main:app --host 0.0.0.0 --port $PORT

