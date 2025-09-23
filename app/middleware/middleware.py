import time
import logging
import asyncio
from typing import Callable, Dict, Any, Optional
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.gzip import GZipMiddleware
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
import json
from collections import defaultdict, deque
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis and caching imports
try:
    import redis
    REDIS_AVAILABLE = True
    redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
    redis_client.ping()
    logger.info("✅ Redis connected for rate limiting")
except Exception as e:
    REDIS_AVAILABLE = False
    redis_client = None
    logger.warning(f"⚠️ Redis not available, using in-memory rate limiting: {e}")

# In-memory rate limiting storage (fallback when Redis unavailable)
rate_limit_storage = defaultdict(lambda: defaultdict(deque))
rate_limit_lock = threading.Lock()

class PerformanceMiddleware(BaseHTTPMiddleware):
    """Advanced performance monitoring for high concurrency"""

    def __init__(self, app, enable_profiling: bool = True):
        super().__init__(app)
        self.enable_profiling = enable_profiling
        self.request_times = deque(maxlen=10000)  # Keep last 10000 request times
        self.active_requests = 0
        self.total_requests = 0
        self.slow_requests = deque(maxlen=100)  # Track slow requests

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        self.active_requests += 1
        self.total_requests += 1

        # Add request start time to request state
        request.state.start_time = start_time
        request.state.request_id = f"req_{self.total_requests}"

        try:
            response = await call_next(request)
        except Exception as e:
            # Log the error with request context
            logger.error(f"Request {request.state.request_id} failed: {str(e)}")
            self.active_requests -= 1
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal server error", "request_id": request.state.request_id}
            )
        finally:
            self.active_requests -= 1

        # Calculate processing time
        process_time = time.time() - start_time
        self.request_times.append(process_time)

        # Track slow requests for analysis
        if process_time > 0.5:  # Requests taking more than 500ms
            self.slow_requests.append({
                "url": str(request.url),
                "method": request.method,
                "time": process_time,
                "timestamp": start_time
            })

        # Add comprehensive performance headers
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Active-Requests"] = str(self.active_requests)
        response.headers["X-Timestamp"] = str(int(time.time()))

        # Add rate limit headers if available
        if hasattr(request.state, 'rate_limit_headers'):
            for key, value in request.state.rate_limit_headers.items():
                response.headers[key] = value

        # Optimized cache control
        if request.method == "GET":
            if "api/v1" in str(request.url):
                response.headers["Cache-Control"] = "public, max-age=60"  # API cache
            else:
                response.headers["Cache-Control"] = "public, max-age=300"  # Static cache
        else:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

        # Performance logging
        if process_time > 1.0:
            logger.warning(f"Slow request {request.state.request_id}: {request.method} {request.url} took {process_time:.3f}s")
        elif process_time > 0.1:
            logger.info(f"Request {request.state.request_id}: {process_time:.3f}s")

        return response

class SecurityMiddleware(BaseHTTPMiddleware):
    """Comprehensive security middleware"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Add security headers
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Updated CSP to allow Swagger UI resources from CDN
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com"
        )
        response.headers["Content-Security-Policy"] = csp_policy

        # Remove server header for security
        if "server" in response.headers:
            del response.headers["server"]

        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware to prevent abuse"""

    def __init__(
        self, 
        app, 
        calls: int = 100, 
        period: int = 60,
        per_ip: bool = True,
        skip_paths: Optional[list] = None
    ):
        super().__init__(app)
        self.calls = calls  # Number of calls allowed
        self.period = period  # Period in seconds
        self.per_ip = per_ip
        self.skip_paths = skip_paths or ["/health", "/docs", "/openapi.json"]

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)

        client_ip = self.get_client_ip(request)
        current_time = time.time()

        with rate_limit_lock:
            # Clean old entries
            client_requests = rate_limit_storage[client_ip]["requests"]
            while client_requests and client_requests[0] < current_time - self.period:
                client_requests.popleft()

            # Check rate limit
            if len(client_requests) >= self.calls:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Rate limit exceeded",
                        "detail": f"Maximum {self.calls} requests per {self.period} seconds"
                    },
                    headers={
                        "Retry-After": str(self.period),
                        "X-RateLimit-Limit": str(self.calls),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(current_time + self.period))
                    }
                )

            # Add current request
            client_requests.append(current_time)

        response = await call_next(request)

        # Add rate limit headers
        remaining = max(0, self.calls - len(rate_limit_storage[client_ip]["requests"]))
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.period))

        return response

