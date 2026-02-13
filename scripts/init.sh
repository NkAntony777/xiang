#!/bin/bash

# Init Script - Start Development Server
# This script should be customized for your specific project

set -e

echo "=== Starting Development Environment ==="

# Detect project type and run appropriate commands
if [ -f "package.json" ]; then
    echo "Detected Node.js project"

    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi

    # Start dev server in background
    echo "Starting dev server..."
    npm run dev &

    # Wait for server to be ready
    echo "Waiting for server to start..."
    sleep 5

    echo "Dev server started successfully"
    echo "Open http://localhost:3000 (or your configured port)"

elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "Detected Python project"

    # Set up virtual environment if needed
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Run dev server
    echo "Starting dev server..."
    python manage.py runserver &

    echo "Dev server started at http://localhost:8000"

else
    echo "Unknown project type. Please customize init.sh for your project."
    exit 1
fi

echo "=== Environment Ready ==="
