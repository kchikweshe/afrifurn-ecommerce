import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB connection details from environment variables
MONGO_HOST = os.getenv("MONGO_HOST", "afrifurn-mongodb")  # Default to Docker service name
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "afrifurn")
MONGO_USER = os.getenv("MONGO_USER", "afrifurn")
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD", "")

# Construct MongoDB URI
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"

try:
    client = MongoClient(MONGO_URI)
    db = client.get_database(MONGO_DB_NAME)
    # Test the connection
    client.server_info()
    logging.info("====================== Successfully connected to MongoDB ======================")
except Exception as e:
    logging.error(f"====================== Error connecting to MongoDB: \n {e} ======================")
    raise

