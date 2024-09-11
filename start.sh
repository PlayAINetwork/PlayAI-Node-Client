#!/bin/bash

# Start the task getting service in the background
python main.py &
FILE1_PID=$!

# Start Flask endpoint for health in foreground
python app.py &
APP_PID=$!

cleanup() {
    echo "Stopping services..."
    kill $FILE1_PID  # Stop main.py
    kill $APP_PID    # Stop app.py (Flask)
    wait $FILE1_PID  # Ensure the background process is completely stopped
    wait $APP_PID    # Ensure Flask process is completely stopped
    exit
}

# Trap termination signals together
trap cleanup INT TERM

while true; do
    if ! kill -0 $FILE1_PID >/dev/null 2>&1; then
        echo "main.py has exited."
        exit 1
    fi
    sleep 1
done
