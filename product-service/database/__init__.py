import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from config.settings import get_settings
# Connect to MongoDB using settings from get_settings function
try:
    settings = get_settings()
    mongo_host=settings.mongo_host # type: ignore
    mongo_password=settings.mongodb_password # type: ignore
    mongo_port=settings.mongo_port # type: ignore
    mongo_user=settings.mongo_user # type: ignore
    mongo_db_name=settings.mongo_db_name # type: ignore
    



    # Print connection details (consider removing in production)
    print(f"=================== MONGO_PASSWORD: {mongo_password} =====================")
    print(f"=================== MONGO_HOST: {mongo_host} =====================")
    print(f"=================== MONGO_PORT: {mongo_port} =====================")
    print(f"=================== MONGO_DB_NAME: {mongo_db_name} =====================")
    print(f"=================== MONGO_USER: {mongo_user} =====================")

    # Construct MongoDB URI
    MONGO_URI = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db_name}"
    logging.info(f"=================== MONGO_URI: {MONGO_URI} =====================")

    client = MongoClient(MONGO_URI)
    db = client.get_database(mongo_db_name)
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

