import functools
import inspect
from typing import Callable, Type, Any
from pydantic import BaseModel
import logging

from .redis_provider import RedisCacheProvider  # adjust path
redis_app = RedisCacheProvider()

logger = logging.getLogger("redis_cache")
logger.setLevel(logging.INFO)

def cache_response(
    key: str,
    response_model: Type[BaseModel],
    ttl_seconds: int = 3600
):
    """
    Cache decorator with dynamic key support and logging.

    Args:
        key (str): Cache key, can include template placeholders like 'categories:{category_id}'
        response_model (Type[BaseModel]): Pydantic model for response validation
        ttl_seconds (int): Cache expiry time in seconds
    """
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Map args and kwargs to parameter names
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                arg_map = bound_args.arguments
                safe_args = {k: str(v) if v is not None else "" for k, v in arg_map.items()}

                # Format key with any matching parameters (e.g. category_id → categories:{category_id})
                final_key = key.format(**safe_args)


                # Try get from cache
                cached = await redis_app.get(final_key)
                if cached:
                    logger.info(f"[CACHE HIT] Key: {final_key}")
                    if isinstance(cached, list):
                        return [response_model.model_validate(item) for item in cached]
                    else:
                        return response_model.model_validate(cached)

                logger.info(f"[CACHE MISS] Key: {final_key}")
                result = await func(*args, **kwargs)

                def serialize(item):
                    if hasattr(item, "model_dump"):
                        d = item.model_dump(by_alias=True)
                    elif isinstance(item, dict):
                        d = item
                    else:
                        raise TypeError("Unsupported return type for caching")
                    
                    if "_id" in d and d["_id"] is not None:
                        d["_id"] = str(d["_id"])
                    return d


                if isinstance(result, list):
                    data_to_cache = [serialize(item) for item in result]
                else:
                    data_to_cache = serialize(result)

                await redis_app.set(final_key, data_to_cache, ttl_seconds)
                logger.info(f"[CACHE SET] Key: {final_key}")
                return result

            except Exception as e:
                logger.warning(f"[CACHE ERROR] Key: {key} - {e}")
                return await func(*args, **kwargs)

        return wrapper
    return decorator
