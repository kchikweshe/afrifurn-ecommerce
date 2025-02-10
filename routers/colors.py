from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends

from models.products import Color
from models.common import ResponseModel
from services.repository.color_repository import ColorRepository

router = APIRouter(
    prefix="/colors", 
    tags=["Product Color"]
)

# Initialize repository
color_repository = ColorRepository()

@router.post("/", response_model=ResponseModel,response_model_by_alias=False)
async def create_color(name: str  = Form(...),
                       color_code: str  = Form(...),
                       image: UploadFile=File(...),
                       ):
    """Create a new color"""
    try:
        # Create color with image
        is_created = await color_repository.create_color(
            name=name,
            color_code=color_code,
            image=image
        )
        if not is_created:
            raise HTTPException(status_code=500, detail="Failed to save color")

        return ResponseModel.create(
            status_code=201,
            message="Color saved successfully",
            class_name="Color"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to save color: {e}")
        raise HTTPException(status_code=500, detail="Failed to save color")

@router.get("/{code}", response_model=Color)
async def get_color(code: str):
    """Get a color by code"""
    try:
        color = await color_repository.get_color_by_code(code)
        if not color:
            raise HTTPException(status_code=404, detail="Color not found")
        return color
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get color: {e}")
        raise HTTPException(status_code=500, detail="Failed to get color")

@router.get("/", response_model=List[Color])
async def get_colors():
    """Get all colors"""
    try:
        colors = await color_repository.fetch_all()
        return colors
    except Exception as e:
        logging.error(f"Failed to get colors: {e}")
        raise HTTPException(status_code=500, detail="Failed to get colors")

import logging
