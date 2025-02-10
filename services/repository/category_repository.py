import logging
from fastapi import HTTPException, UploadFile
from services.repository.base_repository import BaseRepository
from models.products import Category
from services.image_processor import WebPImageProcessor

class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(model_class=Category, collection_name="categories")
        self.image_processor = WebPImageProcessor()
        self.logger = logging.getLogger(__name__)
    
    async def get_category(self, filter_query: dict) -> Category | None:
        """Get a category by filter query"""
        try:
            if not filter_query:
                raise HTTPException(status_code=400, detail="Filter query is required")
            return await self.fetch_one(filter_query=filter_query)
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get category: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get category"
            )

    async def save_category_image(self, image: UploadFile, category_id: str) -> str:
        """Save category image"""
        try:
            return await self.image_processor.process_image(
                image=image,
                product_folder=f"categories/{category_id}",
                i=0
            )
        except Exception as e:
            self.logger.error(f"Failed to save category image: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to save category image"
            )