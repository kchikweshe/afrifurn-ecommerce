from typing import List

from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Relationship, SQLModel,Field
class OrderCreate(BaseModel):
    customer_name: Optional[str]
    customer_phone: Optional[str]
    customer_address: Optional[str]
    user_id:Optional[str]
    cart_id: str

class OrderInDB(OrderCreate):
    id: int
    price_total: float
    created_at: datetime
    user_id: int
class CartItem(BaseModel):
    product: dict
    variant_id: str
    quantity: int 
    unit_price: float
    total_price: float


class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    total_amount: float = 0

class Order(SQLModel, table=True):  # Changed to inherit from SQLModel and added table=True
    id: int = Field(default=None, primary_key=True)  # Changed to use Field for primary key
    customer_name: str|None = Field(index=True)
    customer_phone: str|None
    customer_address: str|None
    created_at: datetime = Field(default=datetime.now())
    user_id: str
    total_amount: float = Field(default=0.0) 

    def __repr__(self):
        return f"Order:\n" \
               f"Customer Name: {self.customer_name}\n" \
               f"Customer Phone: {self.customer_phone}\n" \
               f"Customer Address: {self.customer_address}\n" \
               f"Created At: {self.created_at}\n" \
               f"User ID: {self.user_id}\n" \
               f"Total Amount: {self.total_amount}\n"


   
from typing import List, Optional, Protocol

# Define an interface for user data fetching





class Invoice(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="order.id")
    invoice_number: str = Field(default_factory=lambda: f"INV-{datetime.now().strftime('%Y-%m-%d')}")
    date: datetime = Field(default_factory=datetime.now)
    expiry_date: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=30))
    
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    customer_phone: Optional[str] = None
    
    sales_rep: str = "KOMBORERAI CHIKWESHE"
    prepared_by: str = "KOMBORERAI CHIKWESHE"
    
    # items: list["CartItem"] = Relationship(back_populates="invoice")

    # def calculate_subtotal(self) -> float:
    #     return sum(item.quantity * item.unit_price for item in self.items)
    
    # def calculate_vat(self, vat_rate: float = 0.15) -> float:
    #     return self.calculate_subtotal() * vat_rate
    
    # def calculate_total(self, vat_rate: float = 0.15) -> float:
    #     return self.calculate_subtotal() * (1 + vat_rate)
# New InvoiceService class to handle invoice generation


# Kafka Consumer for handling order creation notifications


# Example implementations of the services

# ... existing code ...