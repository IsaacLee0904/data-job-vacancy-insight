#!/usr/bin/env python3
"""
FastAPI Application Launcher
"""

import sys
import os
import uvicorn

# Add project root to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # Go up one level from scripts/
sys.path.insert(0, project_root)  # Insert at beginning of path

if __name__ == "__main__":
    print("🚀 Starting Job Vacancy Insight API...")
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )