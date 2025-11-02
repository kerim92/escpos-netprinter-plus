#!/bin/bash
# ESC/POS Network Printer Starter Script
# Author: Kerim Şentürk
#
# This script starts the ESC/POS network printer with recommended settings
# for macOS and Linux environments.

echo "===================================================="
echo "  ESC/POS Network Printer for macOS/Linux"
echo "  Author: Kerim Senturk"
echo "  Based on: gilbertfl/escpos-netprinter"
echo "===================================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "[1/3] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi
echo "OK - Python found ($(python3 --version))"
echo ""

echo "[2/3] Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "WARNING: Flask not found. Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi
echo "OK - Dependencies ready"
echo ""

echo "[3/3] Starting ESC/POS Network Printer..."
echo ""
echo "Configuration:"
echo "  - Web Interface: http://localhost:8100"
echo "  - JetDirect Port: 9100"
echo "  - Debug Mode: OFF"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================================="
echo ""

# Set environment variables
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8100
export PRINTER_PORT=9100
export ESCPOS_DEBUG=False

# Start the printer server
python3 escpos-netprinter.py
