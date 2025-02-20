import logging
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from typing import List, Any
from bson import ObjectId

from constants.paths import LEVEL_THREE_IMAGES_DIR
from models.common import ErrorResponseModel, ResponseModel
from models.products import Level2Category
from services.repository.level2_category_repository import Level2CategoryRepository
from services.repository.level_1_category_repository import Level1CategoryRepository
from services.image_processor import WebPImageProcessor
from database import db
router = APIRouter()

# Initialize repositories and processors
level2_category_repository = Level2CategoryRepository()
level1_category_repository = Level1CategoryRepository()
image_processor = WebPImageProcessor()

@router.post("/", response_model=Any)
async def create_level2_category(
    name: str = Form(min_length=3),
    short_name: str = Form(min_length=3),
    level_1_category_id: str = Form(min_length=1),
    description: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """Create a new level 2 category"""
    try:
        # Validate level 1 category ID
        try:
            level_1_category_idx = ObjectId(level_1_category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Get parent category
        parent_category = await level1_category_repository.find_one(
            {"_id": level_1_category_idx}
        )
        if parent_category is None:
            return ErrorResponseModel(
                error="",
                message="Category not found",
                code="404"
            )

        # Process images
        image_paths = await image_processor.process_images(
            images=images,
            product_id=short_name,
            folder=LEVEL_THREE_IMAGES_DIR,
            color_code=None
        )

        # Create level 2 category
        level2_category = Level2Category(
            name=name,
            level_one_category=parent_category,
            images=image_paths,
            short_name=short_name,
            description=description
        )

        # Save category
        inserted_id = await level2_category_repository.create_category(level2_category)
        if not inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create level 2 category")

        # Update category with inserted ID
        data = level2_category.copy(update={"id": str(inserted_id)})

        return ResponseModel.create(
            class_name="Level2Category",
            data=data.model_dump(),
            status_code=200,
            message=f"Category {name} added successfully!!!"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to create level 2 category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create level 2 category")

@router.get("/", response_model=List[Level2Category])
async def get_level2_categories():
    """Get all level 2 categories"""
    try:
        categories = await level2_category_repository.fetch_all()
        return categories
    except Exception as e:
        logging.error(f"Failed to get level 2 categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get level 2 categories")

@router.get("/{category_id}", response_model=List[Level2Category])
async def get_level2_categories_by_level_one_category(category_id: str):
    """Get level 2 categories by level 1 category ID"""
    try:
        # Validate category ID
        try:
            category_id_obj = ObjectId(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Get categories
        categories =  level2_category_repository.filter(
            {"level_one_category._id": category_id_obj}
        )
        print("categories",categories)
        return categories
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get level 2 categories by level 1 category: {e}")
        raise HTTPException(status_code=500, detail="Failed to get level 2 categories by level 1 category")

@router.get("/short-name/{category_name}", response_model=List[Level2Category])
async def get_level2_categories_by_level_one_category_name(category_name: str):
    """Get level 2 categories by level 1 category name"""
    try:
        categories =  level2_category_repository.filter(
            {"level_one_category.short_name": category_name}
        )
        return categories
    except Exception as e:
        logging.error(f"Failed to get level 2 categories by level 1 category name: {e}")
        raise HTTPException(status_code=500, detail="Failed to get level 2 categories by level 1 category name")