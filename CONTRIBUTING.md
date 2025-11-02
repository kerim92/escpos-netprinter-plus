# Contributing to ESC/POS Network Printer for Windows

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help each other learn and grow

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title**: Describe the problem briefly
- **Steps to reproduce**: List exact steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - Windows version
  - Python version
  - PHP version
  - Relevant dependency versions
- **Logs**: Include error messages or console output

**Example**:
```markdown
**Title**: Windows notification not appearing on Windows 11

**Steps to reproduce**:
1. Start escpos-netprinter.py
2. Send test print via SmartStock
3. Check for notification

**Expected**: Toast notification appears
**Actual**: No notification
**Environment**: Windows 11 23H2, Python 3.11.5
**Logs**: [paste relevant console output]
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:

- **Use case**: Why is this useful?
- **Proposed solution**: How should it work?
- **Alternatives**: What other approaches did you consider?
- **Examples**: Show mockups or code examples if possible

### Pull Requests

1. **Fork & Clone**
```bash
git clone https://github.com/YOUR_USERNAME/escpos-netprinter-windows.git
cd escpos-netprinter-windows
```

2. **Create a Branch**
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/annoying-bug
```

3. **Make Changes**
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed

4. **Test Your Changes**
```bash
# Test basic functionality
python escpos-netprinter.py

# Test with SmartStock integration
# Send test prints and verify notifications
```

5. **Commit**
```bash
git add .
git commit -m "Add amazing feature"
```

**Commit Message Guidelines**:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed

**Examples**:
```
Good:
- "Add support for custom notification sounds"
- "Fix filename encoding issue on Windows"
- "Update README with troubleshooting section"

Bad:
- "fixed stuff"
- "changes"
- "asdfasdf"
```

6. **Push & Create PR**
```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Screenshots/GIFs if UI changed
- Mention any related issues

## Development Setup

### Prerequisites
```bash
# Python dependencies
pip install -r requirements.txt

# PHP dependencies
composer install
```

### Project Structure
```
escpos-netprinter/
├── escpos-netprinter.py    # Main Python server
├── src/                     # PHP ESC/POS processing
│   └── Escpos2Html.php
├── web/                     # Web interface
│   ├── receipts/            # Generated HTML receipts
│   └── tmp/                 # Temporary files
├── vendor/                  # PHP dependencies (composer)
├── requirements.txt         # Python dependencies
├── composer.json           # PHP dependencies
├── README.md               # Documentation
└── LICENSE                 # MIT License
```

### Running Tests

**Basic Connectivity Test**:
```bash
netstat -an | findstr :9100
netstat -an | findstr :5000
```

**Print Test**:
```bash
telnet localhost 9100
# Type some text, then Ctrl+], type 'quit'
# Check http://localhost:5000/recus
```

**Notification Test**:
```python
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Test", "Testing notifications", duration=5)
```

## Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:
- Indentation: 4 spaces
- Line length: 100 characters max
- Docstrings: Use for all functions/classes
- Comments: Explain "why", not "what"

**Example**:
```python
def show_notification(elapsed_time):
    """
    Display Windows toast notification with print duration.

    Args:
        elapsed_time (float): Time taken for print job in seconds
    """
    elapsed_str = f"{elapsed_time:.2f} saniye"

    # Use threading to avoid blocking the main process
    def _show():
        toaster.show_toast(
            "Yazici - Basarili",
            f"Fis yazdirildi!\nSure: {elapsed_str}",
            duration=5,
            threaded=False
        )

    notification_thread = threading.Thread(target=_show)
    notification_thread.start()
```

### PHP Code Style

Follow PSR-12 with these specifics:
- Indentation: 4 spaces
- Line length: 120 characters max
- Use type hints
- Document with PHPDoc

### Documentation

- Update README.md for user-facing changes
- Update networkprinter.md for detailed guides
- Add inline comments for complex logic
- Use clear, simple English

## Priority Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] **macOS/Linux support** - Adapt for non-Windows systems
- [ ] **GUI configuration tool** - Electron or Qt-based settings app
- [ ] **Automated tests** - Unit tests for core functionality
- [ ] **Multi-language support** - i18n for notifications and web interface

### Medium Priority
- [ ] **PDF export** - Convert HTML receipts to PDF
- [ ] **Email receipts** - Send receipts via email
- [ ] **Database storage** - SQLite for receipt history
- [ ] **Performance optimization** - Faster ESC/POS processing

### Low Priority (Nice to Have)
- [ ] **Custom notification sounds** - User-selectable sounds
- [ ] **Windows Service** - Run as background service
- [ ] **Cloud sync** - Backup receipts to cloud
- [ ] **Mobile app** - View receipts on phone

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Contact the maintainer: Kerim Şentürk

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commit history

Thank you for contributing! 🙏
