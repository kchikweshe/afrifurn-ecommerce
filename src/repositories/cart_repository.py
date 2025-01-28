from typing import Optional
from models.cart import Cart
from services.repository.base_repository import BaseRepository

class CartRepository(BaseRepository[Cart]):
    async def find_by_user_id(self, user_id: str) -> Optional[Cart]:
        doc = await self.db[self.collection_name].find_one({
            "user_id": user_id,
            "is_archived": False
        })
        return Cart(**doc) if doc else None

    async def update_cart_items(self, cart_id: str, cart: Cart) -> bool:
        update_data = {
            "items": [item.model_dump() for item in cart.items],
            "total_amount": cart.total_amount
        }
        result = await self.db[self.collection_name].update_one(
            {"_id": cart_id},
            {"$set": update_data}
        )
        return  result.modified_count > 0 