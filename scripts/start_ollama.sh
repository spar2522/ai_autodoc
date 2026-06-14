#!/bin/bash

# Check if Ollama is already running by pinging the API endpoint.
# If the server is not running, start it.

is_ollama_running() {
    # Use curl to check the API endpoint with a timeout to avoid hanging.
    # The exit code of curl will indicate success or failure.
    curl -s --max-time 5 http://localhost:11434/api/tags >/dev/null
    return $?
}

if is_ollama_running; then
    echo "Ollama already running"
else
    echo "Starting Ollama..."
    ollama serve
fi