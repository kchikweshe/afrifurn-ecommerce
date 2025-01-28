from services.repository.base_repository import BaseRepository
from models.products import Level1Category, Level2Category

class Level1CategoryRepository(BaseRepository[Level1Category]):
    def __init__(self):
        super().__init__(model_class=Level1Category, collection_name="level1_categories")
    
    async def get_category(self, category_id: str) -> dict:
        return await self.fetch_one(value=category_id) 