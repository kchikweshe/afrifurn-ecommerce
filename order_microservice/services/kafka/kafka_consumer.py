# src/services/kafka_consumer.py
import json
import logging
import asyncio
import six
import sys

from order_microservice.constants.urls import KAFKA_INSTANCE
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer,KafkaConsumer

producer = KafkaProducer(bootstrap_servers=KAFKA_INSTANCE, value_serializer=lambda v: v, key_serializer=lambda v: json.dumps(v))

from order_microservice.config.settings import KAFKA_BOOTSTRAP_SERVERS, TOPICS, Settings

class CustomKafkaConsumer:
    """
    Asynchronous Kafka Consumer for processing events across microservices
    """
    @staticmethod
    async def consume_orders(topic: str = TOPICS["ORDER_CREATED"]):
        """
        Consume and process order creation events
        """
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="order-service-group",
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
    
        
        try:
             for msg in consumer:
                try:
                    order_data = msg.value
                    logging.info(f"================Received Order for: =========:\n {order_data}")
                    # TODO: Implement order processing logic
                    # For example: validate order, save to database, trigger payment
                    
                except Exception as e:
                    logging.error(f"Error processing order: {e}")
        finally:
             consumer.close()

    @staticmethod
    async def consume_payments(topic: str = TOPICS["PAYMENT_PROCESSED"]):
        """
        Consume and process payment events
        """
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="payment-service-group",
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        
        try:
             for msg in consumer:
                try:
                    payment_data = msg.value
                    logging.info(f"Received Payment: {payment_data}")
                    # TODO: Implement payment processing logic
                    # For example: update order status, generate invoice
                except Exception as e:
                    logging.error(f"Error processing payment: {e}")
        finally:
             consumer.close()

async def start_kafka_consumers():
    """
    Start all Kafka consumer tasks
    """
    consumers = [
        CustomKafkaConsumer.consume_orders(),
        CustomKafkaConsumer.consume_payments()
    ]
    
    try:
        await asyncio.gather(*consumers)
    except Exception as e:
        logging.error(f"Error in Kafka consumers: {e}")