from services.repository.base_repository import BaseRepository
from models.products import Currency

class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(model_class=Currency, collection_name="currencies")
    
    async def get_currency(self, filter_query: dict) -> Currency|None:
        return await self.fetch_one(filter_query=filter_query) 