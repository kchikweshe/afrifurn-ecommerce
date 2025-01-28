from services.repository.base_repository import BaseRepository
from models.product_attributes import Material

class MaterialRepository(BaseRepository[Material]):
    def __init__(self):
        super().__init__(model_class=Material, collection_name="materials")
    
    async def get_material(self, filter_query: dict) -> Material|None:
        return await self.fetch_one(filter_query=filter_query) 