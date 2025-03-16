import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.production",override=True)

# Helper function to validate environment variables
def get_required_env(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if not value:
        raise ValueError(f"Missing  required environment variable: {key}")
    return value

# Get MongoDB connection details from environment variables
try:
    MONGO_HOST = get_required_env("MONGO_HOST", "localhost")
    MONGO_PORT = get_required_env("MONGO_PORT", "27017")
    MONGO_DB_NAME = get_required_env("MONGO_DB_NAME", "afrifurn")
    MONGO_USER = get_required_env("MONGO_USER", "afrifurn")
    MONGO_PASSWORD = get_required_env("MONGODB_PASSWORD", "mypassword")  # No default for password
    print(f"=================== MONGO_PASSWORD: {MONGO_PASSWORD} =====================")
    print(f"=================== MONGO_HOST: {MONGO_HOST} =====================")
    print(f"=================== MONGO_PORT: {MONGO_PORT} =====================")
    print(f"=================== MONGO_DB_NAME: {MONGO_DB_NAME} =====================")
    print(f"=================== MONGO_USER: {MONGO_USER} =====================")
    # Construct MongoDB URI without logging credentials
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    logging.info(f"=================== MONGO_URI: {MONGO_URI} =====================")

    client = MongoClient(MONGO_URI)
    db = client.get_database(MONGO_DB_NAME)
    # Test the connection
    client.server_info()
    logging.info("\033[92m====================== Successfully connected to MongoDB ======================\033[0m")
except ValueError as ve:
    logging.error(f"\033[91m====================== Configuration Error: {str(ve)} ======================\033[0m")
    raise
except Exception as e:
    logging.error(f"\033[91m====================== Error connecting to MongoDB ======================\033[0m")
    logging.error(f"\033[91m====================== {str(e)} ======================\033[0m")
    raise

