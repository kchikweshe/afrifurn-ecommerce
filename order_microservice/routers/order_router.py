from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, logger
from sqlmodel import Session
from constants.urls import KAFKA_INSTANCE
from db import get_session
from models.order import Order, OrderCreate
from services.cart_service import CartService, CartServiceImpl
from services.order_service import OrderService
from typing import Any, Optional

from services.user_service import UserService, UserServiceImpl

router = APIRouter(prefix="/api/v1", tags=["Orders"])

def get_background_task_instance():
    return    BackgroundTasks()
def get_user_service():
    return UserServiceImpl()
def get_cart_service():
    return CartServiceImpl()

def get_order_service():
    return OrderService(
        user_service=get_user_service(),
        cart_service=get_cart_service(),
        session=get_session(),
        bt=get_background_task_instance()

    )

# def get_kafka_producer():
#     return AIOKafkaProducer(bootstrap_servers=KAFKA_INSTANCE)
@router.post("/orders/", response_model=Any)
async def create_order(
       customer_name: str,
    customer_phone: str,
    customer_address: str,
    user_id:str,
    cart_id: str,
    order_service:OrderService=Depends(get_order_service)

  
):
    try:
        # order_service = OrderService(session=db,
        #                              user_service=user_service,
        #                              cart_service=cart_service)
        order_data: OrderCreate=OrderCreate(
            cart_id=cart_id,
            customer_address=customer_address,
            customer_phone=customer_phone,
            customer_name=customer_name,
            user_id=user_id
        )  # Use a Pydantic model for order data
        await order_service.create_order(order=order_data)  # Pass the entire order data model
        return "Done"
    except Exception as e:
        # Handle exceptions appropriately
        logger.logger.error("Error saving file:\n",e)
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/orders/{order_id}", response_model=OrderInDB)
# async def read_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     order_service = OrderService(db)
#     db_order = order_service.read_order(order_id)
#     if db_order is None:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return db_order

# @router.get("/orders/", response_model=List[OrderInDB])
# async def read_orders(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     order_service = OrderService(db)
#     return order_service.read_orders(skip, limit)

# @router.put("/orders/{order_id}", response_model=OrderInDB)
# async def update_order(order_id: int, order: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     order_service = OrderService(db)
#     return order_service.update_order(order_id, order.dict(exclude_unset=True))

# @router.delete("/orders/{order_id}", response_model=OrderInDB)
# async def delete_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     order_service = OrderService(db)
#     return order_service.delete_order(order_id) 