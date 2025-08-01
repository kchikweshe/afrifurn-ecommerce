from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    redis_url: str = "redis://localhost:6379"
    redis_key_prefix: str = "afrifurn"
    redis_ttl_seconds: int = 300  # 5 minutes default TTL
    
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "afrifurn"
    
    # Application Configuration
    app_name: str = "AfriFurn Product Service"
    debug: bool = False
    environment: str = "development"
    
    # API Configuration
    api_prefix: str = "/api/v1"
    cors_origins: list = ["*"]
    
    # Eureka Configuration
    eureka_server_url: str = "http://localhost:8761/eureka/"
    service_name: str = "product-service"
    service_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra='allow')

@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings instance"""
    return Settings()