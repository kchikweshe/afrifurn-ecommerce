from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import List
from bson import ObjectId
import asyncio

from models.common import ResponseModel
from models.products import Color, ProductVariant
from database import db
from services.image import process_image
from services.product import IMAGES_DIR, fetch_one, insert_into_db


collection=db["products"]
variants = db["variants"]
colors = db["colors"]

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

async def get_variant_from_db(product_id: ObjectId, variant_id: ObjectId):
    # Mock implementation of retrieving a variant from the database.
    return ProductVariant(
        color=Color(name="Red", color_code="#FF0000", image="red_color_image.jpg"),
        images=["image1.jpg", "image2.jpg"],
        quantity_in_stock=10,
        product_id="12dwenkn2"
    )

async def archive(collection_name:str,item_id: ObjectId):
    # Updated implementation to archive a variant in the database.
    result = await db[collection_name].update_one(
        {"_id": item_id},
        {"$set": {f"is_archived": True}}
    )
    if result.modified_count == 0:
        return {"message": "Variant not found or already archived"}
    return {"message": "Variant archived successfully"}
# Create a ProductVariant
@router.post("{product_id}/variants", response_model=Any, response_model_by_alias=False)
async def create_product_variant(
    product_id: str,
    color_code: str = Form(...),
    quantity_in_stock: int = Form(...),
    images: List[UploadFile] = File(...)
) -> Any:
    """
    Handles the creation of a new product variant by processing input data, validating the product ID,
    processing and saving images, fetching color details, and inserting the variant into the database.

    Args:
        product_id (str): The ID of the product to which the variant belongs.
        color_code (str): The color code of the variant.
        quantity_in_stock (int): The quantity of the variant in stock.
        images (List[UploadFile]): A list of image files to be processed and saved.

    Returns:
        ProductVariant: Object containing the details of the newly created variant, including image paths.
    """
    try:
        product_obj_id = ObjectId(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    image_paths = await asyncio.gather(*[process_image(image, i, product_id, IMAGES_DIR) for i, image in enumerate(images)])

    color = await fetch_one(collection_name='colors', key='color_code', value=color_code)
    variant = ProductVariant(product_id=str(product_obj_id), color=color, images=image_paths, quantity_in_stock=quantity_in_stock)

    inserted_variant = await insert_into_db(name="variants", item=variant)
    if not inserted_variant:
        raise HTTPException(status_code=500, detail="Error inserting variant")
    variant.id=str(inserted_variant.inserted_id)
    # Update the products collection with the new variant
    product = await db["products"].find_one_and_update(
        {"_id": product_obj_id},
        {"$push": {"variants": variant.model_dump()}}
    )

    if not product:
        raise HTTPException(status_code=500, detail="Error updating product with new variant")
    return ResponseModel(data={}, code=201, message="Product variant added successfully")

# Get a ProductVariant
@router.get("{product_id}/variants/{variant_id}", response_model=ProductVariant)
async def get_product_variant(product_id: str, variant_id: str):
    try:
        product_obj_id = ObjectId(product_id)
        variant_obj_id = ObjectId(variant_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    variant = await fetch_one('variants', variant_id)
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

# # Mock function to simulate image processing
# async def process_image(image: UploadFile, index: int = 0, inserted_product: dict = None):
#     # Mock image processing function
#     return f"/path/to/{image.filename}"
