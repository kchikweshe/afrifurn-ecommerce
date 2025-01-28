import os
import motor
import motor.motor_asyncio
from config import config


client = motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_URI"]) 
db = client.get_database(config['DB_NAME'])

