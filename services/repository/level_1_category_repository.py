import logging
import os
from typing import List

from fastapi import HTTPException, UploadFile
from constants.paths import LEVEL_ONE_IMAGES_DIR
from models.products import Level1Category
from services.repository.base_repository import BaseRepository
from services.image_processor import WebPImageProcessor

class Level1CategoryRepository(BaseRepository[Level1Category]):
    def __init__(self):
        super().__init__(model_class=Level1Category, collection_name="level1_categories")
        self.image_processor = WebPImageProcessor()
    
    async def get_category(self, category_id: str) -> Level1Category | None:
        """Get a level 1 category by ID"""
        try:
            if not category_id:
                raise HTTPException(status_code=400, detail="Category ID is required")
            return await self.find_one(value=category_id)
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Failed to get category: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get category" 
            )

    async def save_category_images(self, images: List[UploadFile], category_id: str) -> List[str]:
        """Process and save category images"""
        try:
            saved_paths = []
            category_folder = os.path.join(LEVEL_ONE_IMAGES_DIR, str(category_id))
            
            for i, image in enumerate(images):
                file_path = await self.image_processor.process_image(
                    image=image,
                    inserted_item=category_id,

                    i=i,
                    directory=category_folder
                )
                saved_paths.append(file_path)

            return saved_paths
        except Exception as e:
            logging.error(f"Failed to save category images: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to save category images"
            )
    
    async def create_category(self, category: Level1Category, images: List[UploadFile] = None) -> bool:
        """Create a new level 1 category with optional images"""
        try:
            # First create the category
            is_created = await self.insert_one(category.model_dump())
            if not is_created:
                raise HTTPException(status_code=500, detail="Failed to create category")

            # If images are provided, save them
            if images:
                image_paths = await self.save_category_images(images, str(category.id))
                # Update the category with image paths
                category.images = image_paths
                await self.update(str(category.id), category.model_dump())

            return True
 
        except Exception as e:
            logging.error(f"Failed to create category: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to create category"
            )
    
    async def update_category(self, category_id: str, category: Level1Category, images: List[UploadFile] = None) -> bool:
        """Update an existing level 1 category with optional new images"""
        try:
            # If images are provided, save them
            if images:
                image_paths = await self.save_category_images(images, category_id)
                category.images = image_paths

            success = await self.update(category_id, category.model_dump())
            if not success:
                raise HTTPException(status_code=404, detail="Category not found")

            return True
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Failed to update category: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update category"
            )