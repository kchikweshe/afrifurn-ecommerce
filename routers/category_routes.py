import logging
from bson import ObjectId
from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List, Any, Optional

from constants.paths import LEVEL_ONE_IMAGES_DIR
from models.products import Category
from services.repository.category_repository import CategoryRepository
from services.image_processor import WebPImageProcessor

router = APIRouter()

# Initialize repositories and processors
category_repository = CategoryRepository()
image_processor = WebPImageProcessor()

@router.get("/", response_model=List[Category])
async def get_categories():
    """Get all categories"""
    try:
        categories = await category_repository.fetch_all()
        return categories
    except Exception as e:
        logging.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """Get a category by ID"""
    try:
        obj_id = ObjectId(category_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    try:
        category = await category_repository.fetch_one({"_id": obj_id})
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get category: {e}")
        raise HTTPException(status_code=500, detail="Failed to get category")

@router.get("/categories/{name}", response_model=Category)
async def filter_category(name: str):
    """Get a category by name"""
    try:
        category = await category_repository.fetch_one({"name": name})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to filter category: {e}")
        raise HTTPException(status_code=500, detail="Failed to filter category")

@router.post("/", response_model=Any, response_model_by_alias=False)
async def create_category(
    short_name: str,
    name: str,
    id: Optional[str] = None,
    description: Optional[str] = None,
    images: List[UploadFile] = File(...)
):
    """Create a new category"""
    try:
        # Process images
        image_paths = await image_processor.process_images(
            images=images,
            product_id=name.lower(),
            folder=LEVEL_ONE_IMAGES_DIR
        )

        # Create category object
        category = Category(
            name=name,
            short_name=short_name,
            description=description,
            images=image_paths
        )

        # Set ID if provided
        if id:
            category.id = id

        # Insert category
        inserted = await category_repository.insert_one(category.model_dump())
        if not inserted:
            raise HTTPException(status_code=500, detail="Failed to create category")

        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to create category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create category")