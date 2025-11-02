# ESC/POS Network Printer - Setup and Usage Guide

This documentation provides detailed information about the installation and usage of the ESC/POS Network Printer system.

## Table of Contents

1. [About the System](#about-the-system)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Starting the Application](#starting-the-application)
5. [Web Interface](#web-interface)
6. [Environment Variables](#environment-variables)
7. [Troubleshooting](#troubleshooting)
8. [Port Information](#port-information)

---

## About the System

ESC/POS Network Printer is a system that receives thermal printer commands (ESC/POS), converts them to HTML format, and displays them in a web interface. It runs directly on Windows without Docker.

### Features

- **ESC/POS Support**: Processes standard thermal printer commands
- **HTML Conversion**: Converts receipts to browser-viewable HTML
- **JetDirect Protocol**: Printer communication over port 9100
- **Web Interface**: View all printed receipts
- **Windows Notifications**: Shows notifications when printing completes
- **Duration Measurement**: Displays how long each print job takes
- **Real-time Updates**: Vue.js powered live receipt preview via Server-Sent Events

---

## Prerequisites

### 1. Python Installation

**Required Version**: Python 3.8 or higher

**Download**:
- https://www.python.org/downloads/
- Check **"Add Python to PATH"** during installation!

**Verification**:
```bash
python --version
```

### 2. PHP and Composer Installation

**PHP**: 8.2 or higher (already installed if you have XAMPP)

**Composer**:
- https://getcomposer.org/download/
- Must be installed globally

**Verification**:
```bash
php --version
composer --version
```

### 3. XAMPP (Optional)

If you don't want to install PHP and Composer separately, XAMPP includes all requirements.

---

## Installation Steps

### Step 1: Place Files

Copy the ESC/POS Network Printer files to this location:
```
C:\xampp\htdocs\escpos-netprinter\
```

### Step 2: Install Python Libraries

Open Command Prompt (CMD) and run these commands:

```bash
pip install Flask
pip install lxml
pip install winotify
pip install pystray
pip install Pillow
```

**Description**:
- **Flask**: For web server and HTTP API
- **lxml**: For HTML/XML processing
- **winotify**: For Windows 10/11 notification system
- **pystray**: For system tray icon
- **Pillow**: For image processing

### Step 3: Install PHP Libraries

Navigate to escpos-netprinter folder in Command Prompt:

```bash
cd C:\xampp\htdocs\escpos-netprinter
composer install
```

This command will install:
- **mike42/escpos-php**: ESC/POS command processing
- **chillerlan/php-qrcode**: QR code generation
- Other dependencies

### Step 4: Create Required Folders

Create these folders if they don't exist:

```bash
cd C:\xampp\htdocs\escpos-netprinter
mkdir web\receipts
mkdir web\tmp
```

**Description**:
- **web/receipts**: Where printed HTML receipts are stored
- **web/tmp**: Where temporary files are kept

### Step 5: Windows Printer Setup

Open PowerShell **as Administrator** and run these commands:

#### 5.1. Create Printer Port

```powershell
Add-PrinterPort -Name "TCP_127.0.0.1_9100" -PrinterHostAddress "127.0.0.1" -PortNumber 9100
```

This creates a TCP/IP printer port.

#### 5.2. Add Printer

```powershell
Add-Printer -Name "ESC/POS Network Printer" -DriverName "Generic / Text Only" -PortName "TCP_127.0.0.1_9100"
```

This adds the printer with "Generic / Text Only" driver.

#### 5.3. Verification

```powershell
Get-Printer | Where-Object {$_.Name -like "*ESC/POS*"}
```

Verify the printer was added successfully.

---

## Starting the Application

### Simple Start (Default Settings)

The simplest usage:

```bash
cd C:\xampp\htdocs\escpos-netprinter
python escpos-netprinter.py
```

This starts with default settings:
- **Web Interface**: http://localhost:8100
- **JetDirect Port**: 9100
- **Debug Mode**: Off

### System Tray Mode (Recommended)

Run with system tray icon:

```bash
cd C:\xampp\htdocs\escpos-netprinter
python escpos-netprinter-tray.py
```

This will:
- Run in the background with a system tray icon
- Right-click the icon for: Open Web Interface, View Receipts, Exit
- No terminal window to keep open

### Standalone EXE (No Python Required)

Build once with:
```bash
build-exe.bat
```

Then run:
```bash
dist\ESC-POS-Printer.exe
```

This provides a ~70MB standalone executable with embedded PHP runtime.

### Advanced Start (With Environment Variables)

Start with customized settings:

```bash
cd C:\xampp\htdocs\escpos-netprinter
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False
python escpos-netprinter.py
```

**Description**:
- **FLASK_RUN_HOST=0.0.0.0**: Access from all network interfaces (0.0.0.0 = accessible from outside)
- **FLASK_RUN_PORT=8100**: Web interface port (default: 80)
- **PRINTER_PORT=9100**: JetDirect printer port
- **ESCPOS_DEBUG=False**: Disable debug logs (True = enabled)

### Add to Windows Startup (Optional)

To start automatically when computer boots:

#### Method 1: Add Shortcut to Startup Folder

1. Create **start-printer.bat** file:

```batch
@echo off
cd C:\xampp\htdocs\escpos-netprinter
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False
python escpos-netprinter.py
```

2. Create a shortcut to this bat file
3. Copy the shortcut to this folder:
```
C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

#### Method 2: Task Scheduler

Use Windows Task Scheduler for more advanced control.

---

## Web Interface

### Home Page
```
http://localhost:8100/
```

The home page shows:
- System status
- Last printed receipt (live preview)
- Total receipt count
- Real-time updates without page refresh

### Receipt List
```
http://localhost:8100/receipts
```

List of all printed receipts:
- Date and time
- Receipt number
- HTML view link

### Single Receipt View
```
http://localhost:8100/receipts/FILENAME.html
```

Full-screen display of a specific receipt.

---

## Environment Variables

Environment variables that control system behavior:

### FLASK_RUN_HOST

**Default**: `127.0.0.1` (local only)
**Recommended**: `0.0.0.0` (for network access)

```bash
set FLASK_RUN_HOST=0.0.0.0
```

**Usage**:
- `127.0.0.1`: Only accessible from the computer itself
- `0.0.0.0`: Accessible from other devices on the network

### FLASK_RUN_PORT

**Default**: `8100`
**Alternative**: `5000`, `80`, etc.

```bash
set FLASK_RUN_PORT=8100
```

**Note**: Using port 80 may require administrator privileges.

### PRINTER_PORT

**Default**: `9100` (JetDirect standard port)

```bash
set PRINTER_PORT=9100
```

**Warning**: If you change this port, the Windows printer port must also be set to the same port!

### ESCPOS_DEBUG

**Default**: `False`
**Values**: `True` or `False`

```bash
set ESCPOS_DEBUG=True
```

**When Debug Mode is On**:
- All ESC/POS commands are logged
- CUPS driver logs are shown
- JetDirect connection details are shown
- Web requests are logged
- Temporary files are not deleted (web/tmp/)

**When Debug Mode is Off**:
- Only error messages are shown
- Cleaner output
- Temporary files are automatically deleted

---

## Troubleshooting

### Problem: Port 9100 in use

**Error Message**:
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solution**:
```bash
netstat -ano | findstr :9100
taskkill /PID XXXX /F
```

### Problem: No Windows notifications

**Check**:
1. Are Windows Notification Settings enabled?
2. Is Python running?

**Solution**:
```bash
# Check Python process
tasklist | findstr python

# Restart if not running
python escpos-netprinter.py
```

### Problem: Printer not found

**Check**:
```powershell
Get-Printer | Where-Object {$_.Name -like "*ESC/POS*"}
```

**Solution - Re-add the printer**:
```powershell
# Check port first
Get-PrinterPort | Where-Object {$_.Name -like "*9100*"}

# Create port if missing
Add-PrinterPort -Name "TCP_127.0.0.1_9100" -PrinterHostAddress "127.0.0.1" -PortNumber 9100

# Add printer
Add-Printer -Name "ESC/POS Network Printer" -DriverName "Generic / Text Only" -PortName "TCP_127.0.0.1_9100"
```

### Problem: HTML receipts not showing

**Possible Causes**:
1. File creation error (error 22)
2. web/receipts folder doesn't exist
3. Permission issue

**Solution**:
```bash
# Check folders
dir C:\xampp\htdocs\escpos-netprinter\web\receipts

# Create if missing
mkdir C:\xampp\htdocs\escpos-netprinter\web\receipts
mkdir C:\xampp\htdocs\escpos-netprinter\web\tmp

# Restart Python
```

### Problem: "Module not found" error

**Error**: `ModuleNotFoundError: No module named 'Flask'`

**Solution**:
```bash
# Reinstall all requirements
pip install Flask lxml winotify pystray Pillow

# Install PHP dependencies
cd C:\xampp\htdocs\escpos-netprinter
composer install
```

### Problem: Port permission error

**Error**: `Permission denied: 127.0.0.1:80`

**Solution 1**: Use a different port
```bash
set FLASK_RUN_PORT=8100
python escpos-netprinter.py
```

**Solution 2**: Open CMD as Administrator

---

## Port Information

The system uses 2 main ports:

### Port 9100 - JetDirect (Printer Protocol)

**Usage**: To receive ESC/POS commands
**Protocol**: TCP/IP
**Connected by**: External applications sending print jobs

**Check**:
```bash
netstat -an | findstr :9100
```

### Port 8100 - Web Interface

**Usage**: To view receipts in browser
**Protocol**: HTTP
**URL**: http://localhost:8100

**Check**:
```bash
netstat -an | findstr :8100
```

---

## System Architecture

```
┌─────────────────────┐
│  Your Application   │  (Any system that can print to network printer)
│   (POS/Inventory)   │
└──────────┬──────────┘
           │ Print Job (ESC/POS commands)
           ▼
┌─────────────────────┐
│ Windows Printer     │  (Generic / Text Only driver)
│ Spooler (Port 9100) │
└──────────┬──────────┘
           │ TCP Socket (127.0.0.1:9100)
           ▼
┌─────────────────────┐
│ escpos-netprinter   │  (Port 9100 + Web 8100)
│  (Python/Flask)     │
└──────────┬──────────┘
           │
           ├─> HTML receipts (web/receipts/)
           ├─> Windows Notification
           └─> Real-time web preview (Vue.js + SSE)
```

---

## Security Notes

### 1. Use Only on Local Network

This system should not be exposed to the internet:
- Uses Flask development server (not suitable for production)
- No authentication
- No encryption

### 2. Firewall Settings

If network access is needed:
- Allow access only from trusted local network
- Open ports 9100 and 8100 only to local network
- Use VPN

### 3. Protect Receipt Data

Printed receipts may contain sensitive information:
- Backup the `web/receipts/` folder regularly
- Delete old receipts regularly
- Check folder permissions

---

## Performance Tips

### 1. Disable Debug Mode

For production use:
```bash
set ESCPOS_DEBUG=False
```

### 2. Clean Old Receipts

Manual cleanup:
```bash
del /Q C:\xampp\htdocs\escpos-netprinter\web\receipts\*.html
```

Use Windows Task Scheduler for automatic cleanup.

### 3. Clean Temporary Files

```bash
del /Q C:\xampp\htdocs\escpos-netprinter\web\tmp\*.*
```

---

## FAQ (Frequently Asked Questions)

### Q: Can I use this on multiple computers?

**A**: Yes! On each computer:
1. Install Python and dependencies
2. Start escpos-netprinter
3. Each computer will show its own receipts on its own screen

### Q: Can I also print to a real printer?

**A**: Yes! Using Windows Printer Sharing:
1. Share the ESC/POS Network Printer
2. Configure "Copy print jobs" on a real thermal printer
3. You can get receipts both in HTML and on paper

### Q: How long should I keep the receipts?

**A**: Depends on your needs:
- For accounting records: Minimum 7 years
- For daily operations: 30-90 days
- If disk space is limited: 7-15 days

### Q: Why is port 9100 used?

**A**: Port 9100 is the standard port for HP JetDirect protocol. Most printer drivers automatically recognize this port.

---

## License and Copyright

This system is developed using open-source ESC/POS tools:

- **escpos-netprinter**: Originally developed by gilbertfl
- **mike42/escpos-php**: MIT License
- **Flask**: BSD License
- **Vue.js**: MIT License

---

## Support and Contact

If you're experiencing issues:

1. **Check logs**: Run with `ESCPOS_DEBUG=True`
2. **Check ports**: `netstat -an | findstr :9100`
3. **Check Python version**: `python --version` (3.8+)

---

**Last Updated**: 2025-01-03
**Version**: 2.0 (Vue.js Edition)
