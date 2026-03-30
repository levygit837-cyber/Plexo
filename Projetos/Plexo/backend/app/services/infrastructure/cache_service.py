"""Cache service for managing Redis connections and caching operations."""

from typing import Any, Optional
from redis.asyncio import Redis, ConnectionPool
from app.config.settings import get_settings
from app.core.logging.logger import get_logger
import json

logger = get_logger(__name__)


class CacheService:
    """Service for managing cache operations with Redis."""

    def __init__(self):
        """Initialize cache service."""
        self.settings = get_settings()
        self.redis: Optional[Redis] = None
        self.pool: Optional[ConnectionPool] = None

    async def initialize(self) -> None:
        """Initialize Redis connection pool."""
        try:
            self.pool = ConnectionPool.from_url(
                self.settings.REDIS_URL,
                decode_responses=True,
                max_connections=10,
            )
            self.redis = Redis(connection_pool=self.pool)
            await self.redis.ping()
            logger.info("Cache service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize cache service: {e}")
            raise

    async def close(self) -> None:
        """Close Redis connections."""
        if self.redis:
            await self.redis.close()
        if self.pool:
            await self.pool.disconnect()
        logger.info("Cache connections closed")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to get cache key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        try:
            serialized = json.dumps(value)
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            return True
        except Exception as e:
            logger.error(f"Failed to set cache key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check cache key {key}: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern.
        
        Args:
            pattern: Key pattern (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        try:
            keys = []
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Failed to clear cache pattern {pattern}: {e}")
            return 0

    async def health_check(self) -> bool:
        """Check cache health.
        
        Returns:
            True if cache is healthy
        """
        try:
            await self.redis.ping()
            return True
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return False


# Global cache service instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get global cache service instance.
    
    Returns:
        CacheService: Cache service instance
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service