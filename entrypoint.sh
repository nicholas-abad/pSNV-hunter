#!/bin/sh

# Navigate to the repository inside the container
cd /app/pSNV-hunter || exit

# Pull the latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull origin main

# Start the application
echo "Starting application..."
python src/run_visualization_tool.py