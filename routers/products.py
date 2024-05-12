import asyncio
import os
from typing import Any, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import Response
from httpcore import NetworkError
from pydantic import ValidationError
from pymongo import ReturnDocument
from bson.json_util import dumps

from models.products import Dimensions, Product
from  models.common import ErrorResponseModel, ResponseModel
from database import db
from bson import ObjectId

from dto.models import ProductFilter
from routers.product_variants import allowed_file, convert_to_webp, readImage, save_image
DEFAULT_IMAGES_DIR = "static/product/"  # Default image storage directory
IMAGES_DIR = os.getenv("PRODUCT_IMAGES_DIR", DEFAULT_IMAGES_DIR)  # Read from environment variable
os.makedirs(IMAGES_DIR, exist_ok=True)


router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)



async def filter_products(p:dict):

    print(p)
    try:
         products =  await db["products"].find(p).to_list(length=None)
          # Convert MongoDB documents to Python dictionaries
         products_data = [product for product in products]
        # Convert Python dictionaries to JSON format
         products_json = dumps(products_data)
    except  Exception as e:
        print("Error: ",e)
    return products_json
@router.get("/products/filter")
async def filter_products_route(
    start_price: float = Query(None, description="Depth of the product"),
    end_price: float = Query(None, description="Depth of the product"),

    color: str = Query(None, description="Color of the product"),
    width: float = Query(None, description="Width of the product"),
    length: float = Query(None, description="Length of the product"),
    depth: float = Query(None, description="Depth of the product"),
    height: float = Query(None, description="Height of the product"),
    material: str = Query(None, description="Material of the product"),
    category: str = Query(None, description="Category of the product")
):
    """
    Filters products based on the provided parameters.

    Args:
        startPrice (float, optional): The minimum price of the products. Defaults to None.
        endPrice (float, optional): The maximum price of the products. Defaults to None.
        length (float, optional): The length of the products. Defaults to None.
        width (float, optional): The width of the products. Defaults to None.
        height (float, optional): The height of the products. Defaults to None.
        depth (float, optional): The depth of the products. Defaults to None.
        categories (List[str], optional): The categories of the products. Defaults to None.
        material_code (str, optional): The material code of the products. Defaults to None.

    Returns:
        dict: A dictionary containing a success message and the filtered products.
    """
    if(start_price>=end_price):
        return ResponseModel(message="Start price cannot be greater or equal than end price. ")
    query_criteria:dict = {"price": {"$gte": start_price, "$lte": end_price}}

    try:
        # Define query criteria for price and other attributes
        if color:
            query_criteria["color.color_code"] = color
        if width:
            query_criteria["dimensions.width"] = width
        if length:
            query_criteria["dimensions.length"] = length
        if depth:
            query_criteria["dimensions.depth"] = depth
        if height:
            query_criteria["dimensions.height"] = height
        if material:
            query_criteria["material.name"] = material
        if category:
            query_criteria["category.id"] = category
            # Use the provided parameters to filter products

    except ValidationError as e:
        # Invalid input error handling
        raise HTTPException(status_code=422, detail=str(e))
    
    # Perform filtering and return products
    try:
        # This part will depend on how you retrieve products in your application
        filtered_products = await filter_products(query_criteria)  # Added 'await' keyword
        if filtered_products is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve products")
        return {"message": "Products filtered with provided parameters", "products": filtered_products}
    except NetworkError as ne:
        # Network error handling
        raise HTTPException(status_code=503, detail="Service unavailable, please try again later")
    except Exception as e:
        print(e)
        # Exception handling
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[Product])
async def get_products():
    try:
         products =  await db["products"].find().to_list(length=None)
        

    except  Exception as e:
        print(e)
    return products



