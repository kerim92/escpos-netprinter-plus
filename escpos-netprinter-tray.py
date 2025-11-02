#!/usr/bin/env python3
"""
ESC/POS Network Printer - System Tray Version
Author: Kerim Şentürk
"""

import sys
import os
import subprocess
import threading
import webbrowser
import platform
from pathlib import Path

# Check if pystray is available
try:
    from pystray import Icon, Menu, MenuItem
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError as e:
    TRAY_AVAILABLE = False
    print(f"WARNING: System tray not available: {e}")
    print("Install with: pip install pystray Pillow")
    print("\nStarting in console mode instead...")
    # Don't exit, fallback to console mode

# Get environment variables
FLASK_HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
FLASK_PORT = os.getenv('FLASK_RUN_PORT', '8100')
PRINTER_PORT = os.getenv('PRINTER_PORT', '9100')

# Server process
server_process = None
icon = None

def create_icon_image():
    """Create a simple printer icon"""
    # Create a 64x64 image
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), 'white')
    dc = ImageDraw.Draw(image)

    # Draw a simple printer shape
    # Printer body (rectangle)
    dc.rectangle([10, 25, 54, 50], fill='#2196F3', outline='#1976D2', width=2)

    # Paper coming out (top)
    dc.rectangle([20, 10, 44, 28], fill='white', outline='#757575', width=2)

    # Paper tray (bottom)
    dc.rectangle([15, 48, 49, 54], fill='#E3F2FD', outline='#1976D2', width=1)

    # Small indicator light
    dc.ellipse([40, 32, 46, 38], fill='#4CAF50')

    return image

def start_server():
    """Start the ESC/POS server in a subprocess"""
    global server_process

    if server_process and server_process.poll() is None:
        print("Server is already running")
        return

    # Get the script directory
    script_dir = Path(__file__).parent
    server_script = script_dir / 'escpos-netprinter.py'

    # Set environment variables
    env = os.environ.copy()
    env['FLASK_RUN_HOST'] = FLASK_HOST
    env['FLASK_RUN_PORT'] = FLASK_PORT
    env['PRINTER_PORT'] = PRINTER_PORT
    env['ESCPOS_DEBUG'] = 'False'

    print(f"Starting ESC/POS Network Printer...")
    print(f"  Web Interface: http://localhost:{FLASK_PORT}")
    print(f"  Printer Port: {PRINTER_PORT}")

    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as EXE - use thread instead of subprocess
        print("Running in EXE mode - starting server in thread")
        import threading

        def run_server_thread():
            # Set environment variables for this process
            os.environ['FLASK_RUN_HOST'] = FLASK_HOST
            os.environ['FLASK_RUN_PORT'] = FLASK_PORT
            os.environ['PRINTER_PORT'] = PRINTER_PORT
            os.environ['ESCPOS_DEBUG'] = 'False'

            # Import and run the server module directly
            import importlib.util
            spec = importlib.util.spec_from_file_location("escpos_server", server_script)
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)

        server_thread = threading.Thread(target=run_server_thread, daemon=True)
        server_thread.start()
        print("Server started in thread mode!")
        print("System tray icon is running. Right-click for options.")
        return

    # Check if server script exists
    if not server_script.exists():
        print(f"ERROR: Server script not found: {server_script}")
        print(f"Looking in: {script_dir}")
        return

    try:
        # Start the server process (normal Python mode)
        if platform.system() == 'Windows':
            # On Windows, keep it simple - just use python.exe
            server_process = subprocess.Popen(
                [sys.executable, str(server_script)],
                env=env,
                cwd=str(script_dir)  # Set working directory
            )
        else:
            server_process = subprocess.Popen(
                [sys.executable, str(server_script)],
                env=env,
                cwd=str(script_dir)
            )

        print("Server started successfully!")
        print(f"Server PID: {server_process.pid}")
        print("System tray icon is running. Right-click for options.")

    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        server_process = None

def stop_server():
    """Stop the ESC/POS server"""
    global server_process

    if server_process and server_process.poll() is None:
        print("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force killing server...")
            server_process.kill()
        server_process = None
        print("Server stopped")
    else:
        print("Server is not running")

def open_web_interface(icon_obj, item):
    """Open the web interface in browser"""
    url = f"http://localhost:{FLASK_PORT}"
    print(f"Opening web interface: {url}")
    webbrowser.open(url)

def open_receipts(icon_obj, item):
    """Open the receipts page in browser"""
    url = f"http://localhost:{FLASK_PORT}/receipts"
    print(f"Opening receipts: {url}")
    webbrowser.open(url)

def on_quit(icon_obj, item):
    """Quit the application"""
    print("Exiting...")
    stop_server()
    icon_obj.stop()

def setup_tray():
    """Setup the system tray icon"""
    global icon

    # Create menu
    menu = Menu(
        MenuItem('ESC/POS Network Printer Plus', None, enabled=False),
        Menu.SEPARATOR,
        MenuItem('Open Web Interface', open_web_interface, default=True),
        MenuItem('View Receipts', open_receipts),
        Menu.SEPARATOR,
        MenuItem('Exit', on_quit)
    )

    # Create icon
    icon_image = create_icon_image()
    icon = Icon(
        'escpos-netprinter-plus',
        icon_image,
        f'ESC/POS Network Printer Plus\nPrinter Port: {PRINTER_PORT} | Web: {FLASK_PORT}\nRight-click for options',
        menu
    )

    # Start server before showing icon
    start_server()

    # Run the icon (this blocks)
    icon.run()

def main():
    """Main entry point"""
    print("=" * 60)
    print("ESC/POS Network Printer - System Tray Version")
    print("Author: Kerim Şentürk")
    print("=" * 60)
    print()

    if not TRAY_AVAILABLE:
        print("WARNING: System tray not available - starting in console mode")
        print()
        # Start server in console mode
        start_server()
        print()
        print("Server is running. Press Ctrl+C to stop.")
        try:
            # Keep running until interrupted
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            stop_server()
        return 0

    try:
        setup_tray()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        stop_server()
    except Exception as e:
        print(f"ERROR: {e}")
        stop_server()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
