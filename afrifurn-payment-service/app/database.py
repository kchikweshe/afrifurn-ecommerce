import logging
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from config import settings



engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

def init_db():
    logging.info("=========================================Settings DB: ", settings.DATABASE_URL,"================================")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session 