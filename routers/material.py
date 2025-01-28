from typing import Any, List
from fastapi import APIRouter, Depends, Form, HTTPException

from dependencies.dependencies import get_material_service
from models.product_attributes import Material
from  models.common import ResponseModel
from database import db
from services.material_service import MaterialService

router = APIRouter(
    prefix="/materials", 
    tags=["Materials"]
)
@router.post("/", response_model=ResponseModel)
async def create(name: str = Form(..., min_length=0),
  material_service: MaterialService = Depends(get_material_service)

    ):
    
    material=Material(
        name=name,
    )
    try:
        is_created = await material_service.create(material)
        if not is_created:
            raise HTTPException(status_code=500,detail="Failed to save material type")
        return ResponseModel.create(status_code=201, message="Material saved successfully", class_name="Material")
    except:
        raise HTTPException(status_code=500,detail="Failed to save material type")
@router.get("/{name}", response_model=Material)
async def get_one(name: str):
    data = await db["materials"].find_one({"name": name})
    if not data:
        raise HTTPException(status_code=404, detail="Material not found")
    return data
@router.get("/", response_model=List[Material])
async def get_all():
    data = await db["materials"].find().to_list(length=None)
    if not data:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

