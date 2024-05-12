import os
from dotenv import load_dotenv

load_dotenv()
config = os.environ


DB_USERNAME = config.get("MONGO_USERNAME", "afrifurn")
DB_PASSWORD = config.get("MONGO_PASSWORD", "mypassword")
DB_HOST = config.get("MONGO_DB_HOST", "127.0.0.1")
DB_PORT = config.get("MONGO_DB_PORT", 27017)
DB_NAME = config.get("MONGO_DB_NAME", "afrifurn")

MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin&retryWrites=true&w=majority"

config["DB_NAME"] = DB_NAME
config["MONGO_URI"] = MONGO_URI