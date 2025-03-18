# Code above omitted 👆

from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from constants.urls import DATABASE_URL

# Update the connection string to match the one in docker-compose.yml

engine = create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
        # Handle the error (e.g., log it or raise a custom exception)
def get_session():
    session=Session(engine)
    return session
   


SessionDep = Annotated[Session, Depends(get_session)]