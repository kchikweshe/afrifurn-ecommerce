from services.repository.base_repository import BaseRepository
from models.products import ProductVariant

class ProductVariantRepository(BaseRepository[ProductVariant]):
    def __init__(self):
        super().__init__(ProductVariant, collection_name="variants")
 