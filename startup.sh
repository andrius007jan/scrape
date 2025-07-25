#!/bin/sh
echo "Starting script"

echo "Removing /tmp/.X0-lock"
rm -f /tmp/.X0-lock

echo "Starting Xvfb on display 0"
Xvfb :0 -screen 0 1280x720x16 &

echo "Starting fluxbox window manager on display 0"
fluxbox -display :0 &

echo "Starting x11vnc on display 0"
x11vnc -display :0 -forever -usepw &

echo "Starting uvicorn server"
uvicorn scraping_service.app:app --host 0.0.0.0 --port 8000
