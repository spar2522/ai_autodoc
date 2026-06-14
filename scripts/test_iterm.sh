#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

osascript <<EOF

tell application "iTerm"

    create window with profile "Redis"

    tell current session of current window
        write text "cd $PROJECT_ROOT && ./scripts/start_redis.sh"
    end tell

    tell current window

        create tab with profile "Ollama"

        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_ollama.sh"
        end tell

        create tab with profile "API"

        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_api.sh"
        end tell

        create tab with profile "Workers"

        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_workers.sh"
        end tell

        create tab with profile "Ngrok"

        tell current session
            write text "cd $PROJECT_ROOT && ./scripts/start_ngrok.sh"
        end tell

    end tell

end tell

EOF