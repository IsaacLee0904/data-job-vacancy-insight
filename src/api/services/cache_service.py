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
    
    def get_or_fetch_education_by_data_role(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get education by data role with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"education_by_data_role_{crawl_date}"
        
        # Try cache first
        cached_education = self.cache_manager.get('education_by_data_role', date=crawl_date, key=cache_key)
        if cached_education:
            self.logger.debug(f"Retrieved education by data role from cache for {crawl_date}")
            return cached_education
        
        # Fetch from database
        try:
            education_df = self.data_fetcher.fetch_education_by_data_role(crawl_date)
            if not education_df.empty:
                education_data = education_df.to_dict('records')
                
                # Cache for 3 days (matches job_metrics TTL)
                self.cache_manager.set('education_by_data_role', education_data, ttl=259200, date=crawl_date, key=cache_key)
                self.logger.info(f"Cached education by data role for {crawl_date}")
                return education_data
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching education by data role for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_taiwan_openings(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get Taiwan openings geographic data with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"taiwan_openings_{crawl_date}"
        
        # Try cache first
        cached_taiwan = self.cache_manager.get('taiwan_openings', date=crawl_date, key=cache_key)
        if cached_taiwan:
            self.logger.debug(f"Retrieved Taiwan openings from cache for {crawl_date}")
            return cached_taiwan
        
        # Fetch from database
        try:
            taiwan_df = self.data_fetcher.fetch_taiwan_openings(crawl_date)
            if not taiwan_df.empty:
                taiwan_data = taiwan_df.to_dict('records')
                
                # Cache for 3 days (geographic data changes weekly)
                self.cache_manager.set('taiwan_openings', taiwan_data, ttl=259200, date=crawl_date, key=cache_key)
                self.logger.info(f"Cached Taiwan openings for {crawl_date}")
                return taiwan_data
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching Taiwan openings for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_major_city_openings(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get major city openings data with caching
        """
        if not crawl_date:
            crawl_date = self.get_or_fetch_latest_date()
            if not crawl_date:
                return None
        
        cache_key = f"major_city_openings_{crawl_date}"
        
        # Try cache first
        cached_cities = self.cache_manager.get('major_city_openings', date=crawl_date, key=cache_key)
        if cached_cities:
            self.logger.debug(f"Retrieved major city openings from cache for {crawl_date}")
            return cached_cities
        
        # Fetch from database
        try:
            cities_df = self.data_fetcher.fetch_major_city_openings(crawl_date)
            if not cities_df.empty:
                cities_data = cities_df.to_dict('records')
                
                # Cache for 3 days (geographic data changes weekly)
                self.cache_manager.set('major_city_openings', cities_data, ttl=259200, date=crawl_date, key=cache_key)
                self.logger.info(f"Cached major city openings for {crawl_date}")
                return cities_data
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching major city openings for {crawl_date}: {e}")
            return None
    
    def get_or_fetch_taipei_historical_openings(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get Taipei historical openings trend with caching
        """
        cache_key = "taipei_historical_openings"
        
        # Try cache first
        cached_taipei_trend = self.cache_manager.get('taipei_historical', key=cache_key)
        if cached_taipei_trend:
            self.logger.debug("Retrieved Taipei historical openings from cache")
            return cached_taipei_trend
        
        # Fetch from database
        try:
            taipei_df = self.data_fetcher.fetch_taipei_historical_openings()
            if not taipei_df.empty:
                taipei_data = taipei_df.to_dict('records')
                
                # Cache for 7 days (historical trend data changes weekly)
                self.cache_manager.set('taipei_historical', taipei_data, ttl=604800, key=cache_key)
                self.logger.info("Cached Taipei historical openings")
                return taipei_data
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching Taipei historical openings: {e}")
            return None
    
    def get_or_fetch_tool_by_data_role(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get tool by data role data with caching (for stack analysis)
        """
        cache_key = "tool_by_data_role"
        
        # Try cache first
        cached_tools = self.cache_manager.get('tool_by_data_role', key=cache_key)
        if cached_tools:
            self.logger.debug("Retrieved tool by data role from cache")
            return cached_tools
        
        # Fetch from database
        try:
            tools_df = self.data_fetcher.fetch_tool_by_data_role()
            if not tools_df.empty:
                tools_data = tools_df.to_dict('records')
                
                # Cache for 3 days (tool trends change weekly)
                self.cache_manager.set('tool_by_data_role', tools_data, ttl=259200, key=cache_key)
                self.logger.info("Cached tool by data role data")
                return tools_data
            
            return []
        except Exception as e:
            self.logger.error(f"Error fetching tool by data role: {e}")
            return None