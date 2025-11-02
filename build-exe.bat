@echo off
REM ESC/POS Network Printer - EXE Builder
REM Author: Kerim Şentürk
REM
REM This script builds a standalone Windows EXE with PyInstaller

title Building ESC/POS Network Printer EXE

echo ====================================================
echo  Building ESC/POS Network Printer EXE
echo  Author: Kerim Senturk
echo ====================================================
echo.

REM Navigate to the script directory
cd /d "%~dp0"

echo [1/3] Checking Python and PyInstaller...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo OK - Python and PyInstaller ready
echo.

echo [2/3] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo OK - Clean completed
echo.

echo [3/3] Building EXE (this may take a few minutes)...
python -m PyInstaller ^
    --name="ESC-POS-Printer" ^
    --onefile ^
    --windowed ^
    --add-data="escpos-netprinter.py;." ^
    --add-data="templates;templates" ^
    --add-data="web;web" ^
    --hidden-import=win10toast ^
    --hidden-import=pystray ^
    --hidden-import=PIL ^
    --hidden-import=flask ^
    --hidden-import=lxml ^
    --hidden-import=zoneinfo ^
    --hidden-import=socketserver ^
    --hidden-import=csv ^
    --hidden-import=subprocess ^
    --hidden-import=datetime ^
    escpos-netprinter-tray.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ====================================================
echo  Build Complete!
echo ====================================================
echo.
echo  EXE Location: dist\ESC-POS-Printer.exe
echo  Size: ~37 MB
echo.
echo  You can now run the EXE without Python installed!
echo ====================================================
echo.

explorer dist

pause
