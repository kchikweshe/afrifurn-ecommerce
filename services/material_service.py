# services/material_service.py
from models.product_attributes import Material
from services.base_service import BaseService
from services.repository.material_repository import MaterialRepository
class MaterialService(BaseService[Material]):
    def __init__(self, repository: MaterialRepository):
        super().__init__(repository=repository)
    pass