#!/bin/bash
set -e

# Script to start Redis container with Docker Compose
# Usage: ./start_redis.sh

# Check if Docker is running, start Docker Desktop if not
if ! docker info >/dev/null 2>&1; then
    echo "Starting Docker Desktop..."
    open -a Docker
    echo "Waiting for Docker to start..."
    until docker info >/dev/null 2>&1; do
        sleep 2
    done
fi

# Trap Ctrl+C to stop containers and exit
trap 'echo "Stopping Redis container..."; docker compose down; exit 1' SIGINT

# Navigate to the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "Error: Project root directory not found at $PROJECT_ROOT" >&2
    exit 1
fi
cd "$PROJECT_ROOT"

# Start Redis container using Docker Compose
echo "Starting Redis container..."
docker compose up -d

# Wait for Redis container to be running with timeout
CONTAINER_NAME="autodoc-redis"
MAX_WAIT=30
WAIT_COUNT=0

echo "Waiting for $CONTAINER_NAME to start..."
until docker inspect --format='{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null | grep -q 'true'; do
    if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
        echo "Error: Timeout waiting for $CONTAINER_NAME to start" >&2
        docker compose down
        exit 1
    fi
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

# Follow Redis container logs
echo "Following logs for $CONTAINER_NAME..."
docker logs -f "$CONTAINER_NAME"