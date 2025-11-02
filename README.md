# escpos-netprinter-plus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PHP 8.2+](https://img.shields.io/badge/php-8.2+-purple.svg)](https://www.php.net/)
[![Vue.js 3](https://img.shields.io/badge/vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com/kerim92/escpos-netprinter-plus)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Enhanced ESC/POS thermal printer emulator** with native notifications and duration tracking. Converts thermal printer commands to HTML receipts and displays them in a web interface.

Perfect for development, testing, and production environments where you need to capture and view thermal printer output without physical hardware. No Docker required - runs natively on all platforms.

**Key Features:** ✨ Toast Notifications • ⏱️ Duration Tracking • 🌍 Cross-platform Support • 🔌 Easy Integration

![ESC/POS Network Printer](https://github.com/gilbertfl/escpos-netprinter/assets/83510612/8aefc8c5-01ab-45f3-a992-e2850bef70f6)

## 🌟 Features

### Core Features
- **ESC/POS Protocol Support**: Full support for standard thermal printer commands
- **JetDirect Protocol**: Listens on port 9100 (standard JetDirect port)
- **LPD Protocol**: Listens on port 515
- **HTML Conversion**: Converts ESC/POS commands to beautiful HTML receipts
- **Web Interface**: View all printed receipts in your browser
- **No Docker Required**: Runs directly on Windows with Python

### New Features (Plus Version)
- ✨ **Native Desktop Notifications**: Platform-specific notifications when printing completes (Windows toast, macOS/Linux console)
- ⏱️ **Print Duration Tracking**: Shows exact time taken for each print job
- 🔄 **Real-time Receipt Preview**: Vue.js 3 powered live updates via Server-Sent Events (SSE)
- 🖼️ **Visual Receipt Display**: Interactive printer visualization with live receipt preview overlay
- 🌍 **Multi-language Support**: Notifications in English (easily customizable to other languages)
- 🔧 **Cross-platform Filename Fix**: Fixed datetime format to avoid illegal characters in filenames
- 🔌 **External System Integration**: Easy integration with any inventory or POS system
- 📊 **Real-time Status Updates**: Live feedback on print operations without page refresh
- 🖥️ **Platform Detection**: Automatically adapts to Windows, macOS, or Linux
- 📦 **Portable PHP**: Embedded PHP runtime for standalone EXE deployment

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Testing](#testing)
- [Web Interface](#web-interface)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## 🔧 Requirements

### Python Dependencies
- Python 3.8 or higher
- Flask (web server)
- lxml (HTML/XML processing)
- Platform-specific notification libraries:
  - **Windows**: win10toast (✅ Tested)
  - **macOS**: osascript (⚠️ Untested - community feedback welcome!)
  - **Linux**: notify-send (⚠️ Untested - community feedback welcome!)

### PHP Dependencies
- PHP 8.2 or higher
- Composer
- mike42/escpos-php (ESC/POS processing)
- chillerlan/php-qrcode (QR code generation)

### System Requirements & Platform Support

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| **Core ESC/POS Processing** | ✅ Tested | ✅ Should work | ✅ Should work |
| **Web Interface** | ✅ Tested | ✅ Should work | ✅ Should work |
| **JetDirect (Port 9100)** | ✅ Tested | ✅ Should work | ✅ Should work |
| **Desktop Notifications** | ✅ Tested (toast) | ⚠️ Untested (osascript) | ⚠️ Untested (notify-send) |
| **Print Duration Tracking** | ✅ Tested | ✅ Should work | ✅ Should work |

**Testing Status:**
- **Windows 10/11**: Fully tested ✅ (build 26100)
- **macOS**: Core features should work, notifications untested ⚠️
- **Linux**: Core features should work, notifications untested ⚠️

**Community Contributions Welcome!** If you test on macOS or Linux, please share your experience via GitHub Issues.

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/kerim92/escpos-netprinter-plus.git
cd escpos-netprinter-plus
```

### Step 2: Install Python Dependencies

```bash
# All platforms
pip install Flask lxml

# Windows only (for toast notifications)
pip install win10toast
```

Or use requirements.txt (automatically installs platform-specific packages):

```bash
pip install -r requirements.txt
```

**Platform-Specific Notes:**
- **Windows**: `win10toast` will be installed automatically
- **macOS**: No extra Python packages needed (uses osascript)
- **Linux**: Install system package: `sudo apt-get install libnotify-bin`

### Step 3: Install PHP Dependencies

```bash
composer install
```

### Step 3.5: Platform-Specific Setup

#### Windows
Continue to Step 5 for Windows printer setup.

#### macOS
Install CUPS (usually pre-installed):
```bash
# CUPS should be available by default
lpstat -p  # List available printers
```

#### Linux
Install CUPS:
```bash
sudo apt-get install cups cups-client  # Debian/Ubuntu
# or
sudo yum install cups  # RHEL/CentOS
```

### Step 4: Setup Printer

**Note:** The required directories (`web/receipts` and `web/tmp`) are already included in the repository via `.gitkeep` files.

#### Windows

Open PowerShell **as Administrator** and run:

```powershell
# Create TCP/IP printer port
Add-PrinterPort -Name "TCP_127.0.0.1_9100" -PrinterHostAddress "127.0.0.1" -PortNumber 9100

# Add printer with Generic/Text Only driver
Add-Printer -Name "ESC/POS Network Printer" -DriverName "Generic / Text Only" -PortName "TCP_127.0.0.1_9100"
```

Verify installation:

```powershell
Get-Printer | Where-Object {$_.Name -like "*ESC/POS*"}
```

#### macOS / Linux

Use CUPS to add a network printer:

```bash
# Add printer via CUPS web interface
open http://localhost:631/admin  # macOS
# or visit http://localhost:631/admin in browser (Linux)

# Or use command line
lpadmin -p "ESCPOS-Network-Printer" -v socket://127.0.0.1:9100 -E
```

## 🚀 Quick Start

### Option 1: Standalone EXE (No Python Required) ⭐

**For users who don't have Python installed:**

1. Build the EXE (one-time only):
```bash
# Double-click build-exe.bat
# Or run manually:
build-exe.bat
```

2. Run the generated EXE:
```bash
# Located in dist/ folder after build
dist\ESC-POS-Printer.exe
```

This will:
- Run with system tray icon (no terminal window)
- No Python installation required (~37MB standalone executable)
- Right-click the tray icon for: Open Web Interface, View Receipts, Exit

**Note**: The EXE build process takes 2-3 minutes and requires Python + PyInstaller. After building once, you can distribute the EXE to any Windows PC without Python.

### Option 2: System Tray Mode with Python

Run with system tray icon (requires Python):

```bash
cd C:\path\to\escpos-netprinter
python escpos-netprinter-tray.py
```

This will:
- Run in the background with a system tray icon
- Right-click the icon for: Open Web Interface, View Receipts, Exit
- No terminal window to keep open

**Requirements for System Tray:**
```bash
pip install pystray Pillow
```

### Basic Usage (Terminal Mode)

```bash
cd C:\path\to\escpos-netprinter
python escpos-netprinter.py
```

The server will start with default settings:
- **Web Interface**: http://localhost:5000
- **JetDirect Port**: 9100
- **LPD Port**: 515

### Advanced Usage with Environment Variables

```bash
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=8100
set PRINTER_PORT=9100
set ESCPOS_DEBUG=False
python escpos-netprinter.py
```

### Windows Startup (Optional)

#### Option 1: System Tray (Recommended)

Create a shortcut to `escpos-netprinter-tray.py` and place it in:
```
C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

Or use the included `start-printer-hidden.vbs` for silent startup:
```batch
# Double-click start-printer-hidden.vbs - runs in background without terminal
```

#### Option 2: Terminal Mode

Use the included `start-printer.bat`:

```batch
cd C:\path\to\escpos-netprinter
start-printer.bat
```

Or place shortcut to `start-printer.bat` in the Startup folder.

### macOS/Linux Startup (Optional)

Use the included `start-printer.sh`:

```bash
cd /path/to/escpos-netprinter
chmod +x start-printer.sh
./start-printer.sh
```

For automatic startup on macOS, create a LaunchAgent:
```bash
# Create plist file at ~/Library/LaunchAgents/com.escpos.printer.plist
# See documentation for details
```

For automatic startup on Linux, add to systemd:
```bash
# Create service file at /etc/systemd/system/escpos-printer.service
# See documentation for details
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_RUN_HOST` | `127.0.0.1` | Web server host (use `0.0.0.0` for network access) |
| `FLASK_RUN_PORT` | `80` | Web interface port |
| `PRINTER_PORT` | `9100` | JetDirect printer port |
| `ESCPOS_DEBUG` | `false` | Enable verbose logging |

### Debug Mode

Enable debug mode for troubleshooting:

```bash
set ESCPOS_DEBUG=True
python escpos-netprinter.py
```

Debug mode provides:
- Detailed ESC/POS command logs
- CUPS driver logs
- JetDirect connection details
- Web request logs
- Temporary files are not deleted

## 🧪 Testing

### Test 1: Basic Connectivity

Check if ports are listening:

```bash
netstat -an | findstr :9100
netstat -an | findstr :5000
```

Expected output:
```
TCP    0.0.0.0:9100           0.0.0.0:0              LISTENING
TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING
```

### Test 2: Simple Print Test

Send test data via telnet:

```bash
# Install telnet if needed (Windows Features)
telnet localhost 9100
```

Then type:
```
Hello World
```

Press `Ctrl+]`, then type `quit`.

Check web interface at http://localhost:5000/receipts - you should see the receipt.

### Test 3: Performance Test

Print 10 receipts and check average duration:

```bash
# Check Python console output
Address connected: ('127.0.0.1', 12345)
19 bytes received.
Receipt decoded
Receipt printed! Duration: 0.15 seconds
```

Average should be < 0.5 seconds per receipt.

### Test 4: Windows Notification Test

Manually trigger notification (Python):

```python
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast(
    "Printer - Success",
    "Receipt printed!\nDuration: 0.25 seconds",
    duration=5
)
```

## 🌐 Web Interface

### Main Page
```
http://localhost:5000/
```

Shows:
- System status
- Last printed receipt
- Total receipt count

### Receipt List
```
http://localhost:5000/receipts
```

Browse all printed receipts:
- Chronological order
- Date and time
- Clickable links to view full receipt

### Individual Receipt
```
http://localhost:5000/receipts/receipt2025Jan02_143045.123456EST.html
```

View specific receipt in full-screen HTML format.

## 🐛 Troubleshooting

### Problem: Port 9100 already in use

**Error**: `OSError: [WinError 10048] Only one usage of each socket address`

**Solution**:
```bash
netstat -ano | findstr :9100
taskkill /PID <PID> /F
```

### Problem: No Windows notifications

**Check**:
1. Windows notification settings enabled?
2. Python process running?

**Solution**:
```bash
# Verify Python is running
tasklist | findstr python

# Restart if needed
python escpos-netprinter.py
```

### Problem: Receipts not saving (Error 22)

**Cause**: Filename contains illegal characters (fixed in this fork)

**Verification**:
Check that `escpos-netprinter.py` line 1437 uses:
```python
html_filename = 'receipt{}.html'.format(heureRecept.strftime('%Y%b%d_%H%M%S.%f%Z'))
```

NOT:
```python
html_filename = 'receipt{}.html'.format(heureRecept.strftime('%Y%b%d_%X.%f%Z'))  # ❌ Wrong
```

### Problem: Module not found

**Error**: `ModuleNotFoundError: No module named 'Flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Frontend Notice

**Note from the author**: I'm not a frontend expert - I did my best to create a visually appealing receipt display interface using Vue.js 3 and CSS. If you're experienced with frontend development and would like to improve the UI/UX, animations, or visual design, I would greatly appreciate your contributions! The receipt preview visualization (templates/accueil.html.j2) is especially open to improvements.

### Areas for Contribution

- [ ] **Frontend/UI Improvements** - Better animations, responsive design, modern UI frameworks
- [ ] Multi-language support (extend beyond Turkish)
- [ ] Customizable notification sounds
- [ ] PDF export of receipts
- [ ] Email receipts functionality
- [ ] SQLite database for receipt storage
- [ ] Windows Service installer
- [ ] GUI configuration tool
- [ ] macOS/Linux native notifications testing

## 📜 Credits

### Original Project

This is a fork of [escpos-netprinter](https://github.com/gilbertfl/escpos-netprinter) by **gilbertfl**.

**Original Features**:
- ESC/POS protocol handling
- JetDirect and LPD server
- HTML conversion
- Web interface
- Docker container support

### Dependencies

- **[mike42/escpos-php](https://github.com/mike42/escpos-php)** - ESC/POS printer library for PHP (MIT License)
- **[chillerlan/php-qrcode](https://github.com/chillerlan/php-qrcode)** - QR code generator (MIT License)
- **[Flask](https://flask.palletsprojects.com/)** - Python web framework (BSD License)
- **[lxml](https://lxml.de/)** - XML/HTML processing library (BSD License)
- **[win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications)** - Windows notifications (BSD License)

### Special Thanks

- **gilbertfl** - For creating the original escpos-netprinter project
- **Mike Connelly (mike42)** - For the excellent escpos-php library
- **ESC/POS Community** - For documentation and support
- **Claude Code** - Claude helped me a lot, thanks to [Claude Code](https://claude.com/claude-code) for helping me build this project

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2025 Kerim Şentürk (escpos-netprinter-plus)
Copyright (c) 2024 gilbertfl (original escpos-netprinter)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔗 Related Projects

- [escpos-netprinter](https://github.com/gilbertfl/escpos-netprinter) - Original Docker-based project
- [escpos-php](https://github.com/mike42/escpos-php) - PHP ESC/POS library
- [python-escpos](https://github.com/python-escpos/python-escpos) - Python ESC/POS library
- [node-escpos](https://github.com/song940/node-escpos) - Node.js ESC/POS library

## 📊 Project Status

- ✅ Core functionality working
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ Platform-specific notifications (Windows)
- ✅ Production-ready
- 🚧 macOS/Linux native notifications (planned)
- 🚧 GUI configuration tool (planned)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/kerim92/escpos-netprinter-plus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kerim92/escpos-netprinter-plus/discussions)
- **Documentation**: [Wiki](https://github.com/kerim92/escpos-netprinter-plus/wiki)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ for the open-source community**
