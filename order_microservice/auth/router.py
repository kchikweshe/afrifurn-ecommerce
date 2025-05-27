# order_microservice/routers/auth_router.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from order_microservice.auth.jwt_handler import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from order_microservice.auth.crud import create_user, get_user_by_username
from order_microservice.auth.hash import verify_password
from order_microservice.auth.jwt_handler import create_access_token
from order_microservice.auth.models import UserCreate, UserRead
from order_microservice.config.db import get_session  # You need a get_session dependency

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_username(session, 
                                form_data.username)
    if not user or not verify_password(form_data.password, 
                                       user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_username(session, user_create.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(session, user_create)
    return user