import logging
from fastapi import APIRouter, Form, File, UploadFile
from typing import List, Any, Optional
from bson import ObjectId
from fastapi.exceptions import HTTPException
from database import db
from constants.paths import LEVEL_TWO_IMAGES_DIR
from models.common import ErrorResponseModel
from models.products import Level1Category
from services.repository.level_1_category_repository import Level1CategoryRepository
from services.repository.category_repository import CategoryRepository
from services.image_processor import WebPImageProcessor

router = APIRouter()

# Initialize repositories and processors
level1_category_repository = Level1CategoryRepository()
category_repository = CategoryRepository()
image_processor = WebPImageProcessor()

@router.post("/", response_model=Any)
async def create_level1_category(
    id: Optional[str] = None,
    name: str = Form(...),
    short_name: str = Form(...),
    category_id: str = Form(...),
    description: str = Form(...),
    images: List[UploadFile] = File(...)
) -> Any:
    """
    Create a new level 1 category.

    This function creates a new level 1 category with the provided details such as name, 
    short name, description, and images. It also associates the category with a parent 
    category specified by the category_id.

    Parameters:
    - id (Optional[str]): The optional ID for the new category.
    - name (str): The name of the category.
    - short_name (str): The short name of the category.
    - category_id (str): The ID of the parent category.
    - description (str): A description of the category.
    - images (List[UploadFile]): A list of images to be associated with the category.

    Returns:
    - Level1Category: The created level 1 category object.

    Raises:
    - HTTPException: If there is an error in creating the category, or if the category ID 
      is invalid, or if the parent category is not found.
    """
    try:
        # Validate category ID
        try:
            category_id_obj = ObjectId(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Get parent category
        parent_category = await category_repository.find_one({"_id": category_id_obj})
        if parent_category is None:
            return ErrorResponseModel(
                error="Category not found",
                message="Category not found",
                code=404
            )

        # Process images
        image_paths = await image_processor.process_images(
            images=images,
            product_id=short_name,
            folder=LEVEL_TWO_IMAGES_DIR,
            color_code=None
        )

        # Create level 1 category
        level1_category = Level1Category(
            name=name,
            short_name=short_name,
            category=parent_category,
            description=description,
            images=image_paths
        )

        # Set ID if provided
        if id:
            level1_category.id = id

        # Save category
        created = await level1_category_repository.create_category(level1_category, images)
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create level 1 category")

        return level1_category

    except Exception as e:
        logging.error(f"Failed to create level 1 category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create level 1 category")

@router.get("/", response_model=List[Level1Category])
async def get_level1_categories():
    """Get all level 1 categories"""
    try:
        categories = await level1_category_repository.fetch_all()
        return categories
    except Exception as e:
        logging.error(f"Failed to get level 1 categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get level 1 categories")

@router.get("/{category_id}", response_model=List[Level1Category])
async def get_level1_categories_by_category(category_id: str):
    """Get level 1 categories by parent category ID"""
    try:
        # Validate category ID
        try:
            category_id_obj = ObjectId(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Get categories
        categories =  db["level1_categories"].find(
            {"category._id": category_id_obj}
        )
        return categories
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get level 1 categories by category: {e}")
        raise HTTPException(status_code=500, detail="Failed to get level 1 categories by category")