@router.post("/", response_model=Any, response_model_by_alias=False)
async def create_product(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    currency_code: str = Form(...),
    width: float = Form(gt=0),
    color_code: str = Form(...),
    quantity: int = Form(gt=0),
    images: List[UploadFile] = [],
    height: float = Form(gt=0),
    length: float = Form(gt=0),
    depth: Optional[float|None] = Form(gt=0,default=None),
    weight:  Optional[float|None] = Form(gt=0,default=None),
    material_id: str = Form(...),

) -> ResponseModel: # type: ignore
    
    """
    Create a new product.

    Args:
        name (str): The name of the product.
        category (str): The ID of the category the product belongs to.
        price_of_item (float): The price of the product.
        description (str): The description of the product.
        currency_code (str): The currency code of the product price.
        width (float): The width of the product dimensions.
        color_code (str): The color code of the product.
        quantity (str): The quantity of the product in stock.
        images (List[UploadFile]): The list of uploaded images for the product.
        height (float): The height of the product dimensions.
        depth (Optional[float]): The depth of the product dimensions.
        weight (Optional[float]): The weight of the product dimensions.

    Returns:
        Any: A response indicating that the product was added successfully.
    """
    try:
        category_id = ObjectId(category)
        material_data=ObjectId(material_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    parent_category, currency, material, color = await extract_data(currency_code, material_data, category_id,color_code)
    print("Image count : ",images.count)
    if len(images)==0:
        return ResponseModel( code=400, message=f"No images provided for the product")


    if parent_category is None:
        return ResponseModel( code=404, message=f"Category {category_id} not found")
    if currency is None:
        return ResponseModel( code=404, message="Currency not found")
    if material is None:
        return ResponseModel( code=404, message=f"Material {material_id} not found")


    if color is None:
        return ErrorResponseModel(error=color_code, code=404, message="Color not found.")

    dimensions = Dimensions(depth=depth, height=height, weight=weight, width=width,length=length)

    product = Product(name=name, color=color, description=description, 
                      currency=currency,
                      material=material,
                      quantity_in_stock=quantity,
                      category=parent_category, price=price, dimensions=dimensions)

    inserted_product = await insert_into_db(name="products",product=product)
    file_paths = []

    

    tasks = [process_image(image,i,inserted_product) for i, image in enumerate(images)]
    file_paths = await asyncio.gather(*tasks)

    data = {
        k: v for k, v in product.model_dump(by_alias=True).items() if v is not None
    }
    if inserted_product is None:
        raise HTTPException(status_code=500, detail={f'Error. {inserted_product}'})
    data["images"] = file_paths
    data["_id"] = inserted_product.inserted_id
    update_result = await update_existing_product(data)
    print("Update: ", update_result)

    return ResponseModel(data={}, code=201, message="Product added successfully")

async def process_image(image:UploadFile,i:int,inserted_product:Any):
        """
Process an uploaded image file.

Parameters:
- image (UploadFile): The uploaded image file.
- i (int): The index of the image in the list of images.
- inserted_product (Any): The inserted product object.

Returns:
- str: The file path where the processed image is saved.

Raises:
- HTTPException: If the file extension is not allowed.

"""
        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

        contents = await image.read()
        img = readImage(contents)

        webp_contents = convert_to_webp(img)
        filename = f"{inserted_product.inserted_id}image{i}.webp"
        file_path = os.path.join(IMAGES_DIR, filename)

        save_image(webp_contents, file_path)
        return file_path
async def update_existing_product(data)->str:
    """
Process an uploaded image file.

Parameters:
- image (UploadFile): The uploaded image file.
- i (int): The index of the image in the list of images.
- inserted_product (Any): The inserted product object.

Returns:
- str: The file path where the processed image is saved.

Raises:
- HTTPException: If the file extension is not allowed.
"""

    return await db["products"].find_one_and_update(
        {"_id": data['_id']},
        {"$set": {"images": data['images']}},
        return_document=ReturnDocument.AFTER,
    )

async def insert_into_db(name:str,product:Product):
  
    inserted_object = await db[f'{name}'].insert_one(product.model_dump(exclude=["id"])) # type: ignore
    return inserted_object

async def extract_data(currency_code, material_id, category_id,color_code):
    print(type(material_id))
    parent_category = await fetch_one(collection_name="level2_categories",value=category_id)
    currency = await fetch_one(collection_name="currencies",key='code',value=currency_code)
    material=await fetch_one(collection_name='materials',value=material_id)
    color = await fetch_one(collection_name='colors',key='color_code',value=color_code)

    return parent_category,currency,material,color

def fetch_one(collection_name:str,key:str="_id",value:str=''):
    return db[collection_name].find_one({key: value})



# @router.delete('{id}')
# async def delete_product(id: str):
#     delete_result = await db["products"].delete({"id", ObjectId(id)})
#     if delete_result.delete_count == 1:raise HTTPException(status_code=404, detail=f"Product {id} not found")

#     update_result = await db["products"].update_one(
#         {"id": ObjectId(id)},
#         {"$set": product_updates.dict(exclude_unset=True, exclude_expr="$")})  # Exclude unset and expressions
    
#     if update_result.modified_count == 0:
#         raise HTTPException(status_code=404, detail="Product not found")

#     # Fetch the updated product for response (optional)
#     updated_product = await db["products"].find_one({"id": ObjectId(productid)})
#     return updated_product