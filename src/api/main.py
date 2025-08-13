#!/usr/bin/env python3
"""
FastAPI Main Application
Job Vacancy Insight Dashboard API Backend
"""

import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from src.api.core.config import settings
from src.api.routers import health, dashboard, cache
from src.api.middleware.cache_middleware import CacheMiddleware, CacheControlMiddleware

# Set up logger
logger = set_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Job Vacancy Insight API...")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
    
    try:
        # Initialize connections, cache, etc.
        logger.info("✅ API startup completed successfully")
        yield
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    finally:
        # Shutdown
        logger.info("🛑 Shutting down Job Vacancy Insight API...")

# Create FastAPI application
app = FastAPI(
    title="Job Vacancy Insight API",
    description="Backend API for Job Vacancy Dashboard with Redis caching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add cache middleware (temporarily disabled for startup)
# app.add_middleware(CacheMiddleware, logger=logger)
# app.add_middleware(CacheControlMiddleware, logger=logger)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500}
    )

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(cache.router, prefix="/api/v1/cache", tags=["Cache Management"])

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Job Vacancy Insight API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🔥 Starting FastAPI development server...")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )