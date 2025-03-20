import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.eureka import get_app_info, lifespan
from constants.paths import STATIC_DIR
from routers import api_router
import database

#
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup information and environment variables"""
    try:
        # Database is automatically initialized when imported
        app_info = get_app_info()
        logger.info(f"""
        {app_info['banner']}
        Framework: FastAPI {app_info['fastapi_version']}
        Python: {app_info['python_version']}
        Running on: http://{app_info['host']}:{app_info['port']}
        """)
        
        # Log environment variables
        logger.info("Environment Variables in use:")
        for key, value in os.environ.items():
            # Mask sensitive information
            if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token']):
                logger.info(f"{key}: ********")
            else:
                logger.info(f"{key}: {value}")
                
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
