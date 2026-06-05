#!/usr/bin/env python3
"""
Run ShrinX Web App
"""
import os
import webbrowser
import threading
import time


def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    print("🧠 ShrinX — Starting web app...")
    print("📡 Open your browser at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop\n")

    # Open browser automatically
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()

    from app import app

    app.run(debug=False, port=5000)