from typing import Any, List
from fastapi import APIRouter, Form, HTTPException

from models.product_attributes import Material
from  models.common import ResponseModel
from database import db

router = APIRouter(
    prefix="/materials", 
    tags=["Materials"]
)
@router.post("/", response_model=Any)
async def create(name: str = Form(..., min_length=0),
 

    ):
    
    material=Material(
        name=name,
    )
    try:
         await db["materials"].insert_one(material.model_dump(
        by_alias=True, exclude=["id"])) # type: ignore
    except:
        raise HTTPException(status_code=500,detail="Failed to save material type")
    return ResponseModel(data={},code=201,message="Material saved successfully")
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

