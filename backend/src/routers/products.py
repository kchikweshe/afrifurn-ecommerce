import os
from typing import Dict, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel

from models.products import Category, Dimensions, Level1Category, Level2Category, Product, Variant
from  models.common import CommonModel
from database import db
from datetime import datetime
from bson import ObjectId
DEFAULT_IMAGES_DIR = "product_images"  # Default image storage directory
IMAGES_DIR = os.getenv("PRODUCT_IMAGES_DIR", DEFAULT_IMAGES_DIR)  # Read from environment variable


router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)



@router.get("/")
async def get_products():
    try:
         products =  db.products.find() 
    except  Exception as e:
        print(e)
    return products



@router.post("/product/", response_model=Product)
async def create_product(
        name: str = Form(...),
         category: Category = Form(...),
         level1_category: Level1Category = Form(...),

         level2category: Level2Category = Form(...),
         description: str=Form(...),
        dimensions: Dimensions=Form(...),
        variants:list[Variant]=Form(...)
    , image: UploadFile = File(...)):
    # Validate image (optional)
    # ...

    # Create image directory if it doesn't exist
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Generate a unique filename for the image
    file_extension = image.filename.split(".")[-1]
    filename = f"{name}_{variants[0].color}.{file_extension}"  # Example filename format
    file_path = os.path.join(IMAGES_DIR, filename)

    try:
        with open(file_path, "wb") as f:
            contents = await image.read()
            f.write(contents)

            product = Product(
            name=name,
            category=category,
            description=description,
            dimensions=dimensions,
            variants=variants,
            # Optional image field, assuming you've added it to the model
            image=filename
        )
        # Update product model with the image path
        product.variants[0].image = filename

        # Insert product into database
        inserted_product =  await db["products"].insert_one(product)
        return inserted_product.insertedid

    except Exception as e:
        raise RuntimeError(f"Error saving image: {e}") from e



@router.put('/{id}')
async def update_product(id: str, product: Product = Body(...)):
    product = {k: v for k, v in product.dict().items() if v is not None}
    if len(product) > 1:
        update_result = await db["products"].update_one({"id": ObjectId(id)}, {"$set": product})
        if update_result.modified.count() > 0:
            if (updated_product := await db["products"].find_one({"id": ObjectId(id)})) is not None:
                return updated_product

    if (existing_product := await db["students"].find_one({"id": id})) is not None:
        return existing_product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete('{id}')
async def delete_product(id: str):
    delete_result = await db["products"].delete({"id", ObjectId(id)})
    if delete_result.delete_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")

@router.put("/products/{productid}", response_model=Product)
async def update_product(productid: str, product_updates: Product):
    update_result = await db["products"].update_one(
        {"id": ObjectId(productid)},
        {"$set": product_updates.dict(exclude_unset=True, exclude_expr="$")})  # Exclude unset and expressions
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch the updated product for response (optional)
    updated_product = await db["products"].find_one({"id": ObjectId(productid)})
    return updated_product