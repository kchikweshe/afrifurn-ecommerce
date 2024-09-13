from pydantic import BaseModel
from typing import List, Optional

from models.common import CommonModel
from models.products import Product
from services.product import create_document

class CartItem(CommonModel):
    product: Product
    quantity: int

class Cart(CommonModel):
    user_id: str
    items: List[CartItem] = []
    

    def clear(self):
        """Clear all items from the cart."""
        self.items.clear()

    
    def add_items_to_cart(self, product: Product,quantity:int):
        """Add items to the cart. If the item already exists, update its quantity."""
        for item in self.items:
            if item.product.name == product.name:
                item.quantity += quantity
                break
        else:
            cart_item=CartItem(product=product,quantity=quantity)
            data=create_document(
                collection_name="cart_item",
                document=cart_item
            )
            self.items.append(cart_item)

    def calculate_total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(item.product.price * item.quantity for item in self.items)

    def remove_items_from_cart(self, product_name: str) -> Optional[CartItem]:
        """Remove an item from the cart by product name."""
        for item in self.items:
            if item.product.name == product_name:
                self.items.remove(item)
                return item
        return None
    
    def size(self)->int:
        return len(self.items)
    def is_empty(self)->bool:
        return len(self.items)==0
    def pop_cart_items_by_ids(self, ids_to_pop):
        """
        Removes items from existing_list if their id matches any id in ids_to_pop.

        :param existing_list: List of dictionaries or objects containing 'id' keys or attributes.
        :param ids_to_pop: List of string IDs to be removed from the existing_list.
        :return: The updated existing list.
        """
       
        # Iterate over the list in reverse order to avoid index issues while removing items
        for i in range(len(self.items) - 1, -1, -1):
            item = self.items[i]
            # Assuming the item is a dictionary with an 'id' key
            if item.id in ids_to_pop:
                self.items.pop(i)

        return self.items
       