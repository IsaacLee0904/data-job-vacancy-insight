#!/usr/bin/env python3
"""
Dashboard API Router
Job vacancy dashboard data endpoints
"""

import sys
import os
from datetime import datetime, date
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

# Add project root to Python path  
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from src.core.dashboard_utils import FetchReportData
from ..services.cache_service import DashboardCacheService

router = APIRouter()
logger = set_logger()

# Dependency for cache service
def get_cache_service():
    """Get cache service instance"""
    return DashboardCacheService(logger)

# Response Models
class ApiResponse(BaseModel):
    """Base API response model"""
    success: bool
    data: Optional[Dict[Any, Any]] = None
    message: Optional[str] = None
    timestamp: datetime

class JobMetricsResponse(BaseModel):
    """Job metrics response model"""
    total_openings: int
    total_openings_change_pct: float
    new_openings_count: int
    new_openings_change_pct: float
    fill_rate: float
    fill_rate_change_pct: float
    average_weeks_to_fill: float
    average_weeks_to_fill_change_pct: float
    crawl_date: str

@router.get("/info")
async def dashboard_info():
    """
    Get dashboard API information
    """
    return ApiResponse(
        success=True,
        data={
            "name": "Job Vacancy Dashboard API",
            "version": "1.0.0",
            "endpoints": [
                "/api/v1/dashboard/latest-date",
                "/api/v1/dashboard/job-metrics",
                "/api/v1/dashboard/data-role-distribution",
                "/api/v1/dashboard/top-tools",
                "/api/v1/dashboard/top-companies"
            ]
        },
        message="Dashboard API is running",
        timestamp=datetime.now()
    )

@router.get("/latest-date")
async def get_latest_crawl_date(cache_service: DashboardCacheService = Depends(get_cache_service)):
    """
    Get the latest data crawl date (cached)
    """
    try:
        latest_date = cache_service.get_or_fetch_latest_date()
        
        if not latest_date:
            raise HTTPException(status_code=404, detail="No data found")
            
        return ApiResponse(
            success=True,
            data={"latest_crawl_date": latest_date},
            message="Latest crawl date retrieved successfully",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting latest crawl date: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job-metrics")
async def get_job_metrics(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get job opening metrics for a specific date (cached)
    """
    try:
        metrics = cache_service.get_or_fetch_job_metrics(crawl_date)
        
        if not metrics:
            raise HTTPException(status_code=404, detail=f"No metrics found for date {crawl_date or 'latest'}")
        
        return ApiResponse(
            success=True,
            data=metrics,
            message=f"Job metrics retrieved for {metrics.get('crawl_date', crawl_date or 'latest')}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting job metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data-role-distribution")
async def get_data_role_distribution(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get data role distribution for pie chart (cached)
    """
    try:
        roles_data = cache_service.get_or_fetch_data_role_distribution(crawl_date)
        
        if not roles_data:
            raise HTTPException(status_code=404, detail=f"No role data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "roles": roles_data,
                "crawl_date": crawl_date,
                "total_count": sum(role['count'] for role in roles_data) if roles_data else 0
            },
            message=f"Data role distribution retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting data role distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-tools")
async def get_top_tools(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    limit: int = Query(3, description="Number of top tools to return", ge=1, le=10),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get top data tools (cached)
    """
    try:
        top_tools = cache_service.get_or_fetch_top_tools(crawl_date, limit)
        
        if not top_tools:
            raise HTTPException(status_code=404, detail=f"No tools data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "tools": top_tools,
                "crawl_date": crawl_date,
                "count": len(top_tools)
            },
            message=f"Top {limit} tools retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting top tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-companies") 
async def get_top_companies(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    limit: int = Query(5, description="Number of top companies to return", ge=1, le=10),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get top companies by job openings (cached)
    """
    try:
        top_companies = cache_service.get_or_fetch_top_companies(crawl_date, limit)
        
        if not top_companies:
            raise HTTPException(status_code=404, detail=f"No companies data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "companies": top_companies,
                "crawl_date": crawl_date,
                "count": len(top_companies)
            },
            message=f"Top {limit} companies retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting top companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_dashboard_summary(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get comprehensive dashboard summary with all key metrics (cached)
    """
    try:
        summary = cache_service.get_or_fetch_dashboard_summary(crawl_date)
        
        if not summary:
            raise HTTPException(status_code=404, detail=f"No dashboard data found for date {crawl_date or 'latest'}")
        
        return ApiResponse(
            success=True,
            data=summary,
            message=f"Dashboard summary retrieved for {summary.get('crawl_date', 'latest')}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/education-by-data-role")
async def get_education_by_data_role(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get education data by data role (cached)
    """
    try:
        education_data = cache_service.get_or_fetch_education_by_data_role(crawl_date)
        
        if education_data is None:
            raise HTTPException(status_code=404, detail=f"No education data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "education_data": education_data,
                "crawl_date": crawl_date,
                "count": len(education_data)
            },
            message=f"Education by data role retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting education by data role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geography/taiwan-openings")
async def get_taiwan_openings(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get Taiwan geographic openings data (cached)
    """
    try:
        taiwan_data = cache_service.get_or_fetch_taiwan_openings(crawl_date)
        
        if taiwan_data is None:
            raise HTTPException(status_code=404, detail=f"No Taiwan openings data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "taiwan_openings": taiwan_data,
                "crawl_date": crawl_date,
                "count": len(taiwan_data)
            },
            message=f"Taiwan openings data retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting Taiwan openings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geography/major-cities")
async def get_major_city_openings(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest"),
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get major city openings data (cached)
    """
    try:
        cities_data = cache_service.get_or_fetch_major_city_openings(crawl_date)
        
        if cities_data is None:
            raise HTTPException(status_code=404, detail=f"No major city openings data found for date {crawl_date or 'latest'}")
        
        # Get actual crawl_date if not provided
        if not crawl_date:
            crawl_date = cache_service.get_or_fetch_latest_date()
        
        return ApiResponse(
            success=True,
            data={
                "major_cities": cities_data,
                "crawl_date": crawl_date,
                "count": len(cities_data)
            },
            message=f"Major city openings retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting major city openings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geography/taipei-historical")
async def get_taipei_historical_openings(
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get Taipei historical openings trend (cached)
    """
    try:
        taipei_data = cache_service.get_or_fetch_taipei_historical_openings()
        
        if taipei_data is None:
            raise HTTPException(status_code=404, detail="No Taipei historical data found")
        
        return ApiResponse(
            success=True,
            data={
                "taipei_historical": taipei_data,
                "count": len(taipei_data)
            },
            message="Taipei historical openings retrieved",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting Taipei historical openings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools-by-data-role")
async def get_tools_by_data_role(
    cache_service: DashboardCacheService = Depends(get_cache_service)
):
    """
    Get tools by data role for stack analysis (cached)
    """
    try:
        tools_data = cache_service.get_or_fetch_tool_by_data_role()
        
        if tools_data is None:
            raise HTTPException(status_code=404, detail="No tools by data role data found")
        
        return ApiResponse(
            success=True,
            data={
                "tools_by_data_role": tools_data,
                "count": len(tools_data)
            },
            message="Tools by data role retrieved for stack analysis",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting tools by data role: {e}")
        raise HTTPException(status_code=500, detail=str(e))