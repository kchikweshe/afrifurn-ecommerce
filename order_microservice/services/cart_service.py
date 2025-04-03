from typing import Protocol

import requests

from models.order import Cart


class CartService(Protocol):
    async def fetch_cart_by_user(self,user_id:str):
        pass
    def fetch_cart_by_cart_id(self,cart_id:str)->Cart|None:
        pass

class CartServiceImpl(CartService):
    
    # Update the fetch_cart_by_cart_id method
    def fetch_cart_by_cart_id(self, cart_id: str) -> Cart:
        response =  requests.get(f"http://localhost:8000/api/v1/cart/{cart_id}")
        data = response.json()
        print("Data:", data)
        # Assuming the response contains 'items' in the JSON
        return Cart(items=data.get('items', []),user_id=data.get('user_id'),total_amount=data.get('total_amount'))


