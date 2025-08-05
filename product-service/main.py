import logging
import os
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import uvicorn.logging
from config.eureka import get_app_info, lifespan
from constants.paths import STATIC_DIR
from routers import api_router

from fastapi import Header, HTTPException

API_KEY = "your-super-secret-api-key"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")



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
# Configure logging
logging.basicConfig(level=logging.INFO,
                        force=True , # Override any existing configuration
                            
                     filename='app.log', 
                     filemode='a', 
                     format='%(asctime)s - %(levelname)s - %(message)s'
                     )
logger = logging.getLogger(__name__)
# Create a middleware class for logging
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request info
        request_id = f"{time.time()}"
        request_path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        
        logger.info(f"Request started - ID: {request_id} | Path: {request_path} | Client: {client_host}")
        
        # Record start time
        start_time = time.time()
        
        # Process the request and get the response
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response info
            logger.info(
                f"Request completed - ID: {request_id} | Status: {response.status_code} | "
                f"Duration: {process_time:.4f}s"
            )
            
            return response
        except Exception as e:
            # Log any exceptions that occur
            logger.error(f"Request failed - ID: {request_id} | Error: {str(e)}")
            raise
app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup information and environment variables"""
    try:
        # Database is automatically initialized when imported
        app_info = get_app_info()
        logging.info(f"""
        {app_info['banner']}
        Framework: FastAPI App{app_info['fastapi_version']}
        Python: {app_info['python_version']}
        Running on: http://{app_info['host']}:{app_info['port']}
        """)
        
        # Log environment variables
        logging.info("++++++++++++++++++Environment Variables in use:==\n")
      
        for key, value in os.environ.items():
            # Mask sensitive information
            if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token']):
                logging.info(f"{key}: ********")
            else:
                logging.info(f"{key}: {value}")
        
    except Exception as e:
        logging.error(f"Error during startup: {str(e)}")
        raise

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)