from typing import Optional, List
import logging
from bson import ObjectId
from fastapi import HTTPException
from models.cart import Cart, CartItem
from services.repository.base_repository import BaseRepository
from services.repository.product_repository import ProductRepository
from services.repository.product_variant_repository import ProductVariantRepository

class CartRepository(BaseRepository[Cart]):
    def __init__(self):
        super().__init__(model_class=Cart, collection_name="cart")
        self.product_repository = ProductRepository()
        self.product_variant_repository = ProductVariantRepository()
        self.logger = logging.getLogger(__name__)

    async def find_by_user_id(self, user_id: str) -> Optional[Cart]:
        """Find cart by user ID"""
        try:
            doc = await self.db[self.collection_name].find_one({
                "user_id": user_id,
                "is_archived": False
            })
            return Cart(**doc) if doc else None
        except Exception as e:
            self.logger.error(f"Failed to find cart by user ID: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to find cart"
            )

    async def update_cart_items(self, cart_id: str, cart: Cart) -> bool:
        """Update cart items and total amount"""
        try:
            update_data = {
                "items": [item.model_dump() for item in cart.items],
                "total_amount": cart.total_amount
            }
            result = await self.db[self.collection_name].update_one(
                {"_id": ObjectId(cart_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            self.logger.error(f"Failed to update cart items: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update cart"
            )

    async def add_to_cart(
        self,
        user_id: str,
        product_id: str,
        variant_id: str,
        quantity: int
    ) -> bool:
        """Add item to cart"""
        try:
            cart = await self.find_by_user_id(user_id)
            product = await self.product_repository.find_one({"_id": ObjectId(product_id)})
            product_variant = await self.product_variant_repository.find_one({"_id": ObjectId(variant_id)})

            if not product or not product_variant:
                return None

            if not cart:
                cart = Cart(user_id=user_id, items=[], total_amount=0)
                cart = await self.insert_one(cart.model_dump())

            cart_item = CartItem(
                product=product,
                variant_id=str(product_variant.id),
                quantity=quantity,
                unit_price=product.price,
                total_price=product.price * quantity
            )
            cart_item.calculate_total()
            
            if isinstance(cart, Cart):
                cart.items.append(cart_item)
                cart.calculate_total()
                return await self.update_cart_items(str(cart.id), cart)
                
            return False
        except Exception as e:
            self.logger.error(f"Failed to add item to cart: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to add item to cart"
            )

    async def remove_from_cart(self, cart_id: str, item_ids: List[str]) -> bool:
        """Remove items from cart"""
        try:
            cart = await self.get_by_id(cart_id)
            if not cart:
                return False
            
            cart_obj = Cart(**cart)
            cart_obj.items = [item for item in cart_obj.items if item.id not in item_ids]
            cart_obj.calculate_total()
            
            return await self.update(cart_id, cart_obj.model_dump())
        except Exception as e:
            self.logger.error(f"Failed to remove items from cart: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to remove items from cart"
            )

    async def clear_cart(self, cart_id: str) -> bool:
        """Clear all items from cart"""
        try:
            cart = await self.get_by_id(cart_id)
            if not cart:
                return False
            
            cart_obj = Cart(**cart)
            cart_obj.items = []
            cart_obj.total_amount = 0
            
            return await self.update(cart_id, cart_obj.model_dump())
        except Exception as e:
            self.logger.error(f"Failed to clear cart: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to clear cart"
            )

    async def update_item_quantity(self, cart_id: str, item_id: str, quantity: int) -> bool:
        """Update quantity of an item in cart"""
        try:
            cart = await self.get_by_id(cart_id)
            if not cart:
                raise HTTPException(status_code=404, detail="Cart not found")

            cart_obj = Cart(**cart)
            item = next((item for item in cart_obj.items if str(item.id) == item_id), None)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found in cart")

            item.quantity = quantity
            item.calculate_total()
            cart_obj.calculate_total()

            return await self.update_cart_items(cart_id, cart_obj)
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update item quantity: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update item quantity"
            )

    async def get_cart_item(self, cart_id: str, product_id: str, variant_id: Optional[str] = None) -> Optional[CartItem]:
        """Get specific item from cart"""
        try:
            cart = await self.get_by_id(cart_id)
            if not cart:
                return None
            
            cart_obj = Cart(**cart)
            for item in cart_obj.items:
                if item.product.id == product_id and (item.variant_id == variant_id or variant_id is None):
                    return item
            return None
        except Exception as e:
            self.logger.error(f"Failed to get cart item: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get cart item"
            )

class CartItemRepository(BaseRepository[CartItem]):
    def __init__(self):
        super().__init__(model_class=CartItem, collection_name="cart_items")
        self.logger = logging.getLogger(__name__)
