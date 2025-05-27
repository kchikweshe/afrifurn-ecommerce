# order_microservice/auth/models.py
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str