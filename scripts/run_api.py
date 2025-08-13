#!/usr/bin/env python3
"""
FastAPI Application Launcher
"""

import sys
import os
import uvicorn

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

if __name__ == "__main__":
    print("🚀 Starting Job Vacancy Insight API...")
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )