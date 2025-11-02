@echo off
REM ESC/POS Network Printer Starter Script
REM Author: Kerim Şentürk
REM
REM This script starts the ESC/POS network printer with recommended settings
REM for Windows environments.

title ESC/POS Network Printer

echo ====================================================
echo  ESC/POS Network Printer for Windows
echo  Author: Kerim Senturk
echo  Based on: gilbertfl/escpos-netprinter
echo ====================================================
echo.

REM Navigate to the script directory
cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo OK - Python found
echo.

echo [2/3] Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Flask not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo OK - Dependencies ready
echo.

echo [3/3] Starting ESC/POS Network Printer...
echo.
echo Configuration:
echo   - Web Interface: http://localhost:8100
echo   - JetDirect Port: 9100
echo   - Debug Mode: OFF
echo.
echo Press Ctrl+C to stop the server
echo ====================================================
echo.

REM Set environment variables
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False

REM Start the printer server
python escpos-netprinter.py

REM If the server stops, pause to show error messages
pause
