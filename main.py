import logging
from pathlib import Path
import sys
from typing import Dict
import os
from dotenv import load_dotenv

from fastapi import FastAPI
import fastapi
from fastapi.staticfiles import StaticFiles
import uvicorn

from config.eureka import get_app_info, lifespan
from constants.paths import STATIC_DIR
from middlewares.cors import apply_cors_middleware
from routers import api_router

#
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(lifespan=lifespan)
    apply_cors_middleware(app)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.include_router(api_router)
    return app

app = create_app()

@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup information"""
    app_info = get_app_info()
    logger.info(f"""
    {app_info['banner']}
    Framework: FastAPI {app_info['fastapi_version']}
    Python: {app_info['python_version']}
    Running on: http://{app_info['host']}:{app_info['port']}
    """)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(get_app_info()['host']),
        port=int(get_app_info()['port']),
        
    )
    