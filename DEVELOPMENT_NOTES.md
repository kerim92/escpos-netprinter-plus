# Development Notes - escpos-netprinter-plus

## Project Overview
Enhanced ESC/POS thermal printer emulator with cross-platform desktop notifications, duration tracking, and SmartStock integration.

**Author:** Kerim Şentürk
**Based on:** gilbertfl/escpos-netprinter
**Project Name:** escpos-netprinter-plus
**GitHub:** https://github.com/kerim92/escpos-netprinter-plus

---

## Development Timeline

### Initial Setup (From Original Project)
- Started with gilbertfl/escpos-netprinter (Docker-based)
- Removed Docker dependency
- Installed in Windows environment (XAMPP)
- Fixed file creation error (error 22) by changing datetime format from `%X` to `%H%M%S`

### Phase 1: Windows Toast Notifications
**Goal:** Add Windows balloon notifications when printing completes

**Implementation:**
1. Installed `win10toast` package
2. Modified `escpos-netprinter.py`:
   - Added start time tracking at beginning of `handle()` method
   - Added notification after HTML file creation
   - Used threading to avoid blocking main process
3. Fixed Turkish messages (initially Turkish, later changed to English)

**Files Modified:**
- `escpos-netprinter.py` (line 63: start_time, lines 1472-1513: notification code)
- `requirements.txt` (added win10toast)

### Phase 2: SmartStock Connector Build
**Goal:** Remove old startup scripts and build new EXE

**Implementation:**
1. Removed old startup shortcuts from Windows Startup folder
2. Installed `electron-builder` as dev dependency
3. Fixed package.json issues:
   - Moved electron from dependencies to devDependencies
   - Removed icon configuration (size issue)
   - Disabled code signing
4. Successfully built new EXE

**Files Modified:**
- `C:\SmartStock-Connector\package.json`

### Phase 3: GitHub Publication Preparation
**Goal:** Prepare comprehensive documentation for open-source release

**Implementation:**
1. Created project documentation:
   - `README.md` - Complete installation guide, features, testing
   - `requirements.txt` - Python dependencies
   - `LICENSE` - MIT License
   - `.gitignore` - Standard Python/PHP ignore patterns
   - `CONTRIBUTING.md` - Contribution guidelines
   - `CHANGELOG.md` - Version history
   - `start-printer.bat` - Windows startup script
   - `networkprinter.md` - Turkish installation guide

2. Project naming evolution:
   - Initial: "escpos-netprinter-windows"
   - Changed to: "escpos-netprinter-plus" (for cross-platform support)

3. Feature descriptions:
   - Changed "Docker-free" to "standalone"
   - Added proper credits to original author (gilbertfl)
   - Added badges for licenses and platform support

### Phase 4: Cross-Platform Support
**Goal:** Add macOS and Linux support

**Implementation:**
1. Added platform detection in `escpos-netprinter.py`:
   - Detects Windows, macOS, Linux using `platform.system()`
   - Windows: win10toast notifications (tested ✅)
   - macOS: osascript notifications (untested ⚠️)
   - Linux: notify-send notifications (untested ⚠️)

2. Updated `requirements.txt`:
   - Added conditional dependency: `win10toast>=0.9; sys_platform == 'win32'`
   - Added comments for macOS/Linux system requirements

3. Created `start-printer.sh`:
   - Bash script for macOS/Linux
   - Checks Python 3 installation
   - Auto-installs dependencies
   - Sets environment variables with `export`

**Files Modified:**
- `escpos-netprinter.py` (lines 1-41: platform detection, lines 1476-1513: cross-platform notifications)
- `requirements.txt` (platform-conditional dependencies)
- `README.md` (platform support table, macOS/Linux instructions)
- `start-printer.sh` - NEW FILE

### Phase 5: Language Internationalization
**Goal:** Change all notifications from Turkish to English

**Implementation:**
1. Changed all notification text in `escpos-netprinter.py`:
   - "Fis yazdirildi!" → "Receipt printed!"
   - "Sure:" → "Duration:"
   - "saniye" → "seconds"
   - "Yazici - Basarili" → "Printer - Success"

2. Updated all documentation:
   - `README.md`: Changed examples to English
   - `CHANGELOG.md`: Updated feature descriptions

**Files Modified:**
- `escpos-netprinter.py` (lines 1474, 1481, 1488-1489, 1497, 1503-1504, 1507, 1510)
- `README.md` (line 30, lines 350, 363, 376-377)
- `CHANGELOG.md` (line 22, title, links)

---

## Key Technical Changes

### escpos-netprinter.py

#### Platform Detection (Lines 17-40)
```python
SYSTEM_PLATFORM = platform.system()
NOTIFICATIONS_ENABLED = False
toaster = None

if SYSTEM_PLATFORM == 'Windows':
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        NOTIFICATIONS_ENABLED = True
        print(f"Platform: Windows - Toast notifications enabled (tested)")
    except ImportError:
        print("win10toast not installed - notifications disabled")
elif SYSTEM_PLATFORM == 'Darwin':  # macOS
    NOTIFICATIONS_ENABLED = True
    print(f"Platform: macOS - Desktop notifications enabled (untested)")
elif SYSTEM_PLATFORM == 'Linux':
    NOTIFICATIONS_ENABLED = True
    print(f"Platform: Linux - Desktop notifications enabled (untested)")
```

#### Start Time Tracking (Line 63)
```python
def handle(self):
    self.start_time = time.time()  # Track start time
```

