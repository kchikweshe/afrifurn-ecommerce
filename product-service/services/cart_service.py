from typing import Optional, List

from bson import ObjectId
from fastapi import HTTPException
from models.cart import Cart, CartItem
from services.repository.product_repository import ProductRepository
from services.repository.cart_repository import CartItemRepository, CartRepository
from services.base_service import BaseService
from services.repository.product_variant_repository import ProductVariantRepository
class CartService(BaseService[Cart]):
    def __init__(self, 
                 repository: CartRepository, 
                 product_repository: ProductRepository,
                 product_variant_repository:ProductVariantRepository,
                 cart_item_repository: CartItemRepository):
        self.repository = repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository
        self.product_variant_repository=product_variant_repository

    async def get_user_cart(self, 
                        user_id: str) -> Optional[Cart]:
        return await self.repository.find_by_user_id(user_id)

    async def add_to_cart(self, 
                          user_id: str,
                          product_id: str,
                           variant_id:str,
                          quantity: int) -> bool|None:
        cart = await self.get_user_cart(user_id)
        product = await self.product_repository.find_one(filter_query={"_id": ObjectId(product_id)})
        product_variant = await self.product_variant_repository.find_one(filter_query={"_id":ObjectId(variant_id) })

        is_updated:bool=False
        if not product or product_variant is None :
            return None

        if not cart:
            cart = Cart(user_id=user_id, items=[], total_amount=0)
            cart = await self.repository.insert_one(cart)
        
        cart_item = CartItem(
            product=product,
            variant_id=str(product_variant.id),
            quantity=quantity,
            unit_price=product.price,
            total_price=product.price * quantity
        )
        cart_item.calculate_total()
        if isinstance(cart,Cart):
            cart.items.append(cart_item)

            cart.calculate_total()
            is_updated= await self.repository.update_cart_items(str(cart.id), cart)
        return is_updated

    async def remove_from_cart(self, cart_id: str, item_ids: List[str]) -> bool:
        cart = await self.get_one(cart_id)
        if not cart:
            return False
        
        cart.items = [item for item in cart.items if item.id not in item_ids]
        return await self.update(cart_id, cart.model_dump())
    
    async def clear_cart(self, cart_id: str) -> bool:
        cart = await self.get_one(cart_id)
        if not cart:
            return False
        cart.items = []
        return await self.update(cart_id, cart.model_dump())

    async def update_item_quantity(
            self, 
            cart_id: str, 
            item_id: str, 
            quantity: int
        ) -> bool:
            cart = await self.get_one(cart_id)
            if not cart:
                raise HTTPException(status_code=404, detail="Cart not found")

            item = next((item for item in cart.items if str(item.id) == item_id), None)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found in cart")


            item.quantity = quantity
            item.calculate_total()
            cart.calculate_total()

            result = await self.repository.update_cart_items(cart_id, cart)
             
            return result 

    async def get_cart_item(self, cart_id: str, product_id: str, variant_id: Optional[str] = None):
        cart = await self.get_one(cart_id)  # Assuming you have a method to get the cart by ID
        if cart:
            for item in cart.items:
                if item.product.id == product_id and (item.variant_id == variant_id or variant_id is None):
                    return item  # Return the existing cart item
        return None  # Return None if the item is not found
