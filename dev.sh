#!/bin/bash

case "$1" in
frontend-dev)
  echo "Starting backend development server..."
  cd backend
  if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  else
    source .venv/bin/activate
  fi
  python3 main.py &
  echo "Starting frontend development server..."
  cd ../app
  npm run frontend-dev | sed 's/^/[FRONTEND] /'
  ;;
app-dev)
  echo "Starting app development server..."
  # Add your app development server start command here
  ;;
frontend-build)
  echo "Building frontend..."
  # Add your frontend build command here
  ;;
backend-build)
  echo "Building backend..."
  # Add your backend build command here
  ;;
*)
  echo "Usage: $0 {frontend-dev|app-dev|frontend-build|backend-build}"
  exit 1
  ;;
esac
