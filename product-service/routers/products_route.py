from fastapi import APIRouter, Form, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
import logging

from models.products import CategoryProducts, Dimensions, Product, ProductPipeline
from models.common import ResponseModel
from utils.query_builder import build_product_query
from database import db

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/filter", response_model=ResponseModel)
async def filter_products_route(
    start_price: Optional[float] = Query(None, description="Minimum price"),
    end_price: Optional[float] = Query(None, description="Maximum price"),
    short_name: Optional[str] = Query(None, description="Short name"),
    colors: str = Query('[]', description="Colors (JSON array)"),
    materials: str = Query('[]', description="Materials (JSON array)"),
    width: float = Query(None, description="Product width"),
    length: Optional[float] = Query(None, description="Product length"), 
    depth: Optional[float] = Query(None, description="Product depth"),
    height: Optional[float] = Query(None, description="Product height"),
    weight: Optional[float] = Query(None, description="Product weight"),
    category_short_name: Optional[str] = Query(None, description="Category short name"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
    name: Optional[str] = Query(None, description="Product name")
):
    """Filter products based on various criteria"""
    try:
        skip = (page - 1) * page_size

        query_criteria = build_product_query(
            start_price=start_price,
            end_price=end_price,
            name=name,
            short_name=short_name,
            colors=colors,
            materials=materials,
            dimensions={
                "length":length,
                "width":width,
                "height":height,
                "depth":depth

            },
            category_short_name=category_short_name,
        )
        
        # Add default criteria
        query_criteria["is_archived"] = False
        
        logging.info(f"Query criteria: {query_criteria}")

        # Get products with a pipeline to properly handle nested objects
        pipeline = [
            {"$match": query_criteria},
            {
                "$addFields": {
                    "category._id": "$category.id",
                    "category.level_one_category._id": "$category.level_one_category.id",
                    "category.level_one_category.category._id": "$category.level_one_category.category.id",
                    "dimensions._id": "$dimensions.id"
                }
            },
            {"$sort": {sort_by: sort_order}},
            {"$skip": skip},
            {"$limit": page_size}
        ]
        
        logging.info(f"Pipeline: {pipeline}")
        cursor = db['products'].aggregate(pipeline)
        products = [Product(**item)  for item in cursor]
        logging.info(f"Found {len(products)} products")
            
        return ResponseModel.create(
            class_name="Product",
            data=products,
            message="Products retrieved successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error filtering products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/filter-one", response_model=ResponseModel)
async def filter_product(
    id: str = Query(None, description="Product ID"),
    short_name: Optional[str] = Query(None, description="Short name"),
    name: Optional[str] = Query(None, description="Product name")
):
    """Get a single product by various criteria"""
    query_criteria = {
        k: v for k, v in {
            "name": {"$regex": name, "$options": "i"} if name else None,
            "_id": id,
            "short_name": {"$regex": short_name, "$options": "i"}
        }.items() if v is not None
    }

    try:
        product:Product|None =  db["products"].find_one(query_criteria)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        updated= db["products"].update_one({"_id":product["_id"]}, {"$inc": {"views": 1}})
        if not updated:
             raise HTTPException(status_code=500, detail="Internal server error")
        product["_id"]= str(product["_id"])
        return ResponseModel.create(
            class_name="Product",
            data=product,
            message="Product retrieved successfully"
        )
    except Exception as e:
        logging.error(f"Error retrieving product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=ResponseModel)
async def create_product(
    id: Optional[str] = None ,
    name: str = Query(...),
    short_name: str = Query(...),
    category: str = Query(...),
    price: float = Query(...),
    description: str = Query(...),
    currency_code: str = Form(...),
    width: float = Query(...),
    length: float = Query(...),
    weight: float = Query(None, description="Weight in grams"),
    height: float = Query( description="Height in mm"),
    depth: float = Query(None, description= "Depth in mm"),
    colors: List[str] = Query(...),
    material_id: str = Query(...),
) -> ResponseModel:
    """Create a new product"""
    try:
        category_id = ObjectId(category)
        material_data = ObjectId(material_id)
        
        # Get related data
        level2_category =   db["level2_categories"].find_one({"_id":category_id})
        if not level2_category:
            raise HTTPException(status_code=400, detail="Invalid category ID")

        dimensions = Dimensions(width=width,
                                 length=length, 
                                 height=height,
                                   depth=depth, weight=weight)
        
       

        product = Product(
            name=name,
            description=description,
            short_name=short_name,
            currency=currency_code,
            material=material_id,
            color_codes=colors,
            category=level2_category,
            price=price,
            dimensions=dimensions
        )

        inserted_product =  db["products"].insert_one(product.model_dump())
        if not inserted_product:
            raise HTTPException(status_code=500, detail="Failed to create product")

        return ResponseModel.create(
            class_name="Product",
            status_code=201,
            message="Product added successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/by-level-two-category/filter", response_model=ResponseModel)
async def get_products_by_level_two_category(
    short_name: str = Query(..., description="Level 2 category name"),
    limit: int = Query(10, description="Number of products to return"),
    skip: int = Query(0, description="Number of products to skip"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)")
):
    """Get products by Level 2 category name"""
    try:
        # Use aggregation pipeline for better performance and flexibility
        pipeline = [
            {"$match": {
                "category.name": short_name,
                "is_archived": False  # Add this if you want to exclude archived products
            }},
            {"$sort": {sort_by: sort_order}},
            {"$skip": skip},
            {"$limit": limit}
        ]
        
        products =  db["products"].aggregate(pipeline)
        data = [Product(**product) for product in products]
        
        return ResponseModel.create(
            class_name="Product",
            data=data,
            message="Products retrieved successfully"
        )
    except Exception as e:
        logging.error(f"Error retrieving products by level two category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
 
@router.get("/by-level-one-category", response_model=ResponseModel)
async def get_products_by_level_one_category(
    name: str = Query(..., description="Level 1 category name"),
    limit: int = Query(10, description="Number of products to return")
):
    """Get products by Level 1 category name"""
    try:
        pipeline = ProductPipeline.get_products_by_level_one_category_name(name, limit)
        products =  db["products"].aggregate(pipeline)
        products= [CategoryProducts(**product) for product in products]
        return ResponseModel.create(
            class_name="Product",
            data=products or [],
            message="Products retrieved successfully"
        )
    except Exception as e:
        logging.error(f"Error retrieving products by level one category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/by-category", response_model=CategoryProducts)
async def get_products_by_category(category_name:str):
    """Get products grouped by category"""
    try:
        pipeline = ProductPipeline.get_products_by_category(name=category_name)
        category_products =  db["products"].aggregate(pipeline)
        
        if category_products is None:
            raise HTTPException(status_code=404, detail="No products found for the specified category")

        return ResponseModel.create(
            class_name="Product",
            data=category_products or [],
            message="Products grouped by category retrieved successfully"
        )
    except Exception as e:
        logging.error(f"Error retrieving products by category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")