# Changelog

All notable changes to escpos-netprinter-plus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-02

### Added (Plus Version by Kerim Şentürk)
- ✨ **Cross-Platform Desktop Notifications** - Platform-specific notifications when printing completes
  - Windows: Toast notifications (tested)
  - macOS: osascript notifications (untested)
  - Linux: notify-send notifications (untested)
  - Shows print duration in seconds
  - Non-blocking thread-based implementation
  - Customizable notification text
- ⏱️ **Print Duration Tracking** - Measure and display exact time for each print job
- 🔧 **Cross-Platform Filename Compatibility Fix** - Changed datetime format to avoid illegal characters
  - Changed from `%X` (includes colons) to `%H%M%S`
  - Fixes "File creation error: 22" on Windows
- 🌍 **English Language Support** - Notification messages in English
- 🖥️ **Platform Detection** - Automatically detects Windows, macOS, or Linux
  - Platform-specific notification methods
  - Conditional dependency installation
- 🔌 **SmartStock Integration** - Full integration with SmartStock inventory system
  - TCP socket communication
  - Automatic print triggering
  - Web-based print queue
- 📖 **Comprehensive Documentation**
  - Detailed README.md with installation and testing
  - networkprinter.md with troubleshooting guide
  - CONTRIBUTING.md for contributors
  - start-printer.bat for Windows
  - start-printer.sh for macOS/Linux

### Changed
- Updated `requirements.txt` with platform-conditional dependencies
- Modified `escpos-netprinter.py` for cross-platform compatibility
- Added threading for non-blocking notifications
- Changed all notification messages from Turkish to English

### Fixed
- Windows filename encoding issue (colons in timestamps)
- Notification blocking main thread issue

### Documentation
- Added installation guide for Windows
- Added 5 comprehensive test cases
- Added SmartStock integration architecture diagram
- Added troubleshooting section with common issues

---

## [3.1.1] - 2024 (Original by gilbertfl)

### Added (Original Project)
- ESC/POS protocol handling
- JetDirect server (port 9100)
- LPD server (port 515)
- HTML conversion of receipts
- Web interface for viewing receipts
- CUPS printer driver integration
- Status request handling per Epson APG

### Docker Support
- Container-based deployment
- Volume mounting for persistent receipts
- Configurable ports via environment variables

---

## Unreleased / Planned Features

### Upcoming
- [ ] GUI configuration tool
- [ ] Multi-language support (beyond English)
- [ ] Automated testing suite
- [ ] Windows Service installer
- [ ] macOS/Linux notification testing and verification

### Considering
- [ ] PDF export of receipts
- [ ] Email receipt functionality
- [ ] SQLite database storage
- [ ] Cloud backup integration
- [ ] Custom notification sounds

---

## Links

- [Original Project](https://github.com/gilbertfl/escpos-netprinter) by gilbertfl
- [Plus Version](https://github.com/kerim92/escpos-netprinter-plus) by Kerim Şentürk
- [mike42/escpos-php](https://github.com/mike42/escpos-php) - Core ESC/POS library

---

**Note**: Version 1.0.0 is the first cross-platform release with desktop notifications. Original project versions (3.1.1 and earlier) refer to the Docker-based implementation.
