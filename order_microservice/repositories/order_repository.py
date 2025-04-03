from sqlalchemy.orm import Session
from models.order import Order

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_order(self, order: Order):
        """Add a new order to the database."""
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int):
        """Retrieve an order by its ID."""
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_orders(self, skip: int = 0, limit: int = 100):
        """Retrieve a list of orders with pagination."""
        return self.db.query(Order).offset(skip).limit(limit).all()

    def update_order(self, order: Order):
        """Update an existing order in the database."""
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order: Order):
        """Delete an order from the database."""
        self.db.delete(order)
        self.db.commit() 