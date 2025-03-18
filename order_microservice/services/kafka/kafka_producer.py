# src/services/kafka_producer.py
import json
import logging

from kafka import KafkaProducer

from config.settings import Settings

class CustomKafkaProducer:
    """
    Asynchronous Kafka Producer for sending events across microservices
    """
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._producer = None
        return cls._instance

    async def get_producer(self):
        """
        Create or return existing Kafka producer
        """
        if not self._producer:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=Settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
            except Exception as e:
                logging.error(f"Failed to create Kafka producer: {e}")
                raise
        return self._producer

    async def send_message(self, topic: str, message: dict):
        """
        Send a message to a specific Kafka topic
        
        :param topic: Kafka topic name
        :param message: Message to be sent (will be JSON serialized)
        """
        try:
            producer = await self.get_producer()
            await producer.send(topic, message)
            logging.info(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            logging.error(f"Error sending message to Kafka: {e}")

    async def close(self):
        """
        Close the Kafka producer connection
        """
        if self._producer:
            self._producer.close()
            self._producer = None

# Singleton instance for easier importing
kafka_producer = KafkaProducer()