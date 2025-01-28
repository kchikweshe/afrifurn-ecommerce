from typing import Any, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import List
from bson import ObjectId
import asyncio

from dependencies.dependencies import get_color_service, get_product_variant_service
from models.common import ResponseModel
from models.products import ProductVariant
from database import db
from constants.paths import PRODUCT_IMAGES_DIR
from services.image_processor import WebPImageProcessor
from services.color_service import ColorService
from services.product_variant_service import ProductVariantService
collection=db["products"]
variants = db["variants"]
colors = db["colors"]

image_processor = WebPImageProcessor()

router = APIRouter(
    prefix="/product/variant", 
    tags=["Product Variant"]
)




# Mock database functions
async def insert_variant_into_db(product_id: ObjectId, variant: ProductVariant):
    # Mock implementation of inserting a variant into the database.
    return {"inserted_id": ObjectId()}

async def update_variant_in_db(product_id: ObjectId, variant_id: ObjectId, variant_data: dict):
    # Mock implementation of updating a variant in the database.
    return {"modified_count": 1}

async def archive(collection_name:str,item_id: ObjectId):
    # Updated implementation to archive a variant in the database.
    result = await db[collection_name].update_one(
        {"_id": item_id},
        {"$set": {f"is_archived": True}}
    )
    if result.modified_count == 0:
        return {"message": "Variant not found or already archived"}
    return {"message": "Variant archived successfully"}

async def process_images(images: List[UploadFile], product_id: str) -> List[str]:
    """Process multiple images in parallel using the WebP image processor"""
    return await asyncio.gather(
        *[image_processor.process_image(image, i, product_id, PRODUCT_IMAGES_DIR) 
          for i, image in enumerate(images)]
    )

# Create a ProductVariant
@router.post("{product_id}/variants/", response_model=Any, response_model_by_alias=False)
async def create_product_variant(
    product_id: str,
    color_code: str = Form(...),
    quantity_in_stock: int = Form(...),
    images: List[UploadFile] = File(...),
    color_service: ColorService = Depends(get_color_service),
    product_variant_service: ProductVariantService = Depends(get_product_variant_service)
) -> Any:
    """
    Create a new product variant with associated images and color.
    Images will be automatically converted to WebP format.
    """
    try:
        product_obj_id = ObjectId(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    image_paths = await process_images(images, product_id)

    color = await color_service.filter(filters={"color_code": color_code})
    variant = ProductVariant(product_id=str(product_obj_id), color_id=color[0].color_code, images=image_paths, quantity_in_stock=quantity_in_stock)

    inserted_variant = await product_variant_service.create(item=variant)
    if not inserted_variant:
        raise HTTPException(status_code=500, detail="Error inserting variant")
   
    # Update the products collection using the base service
    product = await product_variant_service.update_related_document(
        collection_name="products",
        filter_query={"_id": product_obj_id},
        update_query={"$push": {"product_variants": variant.model_dump()}}
    )

    if not product:
        raise HTTPException(status_code=500, detail="Error updating product with new variant")
    
    return ResponseModel(status_code=201, message="Product variant added successfully", class_name="ProductVariant", number_of_data_items=1)

# Get a ProductVariant
@router.get("{product_id}/variants/{variant_id}", response_model=ProductVariant)
async def get_product_variant(product_id: str, variant_id: str,
                              product_variant_service: ProductVariantService = Depends(get_product_variant_service)
                              ):
    try:
        product_obj_id = ObjectId(product_id)
        variant_obj_id = ObjectId(variant_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    variant = await product_variant_service.filter_one(filters={"_id": variant_obj_id})
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    return variant

# Soft Delete a ProductVariant
@router.delete("{product_id}/variants/{variant_id}", response_model=dict)
async def soft_delete_product_variant(product_id: str, variant_id: str):
    try:
        product_obj_id = ObjectId(product_id)
        variant_obj_id = ObjectId(variant_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    delete_result = await archive(collection_name="variants",item_id= variant_obj_id)
    if delete_result["modified_count"] == 0:
        raise HTTPException(status_code=404, detail="Variant not found or already deleted")

    return {"message": "Variant deleted successfully"}
