"""
Unit tests for ProductService following SOLID principles and best practices.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, Optional
from datetime import datetime

from services.product_service import ProductService
from core.dto import (
    ProductCreateDTO, 
    ProductUpdateDTO, 
    ProductFilterParams,
    PaginationParams,
    SortParams,
    PaginatedResponseDTO
)
from core.exceptions import (
    ValidationError, 
    NotFoundError, 
    BusinessLogicError,
    DatabaseError,
    DuplicateError
)
from models.products import Level1Category, Level2Category, Product, Dimensions


class TestProductService:
    """Test cases for ProductService."""
    
    @pytest.fixture
    def mock_cache_service(self):
        """Mock cache service."""
        cache_service = AsyncMock()
        cache_service.get.return_value = None
        cache_service.set.return_value = None
        cache_service.delete.return_value = None
        return cache_service
    
    @pytest.fixture
    def mock_repository(self):
        """Mock product repository."""
        repository = AsyncMock()
        repository.create.return_value = "test_product_id"
        repository.get_by_id.return_value = None
        repository.update.return_value = True
        repository.delete.return_value = True
        repository.find_by_criteria.return_value = []
        repository.count.return_value = 0
        return repository
    
    @pytest.fixture
    def product_service(self, mock_cache_service):
        """Product service instance with mocked dependencies."""
        with patch('services.product_service.ProductRepository') as mock_repo_class:
            mock_repo_class.return_value = AsyncMock()
            service = ProductService(cache_service=mock_cache_service)
            return service
    
    @pytest.fixture
    def sample_product_data(self):
        """Sample product creation data."""
        return ProductCreateDTO(
            name="Test Product",
            short_name="test-prod",
            description="A test product for testing",
            category_id="test_category_id",
            price=100.0,
            currency_code="USD",
            material_id="test_material_id",
            width=50.0,
            length=100.0,
            height=75.0,
            depth=25.0,
            weight=500.0,
            color_ids=["color1", "color2"],
            product_features=[{"name": "Feature 1", "description": "Test feature"}]
        )
    
    @pytest.fixture
    def sample_product(self):
        """Sample product instance."""
        return Product(
            _id="test_product_id",
            name="Test Product",
            short_name="test-prod",
            description="A test product for testing",
            category=Level2Category(
                _id="test_category_id",
                name="Test Category",
                description="Test Category Description",
                level_one_category=Level1Category(
                    _id="test_level_one_category_id",
                        name="Test Level One Category",
                    description="Test Level One Category Description"
                    
                )
            ),
            dimensions=Dimensions(
                width=50.0,
                length=100.0,
                height=75.0,
                depth=25.0,
                weight=500.0
            ),
            price=100.0,
            currency="USD",
            material="test_material_id",
            is_new=True,
            views=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_create_entity_success(self, product_service, sample_product_data, sample_product):
        """Test successful product creation."""
        # Arrange
        product_service.repository.create.return_value = "test_product_id"
        product_service.repository.get_by_id.return_value = sample_product
        
        # Act
        result = await product_service.create_entity(sample_product_data)
        
        # Assert
        assert result == sample_product
        product_service.repository.create.assert_called_once_with(sample_product_data)
        product_service.repository.get_by_id.assert_called_once_with("test_product_id")
        product_service.cache_service.delete.assert_called()
    
    @pytest.mark.asyncio
    async def test_create_entity_validation_error(self, product_service, sample_product_data):
        """Test product creation with validation error."""
        # Arrange
        sample_product_data.price = -100.0  # Invalid price
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Price must be greater than 0"):
            await product_service.create_entity(sample_product_data)
    
    @pytest.mark.asyncio
    async def test_create_entity_database_error(self, product_service, sample_product_data):
        """Test product creation with database error."""
        # Arrange
        product_service.repository.create.side_effect = DatabaseError("create", "Database error")
        
        # Act & Assert
        with pytest.raises(DatabaseError):
            await product_service.create_entity(sample_product_data)
    
    @pytest.mark.asyncio
    async def test_get_entity_by_id_success(self, product_service, sample_product):
        """Test successful product retrieval by ID."""
        # Arrange
        product_service.repository.get_by_id.return_value = sample_product
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.get_entity_by_id("test_product_id")
        
        # Assert
        assert result == sample_product
        product_service.repository.get_by_id.assert_called_once_with("test_product_id")
        product_service.repository.increment_views.assert_called_once_with("test_product_id")
    
    @pytest.mark.asyncio
    async def test_get_entity_by_id_from_cache(self, product_service, sample_product):
        """Test product retrieval from cache."""
        # Arrange
        product_service.cache_service.get.return_value = sample_product.dict()
        
        # Act
        result = await product_service.get_entity_by_id("test_product_id")
        
        # Assert
        assert result.id == sample_product.id
        product_service.repository.get_by_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_entity_by_id_not_found(self, product_service):
        """Test product retrieval when not found."""
        # Arrange
        product_service.repository.get_by_id.return_value = None
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.get_entity_by_id("nonexistent_id")
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_entity_success(self, product_service, sample_product):
        """Test successful product update."""
        # Arrange
        update_data = ProductUpdateDTO(name="Updated Product")
        product_service.repository.update.return_value = True
        product_service.repository.get_by_id.return_value = sample_product
        
        # Act
        result = await product_service.update_entity("test_product_id", update_data)
        
        # Assert
        assert result == sample_product
        product_service.repository.update.assert_called_once_with("test_product_id", update_data)
        product_service.cache_service.delete.assert_called()
    
    @pytest.mark.asyncio
    async def test_update_entity_not_found(self, product_service):
        """Test product update when not found."""
        # Arrange
        update_data = ProductUpdateDTO(name="Updated Product")
        product_service.repository.update.return_value = False
        
        # Act
        result = await product_service.update_entity("nonexistent_id", update_data)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_delete_entity_success(self, product_service):
        """Test successful product deletion."""
        # Arrange
        product_service.repository.delete.return_value = True
        
        # Act
        result = await product_service.delete_entity("test_product_id")
        
        # Assert
        assert result is True
        product_service.repository.delete.assert_called_once_with("test_product_id")
        product_service.cache_service.delete.assert_called()
    
    @pytest.mark.asyncio
    async def test_delete_entity_not_found(self, product_service):
        """Test product deletion when not found."""
        # Arrange
        product_service.repository.delete.return_value = False
        
        # Act
        result = await product_service.delete_entity("nonexistent_id")
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_find_products_by_filters_success(self, product_service):
        """Test successful product filtering."""
        # Arrange
        filters = ProductFilterParams(search="test", start_price=50.0, end_price=200.0)
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        expected_response = PaginatedResponseDTO(
            items=[],
            total=0,
            page=1,
            page_size=10,
            total_pages=0,
            has_next=False,
            has_prev=False
        )
        
        product_service.repository.find_products_by_filters.return_value = []
        product_service.repository.count.return_value = 0
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.find_products_by_filters(filters, pagination, sort)
        
        # Assert
        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 10
        product_service.repository.find_products_by_filters.assert_called_once_with(filters, pagination, sort)
    
    @pytest.mark.asyncio
    async def test_find_products_by_filters_from_cache(self, product_service):
        """Test product filtering from cache."""
        # Arrange
        filters = ProductFilterParams(search="test")
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        cached_response = {
            "items": [],
            "total": 0,
            "page": 1,
            "page_size": 10,
            "total_pages": 0,
            "has_next": False,
            "has_prev": False
        }
        
        product_service.cache_service.get.return_value = cached_response
        
        # Act
        result = await product_service.find_products_by_filters(filters, pagination, sort)
        
        # Assert
        assert result.total == 0
        product_service.repository.find_products_by_filters.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_new_products_success(self, product_service, sample_product):
        """Test successful retrieval of new products."""
        # Arrange
        product_service.repository.find_new_products.return_value = [sample_product]
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.get_new_products(limit=5)
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_product
        product_service.repository.find_new_products.assert_called_once_with(5)
    
    @pytest.mark.asyncio
    async def test_get_popular_products_success(self, product_service, sample_product):
        """Test successful retrieval of popular products."""
        # Arrange
        product_service.repository.get_popular_products.return_value = [sample_product]
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.get_popular_products(limit=5)
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_product
        product_service.repository.get_popular_products.assert_called_once_with(5)
    
    @pytest.mark.asyncio
    async def test_search_products_success(self, product_service):
        """Test successful product search."""
        # Arrange
        search_term = "test"
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        expected_response = PaginatedResponseDTO(
            items=[],
            total=0,
            page=1,
            page_size=10,
            total_pages=0,
            has_next=False,
            has_prev=False
        )
        
        product_service.repository.search_products.return_value = []
        product_service.repository.count.return_value = 0
        product_service.cache_service.get.return_value = None
        
        # Act
        result = await product_service.search_products(search_term, pagination, sort)
        
        # Assert
        assert result.total == 0
        product_service.repository.search_products.assert_called_once_with(search_term, pagination, sort)
    
    @pytest.mark.asyncio
    async def test_validate_product_creation_success(self, product_service, sample_product_data):
        """Test successful product creation validation."""
        # Act & Assert (should not raise exception)
        await product_service._validate_product_creation(sample_product_data)
    
    @pytest.mark.asyncio
    async def test_validate_product_creation_invalid_price(self, product_service, sample_product_data):
        """Test product creation validation with invalid price."""
        # Arrange
        sample_product_data.price = -100.0
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Price must be greater than 0"):
            await product_service._validate_product_creation(sample_product_data)
    
    @pytest.mark.asyncio
    async def test_validate_product_creation_invalid_dimensions(self, product_service, sample_product_data):
        """Test product creation validation with invalid dimensions."""
        # Arrange
        sample_product_data.width = -50.0
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Width must be greater than 0"):
            await product_service._validate_product_creation(sample_product_data)
    
    @pytest.mark.asyncio
    async def test_validate_product_update_success(self, product_service, sample_product):
        """Test successful product update validation."""
        # Arrange
        update_data = ProductUpdateDTO(name="Updated Product")
        product_service.repository.get_by_id.return_value = sample_product
        
        # Act & Assert (should not raise exception)
        await product_service._validate_product_update("test_product_id", update_data)
    
    @pytest.mark.asyncio
    async def test_validate_product_update_not_found(self, product_service):
        """Test product update validation when product not found."""
        # Arrange
        update_data = ProductUpdateDTO(name="Updated Product")
        product_service.repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundError):
            await product_service._validate_product_update("nonexistent_id", update_data)
    
    @pytest.mark.asyncio
    async def test_validate_product_update_invalid_price(self, product_service, sample_product):
        """Test product update validation with invalid price."""
        # Arrange
        update_data = ProductUpdateDTO(price=-100.0)
        product_service.repository.get_by_id.return_value = sample_product
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Price must be greater than 0"):
            await product_service._validate_product_update("test_product_id", update_data)
    
    def test_generate_filter_cache_key(self, product_service):
        """Test cache key generation for filters."""
        # Arrange
        filters = ProductFilterParams(search="test", start_price=50.0)
        pagination = PaginationParams(page=1, page_size=10)
        sort = SortParams(sort_by="name", sort_order=1)
        
        # Act
        cache_key = product_service._generate_filter_cache_key(filters, pagination, sort)
        
        # Assert
        assert cache_key.startswith("product_filters:")
        assert "test" in cache_key
        assert "50.0" in cache_key
    
    @pytest.mark.asyncio
    async def test_clear_product_cache_specific_id(self, product_service):
        """Test clearing cache for specific product ID."""
        # Act
        await product_service._clear_product_cache("test_product_id")
        
        # Assert
        product_service.cache_service.delete.assert_called_once_with("product:test_product_id")
    
    @pytest.mark.asyncio
    async def test_clear_product_cache_all(self, product_service):
        """Test clearing all product cache."""
        # Act
        await product_service._clear_product_cache()
        
        # Assert
        assert product_service.cache_service.delete.call_count == 3  # new_products, popular_products, product_filters 