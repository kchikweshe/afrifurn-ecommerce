import logging
from typing import  List, Union
from .base_repository import BaseRepository
from models.products import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__( Product,collection_name="products")

    async def find_by_color_code(self, color_code: str) -> Union[Product, None]:
        product_data = await self.find_one({"color_code": color_code})
        if product_data:    
            return product_data

        return None
    async def find_by_category(self, category_id: str) -> List[Product]:
            cursor = self.db[self.collection_name].find({
                "category_id": category_id,
                "is_archived": False
            })
            documents = await cursor.to_list(length=None)
            return [Product(**doc) for doc in documents]

    async def find_by_material(self, material_id: str) -> List[Product]:
            cursor = self.db[self.collection_name].find({
                "material.id": material_id,
                "is_archived": False
            })
            documents = await cursor.to_list(length=None)
            return [Product(**doc) for doc in documents]

    async def update_views(self, product_id: str) -> bool:
            result = await self.db[self.collection_name].update_one(
                {"_id": product_id},
                {"$inc": {"views": 1}}
            )
            return result.modified_count > 0
    async def aggregate(self, pipeline: list) -> list:
            """
            Execute an aggregation pipeline on the products collection.

            Args:
                pipeline (list): The aggregation pipeline to execute.

            Returns:
                list: The results of the aggregation.
            """
            try:
                results = await self.db[self.collection_name].aggregate(pipeline).to_list(length=None)
                return results
            except Exception as e:
                logging.error(f"Error executing aggregation: {e}")
                raise