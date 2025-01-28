from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from typing import List, Any
from constants.paths import LEVEL_THREE_IMAGES_DIR
from dependencies.dependencies import get_level_2_category_service
from models.common import ErrorResponseModel, ResponseModel
from models.products import Level2Category
from services.level_2_category_service import Level2CategoryService
from bson import ObjectId
from database import db

router = APIRouter()

@router.post("/", response_model=Any)
async def create_level2_category(
    name: str = Form(min_length=3),
    short_name: str = Form(min_length=3),
    level_1_category_id: str = Form(min_length=1),
    description: str = Form(...),
    images: List[UploadFile] = File(...),
    service: Level2CategoryService = Depends(get_level_2_category_service)
):
    try:
        level_1_category_idx = ObjectId(level_1_category_id)
        parent_category = await db["level1_categories"].find_one({"_id": level_1_category_idx})
        if parent_category is None:
            return ErrorResponseModel(error="", message="Category not found", code="404")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    image_paths = await service.image_processor.process_images(images=images, product_id=short_name, folder=LEVEL_THREE_IMAGES_DIR)
    level2_category = Level2Category(name=name, level_one_category=parent_category, images=image_paths, short_name=short_name, description=description)

    insert_result = await db["level2_categories"].insert_one(level2_category.model_dump(by_alias=True, exclude=["id"]))  # type: ignore
    inserted_id = insert_result.inserted_id
    data = level2_category.copy(update={"id": str(inserted_id)})
    return ResponseModel.create(class_name="Level2Category", data=data.model_dump(), status_code=200, message=f"Category {name} added successfully!!!") 

@router.get("/", response_model=List[Level2Category])
async def get_level2_categories():
    level2_categories = await db["level2_categories"].find().to_list(length=None)
    return level2_categories

@router.get("/{category_id}", response_model=List[Level2Category])
async def get_level2_categories_by_level_one_category(category_id: str):
    cid = ObjectId(category_id)
    level2_categories = await db["level2_categories"].find({'level_one_category._id': cid}).to_list(length=None)
    return level2_categories

@router.get("/short-name/{category_name}", response_model=List[Level2Category])
async def get_level2_categories_by_level_one_category_name(category_name: str):
    level2_categories = await db["level2_categories"].find({'level_one_category.short_name': category_name}).to_list(length=None)
    return level2_categories 