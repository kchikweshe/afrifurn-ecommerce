from services.repository.base_repository import BaseRepository
from models.products import Level2Category

class Level2CategoryRepository(BaseRepository[Level2Category]):
    def __init__(self):
        super().__init__(model_class=Level2Category, collection_name="level2_categories")
    
    async def get_category(self, filter_query: dict) -> Level2Category|None:
        return await self.fetch_one(filter_query=filter_query) 