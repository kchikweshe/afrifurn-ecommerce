# Redis Setup for Production

This document explains how to configure and use Redis caching in the AfriFurn product service for production deployment.

## Configuration

### Environment Variables

The following environment variables are used to configure Redis:

- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_PASSWORD`: Redis authentication password
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_URL`: Complete Redis connection URL
- `REDIS_KEY_PREFIX`: Prefix for all cache keys (default: afrifurn)
- `REDIS_TTL_SECONDS`: Default TTL for cached items in seconds (default: 300)

### Docker Production Setup

The `docker-compose.yml` file includes a Redis service:

```yaml
afrifurn-redis:
  container_name: afrifurn-redis
  image: redis:7-alpine
  command: redis-server --appendonly yes --requirepass afrifurn_redis_password
  environment:
    - REDIS_PASSWORD=afrifurn_redis_password
  networks:
    - afrifurn-network
  ports:
    - 6379:6379
  volumes:
    - redis_data_container:/data
  restart: unless-stopped
```

## Usage

### Creating a Cache Provider

```python
from decorators import create_redis_cache_provider

# Create cache provider with settings
cache_provider = create_redis_cache_provider()

# Or create with custom configuration
from decorators import RedisCacheProvider
cache_provider = RedisCacheProvider(
    redis_url="redis://:password@host:6379/0",
    key_prefix="custom_prefix"
)
```

### Basic Operations

```python
# Set a value with default TTL
await cache_provider.set("user:123", {"name": "John", "email": "john@example.com"})

# Set a value with custom TTL
await cache_provider.set("user:123", user_data, ttl_seconds=600)

# Get a value
user_data = await cache_provider.get("user:123")

# Check if key exists
exists = await cache_provider.exists("user:123")

# Delete a key
await cache_provider.delete("user:123")

# Clear all keys with prefix
await cache_provider.clear()

# Close connection
await cache_provider.close()
```

### Cache Decorator Usage

```python
from decorators import cache

@cache(ttl_seconds=300)
async def get_product_by_id(product_id: str):
    # This function result will be cached for 5 minutes
    return await product_service.get_product(product_id)
```

## Production Considerations

1. **Security**: Always use strong passwords for Redis in production
2. **Persistence**: Redis is configured with AOF (Append Only File) for data persistence
3. **Networking**: Redis is accessible only within the Docker network
4. **Monitoring**: Consider adding Redis monitoring tools like Redis Commander
5. **Backup**: Regular backups of Redis data are recommended
6. **Memory**: Monitor Redis memory usage and configure maxmemory policies

## Environment Files

Copy `env.production.example` to `.env.production` and modify the values as needed:

```bash
cp env.production.example .env.production
```

## Deployment

To deploy with Redis:

```bash
# Start all services including Redis
docker-compose up -d

# Check Redis status
docker-compose logs afrifurn-redis

# Connect to Redis CLI
docker-compose exec afrifurn-redis redis-cli -a afrifurn_redis_password
```

## Troubleshooting

1. **Connection Issues**: Check if Redis container is running
2. **Authentication Errors**: Verify Redis password in environment variables
3. **Network Issues**: Ensure services are on the same Docker network
4. **Memory Issues**: Monitor Redis memory usage and adjust maxmemory settings 