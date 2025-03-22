import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Histogram
from config.eureka import get_app_info, lifespan
from constants.paths import STATIC_DIR
from routers import api_router
import database
from fastapi.logger import logger as fastapi_logger

#

class StructuredLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        if extra is None:
            extra = {}
        extra['app_name'] = 'MyFastAPIApp'
        super()._log(level, json.dumps(msg) if isinstance(msg, dict) else msg, args, exc_info, extra, stack_info)


logging.setLoggerClass(StructuredLogger)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path=".env.development")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS",'').split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.include_router(api_router)
    
    return app

app = create_app()

# Define custom metrics
REQUEST_COUNT = Counter('request_count', 'Total request count')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

@app.middleware("http")
async def log_structured_requests(request: Request, call_next):
    logger.info({
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host
    })
    response = await call_next(request)
    logger.info({
        "event": "response",
        "status_code": response.status_code
    })
    return response
@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup information and environment variables"""
    try:
        # Database is automatically initialized when imported
        app_info = get_app_info()
        logging.info(f"""
        {app_info['banner']}
        Framework: FastAPI {app_info['fastapi_version']}
        Python: {app_info['python_version']}
        Running on: http://{app_info['host']}:{app_info['port']}
        """)
        
        # Log environment variables
        logging.info("Environment Variables in use:")
        for key, value in os.environ.items():
            # Mask sensitive information
            if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token']):
                logging.info(f"{key}: ********")
            else:
                logging.info(f"{key}: {value}")
                
    except Exception as e:
        logging.error(f"Error during startup: {str(e)}")
        raise

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
