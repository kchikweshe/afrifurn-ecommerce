# order_microservice/auth/crud.py
from sqlmodel import Session, select
from order_microservice.auth.models import User, UserCreate
from order_microservice.auth.hash import hash_password, verify_password

def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user_create: UserCreate):
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hash_password(user_create.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user