from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Get CORS origins from environment variable or use default
default_origins = [
    "http://localhost:3000",  # React default port
    "http://localhost:8000",  # FastAPI default port
    "http://localhost:8090",  # API Gateway
]
origins = os.getenv("CORS_ORIGINS", ",".join(default_origins)).split(",")
print("CORS origins configured:", origins)

def apply_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app