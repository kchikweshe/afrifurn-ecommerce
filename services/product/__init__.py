from functools import lru_cache
import os
from typing import Any, Dict
from bson import ObjectId
from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from database import db
from models.products import Product
from services.image import allowed_file, convert_to_webp, readImage, save_image

DEFAULT_IMAGES_DIR = "static/product/"  # Default image storage directory
DEFAULT_COLORS_IMAGES_DIR = "static/colors/"  # Default image storage directory
COLORS_IMAGE_DIR=os.getenv("COLORS_IMAGES_DIR", DEFAULT_COLORS_IMAGES_DIR)   # Default image storage directory

IMAGES_DIR = os.getenv("COLORS_IMAGES_DIR", DEFAULT_COLORS_IMAGES_DIR)  # Read from environment variable
async def insert_into_db(name:str,item:Any):
  
    inserted_object = await db[name].insert_one(item.model_dump(exclude=["id"])) # type: ignore
    return inserted_object

async def extract_product_information(currency_code, material_id, category_id,colors):
    c=[]
    parent_category = await fetch_one(collection_name="level2_categories",value=category_id)
    currency = await fetch_one(collection_name="currencies",key='code',value=currency_code)
    material=await fetch_one(collection_name='materials',value=material_id)
    for color in colors:
      c.append( await fetch_one(collection_name='colors',key='color_code',value=color))

    return parent_category,currency,material,c

def fetch_one(collection_name:str,key:str="_id",value:str=''):
    print("Fetching product with id:",id)
    if(key=='_id'):
        return db[collection_name].find_one({key: ObjectId(value)})

    return db[collection_name].find_one({key: value})
async def process_product_image(image: UploadFile, i: int, inserted_product: Any):
    """Process an uploaded image file and save it in a product-specific folder."""
    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

    contents = await image.read()
    img = readImage(contents)
    webp_contents = convert_to_webp(img)

    # Create product folder if it doesn't exist
    product_folder = os.path.join(IMAGES_DIR, str(inserted_product.inserted_id))
    os.makedirs(product_folder, exist_ok=True)  

    filename = f"image{i}.webp"  # Removed product ID from filename
    file_path = os.path.join(product_folder, filename)

    save_image(webp_contents, file_path)
    return file_path

import logging

async def filter_one_product(filters: dict) -> Any:
    try:
        product = await db["products"].find_one(filters)
        logging.info(f"Filtered product: {product}")
    except Exception as e:
        logging.error(f"Error filtering product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return product
async def filter_products(filters:dict,page:int,page_size:int,skip:int,limit:int,sort_by:str,sort_order:int):

    try:
         products = await db["products"].find(filters).skip(skip).limit(limit).sort(sort_by, sort_order).to_list(length=None)
    except  Exception as e:
        print("Error: ",e)
    return products

@lru_cache(maxsize=None)
async def filter_items(collection_name:str, p:dict, page:int, page_size:int, skip:int, limit:int, sort_by:str, sort_order:int):
    print("Fetching: ",collection_name)
    try:
        items = await db[collection_name].find(p).skip(skip).limit(limit).sort(sort_by, sort_order).to_list(length=None)
    except Exception as e:
        print("Error: ", e)
    return items

import pymongo.errors
async def create_document(collection_name: str, document: Any):
    try:
        collection = db[collection_name]
        result = await collection.insert_one(document)
        return str(result.inserted_id)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # Handle any other exceptions like connection errors, or database issues
        raise HTTPException(status_code=500, detail="An error occurred while inserting the document.")
async def filter_one(filters: dict,collection_name:str) -> Any:
    try:
        if not isinstance(filters, dict):
            raise ValueError("Filters must be a dictionary")
        
        product = await db[collection_name].find_one(filters)
        logging.info(f"Filtered product: {product}")
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    except pymongo.errors.PyMongoError as e:
        logging.error(f"MongoDB Error: {e}")
        raise HTTPException(status_code=500, detail="Database Error")
    except ValueError as e:
        logging.error(f"Input Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
async def update_document(collection_name: str, filter_criteria: dict, update_data: dict) -> bool:
    """
    Update a document in the specified collection.

    :param collection_name: Name of the collection where the document resides.
    :param filter_criteria: Dictionary specifying the criteria to match the document.
    :param update_data: Dictionary specifying the fields to update.
    :return: True if the document was updated, False if no document matched the criteria.
    :raises: HTTPException if the update fails.
    """
    try:
        collection = db[collection_name]
        result = await collection.update_one(filter_criteria, {"$set": update_data})
        if result.matched_count == 0:
            return False
        return result.modified_count > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")