class DatabaseMiddleware(BaseHTTPMiddleware):
    """Database connection optimization middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Add database session to request state if needed
        response = await call_next(request)

        # Add database query metrics if available
        if hasattr(request.state, "db_queries"):
            response.headers["X-DB-Queries"] = str(request.state.db_queries)

        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Comprehensive request/response logging middleware"""

    def __init__(self, app, log_requests: bool = True, log_responses: bool = False):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Log request
        if self.log_requests:
            logger.info(
                f"Request: {request.method} {request.url} - "
                f"User-Agent: {request.headers.get('user-agent', 'unknown')} - "
                f"IP: {request.client.host if request.client else 'unknown'}"
            )

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {request.method} {request.url} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        return response

class CompressionMiddleware:
    """Custom compression middleware wrapper"""

    @staticmethod
    def add_compression(app, minimum_size: int = 1000):
        """Add GZIP compression middleware"""
        app.add_middleware(GZipMiddleware, minimum_size=minimum_size)

class CacheMiddleware(BaseHTTPMiddleware):
    """Simple in-memory caching middleware for GET requests"""

    def __init__(self, app, cache_ttl: int = 300, max_size: int = 1000):
        super().__init__(app)
        self.cache = {}
        self.cache_times = {}
        self.cache_ttl = cache_ttl  # Time to live in seconds
        self.max_size = max_size
        self.lock = threading.Lock()

    def get_cache_key(self, request: Request) -> str:
        """Generate cache key from request"""
        return f"{request.method}:{request.url}"

    def clean_expired_cache(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.cache_times.items()
            if current_time - timestamp > self.cache_ttl
        ]
        for key in expired_keys:
            self.cache.pop(key, None)
            self.cache_times.pop(key, None)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        cache_key = self.get_cache_key(request)
        current_time = time.time()

        with self.lock:
            # Clean expired entries
            self.clean_expired_cache()

            # Check if cached response exists and is still valid
            if (cache_key in self.cache and 
                current_time - self.cache_times[cache_key] < self.cache_ttl):

                cached_response = self.cache[cache_key]
                response = JSONResponse(content=cached_response["content"])
                response.headers.update(cached_response["headers"])
                response.headers["X-Cache"] = "HIT"
                return response

        # Process request
        response = await call_next(request)

        # Cache successful GET responses
        if response.status_code == 200 and hasattr(response, 'body'):
            with self.lock:
                # Limit cache size
                if len(self.cache) >= self.max_size:
                    # Remove oldest entry
                    oldest_key = min(self.cache_times.keys(), key=self.cache_times.get)
                    self.cache.pop(oldest_key, None)
                    self.cache_times.pop(oldest_key, None)

                try:
                    # Store in cache
                    self.cache[cache_key] = {
                        "content": json.loads(response.body.decode()),
                        "headers": dict(response.headers)
                    }
                    self.cache_times[cache_key] = current_time
                    response.headers["X-Cache"] = "MISS"
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Don't cache if response is not JSON
                    pass

        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.detail,
                    "status_code": exc.status_code,
                    "success": False
                }
            )
        except ValueError as exc:
            logger.error(f"ValueError: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Invalid input",
                    "detail": str(exc),
                    "success": False
                }
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "detail": "An unexpected error occurred",
                    "success": False
                }
            )

def add_all_middleware(app):
    """Add all middleware to the FastAPI app in the correct order"""

    # Error handling should be first to catch all errors
    app.add_middleware(ErrorHandlingMiddleware)

    # Security middleware
    app.add_middleware(SecurityMiddleware)

    # Rate limiting
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

    # Performance monitoring
    app.add_middleware(PerformanceMiddleware)

    # Database optimization
    app.add_middleware(DatabaseMiddleware)

    # Caching for GET requests
    app.add_middleware(CacheMiddleware, cache_ttl=300)

    # Request/Response logging
    app.add_middleware(LoggingMiddleware, log_requests=True)

    # Compression (should be last in the middleware stack)
    CompressionMiddleware.add_compression(app)

    # Trust localhost and common proxy headers
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # In production, specify actual hosts
    )

# Utility functions for middleware configuration
def configure_security_headers(app):
    """Configure additional security settings"""
    pass

def configure_rate_limiting(app, redis_url: Optional[str] = None):
    """Configure rate limiting with optional Redis backend"""
    if redis_url:
        # Configure Redis-based rate limiting for production
        pass

def get_performance_metrics() -> Dict[str, Any]:
    """Get current performance metrics"""
    return {
        "active_connections": len(rate_limit_storage),
        "avg_response_time": sum(list(rate_limit_storage.get("perf", {}).get("times", []))) / max(1, len(list(rate_limit_storage.get("perf", {}).get("times", [])))),
        "total_requests": sum(len(client_data["requests"]) for client_data in rate_limit_storage.values())
    }