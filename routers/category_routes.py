from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List, Any, Optional
from constants.paths import LEVEL_ONE_IMAGES_DIR
from dependencies.dependencies import get_category_service
from models.products import Category
from services.category_service import CategoryService
from database import db

router = APIRouter()

@router.get("/", response_model=List[Category])
async def get_categories():
    categories = await db.get_collection("categories").find().to_list(length=None)
    return categories

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    try:
        obj_id = ObjectId(category_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    category = await db.get_collection("categories").find_one({"_id": obj_id})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category

@router.get("/categories/{name}", response_model=Category)
async def filter_category(name: str, service: CategoryService = Depends(get_category_service)):
    try:
        category = await service.filter(filters={"name": name})
        return category 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Any, response_model_by_alias=False)
async def create_category(
    short_name: str,
    name: str,
    description: Optional[str] = None,
    service: CategoryService = Depends(get_category_service),
    images: List[UploadFile] = File(...),
):
    try:
        image_paths = await service.image_processor.process_images(images=images, product_id=name.lower(), folder=LEVEL_ONE_IMAGES_DIR)
        cat = Category(name=name, short_name=short_name, description=description, images=image_paths)
        result = await service.create(cat)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions that occur 