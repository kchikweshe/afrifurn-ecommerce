
import os
from typing import Any, Coroutine, List

from fastapi import UploadFile
from constants.paths import LEVEL_ONE_IMAGES_DIR, PRODUCT_IMAGES_DIR
from models.products import Level1Category
from services.base_service import BaseService
from services.image_processor import WebPImageProcessor
from services.repository.level_1_category_repository import Level1CategoryRepository
class Level1CategoryService(BaseService[Level1Category]):

    def __init__(
        self,
        repository: Level1CategoryRepository,
        image_proccessor:WebPImageProcessor
    ):
        super().__init__(repository=repository)
        self.image_proccessor=image_proccessor

  

async def save_categories_images(self, images: List[UploadFile], product_id: str) -> List[str]:
        """Process and save product images"""
        saved_paths = []
        product_folder = os.path.join(PRODUCT_IMAGES_DIR, str(product_id))
        
        for i, image in enumerate(images):
            file_path = await self.image_proccessor.process_image(
                image=image,
                i=i,
                inserted_item=product_id,
                directory=product_folder
            )
            saved_paths.append(file_path)

        return saved_paths