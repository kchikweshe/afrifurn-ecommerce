import os
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel, Field

from models.products import Category, Dimensions, Level1Category, Level2Category, Price, Product, Variant
from  models.common import CommonModel, ErrorResponseModel, ResponseModel
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



@router.post("/", response_model=Any)
async def create_product(
        name: str = Form(...),
        category: str = Form(...),
        price_of_item:float=Form(...),
         description: str=Form(...),
         currency_code:str=Form(...),
           width: float = Form(gt=0),
    height: float = Form(gt=0),
    depth: float = Form(gt=0, optional=True) , # Optional depth
    weight: float = Form(gt=0))->Any:
    # Validate image (optional)
    # ..
    try:
        category_id = ObjectId(category)
      
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    try:
        parent_category = await db['level2_categories'].find_one({"_id": category_id})
        currency = await db['currencies'].find_one({"code": currency_code})
    except  Exception as e:
        raise HTTPException(status_code=500,detail=f"Error.{e}")
   
    if parent_category is None:
        return ErrorResponseModel(error=404,code=404,message="Category not found")
    if currency is None:
        return ErrorResponseModel(error=404,code=404,message="Currency not found")
    
    dimensions= Dimensions(
        depth=depth,
        height=height,
        weight=weight,
        width=width
    )
    price=Price(
        value=price_of_item,currency=currency
    )
    product=Product(
        name=name,
        description=description,
        category=parent_category,
        price=price,
        dimensions=dimensions
    )
     # Insert product into database
    inserted_product =  await db["products"].insert_one(product.dict())
    # data = product.copy(update={"id": str(inserted_product.inserted_id)})

    return ResponseModel(data=None,code=201,message="Product added successfully")

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