#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

osascript <<EOF
tell application "iTerm"

    create window with default profile

    tell current session of current window
        write text "cd $PROJECT_ROOT && docker compose up"
    end tell

    tell current window
        create tab with default profile
    end tell

    tell current session of current window
        write text \"cd $PROJECT_ROOT && ./scripts/start_ollama.sh\"
    end tell

    tell current window
        create tab with default profile
    end tell

    tell current session of current window
        write text \"cd $PROJECT_ROOT && ./scripts/start_api.sh\"
    end tell

    tell current window
        create tab with default profile
    end tell

    tell current session of current window
        write text \"cd $PROJECT_ROOT && ./scripts/start_workers.sh\"
    end tell

    tell current window
        create tab with default profile
    end tell

    tell current session of current window
        write text \"cd $PROJECT_ROOT && ./scripts/start_ngrok.sh\"
    end tell

end tell
EOF