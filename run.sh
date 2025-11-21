#!/bin/bash
# Quick launcher for Bank Statement Analyzer Web App

set -e

echo "🚀 Starting Bank Statement Analyzer..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: ./setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install -q flask
fi

# Run the app
echo "✓ Launching web application..."
echo
python3 app.py
