import os
from dotenv import load_dotenv

load_dotenv()
config = os.environ

DB_USERNAME = config.get("MONGO_USERNAME")
DB_PASSWORD = config.get("MONGO_PASSWORD")
DB_HOST = config.get("MONGO_DB_HOST","localhost")
DB_PORT = config.get("MONGO_DB_PORT","27017")
DB_NAME = config.get("MONGO_DB_NAME","product_images")

MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin&retryWrites=true&w=majority"

