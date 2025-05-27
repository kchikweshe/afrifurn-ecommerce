import asyncio
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from py_eureka_client import eureka_client


from order_microservice.constants.urls import HOST, PORT, EURKEKA_SERVER, APP_NAME
from order_microservice.config.db import DATABASE_URL, create_db_and_tables
from order_microservice.routers.order_router import router as order_router
from order_microservice.services.kafka.kafka_consumer import start_kafka_consumers

from order_microservice.auth.router import router as auth_router

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        # await start_kafka_consumers()
        # Eureka initialization
        await asyncio.to_thread(start_kafka_consumers)
        await eureka_client.init_async(
            eureka_server=EURKEKA_SERVER, 
            app_name=APP_NAME, 
            instance_port=PORT
        )
 
        yield
    except Exception as e:
        print(f"Startup error: {e}")
        raise e

def create_app() -> FastAPI:
    app = FastAPI(lifespan=app_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router)

    app.include_router(order_router)
    create_db_and_tables()

    # Add a simple root endpoint for health check


    return app

app = create_app()

if __name__ == "__main__":
    
    if sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    import uvicorn
    uvicorn.run("order_microservice.main:app", host=HOST, port=PORT, reload=True)
