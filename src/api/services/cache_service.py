#!/usr/bin/env python3
"""
Cache Service for Business Logic
High-level caching functions for dashboard data
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd

from ..core.cache import get_cache_manager, CacheDecorator
from ..core.config import settings
from src.core.dashboard_utils import FetchReportData
from src.core.log_utils import set_logger


class DashboardCacheService:
    """
    Service for caching dashboard-specific data with business logic
    """
    
    def __init__(self, logger=None):
        self.logger = logger or set_logger()
        self.cache_manager = get_cache_manager(self.logger)
        self.data_fetcher = FetchReportData(self.logger)
    
    def get_or_fetch_latest_date(self) -> Optional[str]:
        """
        Get latest crawl date with caching
        """
        cache_key = "latest_crawl_date"
        
        # Try cache first
        cached_date = self.cache_manager.get('latest_date', key=cache_key)
        if cached_date:
            self.logger.debug("Retrieved latest date from cache")
            return cached_date
        
        # Fetch from database
        try:
            latest_date = self.data_fetcher.get_newest_crawl_date()
            if latest_date:
                # Cache for 30 minutes
                self.cache_manager.set('latest_date', latest_date, ttl=1800, key=cache_key)
                self.logger.info(f"Cached latest date: {latest_date}")
            return latest_date
        except Exception as e:
            self.logger.error(f"Error fetching latest date: {e}")
            return None
    
    def get_or_fetch_job_metrics(self, crawl_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get job metrics with caching
        """
        # Use latest date if not provided
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"job_metrics_{crawl_date}"
        
        # Try cache first
        cached_metrics = self.cache_manager.get('job_metrics', date=crawl_date, key=cache_key)
        if cached_metrics:
            self.logger.debug(f"Retrieved job metrics from cache for {crawl_date}")
            return cached_metrics
        
        # Fetch from database
        try:
            metrics_df = self.data_fetcher.fetch_openings_statistics_metrics(crawl_date)
            if not metrics_df.empty:
                metrics_dict = metrics_df.iloc[0].to_dict()
                
                # Cache for 1 hour
                self.cache_manager.set('job_metrics', metrics_dict, ttl=3600, date=crawl_date, key=cache_key)
                self.logger.info(f"Cached job metrics for {crawl_date}")
                return metrics_dict
            
            return None
        except Exception as e:
            self.logger.error(f"Error fetching job metrics for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_data_role_distribution(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get data role distribution with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"data_role_{crawl_date}"
        
        # Try cache first
        cached_roles = self.cache_manager.get('data_role_distribution', date=crawl_date, key=cache_key)
        if cached_roles:
            self.logger.debug(f"Retrieved data roles from cache for {crawl_date}")
            return cached_roles
        
        # Fetch from database
        try:
            roles_df = self.data_fetcher.fetch_data_role(crawl_date)
            if not roles_df.empty:
                roles_list = roles_df.to_dict('records')
                
                # Cache for 1 hour
                self.cache_manager.set('data_role_distribution', roles_list, ttl=3600, date=crawl_date, key=cache_key)
                self.logger.info(f"Cached data roles for {crawl_date}")
                return roles_list
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching data roles for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_top_tools(self, crawl_date: Optional[str] = None, limit: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Get top tools with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"top_tools_{crawl_date}_{limit}"
        
        # Try cache first
        cached_tools = self.cache_manager.get('top_tools', date=crawl_date, limit=limit, key=cache_key)
        if cached_tools:
            self.logger.debug(f"Retrieved top tools from cache for {crawl_date}")
            return cached_tools
        
        # Fetch from database
        try:
            tools_df = self.data_fetcher.fetch_data_tool(crawl_date)
            if not tools_df.empty:
                top_tools = tools_df.head(limit).to_dict('records')
                
                # Cache for 30 minutes
                self.cache_manager.set('top_tools', top_tools, ttl=1800, date=crawl_date, limit=limit, key=cache_key)
                self.logger.info(f"Cached top {limit} tools for {crawl_date}")
                return top_tools
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching top tools for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_top_companies(self, crawl_date: Optional[str] = None, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Get top companies with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"top_companies_{crawl_date}_{limit}"
        
        # Try cache first
        cached_companies = self.cache_manager.get('top_companies', date=crawl_date, limit=limit, key=cache_key)
        if cached_companies:
            self.logger.debug(f"Retrieved top companies from cache for {crawl_date}")
            return cached_companies
        
        # Fetch from database
        try:
            companies_df = self.data_fetcher.fetch_openings_company(crawl_date)
            if not companies_df.empty:
                top_companies = companies_df.head(limit).to_dict('records')
                
                # Cache for 30 minutes
                self.cache_manager.set('top_companies', top_companies, ttl=1800, date=crawl_date, limit=limit, key=cache_key)
                self.logger.info(f"Cached top {limit} companies for {crawl_date}")
                return top_companies
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching top companies for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_dashboard_summary(self, crawl_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive dashboard summary with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"dashboard_summary_{crawl_date}"
        
        # Try cache first
        cached_summary = self.cache_manager.get('dashboard_summary', date=crawl_date, key=cache_key)
        if cached_summary:
            self.logger.debug(f"Retrieved dashboard summary from cache for {crawl_date}")
            return cached_summary
        
        # Fetch all data
        try:
            summary = {
                'crawl_date': crawl_date,
                'job_metrics': self.get_or_fetch_job_metrics(crawl_date),
                'data_roles': self.get_or_fetch_data_role_distribution(crawl_date),
                'top_tools': self.get_or_fetch_top_tools(crawl_date, 3),
                'top_companies': self.get_or_fetch_top_companies(crawl_date, 5),
                'generated_at': datetime.now().isoformat()
            }
            
            # Cache for 15 minutes
            self.cache_manager.set('dashboard_summary', summary, ttl=900, date=crawl_date, key=cache_key)
            self.logger.info(f"Cached dashboard summary for {crawl_date}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating dashboard summary for {crawl_date}: {e}")
            return None
    
    def invalidate_date_cache(self, crawl_date: str):
        """
        Invalidate all cache entries for a specific date
        """
        patterns = [
            f"job_metrics*{crawl_date}*",
            f"data_role*{crawl_date}*",
            f"top_tools*{crawl_date}*",
            f"top_companies*{crawl_date}*",
            f"dashboard_summary*{crawl_date}*"
        ]
        
        total_invalidated = 0
        for pattern in patterns:
            total_invalidated += self.cache_manager.invalidate_pattern(pattern)
        
        self.logger.info(f"Invalidated {total_invalidated} cache entries for date {crawl_date}")
        return total_invalidated
    
    def warm_cache(self, crawl_date: Optional[str] = None) -> Dict[str, bool]:
        """
        Pre-warm cache with commonly accessed data
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return {'error': 'No crawl date available'}
        
        self.logger.info(f"Warming cache for date: {crawl_date}")
        
        results = {
            'latest_date': bool(self.get_or_fetch_latest_date()),
            'job_metrics': bool(self.get_or_fetch_job_metrics(crawl_date)),
            'data_roles': bool(self.get_or_fetch_data_role_distribution(crawl_date)),
            'top_tools': bool(self.get_or_fetch_top_tools(crawl_date, 3)),
            'top_companies': bool(self.get_or_fetch_top_companies(crawl_date, 5)),
            'dashboard_summary': bool(self.get_or_fetch_dashboard_summary(crawl_date))
        }
        
        success_count = sum(results.values())
        self.logger.info(f"Cache warming completed: {success_count}/{len(results)} successful")
        
        return results
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get cache usage statistics
        """
        try:
            cache_info = self.cache_manager.get_cache_info()
            
            # Calculate hit rate if available
            hits = cache_info.get('keyspace_hits', 0)
            misses = cache_info.get('keyspace_misses', 0)
            total_requests = hits + misses
            hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'cache_info': cache_info,
                'hit_rate_percentage': round(hit_rate, 2),
                'total_requests': total_requests,
                'service_status': 'healthy'
            }
        except Exception as e:
            self.logger.error(f"Error getting cache statistics: {e}")
            return {
                'error': str(e),
                'service_status': 'unhealthy'
            }