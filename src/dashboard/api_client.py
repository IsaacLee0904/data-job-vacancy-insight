"""
Dashboard API Client
Centralized API client for dashboard to communicate with FastAPI backend
"""

import sys
import os
import requests
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.core.log_utils import set_logger


class DashboardAPIClient:
    """
    API client for dashboard to interact with FastAPI backend
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", logger=None):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API server
            logger: Logger instance
        """
        self.base_url = base_url.rstrip('/')
        self.logger = logger or set_logger()
        self.session = requests.Session()
        
        # Set default timeout and headers
        self.session.timeout = 30
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Dashboard-Client/1.0'
        })
        
        self.logger.info(f"🔗 Dashboard API Client initialized with base URL: {base_url}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request with error handling and retries
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data or None if failed
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            self.logger.debug(f"Making {method} request to: {endpoint}")
            start_time = time.time()
            
            response = self.session.request(method, url, **kwargs)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                data = response.json()
                self.logger.debug(f"{method} {endpoint} - {response_time:.2f}ms")
                return data
            else:
                self.logger.error(f"{method} {endpoint} - Status: {response.status_code}")
                self.logger.error(f"Error: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Connection error for {endpoint}: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error for {endpoint}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            return None
    
    def get_latest_date(self) -> Optional[str]:
        """
        Get the latest crawl date
        
        Returns:
            Latest crawl date string or None
        """
        response = self._make_request('GET', '/api/v1/latest-date')
        if response and response.get('success'):
            return response['data']['latest_crawl_date']
        return None
    
    def get_job_metrics(self, crawl_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get job opening metrics
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            Job metrics data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/job-metrics', params=params)
        if response and response.get('success'):
            return response['data']
        return None
    
    def get_data_role_distribution(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get data role distribution for pie chart
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            List of role data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/data-role-distribution', params=params)
        if response and response.get('success'):
            return response['data']['roles']
        return None
    
    def get_top_tools(self, crawl_date: Optional[str] = None, limit: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Get top data tools
        
        Args:
            crawl_date: Specific date or None for latest
            limit: Number of tools to return
            
        Returns:
            List of tool data or None
        """
        params = {'limit': limit}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/top-tools', params=params)
        if response and response.get('success'):
            return response['data']['tools']
        return None
    
    def get_top_companies(self, crawl_date: Optional[str] = None, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Get top companies by job openings
        
        Args:
            crawl_date: Specific date or None for latest
            limit: Number of companies to return
            
        Returns:
            List of company data or None
        """
        params = {'limit': limit}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/top-companies', params=params)
        if response and response.get('success'):
            return response['data']['companies']
        return None
    
    def get_dashboard_summary(self, crawl_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive dashboard summary with all key metrics
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            Complete dashboard data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/summary', params=params)
        if response and response.get('success'):
            return response['data']
        return None
    
    def check_api_health(self) -> bool:
        """
        Check if API is healthy and accessible
        
        Returns:
            True if API is healthy, False otherwise
        """
        response = self._make_request('GET', '/api/v1/health')
        return response is not None and response.get('status') == 'healthy'
    
    def warm_cache(self, crawl_date: Optional[str] = None) -> bool:
        """
        Pre-warm API cache for better performance
        
        Args:
            crawl_date: Specific date to warm cache for
            
        Returns:
            True if successful, False otherwise
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('POST', '/api/v1/cache/warm', params=params)
        return response is not None and response.get('success', False)
    
    def get_education_by_data_role(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get education data by data role
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            List of education data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/education-by-data-role', params=params)
        if response and response.get('success'):
            return response['data']['education_data']
        return None
    
    def get_taiwan_openings(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get Taiwan geographic openings data
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            List of Taiwan openings data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/geography/taiwan-openings', params=params)
        if response and response.get('success'):
            return response['data']['taiwan_openings']
        return None
    
    def get_major_city_openings(self, crawl_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get major city openings data
        
        Args:
            crawl_date: Specific date or None for latest
            
        Returns:
            List of major city data or None
        """
        params = {}
        if crawl_date:
            params['crawl_date'] = crawl_date
        
        response = self._make_request('GET', '/api/v1/geography/major-cities', params=params)
        if response and response.get('success'):
            return response['data']['major_cities']
        return None
    
    def get_taipei_historical_openings(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get Taipei historical openings trend
        
        Returns:
            List of Taipei historical data or None
        """
        response = self._make_request('GET', '/api/v1/geography/taipei-historical')
        if response and response.get('success'):
            return response['data']['taipei_historical']
        return None
    
    def get_tools_by_data_role(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get tools by data role for stack analysis
        
        Returns:
            List of tools by data role or None
        """
        response = self._make_request('GET', '/api/v1/tools-by-data-role')
        if response and response.get('success'):
            return response['data']['tools_by_data_role']
        return None


class DashboardDataService:
    """
    High-level service for dashboard data operations
    Provides dashboard-specific data formatting and caching
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8000", logger=None):
        """
        Initialize dashboard data service
        
        Args:
            api_base_url: Base URL of the API server
            logger: Logger instance
        """
        self.api_client = DashboardAPIClient(api_base_url, logger)
        self.logger = logger or set_logger()
        self._cached_latest_date = None
        self._cache_timestamp = None
        self._cache_ttl = 300  # 5 minutes local cache
    
    def get_newest_crawl_date(self) -> Optional[str]:
        """
        Get newest crawl date with local caching
        
        Returns:
            Latest crawl date or None
        """
        # Check local cache first
        current_time = time.time()
        if (self._cached_latest_date and self._cache_timestamp and 
            current_time - self._cache_timestamp < self._cache_ttl):
            return self._cached_latest_date
        
        # Fetch from API
        latest_date = self.api_client.get_latest_date()
        if latest_date:
            self._cached_latest_date = latest_date
            self._cache_timestamp = current_time
            self.logger.info(f"Latest crawl date: {latest_date}")
        
        return latest_date
    
    def load_home_page_data(self) -> tuple:
        """
        Load all data needed for home page using API
        Replaces the original load_home_page_data function
        
        Returns:
            Tuple of (openings_statistics, historical_total_openings, data_role, 
                     data_tools, openings_company, taiepi_area_openings)
        """
        self.logger.info("Loading home page data via API...")
        
        # Get comprehensive dashboard summary (this is more efficient than individual calls)
        summary = self.api_client.get_dashboard_summary()
        
        if not summary:
            self.logger.error("Failed to load dashboard summary from API")
            return None, None, None, None, None, None
        
        # Extract data from summary
        job_metrics = summary.get('job_metrics')
        data_roles = summary.get('data_roles', [])
        top_tools = summary.get('top_tools', [])
        top_companies = summary.get('top_companies', [])
        
        # Convert API response to DataFrame-like format for compatibility
        import pandas as pd
        
        # Job metrics
        openings_statistics = pd.DataFrame([job_metrics]) if job_metrics else pd.DataFrame()
        
        # Data roles
        data_role = pd.DataFrame(data_roles) if data_roles else pd.DataFrame()
        
        # Top tools (top 3)
        data_tools = pd.DataFrame(top_tools) if top_tools else pd.DataFrame()
        
        # Top companies (top 5)
        openings_company = pd.DataFrame(top_companies) if top_companies else pd.DataFrame()
        
        # For historical and area data, fall back to database for now
        # These could be added as API endpoints later
        try:
            from src.core.dashboard_utils import FetchReportData
            from src.dashboard.pages.home_pages import fetch_historical_total_openings_for_dashboard, fetch_taiepi_area_openings_for_dashboard
            
            # Create database fetcher for missing data
            db_fetcher = FetchReportData(self.logger)
            
            # Get historical data from database
            historical_total_openings = fetch_historical_total_openings_for_dashboard(db_fetcher)
            
            # Get area data from database
            latest_date = summary.get('crawl_date')
            if latest_date:
                taiepi_area_openings = fetch_taiepi_area_openings_for_dashboard(db_fetcher, latest_date)
            else:
                taiepi_area_openings = pd.DataFrame()
            
            # Close database connection
            if db_fetcher.connection:
                db_fetcher.connection.close()
                
        except Exception as e:
            self.logger.warning(f"Failed to fetch historical/area data from database: {e}")
            historical_total_openings = pd.DataFrame()
            taiepi_area_openings = pd.DataFrame()
        
        self.logger.info("Home page data loaded successfully via API")
        
        return (openings_statistics, historical_total_openings, data_role, 
                data_tools, openings_company, taiepi_area_openings)
    
    def check_api_connection(self) -> bool:
        """
        Check API connectivity and log status
        
        Returns:
            True if API is accessible, False otherwise
        """
        self.logger.info("Checking API connection...")
        
        if self.api_client.check_api_health():
            self.logger.info("API connection is healthy")
            return True
        else:
            self.logger.error("API connection failed")
            return False


# Global API client instance for easy import
api_client = DashboardAPIClient()
data_service = DashboardDataService()


if __name__ == "__main__":
    # Test the API client
    print("Testing Dashboard API Client...")
    
    client = DashboardAPIClient()
    
    # Test basic connectivity
    if client.check_api_health():
        print("API is healthy")
        
        # Test data retrieval
        latest_date = client.get_latest_date()
        print(f"Latest date: {latest_date}")
        
        if latest_date:
            job_metrics = client.get_job_metrics()
            print(f"Job metrics: {job_metrics is not None}")
            
            roles = client.get_data_role_distribution()
            print(f"Data roles: {len(roles) if roles else 0} roles")
            
            tools = client.get_top_tools()
            print(f"Top tools: {len(tools) if tools else 0} tools")
            
            companies = client.get_top_companies()
            print(f"Top companies: {len(companies) if companies else 0} companies")
    else:
        print("API is not accessible")