#!/bin/bash

cd "$(dirname "$0")/.."

uv run src/autodoc/worker/start_worker.py