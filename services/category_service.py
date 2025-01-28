# category service
from services.base_service import BaseService
from services.image_processor import WebPImageProcessor
from services.repository.category_repository import CategoryRepository
from models.products import Category

class CategoryService(BaseService[Category]):
    def __init__(self, image_processor:WebPImageProcessor, repository: CategoryRepository):
        self.image_processor=image_processor
        super().__init__(repository=repository)

