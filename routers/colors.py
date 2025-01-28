from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends

from dependencies.dependencies import get_color_service
from models.products import Color
from  models.common import ResponseModel
from database import db

from services.color import save_image
from services.color_service import ColorService
router = APIRouter(
    prefix="/colors", 
    tags=["Product Color"]
)
@router.post("/", response_model=ResponseModel,response_model_by_alias=False)
async def create_color(name: str  = Form(...),
                       color_code: str  = Form(...),
                       image: UploadFile=File(...),
                       color_service: ColorService = Depends(get_color_service)
                       ):
    print(f"Received name: {name}")
    print(f"Received color_code: {color_code}")
    print(f"Received image filename: {image.filename}")
    # Input validation for name and color_code

 

    try:
        is_created = await color_service.create(name=name, color_code=color_code, image=image)
        if not is_created:
            raise HTTPException(status_code=500, detail="Failed to save color") 
        return ResponseModel.create(status_code=201, message="Color saved successfully", class_name="Color")
    except Exception as e:
        logging.error(f"An error occurred while saving color: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save color")

@router.get("/{code}", response_model=Color)
async def get_color(code: str):
    color = await db["colors"].find_one({"code": code})
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color
@router.get("/", response_model=List[Color])
async def get_colors():
    colors = await db["colors"].find().to_list(length=None)
  
    return colors

import logging

async def save(name: str, item: Any):
    try:
        logging.info(f"Inserting product into {name} collection. Product details: {item}")
        inserted_object = await db[f'{name}'].insert_one(item.model_dump(exclude=["id"])) # type: ignore
        return inserted_object
    except Exception as e:
        logging.error(f"Error inserting product into {name} collection: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