#### Notification Function (Lines 1472-1513)
```python
# Calculate print duration and show notification
elapsed_time = time.time() - self.start_time
elapsed_str = f"{elapsed_time:.2f} seconds"

# Platform-specific notification (run in thread - non-blocking)
def show_notification():
    global SYSTEM_PLATFORM, NOTIFICATIONS_ENABLED, toaster

    if not NOTIFICATIONS_ENABLED:
        print(f"Receipt printed! Duration: {elapsed_str}", flush=True)
        return

    try:
        if SYSTEM_PLATFORM == 'Windows':
            # Windows toast notification (tested)
            toaster.show_toast(
                "Printer - Success",
                f"Receipt printed!\nDuration: {elapsed_str}",
                duration=5,
                threaded=False
            )
        elif SYSTEM_PLATFORM == 'Darwin':
            # macOS notification via osascript (untested)
            subprocess.run([
                'osascript', '-e',
                f'display notification "Receipt printed! Duration: {elapsed_str}" with title "Printer - Success"'
            ], check=False)
        elif SYSTEM_PLATFORM == 'Linux':
            # Linux notification via notify-send (untested)
            subprocess.run([
                'notify-send',
                'Printer - Success',
                f'Receipt printed!\nDuration: {elapsed_str}'
            ], check=False)

        print(f"Receipt printed! Duration: {elapsed_str}", flush=True)
    except Exception as e:
        print(f"Notification error: {e}", flush=True)
        print(f"Receipt printed! Duration: {elapsed_str}", flush=True)

notification_thread = threading.Thread(target=show_notification)
notification_thread.start()
```

#### Fixed Filename Format (Line 1437)
```python
# OLD (caused error 22 on Windows):
html_filename = 'receipt{}.html'.format(heureRecept.strftime('%Y%b%d_%X.%f%Z'))

# NEW (fixed):
html_filename = 'receipt{}.html'.format(heureRecept.strftime('%Y%b%d_%H%M%S.%f%Z'))
```

---

## Architecture

### System Flow
```
SmartStock Web (Remote Server)
    ↓ JavaScript fetch()
Browser (User's PC)
    ↓ HTTP Request (localhost:37842)
SmartStock Connector (Electron App)
    ↓ TCP Socket (localhost:9100)
ESC/POS Network Printer (Python Flask)
    ↓
HTML Receipt + Desktop Notification
```

### Port Configuration
- **9100** - JetDirect protocol (ESC/POS printer input)
- **515** - LPD protocol (legacy support)
- **8100** - Flask web interface (receipt viewing)
- **37842** - SmartStock Connector API

---

## Platform Support Status

| Platform | Status | Notification Method | Tested |
|----------|--------|-------------------|--------|
| **Windows 10/11** | ✅ Full Support | win10toast | ✅ Yes |
| **macOS** | ⚠️ Should Work | osascript | ❌ No |
| **Linux** | ⚠️ Should Work | notify-send | ❌ No |

---

## Testing Results

### Test 1: Windows Toast Notifications
- ✅ Notifications appear on Windows 10/11
- ✅ Duration tracking accurate (< 0.5 seconds average)
- ✅ Non-blocking (doesn't freeze print queue)
- ✅ English language messages working

### Test 2: SmartStock Integration
- ✅ TCP socket communication working
- ✅ Receipt HTML generation successful
- ✅ Web interface accessible at localhost:8100
- ✅ Notifications trigger correctly

### Test 3: File Creation
- ✅ Fixed error 22 (illegal characters in filename)
- ✅ Receipts saving correctly
- ✅ HTML format renders properly in browser

---

## Known Issues

### Resolved
1. ✅ **Error 22 (File Creation)** - Fixed by changing `%X` to `%H%M%S`
2. ✅ **Blocking Notifications** - Fixed by using threading
3. ✅ **Electron Build Errors** - Fixed by moving electron to devDependencies and disabling code signing

### Pending
1. ⚠️ **macOS Notifications** - Untested (need community testing)
2. ⚠️ **Linux Notifications** - Untested (need community testing)

---

## Future Enhancements

### Planned
- GUI configuration tool
- Multi-language support (beyond English)
- Automated testing suite
- Windows Service installer
- macOS LaunchAgent configuration
- Linux systemd service

### Under Consideration
- PDF export of receipts
- Email receipt functionality
- SQLite database storage
- Cloud backup integration
- Custom notification sounds

---

## Installation Summary

### Windows
```batch
cd C:\path\to\escpos-netprinter-plus
pip install -r requirements.txt
start-printer.bat
```

### macOS/Linux
```bash
cd /path/to/escpos-netprinter-plus
pip3 install -r requirements.txt
chmod +x start-printer.sh
./start-printer.sh
```

---

## Dependencies

### Python
- Flask >= 2.3.0 (web server)
- lxml >= 4.9.0 (HTML/XML processing)
- win10toast >= 0.9 (Windows only)

### PHP
- PHP 8.2+ with Composer
- mike42/escpos-php (ESC/POS processing)
- chillerlan/php-qrcode (QR code generation)

### System
- Windows: Nothing extra needed
- macOS: osascript (built-in)
- Linux: libnotify-bin (`sudo apt-get install libnotify-bin`)

---

## Credits

- **gilbertfl** - Original escpos-netprinter project
- **Mike Connelly (mike42)** - escpos-php library
- **SmartStock Team** - Integration testing
- **ESC/POS Community** - Documentation and support

---

## License

MIT License - See LICENSE file for details

Copyright (c) 2025 Kerim Şentürk
Copyright (c) 2024 gilbertfl (original project)

---

**Last Updated:** 2025-01-02
**Version:** 1.0.0
