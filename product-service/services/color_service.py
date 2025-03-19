from typing import Optional
from fastapi import UploadFile, HTTPException
from services.base_service import BaseService
from services.image_processor import ColorImageProcessor
from services.repository.color_repository import ColorRepository
from models.products import Color

class ColorService(BaseService[Color]):
    def __init__(self, repository: ColorRepository):
        super().__init__(repository=repository)
        self.image_processor = ColorImageProcessor()

    async def create(self, name: str, color_code: str, image: UploadFile) -> bool:
        """
        Create a new color with an associated image.
        The image is processed and saved, and the color is stored in the repository.
        """
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
            is_created = await super().create(color)
            if not is_created:
                raise HTTPException(status_code=500, detail="Failed to create color")

            return True

        except Exception as e:
            # Handle any unexpected errors
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    async def get_color_by_code(self, color_code: str) -> Optional[Color]:
        """
        Fetch color information by color code.
        """
        try:
            color = await self.repository.find_one({"color_code": color_code})
            if not color:
                raise HTTPException(status_code=404, detail="Color not found")
            return color
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching color: {str(e)}")