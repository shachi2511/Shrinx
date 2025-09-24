#!/usr/bin/env python3
"""
Simple launcher for Shrinx GUI
Run this file to start the GUI application
"""

import sys
import os

def main():
    print("🧠 Starting Shrinx GUI...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required.")
        return
    
    # Check tkinter availability
    try:
        import tkinter as tk
        print("✅ tkinter found")
    except ImportError:
        print("❌ Error: tkinter not found. Please install tkinter:")
        print("   Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   CentOS/RHEL: sudo yum install tkinter")
        print("   macOS/Windows: tkinter should be include