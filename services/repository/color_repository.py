from services.repository.base_repository import BaseRepository
from models.products import Color

class ColorRepository(BaseRepository[Color]):
    def __init__(self):
        super().__init__(model_class=Color, collection_name="colors")
    
    async def get_color(self, filter_query: dict) -> Color|None:
        return await self.fetch_one(filter_query=filter_query) 