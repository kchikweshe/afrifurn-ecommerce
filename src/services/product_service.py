from typing import List, Optional
from models.products import Product, ProductVariant
from services.base_service import BaseService
class ProductService(BaseService[Product]):
 
    async def get_product(self, product_id: str) -> Optional[Product]:
        product = await self.repository.find_one(filter_query={"_id": product_id})
        if product:
            await self.repository.update_views(product_id)
        return product

    async def get_products_by_category(self, category_id: str) -> List[Product]:
        return await self.repository.find_by_category(category_id)

    async def create_product(self, product: Product) -> bool|None:
        return await self.repository.create(product.model_dump(exclude={'id'}))

    async def update_product(self, product_id: str, product: Product) -> bool|None:
        return await self.repository.update(product_id, product.model_dump(exclude={'id'}))

    async def delete_product(self, product_id: str) -> bool|None:
        return await self.repository.delete(product_id) 