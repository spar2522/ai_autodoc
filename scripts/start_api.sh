#!/bin/bash
set -e

# Navigate to the project root directory
cd "$(dirname "$0")/.." || { echo "Failed to change directory"; exit 1; }

# Configuration variables
HOST="0.0.0.0"
PORT="9000"
APP_MODULE="autodoc.api.app:app"

# Start the Uvicorn server
uv run uvicorn "$APP_MODULE" \
    --reload \
    --host "$HOST" \
    --port "$PORT"