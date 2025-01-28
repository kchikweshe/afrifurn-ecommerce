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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

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

@app.on_event("startup")
async def startup_event():
    banner = read_banner()
    fastapi_version = get_fastapi_version()
    python_version = get_python_version()
    port = 8000  # Default port, you can change this or make it configurable

    info = f"""
    {banner}
    Framework: FastAPI {fastapi_version}
    Python: {python_version}
    Running on: http://localhost:{port}
        """
    logger.info(info)

origins = [
    "http://localhost:8004",
    "http://localhost:8090"
]

image_dir = Path(__file__).parent / "product_images"

directory = StaticFiles(directory='static')
app.mount("/static", directory, name="images")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run("main:app")