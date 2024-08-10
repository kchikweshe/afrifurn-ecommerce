from typing import List

from models.cart import CartItem
from models.products import Product
from services.generic import CartItemRepository, CartRepository



class CartService:
    def __init__(self, cart_repository: CartRepository, cart_item_repository: CartItemRepository):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository

    async def add_product_to_cart(self, 
                    cart_id: str,
                    product: Product, 
                    quantity: int):
        
        try:
             cart = await self.cart_repository.find_by_id(cart_id)

             
             if cart is None:
                 raise Exception("Cart not found")
             for item in cart.items:
                if item.product.name == product.name:
                    item.quantity += quantity
                    break
                else:
                    # Create a new CartItem and add it to the cart
                    cart_item = CartItem(product=product, quantity=quantity)
                    cart_item_saved=await self.cart_item_repository.create(cart_item)
                    cart.items.append(cart_item_saved)
            
            
        except Exception as e:
            print(e)
        # Business logic for adding product to cart
        # Use the repositories to manage Cart and CartItem entities

   



