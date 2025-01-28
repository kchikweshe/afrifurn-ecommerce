
from models.products import Level2Category
from services.base_service import BaseService
from services.image_processor import WebPImageProcessor
from services.repository.level2_category_repository import Level2CategoryRepository
class Level2CategoryService(BaseService[Level2Category]):

    def __init__(
        self,
        image_processor:WebPImageProcessor,
        repository: Level2CategoryRepository,
    ):
        self.image_processor=image_processor
        super().__init__(repository=repository)
