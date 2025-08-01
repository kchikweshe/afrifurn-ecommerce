import json
import logging
from bson import ObjectId
from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List, Any, Optional
from database import db
from constants.paths import LEVEL_ONE_IMAGES_DIR
from models.products import Category
from services.repository.category_repository import CategoryRepository
from services.image_processor import WebPImageProcessor
from decorators.redis_provider import RedisCacheProvider
router = APIRouter()

# Initialize repositories and processors
category_repository = CategoryRepository()
image_processor = WebPImageProcessor()
redis_app=RedisCacheProvider()
key="categories"
@router.get("/", )
async def get_categories():
    """Get all categories"""
    categories:List[Category]
    data=[]
    try:
        categories_from_cache= await redis_app.get(key)
        if categories_from_cache:
            print("Fetching from client")
            raw_list = json.loads(categories_from_cache)
            categories = [Category.model_validate(item) for item in raw_list]   
            return categories
        else:
            categories = await category_repository.fetch_all()
            for category in categories:
                safe_dict =category.model_dump(by_alias=True) 
                safe_dict["_id"] = str(safe_dict["_id"]) if safe_dict["_id"] else None
                data.append(safe_dict)
          
        await redis_app.set(key=key,value=json.dumps(data))
        return categories
    except Exception as e:
        logging.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get categories {e}")

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """Get a category by ID"""
    try:
        obj_id = ObjectId(category_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    try:
        category =  db["categories"].find_one({"_id": obj_id})
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
        category =  db["categories"].find_one({"name": name})
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
            folder=LEVEL_ONE_IMAGES_DIR,
            color_code=None
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
        inserted =  db["categories"].insert_one(category.model_dump())
        if not inserted:
            raise HTTPException(status_code=500, detail="Failed to create category")

        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to create category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create category")