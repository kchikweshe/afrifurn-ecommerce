import os
from typing import Any, List, Optional
from fastapi import APIRouter, Form, HTTPException, Query
from httpcore import NetworkError
from pydantic import ValidationError
from pymongo import ReturnDocument

from models.products import Dimensions, Product
from  models.common import ErrorResponseModel, ResponseModel
from database import db
from bson import ObjectId

from services.product import IMAGES_DIR, extract_product_information, fetch_one, filter_one_product, filter_products, insert_into_db

os.makedirs(IMAGES_DIR, exist_ok=True)


router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)



@router.get("/filter",response_model=List[Product])
async def filter_products_route(
    start_price: float = Query(None, description="Depth of the product"),
    end_price: float = Query(None, description="Depth of the product"),
   short_name=Query(None, description="Color of the product"),
    color: str = Query(None, description="Color of the product"),
    width: float = Query(None, description="Width of the product"),
    length: float = Query(None, description="Length of the product"),
    depth: float = Query(None, description="Depth of the product"),
    height: float = Query(None, description="Height of the product"),
    material: str = Query(None, description="Material of the product"),
    category: str = Query(None, description="Category of the product"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of products per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
 name: str = Query(None, description="Name of the product"),

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

     # Calculate skip and limit for pagination
    skip = (page - 1) * page_size
    limit = page_size
    query_criteria:dict =  {}

    try:
        # Define query criteria for price and other attributes
        if start_price is not None and end_price is not None:
            if(start_price>=end_price):
                return ResponseModel(message="Start price cannot be greater than or equal to end price. ")
            query_criteria["price"] =  {"$gte": start_price, "$lte": end_price}
        if name is not None:
            query_criteria["name"] ={"$regex": name,"$options": "i"}
        # if category:
        #     query_criteria["category.short_name"] = category
        if short_name is not None:
            query_criteria["short_name"] ={"$regex": short_name
                                           ,"$options": "i"}
        if color is not None:
            query_criteria["variants.color.color_code"] = color.replace("%23","#")
        if width is not None:
            query_criteria["dimensions.width"] = width
        if length is not None:
            query_criteria["dimensions.length"] = {"$gte": length}
        if depth is not None:
            query_criteria["dimensions.depth"] = depth
        if height is not None:
            query_criteria["dimensions.height"] = height
        if material is not None:
            query_criteria["material.name"] = material
        if category is not None:
            query_criteria["category.id"] = category
            # Use the provided parameters to filter products

    except ValidationError as e:
        # Invalid input error handling
        raise HTTPException(status_code=422, detail=str(e))
    
    # Perform filtering and return products
    try:
        # This part will depend on how you retrieve products in your application
        filtered_products =  await filter_products(
                                              filters=  query_criteria,
                                              page=page,
                                              page_size=page_size,
                                              skip=skip,
                                              limit=limit,
                                              sort_by=sort_by,
                                              sort_order=sort_order

                                                  )  # Added 'await' keyword
        if filtered_products is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve products")
        print("Filtered products: ",len(filtered_products))
        return filtered_products
    except NetworkError as ne:
        # Network error handling
        raise HTTPException(status_code=503, detail=f"Service unavailable, please try again later. {ne}")
    except Exception as e:
        print(e.__cause__)
        # Exception handling
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.get("/", response_model=List[Product])
async def get_products():
    try:
         products =  await db["products"].find().to_list(length=None)
    except  Exception as e:
        print(e)
    return products

@router.get("/filter-one",response_model=Product)
async def filter_product(
    id:str=Query(None, description="Id of the product"),
    short_name: str = Query(None, description="Short name of the product"),
    name: str = Query(None, description="Name of the product"),
): 
    query_criteria:dict =  {}
    if name:
        query_criteria["name"] ={"$regex": name,"$options": "i"}
    if id:
        query_criteria["_id"] =id
    if short_name:
        query_criteria["short_name"] = short_name


    # Perform filtering and return products
    try:
        # This part will depend on how you retrieve products in your application

        filtered_product = await filter_one_product(
                    query_criteria

        )  # Added 'await' keyword
        if filtered_product is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve product")
        result = await db['products'].update_one({"_id": filtered_product['_id']}, {"$inc": {"views": 1}})

    # Check if the document was found and updated
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        print('Product views count updated')
    except NetworkError as ne:
        # Network error handling
        raise HTTPException(status_code=503, detail="Service unavailable, please try again later")
    except Exception as e:
        print(e)
        # Exception handling
        raise HTTPException(status_code=500, detail="Internal server error")
    return filtered_product

@router.post("/", response_model=Any, response_model_by_alias=False)
async def create_product(
    name: str = Form(...),
    short_name:str=Form(),
    category: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    currency_code: str = Form(...),
    width: float = Form(gt=0),
    colors: List[str] = Form(...),
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

    parent_category, currency, material, color = await extract_product_information(currency_code, material_data, category_id,colors)


    if parent_category is None:
        return ResponseModel( code=404, message=f"Category {category_id} not found")
    if currency is None:
        return ResponseModel( code=404, message="Currency not found")
    if material is None:
        return ResponseModel( code=404, message=f"Material {material_id} not found")

    for color in colors:
        if color is None:
            return ErrorResponseModel(error=colors, code=404, message="Color not found.")

    dimensions = Dimensions(depth=depth, height=height, weight=weight, width=width,length=length)

    product = Product(name=name,  description=description, 
                      short_name=short_name,
                      currency=currency,
                      material=material,
                      colors=colors,
                      category=parent_category, price=price, dimensions=dimensions)

    inserted_product = await insert_into_db(name="products",item=product)
    if inserted_product is None:
        raise HTTPException(status_code=500, detail={f'Error. {inserted_product}'})


    return ResponseModel(data={}, code=201, message="Product added successfully")




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