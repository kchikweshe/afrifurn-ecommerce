import logging
from pathlib import Path
import sys
from fastapi import FastAPI
import fastapi
from fastapi.concurrency import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import uvicorn

from config.eureka import lifespan
from middlewares.cors import apply_cors_middleware
from routers import api_router
from routers.level1_routes import router as level1_router  # Import level 1 router
from routers.level2_routes import router as level2_router  # Import level 2 router
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Function to read the banner from file
def read_banner():
    with open('banner.txt', 'r') as f:
        return f.read()

# Function to get the FastAPI version
def get_fastapi_version():
    return fastapi.__version__

# Function to get the Python version
def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

# App configuration
def create_app():
    app = FastAPI(lifespan=lifespan)
    
    # Configure CORS
    origins = [
        "http://localhost:8004",
        "http://localhost:8090"
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    image_dir = Path(__file__).parent / "product_images"
    app.mount("/static", StaticFiles(directory='static'), name="images")
    
    # Include routers
    app.include_router(api_router)
    
    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    app_info = {
        'banner': read_banner(),
        'fastapi_version': get_fastapi_version(),
        'python_version': get_python_version(),
        'port': 8000
    }
    
    logger.info(f"""
    {app_info['banner']}
    Framework: FastAPI {app_info['fastapi_version']}
    Python: {app_info['python_version']}
    Running on: http://localhost:{app_info['port']}
    """)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)