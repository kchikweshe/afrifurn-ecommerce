from fastapi import Depends
from database import db
from services.cart import CartService
from services.generic import CartRepository, CartItemRepository
async def get_cart_service() -> CartService:
    return CartService(cart_repository=CartRepository(), cart_item_repository=CartItemRepository()) 