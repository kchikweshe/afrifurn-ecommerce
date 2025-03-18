from fastapi import FastAPI
from database import init_db
from routers import payment

app = FastAPI(title="Payments API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(payment.router) 