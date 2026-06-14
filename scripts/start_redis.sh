#!/bin/bash
set -e

# Trap Ctrl+C to stop containers and exit
trap 'echo "Stopping Redis container..."; docker compose down; exit 1' SIGINT

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Start Redis container using Docker Compose
echo "Starting Redis container..."
docker compose up -d

# Wait for Redis container to be running
CONTAINER_NAME="autodoc-redis"
echo "Waiting for $CONTAINER_NAME to start..."
until docker inspect --format='{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null | grep -q 'true'; do
  echo "Waiting for $CONTAINER_NAME to start..."
  sleep 1
done

# Follow Redis container logs
echo "Following logs for $CONTAINER_NAME..."
docker logs -f "$CONTAINER_NAME"