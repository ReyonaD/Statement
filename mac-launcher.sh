#!/bin/bash
# Bank Statement Analyzer - Mac Launcher
# This script sets up and launches the web application

# Color codes for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Bank Statement Analyzer                    ║${NC}"
echo -e "${BLUE}║    Starting Application...                     ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚙${NC}  Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import pandas" &> /dev/null || ! python3 -c "import flask" &> /dev/null; then
    echo -e "${YELLOW}⚙${NC}  Installing dependencies (this may take a minute)..."
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${GREEN}✓${NC} Dependencies already installed"
fi

# Create statements folder if it doesn't exist
mkdir -p statements
mkdir -p output

echo ""
echo -e "${GREEN}✓${NC} Setup complete!"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Starting Bank Statement Analyzer...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo ""
echo -e "The application will open in your browser at:"
echo -e "${YELLOW}http://localhost:5000${NC}"
echo ""
echo -e "${RED}⚠️  DO NOT CLOSE THIS WINDOW!${NC}"
echo -e "Keep this window open while using the app."
echo ""
echo -e "To stop the application: Press ${YELLOW}Ctrl+C${NC}"
echo ""

# Wait a moment for user to read
sleep 2

# Start the Flask app in background
python3 app.py &
APP_PID=$!

# Wait for the server to start
sleep 3

# Try to open in browser
if command -v open &> /dev/null; then
    open http://localhost:5000
else
    echo "Please open your browser and go to: http://localhost:5000"
fi

echo ""
echo -e "${GREEN}✓ Application is running!${NC}"
echo ""
echo -e "To stop: Press ${YELLOW}Ctrl+C${NC} or close this window"
echo ""

# Wait for the Flask app to finish (user presses Ctrl+C)
wait $APP_PID
