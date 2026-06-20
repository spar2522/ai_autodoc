#!/bin/bash

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "======================================="
echo "Cleaning up previous AutoDoc processes"
echo "======================================="

# Stop previous API instance
echo "Stopping API..."
lsof -ti:9000 | xargs kill -9 2>/dev/null || true

# Stop previous worker instances
echo "Stopping Workers..."
pkill -f "autodoc/worker/start_worker.py" 2>/dev/null || true

# Stop previous ngrok instances
echo "Stopping ngrok..."
pkill -f "ngrok http 9000" 2>/dev/null || true

sleep 1

echo "Cleanup complete."
echo ""
# Check for required scripts
required_scripts=(
    "start_redis.sh"
    "start_ollama.sh"
    "start_api.sh"
    "start_workers.sh"
    "start_ngrok.sh"
)

for script in "${required_scripts[@]}"; do
    if [ ! -f "./scripts/$script" ]; then
        echo "Error: Required script './scripts/$script' not found."
        exit 1
    fi
done

osascript <<EOF
tell application "iTerm"
    # Create main window with Redis profile
    # Ensure "Redis" profile exists in iTerm preferences
    create window with profile "Redis"
    
    # Configure Redis session
    tell current session of current window
        write text "cd $PROJECT_ROOT && ./scripts/start_redis.sh"
    end tell
    
    # Create additional tabs in the same window
    tell current window
        # Ollama tab
        # Ensure "Ollama" profile exists in iTerm preferences
        create tab with profile "Ollama"
        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_ollama.sh"
        end tell
        
        # API tab
        # Ensure "API" profile exists in iTerm preferences
        create tab with profile "API"
        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_api.sh"
        end tell
        
        # Workers tab
        # Ensure "Workers" profile exists in iTerm preferences
        create tab with profile "Workers"
        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_workers.sh"
        end tell
        
        # Ngrok tab
        # Ensure "Ngrok" profile exists in iTerm preferences
        create tab with profile "Ngrok"
        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_ngrok.sh"
        end tell
    end tell
end tell
EOF