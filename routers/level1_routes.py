from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from typing import List, Any
from constants.paths import LEVEL_TWO_IMAGES_DIR
from dependencies.dependencies import get_level_1_category_service
from models.common import ErrorResponseModel
from models.products import Level1Category
from services.level_1_category_service import Level1CategoryService
from bson import ObjectId
from database import db

router = APIRouter()

@router.post("/", response_model=Any)
async def create_level1_category(
    name: str = Form(...),
    short_name: str = Form(...),
    category_id: str = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(...),
    service: Level1CategoryService = Depends(get_level_1_category_service)
) -> Any:
    try:
        category_id = ObjectId(category_id)  # type: ignore
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    parent_category = await db.get_collection("categories").find_one({"_id": category_id})
    if parent_category is None:
        return ErrorResponseModel(error="Category not found", message="Category not found", code=404)

    image_paths = await service.image_proccessor.process_images(images=images, product_id=short_name, folder=LEVEL_TWO_IMAGES_DIR)
    level1_category = Level1Category(name=name, short_name=short_name, category=parent_category, description=description, images=image_paths)
    result = await service.create(level1_category)
    return result

@router.get("/", response_model=List[Level1Category])
async def get_level1_categories():
    level1_categories = await db["level1_categories"].find().to_list(length=None)
    return level1_categories

@router.get("/{category_id}", response_model=List[Level1Category])
async def get_level1_categories_by_category(category_id: str):
    cid = ObjectId(category_id)
    level1_categories = await db["level1_categories"].find({'category._id': category_id}).to_list(length=None)
    return level1_categories 