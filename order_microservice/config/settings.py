# src/config/settings.py
import os
from dotenv import load_dotenv

from constants.urls import APP_NAME, EURKEKA_SERVER, HOST, KAFKA_INSTANCE, PORT

# Load environment variables
load_dotenv()

class Settings:
    """
    Centralized configuration settings for the Order Management Service
    """
    # Service Configuration
    SERVICE_NAME = os.getenv("SERVICE_NAME", APP_NAME)
    SERVICE_HOST = os.getenv("SERVICE_HOST",HOST)
    SERVICE_PORT = int(os.getenv("SERVICE_PORT", PORT))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

 

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

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")