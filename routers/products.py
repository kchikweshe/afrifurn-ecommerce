from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
import asyncio

from models.products import Dimensions, Product
from models.common import ErrorResponseModel, ResponseModel
from services.repository.product_repository import ProductRepository
from services.repository.color_repository import ColorRepository
from services.repository.material_repository import MaterialRepository
from services.repository.currency_repository import CurrencyRepository
from services.repository.level2_category_repository import Level2CategoryRepository
from utils.query_builder import build_product_query
from utils.validators import validate_product_data, validate_object_ids

router = APIRouter(prefix="/products", tags=["Products"])

# Initialize repositories
product_repo = ProductRepository()
color_repo = ColorRepository()
material_repo = MaterialRepository()
currency_repo = CurrencyRepository()
level2category_repo = Level2CategoryRepository()

@router.get("/filter", response_model=ResponseModel)
async def filter_products_route(
    start_price: Optional[float] = Query(None, description="Minimum price"),
    end_price: Optional[float] = Query(None, description="Maximum price"),
    short_name: Optional[str] = Query(None, description="Short name"),
    colors: str = Query('[]', description="Colors (JSON array)"),
    materials: str = Query('[]', description="Materials (JSON array)"),
    width: float = Query(None, description="Product width"),
    length: float = Query(None, description="Product length"), 
    depth: float = Query(None, description="Product depth"),
    height: float = Query(None, description="Product height"),
    weight: float = Query(None, description="Product weight"),
    category: Optional[str] = Query(None, description="Category name"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
    name: Optional[str] = Query(None, description="Product name")
):
    try:
        dimensions = Dimensions(width=width, length=length, depth=depth, height=height, weight=weight)
        query_criteria = build_product_query(
            start_price=start_price,
            end_price=end_price,
            name=name,
            short_name=short_name,
            colors=colors,
            materials=materials,
            dimensions=dimensions.model_dump(),
            category=category
        )
        
        skip = (page - 1) * page_size
        products = await product_repo.filter(
            filter_query=query_criteria,
            skip=skip,
            limit=page_size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
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
    try:
        product = await product_repo.get_by_id(id) if id else None
        if not product:
            query_criteria = {
                k: v for k, v in {
                    "name": {"$regex": name, "$options": "i"} if name else None,
                    "short_name": short_name
                }.items() if v is not None
            }
            product = await product_repo.find_one(query_criteria)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        await product_repo.update_views(str(product.id))
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
    name: str = Query(...),
    description: str = Query(...),
    short_name: str = Query(...),
    price: float = Query(...),
    currency_code: str = Query(...),
    category_id: str = Query(...),
    width: float = Query(..., description="Width in mm"),
    length: float = Query(..., description="Length in mm"),
    height: float = Query(..., description="Height in mm"),
    depth: float = Query(None, description="Depth in mm"),
    colors: List[str] = Query(...),
    material_id: str = Query(...)
):
    try:
        # Fetch all references in parallel
        category, currency, material, color_docs = await asyncio.gather(
            level2category_repo.get_category({"id": category_id}),
            currency_repo.get_currency({"code": currency_code}),
            material_repo.get_material({"id": material_id}),
            *[color_repo.get_color({"color_id": color}) for color in colors]
        )
        
        if not all([category, currency, material] + color_docs):
            raise HTTPException(
                status_code=404,
                detail="One or more referenced documents not found"
            )
            
        product_data = {
            "name": name,
            "description": description,
            "short_name": short_name,
            "price": price,
            "currency": currency,
            "category": category,
            "dimensions": {
                "width": width,
                "length": length,
                "height": height,
                "depth": depth
            },
            "colors": color_docs,
            "material": material
        }
        
        validate_product_data(product_data)
        product = Product(**product_data)
        success = await product_repo.insert_one(product.model_dump())
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to create product"
            )
            
        return ResponseModel.create(
            class_name="Product",
            data=product,
            message="Product created successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{product_id}", response_model=ResponseModel)
async def delete_product(product_id: str):
    try:
        success = await product_repo.delete(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return ResponseModel.create(
            class_name="Product",
            data=None,
            message="Product deleted successfully"
        )
    except Exception as e:
        logging.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")