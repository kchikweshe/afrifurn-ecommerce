import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Helper function to validate environment variables
def get_required_env(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

# Get MongoDB connection details from environment variables
try:
    MONGO_HOST = get_required_env("MONGO_HOST", "afrifurn-mongodb")
    MONGO_PORT = get_required_env("MONGO_PORT", "27017")
    MONGO_DB_NAME = get_required_env("MONGO_DB_NAME", "afrifurn")
    MONGO_USER = get_required_env("MONGO_USER", "afrifurn")
    MONGO_PASSWORD = get_required_env("MONGODB_PASSWORD")  # No default for password

    # Construct MongoDB URI without logging credentials
    MONGO_URI = f"mongodb://{MONGO_USER}:****@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    logging.info(f"Attempting to connect to MongoDB at {MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}")

    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}")
    db = client.get_database(MONGO_DB_NAME)
    # Test the connection
    client.server_info()
    logging.info("\033[92m====================== Successfully connected to MongoDB ======================\033[0m")
except ValueError as ve:
    logging.error(f"\033[91m====================== Configuration Error: {str(ve)} ======================\033[0m")
    raise
except Exception as e:
    logging.error(f"\033[91m====================== Error connecting to MongoDB ======================\033[0m")
    raise

