"""
Product router implementation following SOLID principles.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body, UploadFile, File, status
from fastapi.responses import FileResponse
import logging
import os
import pandas as pd
from datetime import datetime

from core.interfaces import IService
from core.exceptions import (
    NotFoundError, 
    ValidationError, 
    BusinessLogicError,
    DatabaseError,
    DuplicateError
)
from core.dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductFilterParams,
    PaginationParams,
    SortParams,
    PaginatedResponseDTO,
    BulkImportResultDTO
)
from services.product_service import ProductService
from models.products import Product
from utils.auth import verify_api_key
from utils.validators import validate_csv_file, validate_csv_headers
from utils.decorators import log_operation


router = APIRouter(prefix="/products", tags=["Products"])


def get_product_service() -> IService[Product]:
    """Dependency injection for product service."""
    return ProductService()


@router.get("/", response_model=PaginatedResponseDTO)
@log_operation("Get all products")
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, ge=-1, le=1, description="Sort order (1=asc, -1=desc)"),
    service: IService[Product] = Depends(get_product_service)
):
    """
    Get all products with pagination.
    
    Args:
        page: Page number
        page_size: Items per page
        sort_by: Field to sort by
        sort_order: Sort order
        service: Product service dependency
        
    Returns:
        Paginated list of products
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        sort = SortParams(sort_by=sort_by, sort_order=sort_order)
        
        products = await service.get_all_entities(
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        total = len(products)  # In a real implementation, get total from repository
        
        return PaginatedResponseDTO(
            items=[product.dict() for product in products],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=(total + pagination.page_size - 1) // pagination.page_size,
            has_next=pagination.page * pagination.page_size < total,
            has_prev=pagination.page > 1
        )
        
    except Exception as e:
        logging.error(f"Failed to get all products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )


@router.get("/{product_id}", response_model=Product)
@log_operation("Get product by ID")
async def get_product_by_id(
    product_id: str,
    service: IService[Product] = Depends(get_product_service)
):
    """
    Get product by ID.
    
    Args:
        product_id: Product ID
        service: Product service dependency
        
    Returns:
        Product details
    """
    try:
        product = await service.get_entity_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        return product
        
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Failed to get product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve product"
        )


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
@log_operation("Create product")
async def create_product(
    product_data: ProductCreateDTO = Body(...),
    service: IService[Product] = Depends(get_product_service),
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new product.
    
    Args:
        product_data: Product creation data
        service: Product service dependency
        api_key: API key for authentication
        
    Returns:
        Created product
    """
    try:
        product = await service.create_entity(product_data)
        return product
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except BusinessLogicError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Failed to create product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


@router.put("/{product_id}", response_model=Product)
@log_operation("Update product")
async def update_product(
    product_id: str,
    product_data: ProductUpdateDTO = Body(...),
    service: IService[Product] = Depends(get_product_service),
    api_key: str = Depends(verify_api_key)
):
    """
    Update a product.
    
    Args:
        product_id: Product ID
        product_data: Product update data
        service: Product service dependency
        api_key: API key for authentication
        
    Returns:
        Updated product
    """
    try:
        product = await service.update_entity(product_id, product_data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        return product
        
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Failed to update product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_operation("Delete product")
async def delete_product(
    product_id: str,
    service: IService[Product] = Depends(get_product_service),
    api_key: str = Depends(verify_api_key)
):
    """
    Delete a product (soft delete).
    
    Args:
        product_id: Product ID
        service: Product service dependency
        api_key: API key for authentication
    """
    try:
        success = await service.delete_entity(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Failed to delete product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )


@router.get("/filter/advanced", response_model=PaginatedResponseDTO)
@log_operation("Filter products")
async def filter_products(
    search: Optional[str] = Query(None, description="Search term"),
    start_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    end_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    category_id: Optional[str] = Query(None, description="Category ID"),
    material_id: Optional[str] = Query(None, description="Material ID"),
    color_ids: List[str] = Query(default_factory=list, description="Color IDs"),
    min_width: Optional[float] = Query(None, ge=0, description="Minimum width"),
    max_width: Optional[float] = Query(None, ge=0, description="Maximum width"),
    min_height: Optional[float] = Query(None, ge=0, description="Minimum height"),
    max_height: Optional[float] = Query(None, ge=0, description="Maximum height"),
    min_depth: Optional[float] = Query(None, ge=0, description="Minimum depth"),
    max_depth: Optional[float] = Query(None, ge=0, description="Maximum depth"),
    min_length: Optional[float] = Query(None, ge=0, description="Minimum length"),
    max_length: Optional[float] = Query(None, ge=0, description="Maximum length"),
    min_weight: Optional[float] = Query(None, ge=0, description="Minimum weight"),
    max_weight: Optional[float] = Query(None, ge=0, description="Maximum weight"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, ge=-1, le=1, description="Sort order"),
    service: ProductService = Depends(get_product_service)
):
    """
    Filter products with advanced criteria.
    
    Args:
        search: Search term
        start_price: Minimum price
        end_price: Maximum price
        category_id: Category ID
        material_id: Material ID
        color_ids: Color IDs
        min_width: Minimum width
        max_width: Maximum width
        min_height: Minimum height
        max_height: Maximum height
        min_depth: Minimum depth
        max_depth: Maximum depth
        min_length: Minimum length
        max_length: Maximum length
        min_weight: Minimum weight
        max_weight: Maximum weight
        page: Page number
        page_size: Items per page
        sort_by: Field to sort by
        sort_order: Sort order
        service: Product service dependency
        
    Returns:
        Paginated filtered products
    """
    try:
        filters = ProductFilterParams(
            search=search,
            start_price=start_price,
            end_price=end_price,
            category_id=category_id,
            material_id=material_id,
            color_ids=color_ids,
            min_width=min_width,
            max_width=max_width,
            min_height=min_height,
            max_height=max_height,
            min_depth=min_depth,
            max_depth=max_depth,
            min_length=min_length,
            max_length=max_length,
            min_weight=min_weight,
            max_weight=max_weight
        )
        
        pagination = PaginationParams(page=page, page_size=page_size)
        sort = SortParams(sort_by=sort_by, sort_order=sort_order)
        
        return await service.find_products_by_filters(filters, pagination, sort)
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Failed to filter products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to filter products"
        )


@router.get("/new", response_model=List[Product])
@log_operation("Get new products")
async def get_new_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    service: ProductService = Depends(get_product_service)
):
    """
    Get new products.
    
    Args:
        limit: Number of products to return
        service: Product service dependency
        
    Returns:
        List of new products
    """
    try:
        return await service.get_new_products(limit)
        
    except Exception as e:
        logging.error(f"Failed to get new products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get new products"
        )


@router.get("/popular", response_model=List[Product])
@log_operation("Get popular products")
async def get_popular_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    service: ProductService = Depends(get_product_service)
):
    """
    Get popular products.
    
    Args:
        limit: Number of products to return
        service: Product service dependency
        
    Returns:
        List of popular products
    """
    try:
        return await service.get_popular_products(limit)
        
    except Exception as e:
        logging.error(f"Failed to get popular products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get popular products"
        )


@router.get("/search", response_model=PaginatedResponseDTO)
@log_operation("Search products")
async def search_products(
    q: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, ge=-1, le=1, description="Sort order"),
    service: ProductService = Depends(get_product_service)
):
    """
    Search products by term.
    
    Args:
        q: Search term
        page: Page number
        page_size: Items per page
        sort_by: Field to sort by
        sort_order: Sort order
        service: Product service dependency
        
    Returns:
        Paginated search results
    """
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        sort = SortParams(sort_by=sort_by, sort_order=sort_order)
        
        return await service.search_products(q, pagination, sort)
        
    except Exception as e:
        logging.error(f"Failed to search products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search products"
        )


@router.post("/bulk-import", response_model=BulkImportResultDTO)
@validate_csv_file
@validate_csv_headers
@log_operation("Bulk import products")
async def bulk_import_products(
    file: UploadFile = File(...),
    service: ProductService = Depends(get_product_service),
    api_key: str = Depends(verify_api_key)
):
    """
    Bulk import products from CSV file.
    
    Args:
        file: CSV file with product data
        service: Product service dependency
        api_key: API key for authentication
        
    Returns:
        Import results
    """
    try:
        start_time = datetime.now()
        
        # Read CSV file
        df = pd.read_csv(file.file)
        total_processed = len(df)
        successful = 0
        failed = 0
        errors = []
        
        # Process each row
        for index, row in df.iterrows():
            try:
                # Convert row to DTO
                product_data = ProductCreateDTO(**row.to_dict())
                
                # Create product
                await service.create_entity(product_data)
                successful += 1
                
            except Exception as e:
                failed += 1
                errors.append({
                    "row": index + 1,
                    "error": str(e),
                    "data": row.to_dict()
                })
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return BulkImportResultDTO(
            total_processed=total_processed,
            successful=successful,
            failed=failed,
            errors=errors,
            processing_time=processing_time
        )
        
    except Exception as e:
        logging.error(f"Failed to bulk import products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to import products"
        )


@router.get("/bulk-import/template")
@log_operation("Download bulk import template")
async def download_bulk_import_template():
    """
    Download bulk import template.
    
    Returns:
        CSV template file
    """
    try:
        template_path = "bulk_import_template.csv"
        if not os.path.exists(template_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template file not found"
            )
        
        return FileResponse(
            template_path,
            media_type="text/csv",
            filename="product_import_template.csv"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to download template: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download template"
        ) 