import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import py_eureka_client.eureka_client as eureka_client
from typing import Dict
import os
from dotenv import load_dotenv


your_rest_server_port = 8000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
STATIC_DIR = "static"
BANNER_FILE = "banner.txt"


import logging
from contextlib import asynccontextmanager
import sys
import fastapi

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path=".env.production")
env=os.environ


def read_banner():
    with open('banner.txt', 'r') as f:
        return f.read()

def get_fastapi_version():
    return fastapi.__version__

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_app_info() -> Dict[str, str | int]:
    """Gather all application information in one place"""
    try:
        with open(BANNER_FILE, 'r') as f:
            banner = f.read()
    except FileNotFoundError:
        banner = "Banner file not found"
        logger.warning(f"{BANNER_FILE} not found")

    return {
        'banner': banner,
        'fastapi_version': fastapi.__version__,
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'host': env.get("HOST_IP", DEFAULT_HOST),
        'port': int(env.get("PORT", DEFAULT_PORT))
    }
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    host = env.get("HOST_IP", DEFAULT_HOST)
    # Startup logic
    banner = read_banner()
    fastapi_version = get_fastapi_version()
    python_version = get_python_version()
    port = 8000  # Default port, you can change this or make it configurable
    await eureka_client.init_async(
            eureka_server="http://5.189.146.192:8761/eureka/",
            app_name="product-service",
            instance_port=8000,
            instance_host=host
    )
    info = f"""
    {banner}
    Framework: FastAPI {fastapi_version}
    Python: {python_version}
    Running on: http://{host}:{port}
    """
    logger.info(info)

    # Your existing startup logic here (if any)
    # ...

    yield

    # Shutdown logic
    # Your existing shutdown logic here (if any)
    # ...