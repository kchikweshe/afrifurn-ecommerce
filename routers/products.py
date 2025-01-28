# from fastapi import APIRouter, Form, Body, HTTPException, Query
# from typing import Any, List, Optional
# from bson import ObjectId
# import logging

# from models.products import Dimensions, Product
# from models.common import ErrorResponseModel, ResponseModel
# from services.product_service import ProductService
# from utils.query_builder import build_product_query
# from utils.validators import validate_product_data, validate_object_ids
# from database import db

# router = APIRouter(prefix="/products", tags=["Products"])

# # Inject ProductService with required repositories
# product_service = ProductService(
#     repository=db["products"],
#     color_repository=db["colors"],
#     material_repository=db["materials"],
#     currency_repository=db["currencies"],
#     level2category_repository=db["categories"]
# )

# @router.get("/filter", response_model=ResponseModel)
# async def filter_products_route(
#     start_price: Optional[float] = Query(None, description="Minimum price"),
#     end_price: Optional[float] = Query(None, description="Maximum price"),
#     short_name: Optional[str] = Query(None, description="Short name"),
#     colors: str = Query('[]', description="Colors (JSON array)"),
#     materials: str = Query('[]', description="Materials (JSON array)"),
#     width: float = Query(None, description="Product width"),
#     length: float = Query(None, description="Product length"), 
#     depth: float = Query(None, description="Product depth"),
#     height: float = Query(None, description="Product height"),
#     weight: float = Query(None, description="Product weight"),
#     category: Optional[str] = Query(None, description="Category name"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of items per page"),
#     sort_by: str = Query("_id", description="Field to sort by"),
#     sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
#     name: Optional[str] = Query(None, description="Product name")
# ):
    
#     dimensions = Dimensions(width=width, length=length, depth=depth, height=height, weight=weight   )
#     """Filter products based on various criteria"""
#     try:
#         query_criteria = build_product_query(
#             start_price=start_price,
#             end_price=end_price,
#             name=name,
#             short_name=short_name,
#             colors=colors,
#             materials=materials,
#             dimensions=dimensions.model_dump(),
#             category=category
#         )
        
#         skip = (page - 1) * page_size
        
#         products = await product_service.filter(
#             filters=query_criteria,
#             skip=skip,
#             limit=page_size,
#             sort_by=sort_by,
#             sort_order=sort_order
#         )
        
#         return ResponseModel.create(
#             class_name="Product",
#             data=products,
#             message="Products retrieved successfully"
#         )
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         logging.error(f"Error filtering products: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @router.get("/filter-one", response_model=ResponseModel)
# async def filter_product(
#     id: str = Query(None, description="Product ID"),
#     short_name: Optional[str] = Query(None, description="Short name"),
#     name: Optional[str] = Query(None, description="Product name")
# ):
#     """Get a single product by various criteria"""
#     query_criteria = {
#         k: v for k, v in {
#             "name": {"$regex": name, "$options": "i"} if name else None,
#             "_id": id,
#             "short_name": short_name
#         }.items() if v is not None
#     }

#     try:
#         product = await product_service.get_one(item_id=id)
#         if not product:
#             raise HTTPException(status_code=404, detail="Product not found")
            
#         await product_service.increment_product_views(str(product.id))
#         return ResponseModel.create(
#             class_name="Product",
#             data=product,
#             message="Product retrieved successfully"
#         )
#     except Exception as e:
#         logging.error(f"Error retrieving product: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @router.post("/", response_model=ResponseModel)
# async def create_product(
#     name: str = Query(...),
#     short_name: str = Query(...),
#     category: str = Query(...),
#     price: float = Query(...),
#     description: str = Query(...),
#     currency_code: str = Form(...),
#     width: float = Query(...),
#     length: float = Query(...),
#     weight: float = Query(None, description="Weight in grams"),
#     height: float = Query( description="Height in mm"),
#     depth: float = Query(None, description= "Depth in mm"),
#     colors: List[str] = Query(...),
#     material_id: str = Query(...)
# ) -> ResponseModel:
#     """Create a new product"""
#     try:
        
#         # Get related data

#         dimensions = Dimensions(width=width,
#                                  length=length, 
#                                  height=height,
#                                    depth=depth, weight=weight)
#         product = Product(
#             name=name,
#             description=description,
#             short_name=short_name,
#             currency=currency_code,
#             material=material_id,
#             color_codes=colors,
#             category=category,
#             price=price,
#             dimensions=dimensions
#         )

#         inserted_product = await product_service.create(product)
#         if not inserted_product:
#             raise HTTPException(status_code=500, detail="Failed to create product")

#         return ResponseModel.create(
#             class_name="Product",
#             status_code=201,
#             message="Product added successfully"
#         )

#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         logging.error(f"Error creating product: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")