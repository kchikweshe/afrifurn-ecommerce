"""
Parameterized integration tests for ProductService.
"""
import pytest
from typing import List, Dict, Any
from datetime import datetime

from services.product_service import ProductService
from repositories.product_repository import ProductRepository
from core.dto import (
    ProductCreateDTO, 
    ProductUpdateDTO, 
    ProductFilterParams,
    PaginationParams,
    SortParams
)
from core.exceptions import ValidationError, NotFoundError, DatabaseError
from models.products import Product, Dimensions


class TestProductServiceIntegration:
    """Integration tests for ProductService with real dependencies."""
    
    @pytest.fixture
    def product_service(self):
        """Product service with real repository."""
        return ProductService()
    
    @pytest.fixture
    def sample_products_data(self):
        """Sample product data for parameterized tests."""
        return [
            {
                "name": "Modern Chair",
                "short_name": "modern-chair",
                "description": "A comfortable modern chair",
                "category_id": "chair_category",
                "price": 150.0,
                "currency_code": "USD",
                "material_id": "wood_material",
                "width": 60.0,
                "length": 70.0,
                "height": 85.0,
                "depth": 65.0,
                "weight": 800.0,
                "color_ids": ["brown", "black"],
                "product_features": [{"name": "Ergonomic", "description": "Ergonomic design"}]
            },
            {
                "name": "Dining Table",
                "short_name": "dining-table",
                "description": "Large dining table for 6 people",
                "category_id": "table_category",
                "price": 300.0,
                "currency_code": "USD",
                "material_id": "oak_material",
                "width": 180.0,
                "length": 90.0,
                "height": 75.0,
                "depth": 90.0,
                "weight": 2500.0,
                "color_ids": ["natural", "dark"],
                "product_features": [{"name": "Expandable", "description": "Expandable table"}]
            },
            {
                "name": "Bookshelf",
                "short_name": "bookshelf",
                "description": "Tall bookshelf with multiple shelves",
                "category_id": "shelf_category",
                "price": 200.0,
                "currency_code": "USD",
                "material_id": "pine_material",
                "width": 80.0,
                "length": 30.0,
                "height": 180.0,
                "depth": 30.0,
                "weight": 1200.0,
                "color_ids": ["white", "brown"],
                "product_features": [{"name": "Adjustable", "description": "Adjustable shelves"}]
            }
        ]
    
    @pytest.fixture
    def filter_test_cases(self):
        """Test cases for product filtering."""
        return [
            {
                "name": "filter_by_price_range",
                "filters": ProductFilterParams(start_price=100.0, end_price=250.0),
                "expected_count": 2,  # Modern Chair and Bookshelf
                "description": "Filter products by price range"
            },
            {
                "name": "filter_by_width_range",
                "filters": ProductFilterParams(min_width=50.0, max_width=100.0),
                "expected_count": 2,  # Modern Chair and Bookshelf
                "description": "Filter products by width range"
            },
            {
                "name": "filter_by_height_range",
                "filters": ProductFilterParams(min_height=80.0, max_height=200.0),
                "expected_count": 2,  # Modern Chair and Bookshelf
                "description": "Filter products by height range"
            },
            {
                "name": "filter_by_weight_range",
                "filters": ProductFilterParams(min_weight=1000.0, max_weight=3000.0),
                "expected_count": 2,  # Dining Table and Bookshelf
                "description": "Filter products by weight range"
            },
            {
                "name": "filter_by_search_term",
                "filters": ProductFilterParams(search="chair"),
                "expected_count": 1,  # Modern Chair
                "description": "Filter products by search term"
            },
            {
                "name": "filter_by_category",
                "filters": ProductFilterParams(category_id="chair_category"),
                "expected_count": 1,  # Modern Chair
                "description": "Filter products by category"
            },
            {
                "name": "filter_by_material",
                "filters": ProductFilterParams(material_id="wood_material"),
                "expected_count": 1,  # Modern Chair
                "description": "Filter products by material"
            },
            {
                "name": "filter_by_colors",
                "filters": ProductFilterParams(color_ids=["brown", "black"]),
                "expected_count": 1,  # Modern Chair
                "description": "Filter products by colors"
            },
            {
                "name": "complex_filter",
                "filters": ProductFilterParams(
                    start_price=150.0,
                    end_price=250.0,
                    min_width=50.0,
                    max_width=100.0,
                    search="chair"
                ),
                "expected_count": 1,  # Modern Chair
                "description": "Complex filter with multiple criteria"
            }
        ]
    
    @pytest.fixture
    def pagination_test_cases(self):
        """Test cases for pagination."""
        return [
            {
                "name": "first_page",
                "pagination": PaginationParams(page=1, page_size=2),
                "expected_items": 2,
                "expected_has_next": True,
                "expected_has_prev": False,
                "description": "Get first page with 2 items"
            },
            {
                "name": "second_page",
                "pagination": PaginationParams(page=2, page_size=2),
                "expected_items": 1,
                "expected_has_next": False,
                "expected_has_prev": True,
                "description": "Get second page with remaining items"
            },
            {
                "name": "large_page_size",
                "pagination": PaginationParams(page=1, page_size=10),
                "expected_items": 3,
                "expected_has_next": False,
                "expected_has_prev": False,
                "description": "Get all items in one page"
            }
        ]
    
    @pytest.fixture
    def sort_test_cases(self):
        """Test cases for sorting."""
        return [
            {
                "name": "sort_by_name_asc",
                "sort": SortParams(sort_by="name", sort_order=1),
                "expected_order": ["Bookshelf", "Dining Table", "Modern Chair"],
                "description": "Sort by name ascending"
            },
            {
                "name": "sort_by_name_desc",
                "sort": SortParams(sort_by="name", sort_order=-1),
                "expected_order": ["Modern Chair", "Dining Table", "Bookshelf"],
                "description": "Sort by name descending"
            },
            {
                "name": "sort_by_price_asc",
                "sort": SortParams(sort_by="price", sort_order=1),
                "expected_order": ["Modern Chair", "Bookshelf", "Dining Table"],
                "description": "Sort by price ascending"
            },
            {
                "name": "sort_by_price_desc",
                "sort": SortParams(sort_by="price", sort_order=-1),
                "expected_order": ["Dining Table", "Bookshelf", "Modern Chair"],
                "description": "Sort by price descending"
            }
        ]
    
    @pytest.fixture
    def invalid_product_data(self):
        """Invalid product data for validation tests."""
        return [
            {
                "name": "",  # Empty name
                "short_name": "test",
                "description": "Test description",
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": 100.0,
                "height": 75.0,
                "expected_error": "name",
                "description": "Empty product name"
            },
            {
                "name": "Test Product",
                "short_name": "",  # Empty short name
                "description": "Test description",
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": 100.0,
                "height": 75.0,
                "expected_error": "short_name",
                "description": "Empty short name"
            },
            {
                "name": "Test Product",
                "short_name": "test",
                "description": "Short",  # Too short description
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": 100.0,
                "height": 75.0,
                "expected_error": "description",
                "description": "Description too short"
            },
            {
                "name": "Test Product",
                "short_name": "test",
                "description": "Test description",
                "category_id": "test_category",
                "price": -100.0,  # Negative price
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": 100.0,
                "height": 75.0,
                "expected_error": "price",
                "description": "Negative price"
            },
            {
                "name": "Test Product",
                "short_name": "test",
                "description": "Test description",
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": -50.0,  # Negative width
                "length": 100.0,
                "height": 75.0,
                "expected_error": "width",
                "description": "Negative width"
            },
            {
                "name": "Test Product",
                "short_name": "test",
                "description": "Test description",
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": -100.0,  # Negative length
                "height": 75.0,
                "expected_error": "length",
                "description": "Negative length"
            },
            {
                "name": "Test Product",
                "short_name": "test",
                "description": "Test description",
                "category_id": "test_category",
                "price": 100.0,
                "currency_code": "USD",
                "material_id": "test_material",
                "width": 50.0,
                "length": 100.0,
                "height": -75.0,  # Negative height
                "expected_error": "height",
                "description": "Negative height"
            }
        ]
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("product_data", [
        pytest.lazy_fixture("sample_products_data")
    ])
    async def test_create_multiple_products(self, product_service, product_data):
        """Test creating multiple products."""
        created_products = []
        
        for data in product_data:
            # Create product
            product_dto = ProductCreateDTO(**data)
            product = await product_service.create_entity(product_dto)
            
            assert product is not None
            assert product.name == data["name"]
            assert product.short_name == data["short_name"]
            assert product.price == data["price"]
            
            created_products.append(product)
        
        assert len(created_products) == len(product_data)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", [
        pytest.lazy_fixture("filter_test_cases")
    ])
    async def test_filter_products(self, product_service, sample_products_data, test_case):
        """Test product filtering with various criteria."""
        # Create test products
        for data in sample_products_data:
            product_dto = ProductCreateDTO(**data)
            await product_service.create_entity(product_dto)
        
        # Apply filters
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        result = await product_service.find_products_by_filters(
            test_case["filters"], pagination, sort
        )
        
        # Assert results
        assert len(result.items) == test_case["expected_count"], \
            f"Expected {test_case['expected_count']} products for {test_case['name']}, got {len(result.items)}"
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", [
        pytest.lazy_fixture("pagination_test_cases")
    ])
    async def test_pagination(self, product_service, sample_products_data, test_case):
        """Test pagination functionality."""
        # Create test products
        for data in sample_products_data:
            product_dto = ProductCreateDTO(**data)
            await product_service.create_entity(product_dto)
        
        # Get paginated results
        filters = ProductFilterParams()
        sort = SortParams(sort_by="name", sort_order=1)
        
        result = await product_service.find_products_by_filters(
            filters, test_case["pagination"], sort
        )
        
        # Assert pagination
        assert len(result.items) == test_case["expected_items"]
        assert result.has_next == test_case["expected_has_next"]
        assert result.has_prev == test_case["expected_has_prev"]
        assert result.page == test_case["pagination"].page
        assert result.page_size == test_case["pagination"].page_size
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", [
        pytest.lazy_fixture("sort_test_cases")
    ])
    async def test_sorting(self, product_service, sample_products_data, test_case):
        """Test product sorting."""
        # Create test products
        for data in sample_products_data:
            product_dto = ProductCreateDTO(**data)
            await product_service.create_entity(product_dto)
        
        # Get sorted results
        filters = ProductFilterParams()
        pagination = PaginationParams(page=1, page_size=10)
        
        result = await product_service.find_products_by_filters(
            filters, pagination, test_case["sort"]
        )
        
        # Assert sorting
        product_names = [item["name"] for item in result.items]
        assert product_names == test_case["expected_order"]
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("invalid_data", [
        pytest.lazy_fixture("invalid_product_data")
    ])
    async def test_validation_errors(self, product_service, invalid_data):
        """Test validation error handling."""
        # Remove expected_error from data for DTO creation
        dto_data = {k: v for k, v in invalid_data.items() if k not in ["expected_error", "description"]}
        
        # Create DTO and expect validation error
        with pytest.raises(ValidationError) as exc_info:
            product_dto = ProductCreateDTO(**dto_data)
            await product_service.create_entity(product_dto)
        
        # Assert error message contains expected field
        assert invalid_data["expected_error"] in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_product_lifecycle(self, product_service):
        """Test complete product lifecycle (create, read, update, delete)."""
        # Create product
        product_data = ProductCreateDTO(
            name="Lifecycle Test Product",
            short_name="lifecycle-test",
            description="A product for testing lifecycle operations",
            category_id="test_category",
            price=100.0,
            currency_code="USD",
            material_id="test_material",
            width=50.0,
            length=100.0,
            height=75.0
        )
        
        created_product = await product_service.create_entity(product_data)
        assert created_product is not None
        assert created_product.name == "Lifecycle Test Product"
        
        # Read product
        retrieved_product = await product_service.get_entity_by_id(created_product.id)
        assert retrieved_product is not None
        assert retrieved_product.name == "Lifecycle Test Product"
        
        # Update product
        update_data = ProductUpdateDTO(name="Updated Lifecycle Product")
        updated_product = await product_service.update_entity(created_product.id, update_data)
        assert updated_product is not None
        assert updated_product.name == "Updated Lifecycle Product"
        
        # Delete product
        delete_result = await product_service.delete_entity(created_product.id)
        assert delete_result is True
        
        # Verify product is deleted
        deleted_product = await product_service.get_entity_by_id(created_product.id)
        assert deleted_product is None
    
    @pytest.mark.asyncio
    async def test_search_functionality(self, product_service, sample_products_data):
        """Test product search functionality."""
        # Create test products
        for data in sample_products_data:
            product_dto = ProductCreateDTO(**data)
            await product_service.create_entity(product_dto)
        
        # Test search by product name
        search_term = "chair"
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        result = await product_service.search_products(search_term, pagination, sort)
        
        # Should find Modern Chair
        assert len(result.items) == 1
        assert "chair" in result.items[0]["name"].lower()
    
    @pytest.mark.asyncio
    async def test_cache_functionality(self, product_service):
        """Test cache functionality."""
        # Create a product
        product_data = ProductCreateDTO(
            name="Cache Test Product",
            short_name="cache-test",
            description="A product for testing cache",
            category_id="test_category",
            price=100.0,
            currency_code="USD",
            material_id="test_material",
            width=50.0,
            length=100.0,
            height=75.0
        )
        
        created_product = await product_service.create_entity(product_data)
        
        # First retrieval (should hit database)
        product1 = await product_service.get_entity_by_id(created_product.id)
        
        # Second retrieval (should hit cache)
        product2 = await product_service.get_entity_by_id(created_product.id)
        
        # Both should be the same
        assert product1.id == product2.id
        assert product1.name == product2.name
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, product_service):
        """Test concurrent operations on products."""
        import asyncio
        
        # Create multiple products concurrently
        product_data_list = [
            ProductCreateDTO(
                name=f"Concurrent Product {i}",
                short_name=f"concurrent-{i}",
                description=f"Product {i} for concurrent testing",
                category_id="test_category",
                price=100.0 + i,
                currency_code="USD",
                material_id="test_material",
                width=50.0 + i,
                length=100.0 + i,
                height=75.0 + i
            )
            for i in range(5)
        ]
        
        # Create products concurrently
        create_tasks = [
            product_service.create_entity(data) for data in product_data_list
        ]
        created_products = await asyncio.gather(*create_tasks)
        
        # Verify all products were created
        assert len(created_products) == 5
        for i, product in enumerate(created_products):
            assert product.name == f"Concurrent Product {i}"
        
        # Read products concurrently
        read_tasks = [
            product_service.get_entity_by_id(product.id) for product in created_products
        ]
        retrieved_products = await asyncio.gather(*read_tasks)
        
        # Verify all products were retrieved
        assert len(retrieved_products) == 5
        for i, product in enumerate(retrieved_products):
            assert product.name == f"Concurrent Product {i}"
    
    @pytest.mark.asyncio
    async def test_error_handling(self, product_service):
        """Test error handling scenarios."""
        # Test getting non-existent product
        non_existent_product = await product_service.get_entity_by_id("nonexistent_id")
        assert non_existent_product is None
        
        # Test updating non-existent product
        update_data = ProductUpdateDTO(name="Updated Product")
        updated_product = await product_service.update_entity("nonexistent_id", update_data)
        assert updated_product is None
        
        # Test deleting non-existent product
        delete_result = await product_service.delete_entity("nonexistent_id")
        assert delete_result is False 