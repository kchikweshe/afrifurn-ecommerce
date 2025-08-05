"""
Product repository implementation with specific business logic.
"""
import logging
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING

from repositories.base_repository import BaseRepository
from models.products import Product, ProductCreateDTO, ProductUpdateDTO
from core.exceptions import DuplicateError, NotFoundError, DatabaseError
from core.dto import ProductFilterParams, PaginationParams, SortParams


class ProductRepository(BaseRepository[Product]):
    """
    Product repository with specific business logic.
    
    Implements product-specific operations and follows SOLID principles.
    """
    
    def __init__(self):
        super().__init__(Product, "products")
    
    async def _check_duplicates(self, data: ProductCreateDTO) -> None:
        """
        Check for duplicate products.
        
        Args:
            data: Product data to check
            
        Raises:
            DuplicateError: If duplicate found
        """
        # Check for duplicate name
        existing = await self.find_by_criteria({"name": data.name, "is_archived": False})
        if existing:
            raise DuplicateError("Product", "name", data.name)
        
        # Check for duplicate short_name
        existing = await self.find_by_criteria({"short_name": data.short_name, "is_archived": False})
        if existing:
            raise DuplicateError("Product", "short_name", data.short_name)
    
    async def find_products_by_filters(
        self,
        filters: ProductFilterParams,
        pagination: PaginationParams,
        sort: SortParams
    ) -> List[Product]:
        """
        Find products with advanced filtering.
        
        Args:
            filters: Product filter parameters
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            List of products matching criteria
        """
        try:
            # Build query criteria
            criteria = {"is_archived": False}
            
            if filters.search:
                criteria["$or"] = [
                    {"name": {"$regex": filters.search, "$options": "i"}},
                    {"short_name": {"$regex": filters.search, "$options": "i"}},
                    {"description": {"$regex": filters.search, "$options": "i"}}
                ]
            
            if filters.start_price is not None or filters.end_price is not None:
                price_criteria = {}
                if filters.start_price is not None:
                    price_criteria["$gte"] = filters.start_price
                if filters.end_price is not None:
                    price_criteria["$lte"] = filters.end_price
                criteria["price"] = price_criteria
            
            if filters.category_id:
                criteria["category.id"] = ObjectId(filters.category_id)
            
            if filters.material_id:
                criteria["material"] = ObjectId(filters.material_id)
            
            if filters.color_ids:
                criteria["color_codes"] = {"$in": filters.color_ids}
            
            # Dimension filters
            if filters.min_width or filters.max_width:
                width_criteria = {}
                if filters.min_width:
                    width_criteria["$gte"] = filters.min_width
                if filters.max_width:
                    width_criteria["$lte"] = filters.max_width
                criteria["dimensions.width"] = width_criteria
            
            if filters.min_height or filters.max_height:
                height_criteria = {}
                if filters.min_height:
                    height_criteria["$gte"] = filters.min_height
                if filters.max_height:
                    height_criteria["$lte"] = filters.max_height
                criteria["dimensions.height"] = height_criteria
            
            if filters.min_depth or filters.max_depth:
                depth_criteria = {}
                if filters.min_depth:
                    depth_criteria["$gte"] = filters.min_depth
                if filters.max_depth:
                    depth_criteria["$lte"] = filters.max_depth
                criteria["dimensions.depth"] = depth_criteria
            
            if filters.min_length or filters.max_length:
                length_criteria = {}
                if filters.min_length:
                    length_criteria["$gte"] = filters.min_length
                if filters.max_length:
                    length_criteria["$lte"] = filters.max_length
                criteria["dimensions.length"] = length_criteria
            
            if filters.min_weight or filters.max_weight:
                weight_criteria = {}
                if filters.min_weight:
                    weight_criteria["$gte"] = filters.min_weight
                if filters.max_weight:
                    weight_criteria["$lte"] = filters.max_weight
                criteria["dimensions.weight"] = weight_criteria
            
            return await self.find_by_criteria(
                criteria=criteria,
                skip=pagination.skip,
                limit=pagination.limit,
                sort_by=sort.sort_by,
                sort_order=sort.sort_order
            )
            
        except Exception as e:
            self.logger.error(f"Failed to find products by filters: {e}")
            raise DatabaseError("find_products_by_filters", str(e))
    
    async def find_products_by_category(
        self,
        category_id: str,
        pagination: PaginationParams,
        sort: SortParams
    ) -> List[Product]:
        """
        Find products by category.
        
        Args:
            category_id: Category ID
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            List of products in category
        """
        try:
            criteria = {
                "category.id": ObjectId(category_id),
                "is_archived": False
            }
            
            return await self.find_by_criteria(
                criteria=criteria,
                skip=pagination.skip,
                limit=pagination.limit,
                sort_by=sort.sort_by,
                sort_order=sort.sort_order
            )
            
        except Exception as e:
            self.logger.error(f"Failed to find products by category {category_id}: {e}")
            raise DatabaseError("find_products_by_category", str(e))
    
    async def find_products_by_material(
        self,
        material_id: str,
        pagination: PaginationParams,
        sort: SortParams
    ) -> List[Product]:
        """
        Find products by material.
        
        Args:
            material_id: Material ID
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            List of products with material
        """
        try:
            criteria = {
                "material": ObjectId(material_id),
                "is_archived": False
            }
            
            return await self.find_by_criteria(
                criteria=criteria,
                skip=pagination.skip,
                limit=pagination.limit,
                sort_by=sort.sort_by,
                sort_order=sort.sort_order
            )
            
        except Exception as e:
            self.logger.error(f"Failed to find products by material {material_id}: {e}")
            raise DatabaseError("find_products_by_material", str(e))
    
    async def find_new_products(self, limit: int = 10) -> List[Product]:
        """
        Find new products.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of new products
        """
        try:
            criteria = {
                "is_new": True,
                "is_archived": False
            }
            
            return await self.find_by_criteria(
                criteria=criteria,
                limit=limit,
                sort_by="created_at",
                sort_order=DESCENDING
            )
            
        except Exception as e:
            self.logger.error(f"Failed to find new products: {e}")
            raise DatabaseError("find_new_products", str(e))
    
    async def find_discounted_products(self, limit: int = 10) -> List[Product]:
        """
        Find products with discounts.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of discounted products
        """
        try:
            criteria = {
                "discount": {"$gt": 0},
                "is_archived": False
            }
            
            return await self.find_by_criteria(
                criteria=criteria,
                limit=limit,
                sort_by="discount",
                sort_order=DESCENDING
            )
            
        except Exception as e:
            self.logger.error(f"Failed to find discounted products: {e}")
            raise DatabaseError("find_discounted_products", str(e))
    
    async def increment_views(self, product_id: str) -> bool:
        """
        Increment product view count.
        
        Args:
            product_id: Product ID
            
        Returns:
            True if updated, False otherwise
        """
        try:
            if not ObjectId.is_valid(product_id):
                return False
            
            result = self.db[self.collection_name].update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"views": 1}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to increment views for product {product_id}: {e}")
            return False
    
    async def get_popular_products(self, limit: int = 10) -> List[Product]:
        """
        Get popular products by view count.
        
        Args:
            limit: Maximum number of products to return
            
        Returns:
            List of popular products
        """
        try:
            criteria = {"is_archived": False}
            
            return await self.find_by_criteria(
                criteria=criteria,
                limit=limit,
                sort_by="views",
                sort_order=DESCENDING
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get popular products: {e}")
            raise DatabaseError("get_popular_products", str(e))
    
    async def search_products(
        self,
        search_term: str,
        pagination: PaginationParams,
        sort: SortParams
    ) -> List[Product]:
        """
        Search products by term.
        
        Args:
            search_term: Search term
            pagination: Pagination parameters
            sort: Sorting parameters
            
        Returns:
            List of products matching search term
        """
        try:
            criteria = {
                "is_archived": False,
                "$or": [
                    {"name": {"$regex": search_term, "$options": "i"}},
                    {"short_name": {"$regex": search_term, "$options": "i"}},
                    {"description": {"$regex": search_term, "$options": "i"}}
                ]
            }
            
            return await self.find_by_criteria(
                criteria=criteria,
                skip=pagination.skip,
                limit=pagination.limit,
                sort_by=sort.sort_by,
                sort_order=sort.sort_order
            )
            
        except Exception as e:
            self.logger.error(f"Failed to search products with term '{search_term}': {e}")
            raise DatabaseError("search_products", str(e))
    
    async def get_products_with_variants(self, product_ids: List[str]) -> List[Product]:
        """
        Get products with their variants.
        
        Args:
            product_ids: List of product IDs
            
        Returns:
            List of products with variants
        """
        try:
            object_ids = [ObjectId(pid) for pid in product_ids if ObjectId.is_valid(pid)]
            
            if not object_ids:
                return []
            
            criteria = {
                "_id": {"$in": object_ids},
                "is_archived": False
            }
            
            return await self.find_by_criteria(criteria=criteria)
            
        except Exception as e:
            self.logger.error(f"Failed to get products with variants: {e}")
            raise DatabaseError("get_products_with_variants", str(e)) 