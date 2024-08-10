from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.products import Color
from  models.common import ResponseModel
from database import db

from services.color import save_image

router = APIRouter(
    prefix="/colors", 
    tags=["Product Color"]
)
@router.post("/", response_model=Any,response_model_by_alias=False)
async def create_color(name: str  = Form(...),
                       color_code: str  = Form(...),
                       image: UploadFile=File(...)
                       ):
    print(f"Received name: {name}")
    print(f"Received color_code: {color_code}")
    print(f"Received image filename: {image.filename}")
    # Input validation for name and color_code

    try:
        image_path = await save_image(image=image, color_name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save image: {str(e)}")

    color = Color(
        name=name,
        color_code=color_code,
        image=image_path
    )

    try:
        await db["colors"].insert_one(color.model_dump(
            by_alias=True, exclude=["id"] # type: ignore
        )) # type: ignore
    except Exception as e:
        logging.error(f"An error occurred while saving color: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save color")

    return ResponseModel(data={}, code=201, message="Color saved successfully")
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
