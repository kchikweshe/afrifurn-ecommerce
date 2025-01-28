# product variant service
from services.base_service import BaseService
from services.repository.product_variant_repository import ProductVariantRepository
from models.products import ProductVariant

class ProductVariantService(BaseService[ProductVariant]):
    def __init__(self, repository: ProductVariantRepository):
        super().__init__(repository=repository)
