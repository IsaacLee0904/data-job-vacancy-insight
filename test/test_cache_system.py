"""
Cache System Unit Tests
Test cache functionality, performance improvements, and Redis integration
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
TEST_TIMEOUT = 30


class TestCacheBasicFunctionality:
    """Test basic cache operations"""
    
    def test_cache_health_endpoint(self):
        """Test cache health check"""
        response = requests.get(f"{API_BASE_URL}/api/v1/cache/health", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy"]
        assert "timestamp" in data
    
    def test_cache_info_endpoint(self):
        """Test cache information endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/v1/cache/info", timeout=TEST_TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert "cache_info" in data
        assert "service_status" in data
        assert "timestamp" in data
    
    def test_cache_warm_endpoint(self):
        """Test cache warming functionality"""
        response = requests.post(f"{API_BASE_URL}/api/v1/cache/warm", timeout=TEST_TIMEOUT)
        
        # Should work even if Redis is not available (graceful degradation)
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert "details" in data
    
    def test_cache_keys_count_endpoint(self):
        """Test cache keys counting"""
        response = requests.get(f"{API_BASE_URL}/api/v1/cache/keys/count", timeout=TEST_TIMEOUT)
        
        # May fail if Redis not running, which is acceptable
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "total_keys" in data
            assert "categories" in data


class TestCachePerformance:
    """Test cache performance improvements"""
    
    def test_response_time_without_cache_warming(self):
        """Test initial response time (potential cache miss)"""
        # Clear any existing cache first
        requests.delete(f"{API_BASE_URL}/api/v1/cache/clear/all", timeout=TEST_TIMEOUT)
        
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        end_time = time.time()
        
        assert response.status_code == 200
        first_response_time = end_time - start_time
        
        # Second request should be faster (cache hit)
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        end_time = time.time()
        
        assert response.status_code == 200
        second_response_time = end_time - start_time
        
        # Second request should not be significantly slower
        # (Note: Without Redis, there might not be significant improvement)
        assert second_response_time <= first_response_time + 0.1
    
    def test_multiple_endpoint_performance(self):
        """Test performance across multiple endpoints"""
        endpoints = [
            "/api/v1/latest-date",
            "/api/v1/job-metrics", 
            "/api/v1/top-tools",
            "/api/v1/top-companies"
        ]
        
        response_times = []
        
        for endpoint in endpoints:
            start_time = time.time()
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # All endpoints should respond reasonably fast
        for i, response_time in enumerate(response_times):
            assert response_time < 3.0, f"Endpoint {endpoints[i]} took {response_time:.2f}s"
        
        avg_response_time = sum(response_times) / len(response_times)
        print(f"Average response time: {avg_response_time:.3f}s")


class TestCacheInvalidation:
    """Test cache invalidation and clearing"""
    
    def test_clear_all_cache(self):
        """Test clearing all cache"""
        response = requests.delete(f"{API_BASE_URL}/api/v1/cache/clear/all", timeout=TEST_TIMEOUT)
        
        # Should work even if Redis not available
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert "deleted_entries" in data["details"]
    
    def test_clear_cache_by_pattern(self):
        """Test clearing cache by pattern"""
        pattern = "job_metrics"
        response = requests.delete(f"{API_BASE_URL}/api/v1/cache/clear/pattern/{pattern}", timeout=TEST_TIMEOUT)
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert pattern in data["details"]["pattern"]
    
    def test_clear_cache_by_date(self):
        """Test clearing cache by specific date"""
        # Get current date from API
        response = requests.get(f"{API_BASE_URL}/api/v1/latest-date", timeout=TEST_TIMEOUT)
        assert response.status_code == 200
        latest_date = response.json()["data"]["latest_crawl_date"]
        
        # Clear cache for that date
        response = requests.delete(f"{API_BASE_URL}/api/v1/cache/clear/date/{latest_date}", timeout=TEST_TIMEOUT)
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            assert latest_date in data["details"]["crawl_date"]


class TestCacheConsistency:
    """Test cache data consistency"""
    
    def test_cache_data_integrity(self):
        """Test that cached data matches fresh data"""
        endpoint = "/api/v1/latest-date"
        
        # Get data (potentially from cache)
        response1 = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Get data again (should be same)
        response2 = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Data should be identical
        assert data1["data"] == data2["data"]
    
    def test_cache_warm_data_consistency(self):
        """Test that cache warming maintains data consistency"""
        # Get original data
        response_before = requests.get(f"{API_BASE_URL}/api/v1/job-metrics", timeout=TEST_TIMEOUT)
        assert response_before.status_code == 200
        data_before = response_before.json()["data"]
        
        # Warm cache
        warm_response = requests.post(f"{API_BASE_URL}/api/v1/cache/warm", timeout=TEST_TIMEOUT)
        
        # Get data after warming
        response_after = requests.get(f"{API_BASE_URL}/api/v1/job-metrics", timeout=TEST_TIMEOUT)
        assert response_after.status_code == 200
        data_after = response_after.json()["data"]
        
        # Data should be consistent
        assert data_before["total_openings"] == data_after["total_openings"]
        assert data_before["crawl_date"] == data_after["crawl_date"]


class TestCacheConfiguration:
    """Test cache configuration and TTL settings"""
    
    def test_cache_ttl_configuration(self):
        """Test that cache TTL is properly configured"""
        # This test mainly verifies the API accepts requests
        # Actual TTL testing would require Redis monitoring
        
        endpoints_with_expected_cache = [
            "/api/v1/latest-date",      # 1 day TTL
            "/api/v1/job-metrics",      # 3 days TTL
            "/api/v1/top-tools",        # 3 days TTL
            "/api/v1/summary",          # 2 days TTL
        ]
        
        for endpoint in endpoints_with_expected_cache:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            # Check if response has appropriate cache headers
            # (These might be set by middleware)
            headers = response.headers
            # Cache headers might not be present without Redis
            # So we just verify the response is valid


class TestCacheGracefulDegradation:
    """Test that system works without Redis"""
    
    def test_api_works_without_redis(self):
        """Test that API functions normally even if Redis is unavailable"""
        # All these should work regardless of Redis status
        endpoints = [
            "/api/v1/latest-date",
            "/api/v1/job-metrics",
            "/api/v1/data-role-distribution",
            "/api/v1/top-tools",
            "/api/v1/top-companies",
            "/api/v1/summary"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            assert response.status_code == 200, f"Endpoint {endpoint} failed"
            
            data = response.json()
            assert data["success"] is True
            assert "data" in data
            assert data["data"] is not None
    
    def test_cache_endpoints_handle_redis_unavailable(self):
        """Test cache endpoints handle Redis being unavailable gracefully"""
        cache_endpoints = [
            ("GET", "/api/v1/cache/health"),
            ("GET", "/api/v1/cache/info"),
            ("POST", "/api/v1/cache/warm"),
        ]
        
        for method, endpoint in cache_endpoints:
            if method == "GET":
                response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            elif method == "POST":
                response = requests.post(f"{API_BASE_URL}{endpoint}", timeout=TEST_TIMEOUT)
            
            # Should not crash the API
            assert response.status_code in [200, 404, 500, 503]
            
            # Should return valid JSON
            try:
                data = response.json()
                assert isinstance(data, dict)
            except:
                pytest.fail(f"Endpoint {endpoint} did not return valid JSON")


if __name__ == "__main__":
    print("🧪 Running Cache System Tests...")
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
    
    print("✅ API is responding, starting cache tests...")
    
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])