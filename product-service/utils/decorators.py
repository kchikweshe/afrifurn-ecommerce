"""
Decorators for logging and operation tracking.
"""
import asyncio
import logging
import time
import functools
from typing import Any, Callable
from datetime import datetime


def log_operation(operation_name: str):
    """
    Decorator to log operation execution.
    
    Args:
        operation_name: Name of the operation to log
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            start_time = time.time()
            
            try:
                logger.info(f"Starting operation: {operation_name}")
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"Completed operation: {operation_name} in {execution_time:.2f}s")
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Failed operation: {operation_name} in {execution_time:.2f}s - Error: {e}")
                raise
                
        return wrapper
    return decorator


def measure_performance(func: Callable) -> Callable:
    """
    Decorator to measure function performance.
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = _get_memory_usage()
        
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            end_memory = _get_memory_usage()
            memory_used = end_memory - start_memory
            
            logger = logging.getLogger(func.__module__)
            logger.info(
                f"Performance - {func.__name__}: "
                f"Time: {execution_time:.2f}s, "
                f"Memory: {memory_used:.2f}MB"
            )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger = logging.getLogger(func.__module__)
            logger.error(
                f"Performance - {func.__name__} failed: "
                f"Time: {execution_time:.2f}s, "
                f"Error: {e}"
            )
            raise
            
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure.
    
    Args:
        max_retries: Maximum number of retries
        delay: Delay between retries in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger = logging.getLogger(func.__module__)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger = logging.getLogger(func.__module__)
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {e}"
                        )
                        raise last_exception
                        
        return wrapper
    return decorator


def cache_result(ttl_seconds: int = 300):
    """
    Decorator to cache function results.
    
    Args:
        ttl_seconds: Time to live for cached results
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Import here to avoid circular imports
            
            cache_service = create_redis_cache_provider()
            
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            try:
                # Try to get from cache
                cached_result = await cache_service.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Cache the result
                await cache_service.set(cache_key, result, ttl_seconds)
                
                return result
                
            except Exception as e:
                logger = logging.getLogger(func.__module__)
                logger.error(f"Cache operation failed for {func.__name__}: {e}")
                # Fall back to executing function without caching
                return await func(*args, **kwargs)
                
        return wrapper
    return decorator


def validate_input(validator_func: Callable):
    """
    Decorator to validate input parameters.
    
    Args:
        validator_func: Function to validate input
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Validate input
            validation_errors = validator_func(*args, **kwargs)
            if validation_errors:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Validation errors: {', '.join(validation_errors)}"
                )
            
            return await func(*args, **kwargs)
            
        return wrapper
    return decorator


def rate_limit(max_calls: int = 100, time_window: int = 60):
    """
    Decorator to implement rate limiting.
    
    Args:
        max_calls: Maximum number of calls allowed
        time_window: Time window in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        call_history = []
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_time = time.time()
            
            # Remove old calls outside the time window
            call_history[:] = [call_time for call_time in call_history 
                             if current_time - call_time < time_window]
            
            # Check if rate limit exceeded
            if len(call_history) >= max_calls:
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {max_calls} calls per {time_window} seconds."
                )
            
            # Add current call
            call_history.append(current_time)
            
            return await func(*args, **kwargs)
            
        return wrapper
    return decorator


def _get_memory_usage() -> float:
    """
    Get current memory usage in MB.
    
    Returns:
        Memory usage in MB
    """
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    except ImportError:
        return 0.0


def _import_asyncio():
    """Import asyncio to avoid circular imports."""
    import asyncio
    return asyncio 