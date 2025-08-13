#!/usr/bin/env python3
"""
Health Check Router
System status and connectivity checks
"""

import sys
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
import psycopg2
import redis

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.api.core.config import settings
from src.core.log_utils import set_logger

router = APIRouter()
logger = set_logger()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check including database and Redis connectivity
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {}
    }
    
    # Check Database
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        conn.close()
        health_status["services"]["database"] = {
            "status": "healthy",
            "host": settings.DB_HOST,
            "database": settings.DB_NAME
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            socket_connect_timeout=5,
            decode_responses=True
        )
        
        # Test Redis with ping
        redis_client.ping()
        redis_client.close()
        
        health_status["services"]["redis"] = {
            "status": "healthy",
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT
        }
        
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status["services"]["redis"] = {
            "status": "unhealthy", 
            "error": str(e)
        }
        if health_status["status"] == "healthy":
            health_status["status"] = "degraded"
    
    return health_status

@router.get("/health/database")
async def database_health():
    """
    Database-specific health check
    """
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        
        with conn.cursor() as cursor:
            # Check if key tables exist
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'reporting_data'
            """)
            table_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT MAX(crawl_date) 
                FROM reporting_data.rpt_job_openings_metrics
            """)
            latest_data = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "healthy",
            "reporting_tables": table_count,
            "latest_data_date": str(latest_data) if latest_data else None,
            "connection_info": {
                "host": settings.DB_HOST,
                "database": settings.DB_NAME
            }
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")

@router.get("/health/redis")
async def redis_health():
    """
    Redis-specific health check
    """
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            socket_connect_timeout=5,
            decode_responses=True
        )
        
        # Test operations
        test_key = "health_check_test"
        redis_client.set(test_key, "test_value", ex=10)
        value = redis_client.get(test_key)
        redis_client.delete(test_key)
        
        info = redis_client.info()
        redis_client.close()
        
        return {
            "status": "healthy",
            "test_operation": "success" if value == "test_value" else "failed",
            "redis_info": {
                "version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients")
            }
        }
        
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Redis unhealthy: {str(e)}")