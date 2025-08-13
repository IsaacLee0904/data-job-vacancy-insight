"""
Redis Cache Management System
Centralized caching for dashboard data with TTL and invalidation strategies
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List, Union
import redis
from redis import ConnectionPool
import pickle
import logging

from .config import settings


class CacheManager:
    """
    Redis cache manager with TTL strategies and data serialization
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize Redis connection pool and cache manager
        """
        self.logger = logger or logging.getLogger(__name__)
        
        # Create connection pool for better performance
        self.pool = ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=False,  # We'll handle encoding manually for flexibility
            max_connections=20,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
        
        self.redis_client = redis.Redis(connection_pool=self.pool)
        
        # Cache TTL strategies (in seconds) - Optimized for weekly updates
        self.TTL_CONFIG = {
            # Core dashboard data - cache for days since weekly updates
            'job_metrics': 259200,         # 3 days (weekly data, cache most of the week)
            'latest_date': 86400,          # 1 day (check for new data daily)
            'data_role_distribution': 259200, # 3 days
            'top_tools': 259200,           # 3 days
            'top_companies': 259200,       # 3 days
            'dashboard_summary': 172800,   # 2 days (comprehensive data)
            
            # Historical and geographical data - very stable
            'historical_data': 604800,     # 7 days (1 week - matches update cycle)
            'geographical_data': 604800,   # 7 days (location data rarely changes)
            
            # Health checks and system data - keep shorter for monitoring
            'health_check': 1800,          # 30 minutes (system monitoring)
            'system_stats': 3600,          # 1 hour (cache stats)
            
            # API responses - cache for long periods
            'api_response': 259200,        # 3 days (API response caching)
            
            # Default fallback - generous for side project
            'default': 86400              # 1 day
        }
    
    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Generate consistent cache keys with parameters
        """
        # Create a deterministic key from parameters
        key_parts = [prefix]
        
        # Sort kwargs for consistent key generation
        for key, value in sorted(kwargs.items()):
            if value is not None:
                key_parts.append(f"{key}:{value}")
        
        cache_key = ":".join(key_parts)
        
        # If key is too long, use hash
        if len(cache_key) > 200:
            key_hash = hashlib.md5(cache_key.encode()).hexdigest()
            cache_key = f"{prefix}:hash:{key_hash}"
        
        return f"job_vacancy:{cache_key}"
    
    def _serialize_data(self, data: Any) -> bytes:
        """
        Serialize data for Redis storage with fallback methods
        """
        try:
            # Try JSON first for better readability and debugging
            if isinstance(data, (dict, list, str, int, float, bool)) or data is None:
                return json.dumps(data, default=str, ensure_ascii=False).encode('utf-8')
            else:
                # Use pickle for complex objects like pandas DataFrames
                return pickle.dumps(data)
        except (TypeError, ValueError) as e:
            self.logger.warning(f"JSON serialization failed, using pickle: {e}")
            return pickle.dumps(data)
    
    def _deserialize_data(self, data: bytes) -> Any:
        """
        Deserialize data from Redis with fallback methods
        """
        try:
            # Try JSON first
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to pickle
            try:
                return pickle.loads(data)
            except Exception as e:
                self.logger.error(f"Failed to deserialize cached data: {e}")
                return None
    
    def get(self, cache_type: str, **kwargs) -> Optional[Any]:
        """
        Get cached data with automatic deserialization
        """
        try:
            cache_key = self._generate_cache_key(cache_type, **kwargs)
            
            # Get data from Redis
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data is None:
                self.logger.debug(f"Cache miss for key: {cache_key}")
                return None
            
            # Deserialize and return
            data = self._deserialize_data(cached_data)
            self.logger.debug(f"Cache hit for key: {cache_key}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error getting cache for {cache_type}: {e}")
            return None
    
    def set(self, cache_type: str, data: Any, ttl: Optional[int] = None, **kwargs) -> bool:
        """
        Set cached data with automatic serialization and TTL
        """
        try:
            cache_key = self._generate_cache_key(cache_type, **kwargs)
            
            # Get TTL from config or use provided value
            if ttl is None:
                ttl = self.TTL_CONFIG.get(cache_type, self.TTL_CONFIG['default'])
            
            # Serialize data
            serialized_data = self._serialize_data(data)
            
            # Set with TTL
            result = self.redis_client.setex(cache_key, ttl, serialized_data)
            
            self.logger.debug(f"Cached data for key: {cache_key} (TTL: {ttl}s)")
            return result
            
        except Exception as e:
            self.logger.error(f"Error setting cache for {cache_type}: {e}")
            return False
    
    def delete(self, cache_type: str, **kwargs) -> bool:
        """
        Delete specific cached data
        """
        try:
            cache_key = self._generate_cache_key(cache_type, **kwargs)
            result = self.redis_client.delete(cache_key)
            
            self.logger.debug(f"Deleted cache key: {cache_key}")
            return bool(result)
            
        except Exception as e:
            self.logger.error(f"Error deleting cache for {cache_type}: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate multiple cache entries matching a pattern
        """
        try:
            full_pattern = f"job_vacancy:{pattern}*"
            keys = self.redis_client.keys(full_pattern)
            
            if keys:
                deleted_count = self.redis_client.delete(*keys)
                self.logger.info(f"Invalidated {deleted_count} cache entries matching pattern: {pattern}")
                return deleted_count
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Error invalidating cache pattern {pattern}: {e}")
            return 0
    
    def invalidate_all_dashboard_cache(self) -> int:
        """
        Invalidate all dashboard-related cache
        """
        dashboard_patterns = [
            'job_metrics', 'latest_date', 'data_role_distribution',
            'top_tools', 'top_companies', 'dashboard_summary'
        ]
        
        total_deleted = 0
        for pattern in dashboard_patterns:
            total_deleted += self.invalidate_pattern(pattern)
        
        self.logger.info(f"Invalidated all dashboard cache: {total_deleted} entries")
        return total_deleted
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache statistics and information
        """
        try:
            info = self.redis_client.info()
            
            # Get job vacancy specific keys count
            job_vacancy_keys = self.redis_client.keys("job_vacancy:*")
            
            return {
                'redis_version': info.get('redis_version'),
                'connected_clients': info.get('connected_clients'),
                'used_memory_human': info.get('used_memory_human'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'job_vacancy_keys_count': len(job_vacancy_keys),
                'total_keys': info.get('db0', {}).get('keys', 0) if 'db0' in info else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting cache info: {e}")
            return {'error': str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform cache health check
        """
        try:
            # Test basic operations
            test_key = "job_vacancy:health_test"
            test_value = {"timestamp": datetime.now().isoformat(), "test": True}
            
            # Test set
            set_result = self.redis_client.setex(test_key, 10, json.dumps(test_value))
            
            # Test get
            get_result = self.redis_client.get(test_key)
            retrieved_value = json.loads(get_result.decode('utf-8')) if get_result else None
            
            # Test delete
            delete_result = self.redis_client.delete(test_key)
            
            # Test ping
            ping_result = self.redis_client.ping()
            
            return {
                'status': 'healthy',
                'ping': ping_result,
                'set_operation': bool(set_result),
                'get_operation': retrieved_value is not None,
                'delete_operation': bool(delete_result),
                'test_data_match': retrieved_value == test_value if retrieved_value else False
            }
            
        except Exception as e:
            self.logger.error(f"Cache health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def close(self):
        """
        Close Redis connection pool
        """
        try:
            self.redis_client.close()
            self.pool.disconnect()
            self.logger.info("Redis connection pool closed")
        except Exception as e:
            self.logger.error(f"Error closing Redis connection: {e}")


class CacheDecorator:
    """
    Decorator for automatic caching of function results
    """
    
    def __init__(self, cache_manager: CacheManager, cache_type: str, ttl: Optional[int] = None):
        self.cache_manager = cache_manager
        self.cache_type = cache_type
        self.ttl = ttl
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            cache_key_kwargs = {
                'func': func.__name__,
                'args_hash': hashlib.md5(str(args).encode()).hexdigest()[:8],
                **kwargs
            }
            
            # Try to get from cache first
            cached_result = self.cache_manager.get(self.cache_type, **cache_key_kwargs)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            self.cache_manager.set(self.cache_type, result, self.ttl, **cache_key_kwargs)
            
            return result
        
        return wrapper


# Global cache manager instance
_cache_manager = None

def get_cache_manager(logger: Optional[logging.Logger] = None) -> CacheManager:
    """
    Get global cache manager instance (singleton pattern)
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(logger)
    return _cache_manager