import os
import motor
from config import config


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URI"])

db = client.get_database(config['DB_NAME'])
