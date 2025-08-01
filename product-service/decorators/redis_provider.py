
import json, logging as logger

from typing import Any, Optional

import redis.asyncio as redis
from .interface import ICacheProvider
from config.settings import get_settings

# Configure logging
logger.basicConfig(level=logger.INFO)


class RedisCacheProvider(ICacheProvider):
    """Redis implementation of cache provider"""
    
    def __init__(self, redis_url: Optional[str] = None, key_prefix: Optional[str] = None):
        settings = get_settings()
        self.redis_url = redis_url or settings.redis_url
        self.key_prefix = key_prefix or settings.redis_key_prefix
        self._redis: Optional[redis.Redis] = None
    
    async def _get_redis(self) -> redis.Redis:
        """Lazy initialization of Redis connection"""
        if self._redis is None:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis
    
    def _make_key(self, key: str) -> str:
        """Create prefixed cache key"""
        return f"{self.key_prefix}:{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        try:
            redis_client = await self._get_redis()
            data = await redis_client.get(self._make_key(key))
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        try:
            settings = get_settings()
            ttl = ttl_seconds or settings.redis_ttl_seconds
            redis_client = await self._get_redis()
            serialized_value = json.dumps(value, default=str)
            await redis_client.setex(self._make_key(key), ttl, serialized_value)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
    
    async def delete(self, key: str) -> None:
        try:
            redis_client = await self._get_redis()
            await redis_client.delete(self._make_key(key))
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
    
    async def clear(self) -> None:
        try:
            redis_client = await self._get_redis()
            keys = await redis_client.keys(f"{self.key_prefix}:*")
            if keys:
                await redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    async def exists(self, key: str) -> bool:
        try:
            redis_client = await self._get_redis()
            return bool(await redis_client.exists(self._make_key(key)))
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def close(self) -> None:
        """Close Redis connection"""
        if self._redis:
            await self._redis.close()