"""
Data Transfer Objects (DTOs) for the AfriFurn product service.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


class SortParams(BaseModel):
    """Sorting parameters."""
    sort_by: str = Field("_id", description="Field to sort by")
    sort_order: int = Field(1, ge=-1, le=1, description="Sort order (1=asc, -1=desc)")


class FilterParams(BaseModel):
    """Base filter parameters."""
    search: Optional[str] = Field(None, description="Search term")
    is_active: Optional[bool] = Field(True, description="Filter by active status")


class ProductFilterParams(FilterParams):
    """Product-specific filter parameters."""
    start_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    end_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    category_id: Optional[str] = Field(None, description="Category ID")
    material_id: Optional[str] = Field(None, description="Material ID")
    color_ids: List[str] = Field(default_factory=list, description="Color IDs")
    min_width: Optional[float] = Field(None, ge=0, description="Minimum width")
    max_width: Optional[float] = Field(None, ge=0, description="Maximum width")
    min_height: Optional[float] = Field(None, ge=0, description="Minimum height")
    max_height: Optional[float] = Field(None, ge=0, description="Maximum height")
    min_depth: Optional[float] = Field(None, ge=0, description="Minimum depth")
    max_depth: Optional[float] = Field(None, ge=0, description="Maximum depth")
    min_length: Optional[float] = Field(None, ge=0, description="Minimum length")
    max_length: Optional[float] = Field(None, ge=0, description="Maximum length")
    min_weight: Optional[float] = Field(None, ge=0, description="Minimum weight")
    max_weight: Optional[float] = Field(None, ge=0, description="Maximum weight")
    
    @validator('end_price')
    def validate_price_range(cls, v, values):
        if v is not None and 'start_price' in values and values['start_price'] is not None:
            if v < values['start_price']:
                raise ValueError('end_price must be greater than or equal to start_price')
        return v


class ProductCreateDTO(BaseModel):
    """DTO for creating a product."""
    name: str = Field(..., min_length=3, max_length=100, description="Product name")
    short_name: str = Field(..., min_length=2, max_length=50, description="Product short name")
    description: str = Field(..., min_length=10, description="Product description")
    category_id: str = Field(..., description="Category ID")
    price: float = Field(..., gt=0, description="Product price")
    currency_code: str = Field(..., min_length=3, max_length=3, description="Currency code")
    material_id: str = Field(..., description="Material ID")
    width: float = Field(..., gt=0, description="Product width")
    length: float = Field(..., gt=0, description="Product length")
    height: float = Field(..., gt=0, description="Product height")
    depth: Optional[float] = Field(None, gt=0, description="Product depth")
    weight: Optional[float] = Field(None, gt=0, description="Product weight in grams")
    color_ids: List[str] = Field(default_factory=list, description="Color IDs")
    product_features: List[Dict[str, str]] = Field(default_factory=list, description="Product features")


class ProductUpdateDTO(BaseModel):
    """DTO for updating a product."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    short_name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=10)
    category_id: Optional[str] = Field(None)
    price: Optional[float] = Field(None, gt=0)
    currency_code: Optional[str] = Field(None, min_length=3, max_length=3)
    material_id: Optional[str] = Field(None)
    width: Optional[float] = Field(None, gt=0)
    length: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    depth: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    color_ids: Optional[List[str]] = Field(None)
    product_features: Optional[List[Dict[str, str]]] = Field(None)
    is_new: Optional[bool] = Field(None)
    discount: Optional[float] = Field(None, ge=0, le=100)


class ProductResponseDTO(BaseModel):
    """DTO for product responses."""
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    short_name: str = Field(..., description="Product short name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    currency_code: str = Field(..., description="Currency code")
    category: Dict[str, Any] = Field(..., description="Category information")
    material: Dict[str, Any] = Field(..., description="Material information")
    dimensions: Dict[str, Any] = Field(..., description="Product dimensions")
    colors: List[Dict[str, Any]] = Field(default_factory=list, description="Product colors")
    product_features: List[Dict[str, Any]] = Field(default_factory=list, description="Product features")
    is_new: bool = Field(..., description="Is new product")
    discount: Optional[float] = Field(None, description="Discount percentage")
    views: int = Field(..., description="View count")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class PaginatedResponseDTO(BaseModel):
    """DTO for paginated responses."""
    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")


class BulkImportResultDTO(BaseModel):
    """DTO for bulk import results."""
    total_processed: int = Field(..., description="Total records processed")
    successful: int = Field(..., description="Successfully imported records")
    failed: int = Field(..., description="Failed records")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="Import errors")
    processing_time: float = Field(..., description="Processing time in seconds")


class CacheKeyDTO(BaseModel):
    """DTO for cache key generation."""
    prefix: str = Field(..., description="Cache key prefix")
    params: Dict[str, Any] = Field(default_factory=dict, description="Cache parameters")
    
    def generate_key(self) -> str:
        """Generate cache key from prefix and parameters."""
        param_str = ":".join(f"{k}={v}" for k, v in sorted(self.params.items()))
        return f"{self.prefix}:{param_str}" if param_str else self.prefix 