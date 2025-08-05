import logging
from typing import List
from fastapi import APIRouter, Form, HTTPException

from models.product_attributes import Material
from models.common import ResponseModel
from services.repository.material_repository import MaterialRepository
from decorators.decorator import cache_response 

router = APIRouter(
    prefix="/materials", 
    tags=["Materials"]
)

# Initialize repository
material_repository = MaterialRepository()

@router.post("/", response_model=ResponseModel)
async def create_material(
    name: str = Form(..., min_length=0)
):
    """Create a new material"""
    try:
        # Create material object
        material = Material(name=name)

        # Save material
        is_created = await material_repository.create_material(material)
        if not is_created:
            raise HTTPException(status_code=500, detail="Failed to save material")

        return ResponseModel.create(
            status_code=201,
            message="Material saved successfully",
            class_name="Material"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to save material: {e}")
        raise HTTPException(status_code=500, detail="Failed to save material")

@router.get("/{name}", response_model=Material)
@cache_response(key="material", response_model=Material)
async def get_material(name: str):
    """Get a material by name"""
    try:
        material = await material_repository.get_material({"name": name})
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        return material
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get material: {e}")
        raise HTTPException(status_code=500, detail="Failed to get material")

@router.get("/", response_model=List[Material])
@cache_response(key="materials", response_model=Material)
async def get_all_materials():
    """Get all materials"""
    try:
        materials = await material_repository.fetch_all()
        if not materials:
            raise HTTPException(status_code=404, detail="No materials found")
        return materials
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get materials: {e}")
        raise HTTPException(status_code=500, detail="Failed to get materials")
