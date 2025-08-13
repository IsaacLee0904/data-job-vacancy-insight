#!/usr/bin/env python3
"""
Cache Middleware for FastAPI
Automatic caching of API responses with smart invalidation
"""

import time
import json
import hashlib
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..core.cache import get_cache_manager
from ..core.config import settings


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Middleware for automatic API response caching
    """
    
    def __init__(self, app, logger=None):
        super().__init__(app)
        self.cache_manager = get_cache_manager(logger)
        self.logger = logger
        
        # Define which endpoints should be cached
        self.CACHEABLE_ENDPOINTS = {
            '/api/v1/latest-date': {
                'cache_type': 'latest_date',
                'ttl': 86400,  # 1 day
                'cache_methods': ['GET']
            },
            '/api/v1/job-metrics': {
                'cache_type': 'job_metrics',
                'ttl': 259200,  # 3 days
                'cache_methods': ['GET']
            },
            '/api/v1/data-role-distribution': {
                'cache_type': 'data_role_distribution',
                'ttl': 259200,  # 3 days
                'cache_methods': ['GET']
            },
            '/api/v1/top-tools': {
                'cache_type': 'top_tools',
                'ttl': 259200,  # 3 days
                'cache_methods': ['GET']
            },
            '/api/v1/top-companies': {
                'cache_type': 'top_companies',
                'ttl': 259200,  # 3 days
                'cache_methods': ['GET']
            },
            '/api/v1/summary': {
                'cache_type': 'dashboard_summary',
                'ttl': 172800,  # 2 days
                'cache_methods': ['GET']
            },
            '/api/v1/health/detailed': {
                'cache_type': 'health_check',
                'ttl': 1800,   # 30 minutes (keep shorter for monitoring)
                'cache_methods': ['GET']
            }
        }
        
        # Endpoints that should invalidate cache when called
        self.CACHE_INVALIDATION_ENDPOINTS = {
            # When new data is added, invalidate related dashboard cache
            '/api/v1/data/refresh': ['job_metrics', 'latest_date', 'data_role_distribution'],
            '/api/v1/data/load': ['job_metrics', 'latest_date'],
        }
    
    def _generate_cache_key(self, request: Request, cache_type: str) -> str:
        """
        Generate cache key from request details
        """
        # Include path, query parameters, and method
        key_components = {
            'path': str(request.url.path),
            'method': request.method,
            'query': str(sorted(request.query_params.items())),
        }
        
        # Create hash for consistent key length
        key_string = json.dumps(key_components, sort_keys=True)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{cache_type}:api:{key_hash}"
    
    def _should_cache_request(self, request: Request) -> Optional[dict]:
        """
        Determine if request should be cached
        """
        path = str(request.url.path)
        method = request.method
        
        # Check exact path match
        if path in self.CACHEABLE_ENDPOINTS:
            endpoint_config = self.CACHEABLE_ENDPOINTS[path]
            if method in endpoint_config.get('cache_methods', ['GET']):
                return endpoint_config
        
        # Check pattern match for parameterized endpoints
        for endpoint_pattern, config in self.CACHEABLE_ENDPOINTS.items():
            if self._path_matches_pattern(path, endpoint_pattern):
                if method in config.get('cache_methods', ['GET']):
                    return config
        
        return None
    
    def _path_matches_pattern(self, path: str, pattern: str) -> bool:
        """
        Simple pattern matching for endpoints with parameters
        """
        # For now, just exact match. Can be extended for path parameters
        return path == pattern
    
    def _should_invalidate_cache(self, request: Request) -> list:
        """
        Determine if request should invalidate cache
        """
        path = str(request.url.path)
        method = request.method
        
        if method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if path in self.CACHE_INVALIDATION_ENDPOINTS:
                return self.CACHE_INVALIDATION_ENDPOINTS[path]
            
            # Invalidate all dashboard cache for data modification endpoints
            if '/api/v1/data/' in path:
                return ['job_metrics', 'latest_date', 'data_role_distribution', 'top_tools', 'top_companies']
        
        return []
    
    def _create_cached_response(self, cached_data: dict, cache_hit_time: float) -> JSONResponse:
        """
        Create response from cached data with cache headers
        """
        response_data = cached_data.get('data', {})
        
        # Add cache metadata
        if isinstance(response_data, dict):
            response_data['_cache'] = {
                'hit': True,
                'cached_at': cached_data.get('cached_at'),
                'response_time_ms': round((time.time() - cache_hit_time) * 1000, 2)
            }
        
        response = JSONResponse(content=response_data)
        
        # Add cache headers
        response.headers['X-Cache'] = 'HIT'
        response.headers['X-Cache-Timestamp'] = cached_data.get('cached_at', '')
        
        return response
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Main middleware logic
        """
        start_time = time.time()
        
        # Check if we should invalidate cache
        cache_types_to_invalidate = self._should_invalidate_cache(request)
        if cache_types_to_invalidate:
            for cache_type in cache_types_to_invalidate:
                self.cache_manager.invalidate_pattern(cache_type)
            if self.logger:
                self.logger.info(f"Invalidated cache types: {cache_types_to_invalidate}")
        
        # Check if request should be cached
        cache_config = self._should_cache_request(request)
        if not cache_config:
            # Not cacheable, proceed normally
            response = await call_next(request)
            response.headers['X-Cache'] = 'BYPASS'
            return response
        
        # Generate cache key
        cache_key = self._generate_cache_key(request, cache_config['cache_type'])
        
        # Try to get from cache
        cache_hit_time = time.time()
        cached_data = self.cache_manager.get('api_response', cache_key=cache_key)
        
        if cached_data is not None:
            # Cache hit - return cached response
            if self.logger:
                self.logger.debug(f"Cache hit for {request.url.path}")
            return self._create_cached_response(cached_data, cache_hit_time)
        
        # Cache miss - proceed with request
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200 and hasattr(response, 'body'):
            try:
                # Read response body
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk
                
                # Parse JSON response
                response_data = json.loads(response_body.decode())
                
                # Prepare cache data
                cache_data = {
                    'data': response_data,
                    'cached_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status_code': response.status_code
                }
                
                # Cache the response
                self.cache_manager.set(
                    'api_response',
                    cache_data,
                    ttl=cache_config.get('ttl'),
                    cache_key=cache_key
                )
                
                # Add cache metadata to response
                if isinstance(response_data, dict):
                    response_data['_cache'] = {
                        'hit': False,
                        'cached_at': cache_data['cached_at'],
                        'response_time_ms': round((time.time() - start_time) * 1000, 2)
                    }
                
                # Create new response with modified data
                new_response = JSONResponse(content=response_data)
                new_response.headers['X-Cache'] = 'MISS'
                new_response.headers['X-Cache-Timestamp'] = cache_data['cached_at']
                
                # Copy original headers
                for key, value in response.headers.items():
                    if key.lower() not in ['content-length', 'content-type']:
                        new_response.headers[key] = value
                
                if self.logger:
                    self.logger.debug(f"Cached response for {request.url.path}")
                
                return new_response
                
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to cache response for {request.url.path}: {e}")
        
        # Add cache miss header
        response.headers['X-Cache'] = 'MISS'
        return response


class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware for manual cache control via headers
    """
    
    def __init__(self, app, logger=None):
        super().__init__(app)
        self.cache_manager = get_cache_manager(logger)
        self.logger = logger
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Handle cache control headers
        """
        # Check for cache control headers
        cache_control = request.headers.get('Cache-Control', '').lower()
        
        if 'no-cache' in cache_control:
            # Client requests fresh data - invalidate relevant cache
            if self.logger:
                self.logger.info(f"No-cache requested for {request.url.path}")
            
            # You could implement more specific cache invalidation based on the endpoint
            # For now, we'll let the request proceed normally
        
        if 'max-age=0' in cache_control:
            # Client wants to revalidate cache
            if self.logger:
                self.logger.info(f"Cache revalidation requested for {request.url.path}")
        
        response = await call_next(request)
        
        # Add cache control headers to response (optimized for side project)
        if request.url.path.startswith('/api/v1/') and 'dashboard' in request.url.path:
            response.headers['Cache-Control'] = 'public, max-age=259200'  # 3 days
        elif request.url.path.startswith('/api/v1/health/'):
            response.headers['Cache-Control'] = 'public, max-age=1800'   # 30 minutes
        elif request.url.path.startswith('/api/v1/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'  # 1 day (default API)
        
        return response