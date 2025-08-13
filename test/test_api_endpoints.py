"""
API Endpoints Unit Tests
Test all dashboard API endpoints and cache functionality
"""

import sys
import os
import pytest
import requests
import time
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30  # seconds


class TestAPIHealth:
    """Test API health and connectivity"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = requests.get(f"{API_BASE_URL}/", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Job Vacancy Insight API"
        assert data["version"] == "1.0.0"
        assert "docs" in data
        assert "health" in data
    
    def test_basic_health_check(self):
        """Test basic health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"
        assert data["environment"] == "development"
    
    def test_database_health(self):
        """Test database connectivity and data availability"""
        response = requests.get(f"{API_BASE_URL}/api/v1/health/database", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["reporting_tables"] > 0
        assert data["latest_data_date"] is not None
        assert "connection_info" in data


class TestDashboardAPI:
    """Test dashboard data endpoints"""
    
    def test_latest_date_endpoint(self):
        """Test getting latest crawl date"""
        response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "latest_crawl_date" in data["data"]
        assert data["data"]["latest_crawl_date"] is not None
        assert len(data["data"]["latest_crawl_date"]) == 10  # YYYY-MM-DD format
    
    def test_job_metrics_endpoint(self):
        """Test job metrics endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/job-metrics", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        metrics = data["data"]
        required_fields = [
            "total_openings", "total_openings_change_pct",
            "closed_openings_count", "closed_openings_change_pct", 
            "new_openings_count", "new_openings_change_pct",
            "fill_rate", "fill_rate_change_pct",
            "average_weeks_to_fill", "average_weeks_to_fill_change_pct",
            "crawl_date"
        ]
        
        for field in required_fields:
            assert field in metrics, f"Missing required field: {field}"
        
        # Test data types and ranges
        assert isinstance(metrics["total_openings"], int)
        assert metrics["total_openings"] > 0
        assert isinstance(metrics["fill_rate"], float)
        assert 0 <= metrics["fill_rate"] <= 1
    
    def test_data_role_distribution_endpoint(self):
        """Test data role distribution endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/data-role-distribution", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        response_data = data["data"]
        assert "roles" in response_data
        assert "total_count" in response_data
        assert "crawl_date" in response_data
        
        roles = response_data["roles"]
        assert len(roles) > 0
        
        # Test role data structure
        for role in roles:
            assert "data_role" in role
            assert "count" in role
            assert "percentage_of_total" in role
            assert isinstance(role["count"], int)
            assert isinstance(role["percentage_of_total"], float)
            assert role["count"] > 0
            assert role["percentage_of_total"] > 0
        
        # Test that percentages sum up reasonably (allowing for rounding)
        total_percentage = sum(role["percentage_of_total"] for role in roles)
        assert 99 <= total_percentage <= 101  # Allow for rounding errors
    
    def test_top_tools_endpoint(self):
        """Test top tools endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/top-tools", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        response_data = data["data"]
        assert "tools" in response_data
        assert "count" in response_data
        assert "crawl_date" in response_data
        
        tools = response_data["tools"]
        assert len(tools) <= 3  # Default limit is 3
        
        # Test tool data structure
        for tool in tools:
            assert "rank" in tool
            assert "tool_name" in tool
            assert "percentage_of_tool" in tool
            assert isinstance(tool["rank"], int)
            assert isinstance(tool["percentage_of_tool"], float)
            assert tool["rank"] > 0
            assert tool["percentage_of_tool"] > 0
    
    def test_top_tools_with_custom_limit(self):
        """Test top tools endpoint with custom limit"""
        response = requests.get(f"{API_BASE_URL}/api/v1/top-tools?limit=5", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        tools = data["data"]["tools"]
        assert len(tools) <= 5  # Should respect the limit parameter
    
    def test_top_companies_endpoint(self):
        """Test top companies endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/top-companies", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        response_data = data["data"]
        assert "companies" in response_data
        assert "count" in response_data
        assert "crawl_date" in response_data
        
        companies = response_data["companies"]
        assert len(companies) <= 5  # Default limit is 5
        
        # Test company data structure
        for company in companies:
            assert "rank" in company
            assert "company_name" in company
            assert "opening_count" in company
            assert isinstance(company["rank"], int)
            assert isinstance(company["opening_count"], int)
            assert company["rank"] > 0
            assert company["opening_count"] > 0
    
    def test_dashboard_summary_endpoint(self):
        """Test comprehensive dashboard summary endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/summary", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        summary = data["data"]
        required_sections = ["job_metrics", "data_roles", "top_tools", "top_companies", "crawl_date"]
        
        for section in required_sections:
            assert section in summary, f"Missing section: {section}"
        
        # Test that all sections have data
        assert len(summary["data_roles"]) > 0
        assert len(summary["top_tools"]) > 0
        assert len(summary["top_companies"]) > 0
        assert summary["job_metrics"]["total_openings"] > 0


class TestCacheAPI:
    """Test cache management endpoints"""
    
    def test_cache_health(self):
        """Test cache health check - may fail if Redis not running"""
        response = requests.get(f"{API_BASE_URL}/api/v1/cache/health", timeout=TEST_TIMEOUT)
        
        # Accept both healthy (Redis running) and unhealthy (Redis not running) states
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy"]
        assert "timestamp" in data
    
    def test_cache_warm(self):
        """Test cache warming functionality"""
        response = requests.post(f"{API_BASE_URL}/api/v1/cache/warm", timeout=TEST_TIMEOUT)
        
        assert response.status_code in [200, 500]  # May fail if Redis not running
        data = response.json()
        
        if response.status_code == 200:
            assert data["success"] is True
            assert "details" in data
            assert "results" in data["details"]
    
    def test_cache_info(self):
        """Test cache information endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/cache/info", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert "service_status" in data
        assert "timestamp" in data


class TestAPIPerformance:
    """Test API performance and response times"""
    
    def test_response_time_latest_date(self):
        """Test response time for latest date endpoint"""
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_response_time_job_metrics(self):
        """Test response time for job metrics endpoint"""
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/api/v1/job-metrics", timeout=TEST_TIMEOUT)
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 2.0  # Should respond within 2 seconds
    
    def test_concurrent_requests(self):
        """Test API handles concurrent requests"""
        import concurrent.futures
        import threading
        
        def make_request():
            response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
            return response.status_code == 200
        
        # Make 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(results), "Some concurrent requests failed"


class TestAPIErrorHandling:
    """Test API error handling and edge cases"""
    
    def test_invalid_endpoint(self):
        """Test 404 error for non-existent endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/nonexistent", timeout=TEST_TIMEOUT)
        assert response.status_code == 404
    
    def test_invalid_date_parameter(self):
        """Test error handling for invalid date parameter"""
        response = requests.get(f"{API_BASE_URL}/api/v1/job-metrics?crawl_date=invalid-date", timeout=TEST_TIMEOUT)
        
        # Should either return 422 (validation error) or 404 (no data found)
        assert response.status_code in [404, 422, 500]
    
    def test_invalid_limit_parameter(self):
        """Test error handling for invalid limit parameter"""
        response = requests.get(f"{API_BASE_URL}/api/v1/top-tools?limit=999", timeout=TEST_TIMEOUT)
        
        # Should handle gracefully - either return available data or validation error
        assert response.status_code in [200, 422]


class TestDataConsistency:
    """Test data consistency across endpoints"""
    
    def test_date_consistency(self):
        """Test that all endpoints return data for the same date"""
        # Get latest date
        latest_response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        latest_date = latest_response.json()["data"]["latest_crawl_date"]
        
        # Test other endpoints
        endpoints = [
            "/api/v1/job-metrics",
            "/api/v1/data-role-distribution", 
            "/api/v1/top-tools",
            "/api/v1/top-companies"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()["data"]
            # Check if crawl_date is in the response
            if "crawl_date" in data:
                assert data["crawl_date"] == latest_date
            # For nested data structures
            elif isinstance(data, dict) and any("crawl_date" in str(data) for item in data.values() if isinstance(item, list)):
                for key, value in data.items():
                    if isinstance(value, list) and value and isinstance(value[0], dict) and "crawl_date" in value[0]:
                        assert value[0]["crawl_date"] == latest_date


if __name__ == "__main__":
    # Run tests if executed directly
    print("🧪 Running API Unit Tests...")
    print(f"🎯 Testing API at: {API_BASE_URL}")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API. Make sure it's running at http://localhost:8000")
        sys.exit(1)
    
    print("✅ API is responding, starting tests...")
    
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])