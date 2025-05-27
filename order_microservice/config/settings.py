# # src/config/settings.py
import os
from dotenv import load_dotenv

from order_microservice.constants.urls import APP_NAME, EURKEKA_SERVER, HOST, KAFKA_INSTANCE, PORT, DATABASE_URL

# # Load environment variables
load_dotenv()

# class Settings:
#     """
#     Centralized configuration settings for the Order Management Service
#     """
#     # Service Configuration
#     SERVICE_NAME = os.getenv("SERVICE_NAME", APP_NAME)
#     SERVICE_HOST = os.getenv("SERVICE_HOST",HOST)
#     SERVICE_PORT = int(os.getenv("SERVICE_PORT", PORT))
#     DEBUG = os.getenv("DEBUG", "False").lower() == "true"

#     # Database Configuration
#     DB_HOST = os.getenv("DB_HOST", HOST)
#     DB_PORT = os.getenv("DB_PORT", "5432")
#     DB_USER = os.getenv("DB_USER", "fastapi_traefik")
#     DB_PASSWORD = os.getenv("DB_PASSWORD", "fastapi_traefik")
#     DB_NAME = os.getenv("DB_NAME", "afrifurn_order_service")
#     DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    

#     # Logging Configuration
#     LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

from dataclasses import dataclass
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):


    model_config = SettingsConfigDict(env_file=".env",extra='allow')
    
    # Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", 
        KAFKA_INSTANCE
    )
    
    # Kafka Topics
TOPICS = {
        "ORDER_CREATED": "order-created-topic",
        "PAYMENT_PROCESSED": "payment-processed-topic",
        "INVOICE_GENERATED": "invoice-generated-topic"
    }

    # Eureka Configuration
EUREKA_SERVER = os.getenv(
        "EUREKA_SERVER", 
        EURKEKA_SERVER
    )

@lru_cache()
def get_settings() -> Settings:
    """Create and cache settings instance"""
    return Settings()