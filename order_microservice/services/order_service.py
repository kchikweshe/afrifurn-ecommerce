import logging
import asyncio

from kafka import KafkaProducer

from config.settings import Settings
from services.kafka.kafka_producer import CustomKafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from aiokafka import AIOKafkaProducer
from sqlmodel import Session
from db import get_session
from models.order import Cart, Invoice, Order, OrderCreate
from fastapi import BackgroundTasks, Depends

from services.cart_service import CartService
from services.email_service import EmailServiceImpl
from services.invoice_service import InvoiceService
from services.product_service import ProductServiceImpl
from services.user_service import UserService

class OrderService:
    def __init__(self,user_service:UserService,cart_service:CartService,bt:BackgroundTasks,session: Session=Depends(get_session)):
        
        self.session = session
        self.bt=bt
        # self.producer = producer
        self.user_service=user_service
        self.cart_service=cart_service
        self.invoice_service=InvoiceService(
            email_service=EmailServiceImpl(),
            product_service=ProductServiceImpl(),
            user_service=user_service
        )



    async def create_order(self, order: OrderCreate)->Order|None:
        # Logic to create an order in the database
        # After creating the order, send a message to Kafka

        user_service=self.user_service

        if order.user_id is None:
            return None

        cart=self.cart_service.fetch_cart_by_cart_id(cart_id=order.cart_id)
        
        if not isinstance(cart, Cart): return None
        db_order = Order(customer_address=order.customer_address, customer_name=order.customer_name, customer_phone=order.customer_phone, user_id=order.user_id)

        with self.session as session:
            session.add(db_order)
            session.commit()
            session.refresh(db_order)
            logger.info("Updated order: %s", db_order.__repr__)

        invoice = self.invoice_service.save(order=db_order, session=self.session)
        
        # Log before generating PDF
        logger.info("Starting PDF generation for invoice: %s", invoice.id)
        
        # Run PDF generation in the background
        self.bt.add_task(self.invoice_service.generate_pdf,invoice,cart)
         
        producer=CustomKafkaProducer()
        await producer.send_message(topic=Settings.TOPICS["ORDER_CREATED"],message={'message':f"============Order created for=================\n {db_order} "})
        # Log after starting the background task
        logger.info("PDF generation task started for invoice: %s", invoice.id)

        return db_order

    # def read_order(self, order_id: int):
    #     return self.db.query(Order).filter(Order.id == order_id).first()

    # def read_orders(self, skip: int = 0, limit: int = 100):
    #     return self.db.query(Order).offset(skip).limit(limit).all()

    # def update_order(self, order_id: int, order_data: dict):
    #     db_order = self.read_order(order_id)
    #     if db_order is None:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     for key, value in order_data.items():
    #         setattr(db_order, key, value)
    #     self.db.commit()
    #     self.db.refresh(db_order)
    #     return db_order

    # def delete_order(self, order_id: int):
    #     db_order = self.read_order(order_id)
    #     if db_order is None:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     self.db.delete(db_order)
    #     self.db.commit()
    #     return db_order 
    

    # def order_creation_consumer(self):
    #     consumer = KafkaConsumer(
    #     'order_creation_topic',
    #     bootstrap_servers='localhost:9092',
    #     value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    #     auto_offset_reset='earliest',
    #     enable_auto_commit=True
    # )
    
    #     for message in consumer:
    #         order_data = message.value
    #         user_id = order_data['user_id']
    #         total_amount = order_data['total_amount']
    #         items = order_data['items']
            
    #         # Fetch user info and send email notification
    #         user_service = UserServiceImpl()  # Assuming you have an implementation
    #         user_info = user_service.fetch_user_info(user_id)
            
    #         email_service = EmailServiceImpl()
    #         subject = "Order Confirmation"
    #         body = f"Dear {user_info['first_name']},\n\nYour order has been created successfully.\nTotal Amount: {total_amount}\nItems: {items}\n\nThank you!"
    #         email_service.send_email(user_info['email'], subject, body)