from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):


    model_config = SettingsConfigDict(env_file=".env.production",extra='allow')
@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings instance"""
    return Settings()