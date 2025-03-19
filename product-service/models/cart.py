from typing import List, Optional
from pydantic import Field
from .common import CommonModel
from .products import Product, ProductVariant

class CartItem(CommonModel):
    product: Product
    variant_id: str
    quantity: int = Field(gt=0)
    unit_price: float
    total_price: float

    def calculate_total(self):
        if self.product.discount:
            discounted_price = self.unit_price * (1 - self.product.discount)
            self.total_price = discounted_price * self.quantity
        else:
            self.total_price = self.unit_price * self.quantity

class Cart(CommonModel):
    user_id: str
    items: List[CartItem] = []
    total_amount: float = 0

    def calculate_total(self):
        self.total_amount = sum(item.total_price for item in self.items)

    class Settings:
        name = "carts"
    