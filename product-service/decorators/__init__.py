from .redis_provider import RedisCacheProvider
from .interface import ICacheProvider
from config.settings import get_settings

def create_redis_cache_provider() -> ICacheProvider:
    """Factory function to create a Redis cache provider with settings"""
    settings = get_settings()
    return RedisCacheProvider(
        redis_url=settings.redis_url,
        key_prefix=settings.redis_key_prefix
    )

__all__ = ['RedisCacheProvider', 'ICacheProvider', 'create_redis_cache_provider']
