import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import py_eureka_client.eureka_client as eureka_client
from typing import Dict
import os
from decorators.redis_provider import RedisCacheProvider
from config.settings import get_settings
your_rest_server_port = 8000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
STATIC_DIR = "static"
BANNER_FILE = "banner.txt"

settings=get_settings()

import logging
import warnings
import sys
import fastapi

logging.getLogger("py_eureka_client").setLevel(logging.CRITICAL)
logging.getLogger("py_eureka_client.eureka_client").setLevel(logging.CRITICAL)
logging.getLogger("py_eureka_client.http_client").setLevel(logging.CRITICAL)
logging.getLogger("py_eureka_client.eureka_basic").setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")

# Optionally, suppress all uncaught exception tracebacks
# def suppress_traceback(exctype, value, traceback):
#     print(f"Suppressed exception: {value}")
# sys.excepthook = suppress_traceback

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

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
        logging.warning(f"{BANNER_FILE} not found")

    return {
        'banner': banner,
        'fastapi_version': fastapi.__version__,
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'host':settings.host_ip, # type: ignore
        'port': int(settings.port) # type: ignore
    }

def log_eureka_status(status: str, url: str, reason: str = ""):
    color = Colors.GREEN if status == "UP" else Colors.RED
    status_colored = f"{color}{status}{Colors.RESET}"
    print("\nEureka Info {")
    print(f"  Status: {status_colored}")
    print(f"  URL: {url}")
    if reason:
        print(f"  Reason: {reason}")
    print("}\n")

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    redis_app=RedisCacheProvider()

    host = settings.host_ip # type: ignore
    banner = read_banner()
    fastapi_version = get_fastapi_version()
    python_version = get_python_version()
    port = 8000
    eureka_url = settings.eureka_client_service_url # type: ignore
    await redis_app.set(key="categories",value=None)
    await redis_app.set(key="level1_categories",value=None)
    await redis_app.set(key="level2_categories",value=None)
    await redis_app.set(key="level1-categories-by-category",value=None)
    await redis_app.set(key="level2-categories-by-level1",value=None) 
    await redis_app.set(key="materials",value=None)
    await redis_app.set(key="material",value=None)
    await redis_app.set(key="colors",value=None)
    await redis_app.set(key="currencies",value=None)
    await redis_app.set(key="products",value=None)
    await redis_app.set(key="level-one-products",value=None)
    await redis_app.set(key="level-two-products",value=None)
    await redis_app.set(key="filtered-product",value=None)
    await redis_app.set(key="category-product",value=None)
    try:
        await eureka_client.init_async(
            eureka_server=eureka_url, # type: ignore
            app_name="product-service",
            instance_port=int(settings.server_port), # type: ignore
            instance_host=host
        )
        log_eureka_status("UP", eureka_url)
    except Exception as e:
        reason = str(e)
        log_eureka_status("DOWN", eureka_url, reason=reason)

    info = f"""
    {banner}
    Framework: FastAPI {fastapi_version}
    Python: {python_version}
    Running on: http://{host}:{port}
    """
    logging.info(info)
    yield