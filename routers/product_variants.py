from typing import Any, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import List
from bson import ObjectId
import asyncio
import logging

from models.common import ResponseModel
from models.products import Color, ProductVariant
from database import db
from constants.paths import PRODUCT_IMAGES_DIR
from services.image_processor import WebPImageProcessor
from services.repository.product_variant_repository import ProductVariantRepository
from services.repository.product_repository import ProductRepository
from services.repository.color_repository import ColorRepository

collection=db["products"]
variants = db["variants"]
colors = db["colors"]

image_processor = WebPImageProcessor()

router = APIRouter(
    prefix="/product/variant", 
    tags=["Product Variant"]
)

# Initialize repositories and processors
variant_repository = ProductVariantRepository()
product_repository = ProductRepository()
color_repository = ColorRepository()

# Mock database functions
async def insert_variant_into_db(product_id: ObjectId, variant: ProductVariant):
    # Mock implementation of inserting a variant into the database.
    return {"inserted_id": ObjectId()}

async def update_variant_in_db(product_id: ObjectId, variant_id: ObjectId, variant_data: dict):
    # Mock implementation of updating a variant in the database.
    return {"modified_count": 1}

async def archive(collection_name:str,item_id: ObjectId):
    # Updated implementation to archive a variant in the database.
    result =  db[collection_name].update_one(
        {"_id": item_id},
        {"$set": {f"is_archived": True}}
    )
    if result.modified_count == 0:
        return {"message": "Variant not found or already archived"}
    return {"message": "Variant archived successfully"}

async def process_images(images: List[UploadFile], product_id: str, color_code: str) -> List[str]:
    """Process multiple images in parallel using the WebP image processor"""
    return await asyncio.gather(
        *[image_processor.process_image(image, i, product_id, PRODUCT_IMAGES_DIR,color_code) 
          for i, image in enumerate(images)]
    )

@router.post("/product/{product_id}", response_model=ResponseModel, response_model_by_alias=False)
async def create_product_variant(
    product_id: str,
    color_code: str = Form(...),
    quantity_in_stock: int = Form(...),
    images: List[UploadFile] = File(...),
) -> Any:
    """Create a new product variant with associated images and color"""
    try:
        # Validate product ID
        try:
            product_obj_id = ObjectId(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product ID format")

    
        # Get color
        color = await color_repository.get_color_by_code(color_code)
        if not color:
            raise HTTPException(status_code=404, detail="Color not found")
    # Process images
        image_paths = await process_images(images, product_id,color.color_code)

        # Create variant
        variant = ProductVariant(
            product_id=str(product_obj_id),
            color_id=color.color_code,
            images=image_paths,
            quantity_in_stock=quantity_in_stock
        )

        # Save variant
        inserted_id =  db["variants"].insert_one(variant.model_dump())
        if not inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create variant")

        # Update product
        updated =  db["products"].update_one(
            {"_id": product_obj_id},    {"$push": {"product_variants": variant.model_dump()}})
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update product with variant")

        return ResponseModel.create(
            class_name="ProductVariant",
            data=variant.model_dump(),
            message="Product variant created successfully"
        )

    except Exception as e:
        logging.error(f"Failed to create product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product variant")

@router.get("{product_id}/variants/{variant_id}", response_model=ProductVariant)
async def get_product_variant(product_id: str, variant_id: str,
                              ):
    try:
        # Validate IDs
        try:
            product_obj_id = ObjectId(product_id)
            variant_obj_id = ObjectId(variant_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Get variant
        variant =  db["variants"].find_one({"_id": variant_obj_id})
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        return variant
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to get product variant")

@router.delete("{product_id}/variants/{variant_id}", response_model=ResponseModel)
async def soft_delete_product_variant(product_id: str, variant_id: str):
    """Soft delete a product variant"""
    try:
        # Validate IDs
        try:
            product_obj_id = ObjectId(product_id)
            variant_obj_id = ObjectId(variant_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Archive variant
        archived = await archive("variants",variant_obj_id)
        if not archived:
            raise HTTPException(status_code=404, detail="Variant not found or already archived")

        return ResponseModel.create(
            class_name="ProductVariant",
            message="Product variant archived successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to archive product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to archive product variant")
