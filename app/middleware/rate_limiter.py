
import time
import json
import redis
import logging
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from starlette.requests import Request

logger = logging.getLogger(__name__)

class AdvancedRateLimiter:
    def __init__(self, redis_url: str = "redis://localhost:6379/1"):
        try:
            self.redis = redis.Redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=1)
            self.redis.ping()
            logger.info("✅ Redis rate limiter initialized")
        except Exception as e:
            logger.warning(f"⚠️ Redis unavailable: {e}. Using memory fallback.")
            self.redis = None
            self.memory_store = {}
    
    async def is_allowed(
        self, 
        key: str, 
        limit: int, 
        window: int,
        burst_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Advanced rate limiting with burst support
        Returns: {"allowed": bool, "remaining": int, "reset_time": int}
        """
        current_time = int(time.time())
        
        if self.redis:
            return await self._redis_rate_limit(key, limit, window, current_time, burst_limit)
        else:
            return await self._memory_rate_limit(key, limit, window, current_time)
    
    async def _redis_rate_limit(
        self, 
        key: str, 
        limit: int, 
        window: int, 
        current_time: int,
        burst_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Redis-based sliding window rate limiting"""
        pipe = self.redis.pipeline()
        
        # Sliding window key
        window_key = f"rate_limit:{key}:{current_time // window}"
        
        try:
            # Get current count
            current_count = self.redis.get(window_key)
            current_count = int(current_count) if current_count else 0
            
            # Check burst limit first
            if burst_limit and current_count >= burst_limit:
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_time": (current_time // window + 1) * window,
                    "reason": "burst_limit_exceeded"
                }
            
            # Check regular limit
            if current_count >= limit:
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_time": (current_time // window + 1) * window,
                    "reason": "rate_limit_exceeded"
                }
            
            # Increment counter
            pipe.incr(window_key)
            pipe.expire(window_key, window * 2)  # Keep for 2 windows
            pipe.execute()
            
            return {
                "allowed": True,
                "remaining": limit - current_count - 1,
                "reset_time": (current_time // window + 1) * window
            }
            
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            # Fail open for availability
            return {"allowed": True, "remaining": limit, "reset_time": current_time + window}
    
    async def _memory_rate_limit(
        self, 
        key: str, 
        limit: int, 
        window: int, 
        current_time: int
    ) -> Dict[str, Any]:
        """Memory-based rate limiting fallback"""
        window_start = current_time // window * window
        
        if key not in self.memory_store:
            self.memory_store[key] = {"count": 0, "window_start": window_start}
        
        store = self.memory_store[key]
        
        # Reset if new window
        if store["window_start"] < window_start:
            store["count"] = 0
            store["window_start"] = window_start
        
        if store["count"] >= limit:
            return {
                "allowed": False,
                "remaining": 0,
                "reset_time": window_start + window
            }
        
        store["count"] += 1
        return {
            "allowed": True,
            "remaining": limit - store["count"],
            "reset_time": window_start + window
        }
    
    def get_client_key(self, request: Request) -> str:
        """Generate client key for rate limiting"""
        # Try to get real IP from headers (for proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        # Include user agent for better identification
        user_agent = request.headers.get("User-Agent", "")[:50]
        return f"{client_ip}:{hash(user_agent) % 10000}"

# Global rate limiter instance
rate_limiter = AdvancedRateLimiter()

# Rate limiting configurations for different endpoints
RATE_LIMITS = {
    "default": {"limit": 100, "window": 60},
    "auth": {"limit": 10, "window": 60, "burst": 20},
    "api": {"limit": 1000, "window": 60, "burst": 1200},
    "heavy": {"limit": 10, "window": 60},  # For heavy operations
    "search": {"limit": 200, "window": 60}
}

async def apply_rate_limit(request: Request, endpoint_type: str = "default"):
    """Apply rate limiting to request"""
    client_key = rate_limiter.get_client_key(request)
    config = RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])
    
    result = await rate_limiter.is_allowed(
        client_key,
        config["limit"],
        config["window"],
        config.get("burst")
    )
    
    if not result["allowed"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "reset_time": result["reset_time"],
                "reason": result.get("reason", "rate_limit_exceeded")
            },
            headers={
                "X-RateLimit-Limit": str(config["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(result["reset_time"])
            }
        )
    
    # Add rate limit headers
    request.state.rate_limit_headers = {
        "X-RateLimit-Limit": str(config["limit"]),
        "X-RateLimit-Remaining": str(result["remaining"]),
        "X-RateLimit-Reset": str(result["reset_time"])
    }
