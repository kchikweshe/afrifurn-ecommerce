from typing import List, Optional
from models.products import Product, ProductVariant
from .base_repository import BaseRepository

class ProductRepository(BaseRepository[Product]):
    async def find_by_category(self, category_id: str) -> List[Product]:
        cursor = self.collection.find({
            "category_id": category_id,
            "is_archived": False
        })
        documents = await cursor.to_list(length=None)
        return [Product(**doc) for doc in documents]

    async def find_by_material(self, material_id: str) -> List[Product]:
        cursor = self.collection.find({
            "material.id": material_id,
            "is_archived": False
        })
        documents = await cursor.to_list(length=None)
        return [Product(**doc) for doc in documents]

    async def update_views(self, product_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": product_id},
            {"$inc": {"views": 1}}
        )
        return result.modified_count > 0 