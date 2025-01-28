# category service
from fastapi import UploadFile
from services.base_service import BaseService
from services.image_processor import ColorImageProcessor, WebPImageProcessor
from services.repository.color_repository import ColorRepository
from models.products import Color

class ColorService(BaseService[Color]):
    def __init__(self, repository: ColorRepository):
        super().__init__(repository=repository)
    # TODO: override the create method to save the image
    async def create(self, name: str, color_code: str, image: UploadFile) -> bool:
        image_processor = ColorImageProcessor()
        image_path = await image_processor.save_image(
            image=image,
            color_name=name
        )
        color = Color(
            name=name,
            color_code=color_code,
            image=image_path
        )
        is_created = await super().create(color)
        return is_created is not None

