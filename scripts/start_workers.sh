#!/bin/bash
# Script to start the worker processes for the Autodoc project

set -e

# Navigate to the project root directory
cd "$(dirname "$0")/.." || exit 1

# Start the worker using uv
uv run src/autodoc/worker/start_worker.py || exit 1