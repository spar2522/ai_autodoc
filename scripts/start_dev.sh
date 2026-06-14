#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

osascript <<'EOF'
tell application "iTerm"
    create window with default profile
    
    set commands to {"docker compose up", "./scripts/start_ollama.sh", "./scripts/start_api.sh", "./scripts/start_workers.sh", "./scripts/start_ngrok.sh"}
    
    repeat with cmd in commands
        tell current window
            create tab with default profile
        end tell
        
        tell current session of current window
            write text "cd $PROJECT_ROOT && " & cmd
        end tell
    end repeat
end tell
EOF