from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import py_eureka_client.eureka_client as eureka_client

your_rest_server_port = 8000


import logging
from contextlib import asynccontextmanager
import sys
import fastapi

logger = logging.getLogger(__name__)

def read_banner():
    with open('banner.txt', 'r') as f:
        return f.read()

def get_fastapi_version():
    return fastapi.__version__

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Startup logic
    banner = read_banner()
    fastapi_version = get_fastapi_version()
    python_version = get_python_version()
    port = 8000  # Default port, you can change this or make it configurable
    await eureka_client.init_async(
            eureka_server="http://localhost:8761/eureka/",
            app_name="product-service",
            instance_port=8000,
            instance_host="localhost"
    )
    info = f"""
    {banner}
    Framework: FastAPI {fastapi_version}
    Python: {python_version}
    Running on: http://localhost:{port}
    """
    logger.info(info)

    # Your existing startup logic here (if any)
    # ...

    yield

    # Shutdown logic
    # Your existing shutdown logic here (if any)
    # ...