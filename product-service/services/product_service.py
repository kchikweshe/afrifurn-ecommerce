"""
Product service implementation following SOLID principles.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from core.interfaces import IService, ICacheService
from core.exceptions import (
    NotFoundError, 
    ValidationError, 
    BusinessLogicError,
    DatabaseError
)
from core.dto import (
    ProductCreateDTO, 
    ProductUpdateDTO, 
    ProductResponseDTO,
    ProductFilterParams,
    PaginationParams,
    SortParams,
    PaginatedResponseDTO
)
from repositories.product_repository import ProductRepository
from models.products import Product
from decorators import create_redis_cache_provider


class ProductService(IService[Product]):
    """
    Product service with business logic implementation.
    
    Follows SOLID principles:
    - Single Responsibility: Handles product business logic
    - Open/Closed: Extensible through inheritance/composition
    - Liskov Substitution: Implements IService interface
    - Interface Segregation: Uses specific interfaces
    - Dependency Inversion: Depends on abstractions
    """
    
    def __init__(self, cache_service: Optional[ICacheService] = None):
        """
        Initialize product service.
        
        Args:
            cache_service: Optional cache service for performance optimization
        """
        self.repository = ProductRepository()
        self.cache_service = cache_service or create_redis_cache_provider()
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    async def create_entity(self, data: ProductCreateDTO) -> Product:
        """
        Create a new product.
        
        Args:
            data: Product creation data
            
        Returns:
            Created product
            
        Raises:
            ValidationError: If data validation fails
            BusinessLogicError: If business rules are violated
            DatabaseError: If database operation fails
        """
        try:
            # Validate business rules
            await self._validate_product_creation(data)
            
            # Create product
            product_id = await self.repository.create(data)
            
            # Get created product
            product = await self.repository.get_by_id(product_id)
            if not product:
                raise DatabaseError("create", "Product was created but could not be retrieved")
            
            # Clear relevant cache
            await self._clear_product_cache()
            
            self.logger.info(f"Created product with ID: {product_id}")
            return product
            
        except (ValidationError, BusinessLogicError, DatabaseError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to create product: {e}")
            raise DatabaseError("create", str(e))
    
    async def get_entity_by_id(self, entity_id: str) -> Optional[Product]:
        """
        Get product by ID with caching.
        
        Args:
            entity_id: Product ID
            
        Returns:
            Product if found, None otherwise
        """
        try:
            # Try cache first
            cache_key = f"product:{entity_id}"
            cached_product = await self.cache_service.get(cache_key)
            if cached_product:
                return Product(**cached_product)
            
            # Get from database
            product = await self.repository.get_by_id(entity_id)
            if product:
                # Cache the result
                await self.cache_service.set(cache_key, product.dict(), ttl_seconds=300)
                
                # Increment view count
                await self.repository.increment_views(entity_id)
            
            return product
            
        except Exception as e:
            self.logger.error(f"Failed to get product {entity_id}: {e}")
            return None
    
    async def get_all_entities(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get all products with pagination.
        
        Args:
            skip: Number of products to skip
            limit: Maximum number of products to return
            
        Returns:
            List of products
        """
        try:
            return await self.repository.get_all(skip=skip, limit=limit)
        except Exception as e:
            self.logger.error(f"Failed to get all products: {e}")
            raise DatabaseError("get_all", str(e))
    
    async def update_entity(self, entity_id: str, data: ProductUpdateDTO) -> Optional[Product]:
        """
        Update a product.
        
        Args:
            entity_id: Product ID
            data: Update data
            
        Returns:
            Updated product if successful, None otherwise
        """
        try:
            # Validate business rules
            await self._validate_product_update(entity_id, data)
            
            # Update product
            success = await self.repository.update(entity_id, data)
            if not success:
                return None
            
            # Get updated product
            product = await self.repository.get_by_id(entity_id)
            
            # Clear cache
            await self._clear_product_cache(entity_id)
            
            self.logger.info(f"Updated product {entity_id}")
            return product
            
        except (ValidationError, BusinessLogicError, DatabaseError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to update product {entity_id}: {e}")
            raise DatabaseError("update", str(e))
    
    async def delete_entity(self, entity_id: str) -> bool:
        """
        Soft delete a product.
        
        Args:
            entity_id: Product ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            success = await self.repository.delete(entity_id)
            if success:
                # Clear cache
                await self._clear_product_cache(entity_id)
                self.logger.info(f"Deleted product {entity_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to delete product {entity_id}: {e}")
            raise DatabaseError("delete", str(e))
    
    async def find_products_by_filters(
        self,
        filters: ProductFilterParams,
        pagination: PaginationParams,
        sort: SortParams
    ) -> PaginatedResponseDTO:
        """
        Find products with advanced filtering and pagination.
        
        Args:
            filters: Product filter parameters
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            Paginated response with products
        """
        try:
            # Generate cache key
            cache_key = self._generate_filter_cache_key(filters, pagination, sort)
            
            # Try cache first
            cached_result = await self.cache_service.get(cache_key)
            if cached_result:
                return PaginatedResponseDTO(**cached_result)
            
            # Get products from repository
            products = await self.repository.find_products_by_filters(filters, pagination, sort)
            
            # Get total count
            total = await self.repository.count({"is_archived": False})
            
            # Create response
            response = PaginatedResponseDTO(
                items=[product.dict() for product in products],
                total=total,
                page=pagination.page,
                page_size=pagination.page_size,
                total_pages=(total + pagination.page_size - 1) // pagination.page_size,
                has_next=pagination.page * pagination.page_size < total,
                has_prev=pagination.page > 1
            )
            
            # Cache the result
            await self.cache_service.set(cache_key, response.dict(), ttl_seconds=300)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to find products by filters: {e}")
            raise DatabaseError("find_products_by_filters", str(e))
    
    async def get_new_products(self, limit: int = 10) -> List[Product]:
        """
        Get new products.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of new products
        """
        try:
            cache_key = f"new_products:{limit}"
            cached_products = await self.cache_service.get(cache_key)
            
            if cached_products:
                return [Product(**p) for p in cached_products]
            
            products = await self.repository.find_new_products(limit)
            
            # Cache the result
            await self.cache_service.set(cache_key, [p.dict() for p in products], ttl_seconds=600)
            
            return products
            
        except Exception as e:
            self.logger.error(f"Failed to get new products: {e}")
            raise DatabaseError("get_new_products", str(e))
    
    async def get_popular_products(self, limit: int = 10) -> List[Product]:
        """
        Get popular products.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of popular products
        """
        try:
            cache_key = f"popular_products:{limit}"
            cached_products = await self.cache_service.get(cache_key)
            
            if cached_products:
                return [Product(**p) for p in cached_products]
            
            products = await self.repository.get_popular_products(limit)
            
            # Cache the result
            await self.cache_service.set(cache_key, [p.dict() for p in products], ttl_seconds=600)
            
            return products
            
        except Exception as e:
            self.logger.error(f"Failed to get popular products: {e}")
            raise DatabaseError("get_popular_products", str(e))
    
    async def search_products(
        self,
        search_term: str,
        pagination: PaginationParams,
        sort: SortParams
    ) -> PaginatedResponseDTO:
        """
        Search products by term.
        
        Args:
            search_term: Search term
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            Paginated response with search results
        """
        try:
            cache_key = f"search_products:{search_term}:{pagination.page}:{pagination.page_size}"
            cached_result = await self.cache_service.get(cache_key)
            
            if cached_result:
                return PaginatedResponseDTO(**cached_result)
            
            products = await self.repository.search_products(search_term, pagination, sort)
            total = await self.repository.count({"is_archived": False})
            
            response = PaginatedResponseDTO(
                items=[product.dict() for product in products],
                total=total,
                page=pagination.page,
                page_size=pagination.page_size,
                total_pages=(total + pagination.page_size - 1) // pagination.page_size,
                has_next=pagination.page * pagination.page_size < total,
                has_prev=pagination.page > 1
            )
            
            # Cache the result
            await self.cache_service.set(cache_key, response.dict(), ttl_seconds=300)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to search products: {e}")
            raise DatabaseError("search_products", str(e))
    
    async def _validate_product_creation(self, data: ProductCreateDTO) -> None:
        """
        Validate product creation data.
        
        Args:
            data: Product creation data
            
        Raises:
            ValidationError: If validation fails
            BusinessLogicError: If business rules are violated
        """
        # Validate price
        if data.price <= 0:
            raise ValidationError("Price must be greater than 0", "price", data.price)
        
        # Validate dimensions
        if data.width <= 0 or data.length <= 0 or data.height <= 0:
            raise ValidationError("All dimensions must be greater than 0")
        
        # Validate weight if provided
        if data.weight is not None and data.weight <= 0:
            raise ValidationError("Weight must be greater than 0", "weight", data.weight)
        
        # Validate depth if provided
        if data.depth is not None and data.depth <= 0:
            raise ValidationError("Depth must be greater than 0", "depth", data.depth)
    
    async def _validate_product_update(self, entity_id: str, data: ProductUpdateDTO) -> None:
        """
        Validate product update data.
        
        Args:
            entity_id: Product ID
            data: Update data
            
        Raises:
            ValidationError: If validation fails
            NotFoundError: If product not found
        """
        # Check if product exists
        existing_product = await self.repository.get_by_id(entity_id)
        if not existing_product:
            raise NotFoundError("Product", entity_id)
        
        # Validate price if provided
        if data.price is not None and data.price <= 0:
            raise ValidationError("Price must be greater than 0", "price", data.price)
        
        # Validate dimensions if provided
        if data.width is not None and data.width <= 0:
            raise ValidationError("Width must be greater than 0", "width", data.width)
        
        if data.length is not None and data.length <= 0:
            raise ValidationError("Length must be greater than 0", "length", data.length)
        
        if data.height is not None and data.height <= 0:
            raise ValidationError("Height must be greater than 0", "height", data.height)
        
        if data.depth is not None and data.depth <= 0:
            raise ValidationError("Depth must be greater than 0", "depth", data.depth)
        
        if data.weight is not None and data.weight <= 0:
            raise ValidationError("Weight must be greater than 0", "weight", data.weight)
    
    def _generate_filter_cache_key(
        self,
        filters: ProductFilterParams,
        pagination: PaginationParams,
        sort: SortParams
    ) -> str:
        """
        Generate cache key for filter results.
        
        Args:
            filters: Filter parameters
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            Cache key string
        """
        filter_params = {
            "search": filters.search,
            "start_price": filters.start_price,
            "end_price": filters.end_price,
            "category_id": filters.category_id,
            "material_id": filters.material_id,
            "color_ids": filters.color_ids,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "sort_by": sort.sort_by,
            "sort_order": sort.sort_order
        }
        
        # Remove None values
        filter_params = {k: v for k, v in filter_params.items() if v is not None}
        
        return f"product_filters:{hash(str(filter_params))}"
    
    async def _clear_product_cache(self, product_id: str = "") -> None:
        """
        Clear product-related cache.
        
        Args:
            product_id: Specific product ID to clear (optional)
        """
        try:
            if product_id:
                await self.cache_service.delete(f"product:{product_id}")
            else:
                # Clear all product-related cache
                await self.cache_service.delete("new_products")
                await self.cache_service.delete("popular_products")
                await self.cache_service.delete("product_filters")
        except Exception as e:
            self.logger.warning(f"Failed to clear product cache: {e}") 