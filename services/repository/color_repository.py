from typing import Optional
import logging
from fastapi import UploadFile, HTTPException
from services.repository.base_repository import BaseRepository
from services.image_processor import ColorImageProcessor
from models.products import Color

class ColorRepository(BaseRepository[Color]):
    def __init__(self):
        super().__init__(model_class=Color, collection_name="colors")
        self.image_processor = ColorImageProcessor()
        self.logger = logging.getLogger(__name__)
    
    async def get_color(self, filter_query: dict) -> Color | None:
        """Get a color by filter query"""
        try:
            return await self.fetch_one(filter_query=filter_query)
        except Exception as e:
            self.logger.error(f"Failed to get color: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get color"
            )

    async def create_color(self, name: str, color_code: str, image: UploadFile) -> bool:
        """Create a new color with an associated image"""
        try:
            # Save the uploaded image and get the path
            image_path = await self.image_processor.save_image(
                image=image,
                color_name=name
            )

            # Create a Color object
            color = Color(
                name=name,
                color_code=color_code,
                image=image_path
            )

            # Save the color to the repository
            is_created = await self.insert_one(color.model_dump())
            if not is_created:
                raise HTTPException(status_code=500, detail="Failed to create color")

            return True
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to create color: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to create color"
            )

    async def get_color_by_code(self, color_code: str) -> Optional[Color]:
        """Fetch color information by color code"""
        try:
            color = await self.find_one({"color_code": color_code})
            if not color:
                raise HTTPException(status_code=404, detail="Color not found")
            return color
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get color by code: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get color by code"
            )