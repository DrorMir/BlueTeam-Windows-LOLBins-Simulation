#!/usr/bin/env python3
"""
Launcher script for the Attack Simulator Command GUI.

This script provides a simple way to launch the GUI application with proper
error handling and environment setup.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyQt6
        print("PyQt6 is installed")
        return True
    except ImportError:
        print("PyQt6 is not installed. Please install it with: pip install PyQt6")
        return False

def setup_display():
    """Setup display environment for GUI applications."""
    if 'DISPLAY' not in os.environ:
        print("     No DISPLAY environment variable found.")
        print("   If you're running on a headless system, you may need to:")
        print("   1. Install and start an X server (e.g., Xvfb)")
        print("   2. Set the DISPLAY environment variable")
        print("   3. Or use X11 forwarding if connecting via SSH")
        return False
    return True

def launch_gui():
    """Launch the GUI application."""
    script_dir = Path(__file__).parent
    gui_script = script_dir / "command_add_gui.py"
    
    if not gui_script.exists():
        print(f"GUI script not found: {gui_script}")
        return False
    
    try:
        print("Launching Attack Simulator Command GUI...")
        subprocess.run([sys.executable, str(gui_script)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to launch GUI: {e}")
        return False
    except KeyboardInterrupt:
        print("\n GUI application interrupted by user")
        return True

def main():
    """Main launcher function."""
    print("Attack Simulator Command GUI Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check display setup (warning only, not fatal)
    setup_display()
    
    # Launch the GUI
    if launch_gui():
        print("GUI application completed successfully")
    else:
        print("GUI application failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main()