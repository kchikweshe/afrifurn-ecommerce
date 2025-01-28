# category repository
from fastapi import HTTPException
from services.repository.base_repository import BaseRepository
from models.products import Category

class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(model_class=Category, collection_name="categories")
    
    async def get_category(self, filter_query: dict) -> Category | None:
        """Get a category by filter query"""
        # handle edge cases
        if not filter_query:
            raise HTTPException(status_code=400, detail="Filter query is required")
        return  await self.fetch_one(filter_query=filter_query) 