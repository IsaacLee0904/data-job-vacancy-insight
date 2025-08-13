#!/usr/bin/env python3
"""
Dashboard API Router
Job vacancy dashboard data endpoints
"""

import sys
import os
from datetime import datetime, date
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

# Add project root to Python path  
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.core.log_utils import set_logger
from src.core.dashboard_utils import FetchReportData

router = APIRouter()
logger = set_logger()

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
async def get_latest_crawl_date():
    """
    Get the latest data crawl date
    """
    try:
        data_fetcher = FetchReportData(logger)
        latest_date = data_fetcher.get_newest_crawl_date()
        
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
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest")
):
    """
    Get job opening metrics for a specific date
    """
    try:
        data_fetcher = FetchReportData(logger)
        
        # Use latest date if not provided
        if not crawl_date:
            crawl_date = data_fetcher.get_newest_crawl_date()
            if not crawl_date:
                raise HTTPException(status_code=404, detail="No data available")
        
        # Fetch metrics
        metrics_df = data_fetcher.fetch_openings_statistics_metrics(crawl_date)
        
        if metrics_df.empty:
            raise HTTPException(status_code=404, detail=f"No metrics found for date {crawl_date}")
        
        # Convert DataFrame to dict
        metrics = metrics_df.iloc[0].to_dict()
        
        return ApiResponse(
            success=True,
            data=metrics,
            message=f"Job metrics retrieved for {crawl_date}",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting job metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data-role-distribution")
async def get_data_role_distribution(
    crawl_date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format, defaults to latest")
):
    """
    Get data role distribution for pie chart
    """
    try:
        data_fetcher = FetchReportData(logger)
        
        # Use latest date if not provided
        if not crawl_date:
            crawl_date = data_fetcher.get_newest_crawl_date()
            if not crawl_date:
                raise HTTPException(status_code=404, detail="No data available")
        
        # Fetch data role distribution
        role_df = data_fetcher.fetch_data_role(crawl_date)
        
        if role_df.empty:
            raise HTTPException(status_code=404, detail=f"No role data found for date {crawl_date}")
        
        # Convert DataFrame to list of dicts for frontend
        roles_data = role_df.to_dict('records')
        
        return ApiResponse(
            success=True,
            data={
                "roles": roles_data,
                "crawl_date": crawl_date,
                "total_count": sum(role['count'] for role in roles_data)
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
    limit: int = Query(3, description="Number of top tools to return", ge=1, le=10)
):
    """
    Get top data tools
    """
    try:
        data_fetcher = FetchReportData(logger)
        
        # Use latest date if not provided
        if not crawl_date:
            crawl_date = data_fetcher.get_newest_crawl_date()
            if not crawl_date:
                raise HTTPException(status_code=404, detail="No data available")
        
        # Fetch top tools
        tools_df = data_fetcher.fetch_data_tool(crawl_date)
        
        if tools_df.empty:
            raise HTTPException(status_code=404, detail=f"No tools data found for date {crawl_date}")
        
        # Limit results and convert to list of dicts
        top_tools = tools_df.head(limit).to_dict('records')
        
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
    limit: int = Query(5, description="Number of top companies to return", ge=1, le=10)
):
    """
    Get top companies by job openings
    """
    try:
        data_fetcher = FetchReportData(logger)
        
        # Use latest date if not provided
        if not crawl_date:
            crawl_date = data_fetcher.get_newest_crawl_date()
            if not crawl_date:
                raise HTTPException(status_code=404, detail="No data available")
        
        # Fetch top companies
        companies_df = data_fetcher.fetch_openings_company(crawl_date)
        
        if companies_df.empty:
            raise HTTPException(status_code=404, detail=f"No companies data found for date {crawl_date}")
        
        # Limit results and convert to list of dicts
        top_companies = companies_df.head(limit).to_dict('records')
        
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