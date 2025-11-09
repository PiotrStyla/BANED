#!/usr/bin/env python3
"""
Start both API and serve HTML properly to avoid CORS issues
"""
import subprocess
import time
import webbrowser
import os

print("="*60)
print("  🛡️ BANED Double Power - Starting Web Interface")
print("="*60)
print()

# Start API server in background
print("[1/3] Starting API server...")
api_process = subprocess.Popen(
    ["python", "api_double_power.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for API to start
print("[2/3] Waiting for API to start...")
time.sleep(3)

# Open browser to the HTML file served through localhost
print("[3/3] Opening web interface...")
print()
print("="*60)
print("  ✅ BANED Double Power is now running!")
print("="*60)
print()
print("🌐 Web Interface: http://localhost:8000/web")
print("📡 API Documentation: http://localhost:8000/docs")
print("💡 API Status: http://localhost:8000/")
print()
print("Press Ctrl+C to stop the server")
print()

# Open browser
time.sleep(1)
html_path = os.path.join(os.getcwd(), "static", "double_power.html")
webbrowser.open(f"file:///{html_path}")

try:
    # Keep running
    api_process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Stopping server...")
    api_process.terminate()
    print("✅ Server stopped")
