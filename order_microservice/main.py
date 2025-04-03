import asyncio
from re import I
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client import eureka_client
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from constants.urls import APP_NAME, EURKEKA_SERVER, HOST, KAFKA_INSTANCE, PORT
from db import create_db_and_tables
from routers.order_router import router as order_router
from services.kafka.kafka_consumer import start_kafka_consumers
# from services.kafka_consumer import start_kafka_consumers

# Global variables to manage Kafka resources
kafka_producer = None
kafka_consumer = None
consume_task = None

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    global kafka_producer, kafka_consumer, consume_task
    
    try:
        # Eureka initialization
        await eureka_client.init_async(
            eureka_server=EURKEKA_SERVER, 
            app_name=APP_NAME, 
            instance_port=PORT
        )
        
        # Initialize Kafka producer
      
        # Create database tables
        create_db_and_tables()
        
        await start_kafka_consumers()
        
        # # Create a task for consuming messages
        
        # # Explicitly yield the app to satisfy the context manager protocol
        yield
    
    except Exception as e:
        print(f"Startup error: {e}")
        raise  # Re-raise to ensure the error is propagated
    
    # finally:
    #     # Cleanup resources
    #     if consume_task:
    #         consume_task.cancel()
    #         try:
    #             await consume_task
    #         except asyncio.CancelledError:
    #             pass
        
        # Properly close Kafka producer
 

# Create FastAPI app with the new lifespan manager
app = FastAPI(lifespan=app_lifespan)

# Include routers
app.include_router(order_router)


if __name__ == "main":
    import uvicorn
    
    # Ensure event loop policy works correctly on Windows
    if sys.platform.lower() == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Use reload=True for development to enable auto-reload
    uvicorn.run("main:app",host=HOST, port=PORT, reload=True)