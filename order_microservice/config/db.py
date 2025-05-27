import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session
from order_microservice.config.settings import get_settings

def create_db_and_tables():
    try:
        engine = create_engine(DATABASE_URL,echo=True)

        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
        # Handle the error (e.g., log it or raise a custom exception)
def get_session():
    session=Session(engine)
    return session
   


SessionDep = Annotated[Session, Depends(get_session)]
try:
    settings = get_settings()
    host=settings.db_host # type: ignore
    password=settings.db_password # type: ignore
    port=settings.db_port # type: ignore
    user=settings.db_user # type: ignore
    db_name=settings.db_name # type: ignore
    

    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    engine = create_engine(DATABASE_URL,echo=True)
    create_db_and_tables()


    # Print connection details (consider removing in production)
    print(f"=================== DB_PASSWORD: {password} =====================")
    print(f"=================== DB_HOST: {host} =====================")
    print(f"=================== DB_PORT: {port} =====================")
    print(f"=================== DB_NAME: {db_name} =====================")
    print(f"=================== DB_USER: {user} =====================")

    # Construct MongoDB URI
    logging.info(f"=================== DATABASE_URL: {DATABASE_URL} =====================")

    
    logging.info("\033[92m====================== Successfully connected to PostgreSQL ======================\033[0m")
except ValueError as ve:
    logging.error(f"\033[91m====================== Configuration Error: {str(ve)} ======================\033[0m")
    raise
except Exception as e:
    logging.error(f"\033[91m====================== Error connecting to PostgreSQL ======================\033[0m")
    logging.error(f"\033[91m====================== {str(e)} ======================\033[0m")
    raise
