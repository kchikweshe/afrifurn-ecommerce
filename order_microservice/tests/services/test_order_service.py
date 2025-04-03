# test_order_service.py
from unittest.mock import Mock
from kafka import KafkaProducer
import pytest
from fastapi import HTTPException
from services.order_service import OrderService
from models.order import Order, UserService
from sqlalchemy.orm import Session

# Mock dependencies
class MockUserService:
    async def fetch_user_info(self, user_id):
        if user_id == 1:
            return 1  # Valid user ID
        return None  # Invalid user ID

@pytest.fixture
def order_service(monkeypatch):
    # Mock the database session
    class MockDBSession:
        def add(self, order):
            pass  # Mock add method

        def commit(self):
            pass  # Mock commit method

        def refresh(self, order):
            pass  # Mock refresh method

        def query(self, model):
            return self

        def filter(self, condition):
            return self

        def first(self):
            return None  # Simulate order not found

        def offset(self, skip):
            return self

        def limit(self, limit):
            return self

        def all(self):
            return []  # Simulate no orders

        def delete(self, order):
            pass  # Mock delete method

    db = Mock(spec=Session)
    producer = Mock(spec=KafkaProducer)  # Mock KafkaProducer if needed
    user_service = Mock(spec=UserService)
    return OrderService(session=db, producer=producer, user_service=user_service)
@pytest.mark.asyncio
def test_create_order_invalid_user_id(monkeypatch):
    order = Order(user_id=2, total_amount=100, items=[])
    result = order_service.create_order(order)
    assert result == "Not user Id"  # Check for invalid user ID response

 