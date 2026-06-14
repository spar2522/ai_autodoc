#!/bin/bash

if curl -s http://localhost:11434/api/tags >/dev/null
then
    echo "Ollama already running"
else
    echo "Starting Ollama..."
    ollama serve
fi