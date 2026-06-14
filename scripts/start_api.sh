#!/bin/bash

cd "$(dirname "$0")/.."

uv run uvicorn autodoc.api.app:app \
    --reload \
    --host 0.0.0.0 \
    --port 9000