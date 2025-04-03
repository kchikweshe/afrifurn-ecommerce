from dataclasses import dataclass
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    APP_NAME: str = "Payment API"
    DEBUG: bool = False
    DATABASE_URL: str
    PAYNOW_INTEGRATION_ID: str
    PAYNOW_INTEGRATION_KEY: str
    APP_URL: str
    PAYNOW_RETURN_URL: str
    PAYNOW_RESULT_URL: str

    class Config:
        env_file = ".env"

settings = Settings() 