from io import BytesIO
import os
from tkinter import Image
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel, Field

from models.products import Category, Color, Currency, Dimensions, Level1Category, Level2Category, Product, Variant
from  models.common import CommonModel, ErrorResponseModel, ResponseModel
from database import db
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/colors", 
    tags=["Product Color"]
)
@router.post("/", response_model=Any)
async def create_color(name: str = Form(..., min_length=0),
    color_code: str = Form(..., min_length=1),

    ):
    
    color=Color(
        name=name,
        color_code=color_code
    )
    try:
         await db["colors"].insert_one(color.model_dump(
        by_alias=True, exclude=["id"]))
    except:
        raise HTTPException(status_code='500',detail="Failed to save color")
    return ResponseModel(data=None,code=201,message="Color saved successfully")
@router.get("/{code}", response_model=Color)
async def get_color(code: str):
    color = await db["colors"].find_one({"code": code})
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color

