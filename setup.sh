#!/bin/bash
# Setup script for Bank Statement Analyzer

set -e

echo "========================================"
echo "Bank Statement Analyzer - Setup"
echo "========================================"
echo

# Check if venv exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo
echo "Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo

echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q pandas

echo "✓ Dependencies installed"
echo

echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "To use the analyzer:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo
echo "  2. Run the analyzer:"
echo "     python3 main.py"
echo
echo "  3. Check results in output/ folder"
echo
