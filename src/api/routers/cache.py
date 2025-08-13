#!/usr/bin/env python3
"""
Cache Management API Router
Administrative endpoints for cache control
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from ..core.cache import get_cache_manager
from ..services.cache_service import DashboardCacheService

router = APIRouter()
logger = set_logger()

# Response Models
class CacheOperationResponse(BaseModel):
    """Cache operation response model"""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime

class CacheStatsResponse(BaseModel):
    """Cache statistics response model"""
    cache_info: Dict[str, Any]
    hit_rate_percentage: float
    total_requests: int
    service_status: str
    timestamp: datetime

class CacheHealthResponse(BaseModel):
    """Cache health check response model"""
    status: str
    redis_info: Optional[Dict[str, Any]] = None
    operations_test: Optional[Dict[str, Any]] = None
    timestamp: datetime

# Dependency for cache service
def get_cache_service():
    """Get cache service instance"""
    return DashboardCacheService(logger)

@router.get("/info", response_model=CacheStatsResponse)
async def get_cache_info(cache_service: DashboardCacheService = Depends(get_cache_service)):
    """
    Get cache statistics and information
    """
    try:
        stats = cache_service.get_cache_statistics()
        
        return CacheStatsResponse(
            cache_info=stats.get('cache_info', {}),
            hit_rate_percentage=stats.get('hit_rate_percentage', 0.0),
            total_requests=stats.get('total_requests', 0),
            service_status=stats.get('service_status', 'unknown'),
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error getting cache info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache info: {str(e)}")

@router.get("/health", response_model=CacheHealthResponse)
async def cache_health_check():
    """
    Perform comprehensive cache health check
    """
    try:
        cache_manager = get_cache_manager(logger)
        health_result = cache_manager.health_check()
        cache_info = cache_manager.get_cache_info()
        
        return CacheHealthResponse(
            status=health_result.get('status', 'unknown'),
            redis_info=cache_info,
            operations_test=health_result,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Cache health check failed: {str(e)}")

@router.post("/warm", response_model=CacheOperationResponse)
async def warm_cache(
    crawl_date: Optional[str] = Query(None, description="Date to warm cache for (YYYY-MM-DD), defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Pre-warm cache with commonly accessed data
    """
    try:
        logger.info(f"Cache warming requested for date: {crawl_date or 'latest'}")
        results = cache_service.warm_cache(crawl_date)
        
        if 'error' in results:
            raise HTTPException(status_code=404, detail=results['error'])
        
        success_count = sum(results.values())
        total_count = len(results)
        
        return CacheOperationResponse(
            success=success_count > 0,
            message=f"Cache warming completed: {success_count}/{total_count} operations successful",
            details={
                'results': results,
                'crawl_date': crawl_date,
                'success_rate': f"{success_count}/{total_count}"
            },
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error warming cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to warm cache: {str(e)}")

@router.delete("/clear/all", response_model=CacheOperationResponse)
async def clear_all_dashboard_cache():
    """
    Clear all dashboard-related cache entries
    """
    try:
        cache_manager = get_cache_manager(logger)
        deleted_count = cache_manager.invalidate_all_dashboard_cache()
        
        logger.info(f"Cleared all dashboard cache: {deleted_count} entries")
        
        return CacheOperationResponse(
            success=True,
            message=f"Successfully cleared all dashboard cache",
            details={
                'deleted_entries': deleted_count,
                'operation': 'clear_all_dashboard'
            },
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error clearing all cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

@router.delete("/clear/date/{crawl_date}", response_model=CacheOperationResponse)
async def clear_cache_by_date(
    crawl_date: str,
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Clear cache entries for a specific date
    """
    try:
        deleted_count = cache_service.invalidate_date_cache(crawl_date)
        
        logger.info(f"Cleared cache for date {crawl_date}: {deleted_count} entries")
        
        return CacheOperationResponse(
            success=True,
            message=f"Successfully cleared cache for date {crawl_date}",
            details={
                'deleted_entries': deleted_count,
                'crawl_date': crawl_date,
                'operation': 'clear_by_date'
            },
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error clearing cache for date {crawl_date}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache for date: {str(e)}")

@router.delete("/clear/pattern/{pattern}", response_model=CacheOperationResponse)
async def clear_cache_by_pattern(pattern: str):
    """
    Clear cache entries matching a specific pattern
    """
    try:
        cache_manager = get_cache_manager(logger)
        deleted_count = cache_manager.invalidate_pattern(pattern)
        
        logger.info(f"Cleared cache matching pattern '{pattern}': {deleted_count} entries")
        
        return CacheOperationResponse(
            success=True,
            message=f"Successfully cleared cache matching pattern '{pattern}'",
            details={
                'deleted_entries': deleted_count,
                'pattern': pattern,
                'operation': 'clear_by_pattern'
            },
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error clearing cache by pattern '{pattern}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache by pattern: {str(e)}")

@router.get("/keys/count")
async def get_cache_keys_count():
    """
    Get count of cache keys by category
    """
    try:
        cache_manager = get_cache_manager(logger)
        
        # Get different categories of keys
        all_keys = cache_manager.redis_client.keys("job_vacancy:*")
        
        categories = {
            'job_metrics': 0,
            'data_role_distribution': 0,
            'top_tools': 0,
            'top_companies': 0,
            'latest_date': 0,
            'dashboard_summary': 0,
            'api_response': 0,
            'other': 0
        }
        
        for key in all_keys:
            key_str = key.decode('utf-8') if isinstance(key, bytes) else str(key)
            categorized = False
            
            for category in categories.keys():
                if category in key_str:
                    categories[category] += 1
                    categorized = True
                    break
            
            if not categorized:
                categories['other'] += 1
        
        total_keys = len(all_keys)
        
        return {
            'success': True,
            'total_keys': total_keys,
            'categories': categories,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting cache keys count: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache keys count: {str(e)}")

@router.post("/test", response_model=CacheOperationResponse)
async def test_cache_operations():
    """
    Test basic cache operations
    """
    try:
        cache_manager = get_cache_manager(logger)
        
        # Test data
        test_data = {
            'test_time': datetime.now().isoformat(),
            'test_value': 'cache_test_successful',
            'test_number': 12345
        }
        
        # Test set operation
        set_result = cache_manager.set('test_cache', test_data, ttl=60, test_key='cache_test')
        
        # Test get operation
        get_result = cache_manager.get('test_cache', test_key='cache_test')
        
        # Test delete operation
        delete_result = cache_manager.delete('test_cache', test_key='cache_test')
        
        # Verify results
        data_matches = get_result == test_data if get_result else False
        
        test_results = {
            'set_operation': set_result,
            'get_operation': get_result is not None,
            'delete_operation': delete_result,
            'data_integrity': data_matches,
            'all_tests_passed': all([set_result, get_result is not None, delete_result, data_matches])
        }
        
        return CacheOperationResponse(
            success=test_results['all_tests_passed'],
            message="Cache operations test completed",
            details={
                'test_results': test_results,
                'test_data': test_data
            },
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Cache test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Cache test failed: {str(e)}")