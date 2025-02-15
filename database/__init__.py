
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME


client = MongoClient(MONGO_URI) 
db = client.get_database(DB_NAME)

