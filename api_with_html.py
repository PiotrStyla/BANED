#!/usr/bin/env python3
"""
Quick fix: API server that also serves the HTML file
This avoids CORS issues
"""
import subprocess
import sys

# Start the regular API
print("Starting BANED Double Power API...")
print("="*60)
print()
print("📡 API: http://localhost:8000/")
print("🌐 Web Interface: http://localhost:8000/web")
print("📚 API Docs: http://localhost:8000/docs")
print()
print("="*60)
print()

# Import and modify the API
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

# Import the existing API
import api_double_power

# Add HTML serving route
@api_double_power.app.get("/web")
async def serve_html():
    html_path = os.path.join(os.path.dirname(__file__), "static", "double_power.html")
    return FileResponse(html_path)

# Run it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_double_power.app, host="0.0.0.0", port=8000)
