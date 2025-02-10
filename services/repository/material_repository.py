import logging
from fastapi import HTTPException
from services.repository.base_repository import BaseRepository
from models.product_attributes import Material

class MaterialRepository(BaseRepository[Material]):
    def __init__(self):
        super().__init__(model_class=Material, collection_name="materials")
        self.logger = logging.getLogger(__name__)
    
    async def get_material(self, filter_query: dict) -> Material | None:
        """Get a material by filter query"""
        try:
            if not filter_query:
                raise HTTPException(status_code=400, detail="Filter query is required")
            return await self.fetch_one(filter_query=filter_query)
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get material: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get material"
            )
    
    async def create_material(self, material: Material) -> bool:
        """Create a new material"""
        try:
            is_created = await self.insert_one(material.model_dump())
            if not is_created:
                raise HTTPException(status_code=500, detail="Failed to create material")
            return True
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to create material: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to create material"
            )
    
    async def update_material(self, material_id: str, material: Material) -> bool:
        """Update an existing material"""
        try:
            success = await self.update(material_id, material.model_dump())
            if not success:
                raise HTTPException(status_code=404, detail="Material not found")
            return True
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update material: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update material"
            )