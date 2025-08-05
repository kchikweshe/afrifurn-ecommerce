"""
Test configuration and fixtures for the AfriFurn product service.
"""
import pytest
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any
from unittest.mock import AsyncMock, MagicMock

from core.interfaces import ICacheService
from core.dto import ProductCreateDTO, ProductUpdateDTO
from models.products import Product, Dimensions
from services.product_service import ProductService
from repositories.product_repository import ProductRepository


# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_cache_service() -> ICacheService:
    """Mock cache service for testing."""
    cache_service = AsyncMock(spec=ICacheService)
    cache_service.get.return_value = None
    cache_service.set.return_value = None
    cache_service.delete.return_value = None
    cache_service.exists.return_value = False
    return cache_service


@pytest.fixture
def mock_repository() -> ProductRepository:
    """Mock product repository for testing."""
    repository = AsyncMock(spec=ProductRepository)
    repository.create.return_value = "test_product_id"
    repository.get_by_id.return_value = None
    repository.update.return_value = True
    repository.delete.return_value = True
    repository.find_by_criteria.return_value = []
    repository.count.return_value = 0
    repository.find_products_by_filters.return_value = []
    repository.find_new_products.return_value = []
    repository.get_popular_products.return_value = []
    repository.search_products.return_value = []
    repository.increment_views.return_value = True
    return repository


@pytest.fixture
def sample_product_data() -> Dict[str, Any]:
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "short_name": "test-prod",
        "description": "A test product for testing purposes",
        "category_id": "test_category_id",
        "price": 100.0,
        "currency_code": "USD",
        "material_id": "test_material_id",
        "width": 50.0,
        "length": 100.0,
        "height": 75.0,
        "depth": 25.0,
        "weight": 500.0,
        "color_ids": ["color1", "color2"],
        "product_features": [{"name": "Feature 1", "description": "Test feature"}]
    }


@pytest.fixture
def sample_product_dto(sample_product_data) -> ProductCreateDTO:
    """Sample product DTO for testing."""
    return ProductCreateDTO(**sample_product_data)


@pytest.fixture
def sample_product(sample_product_data) -> Product:
    """Sample product instance for testing."""
    return Product(
        id="test_product_id",
        name=sample_product_data["name"],
        short_name=sample_product_data["short_name"],
        description=sample_product_data["description"],
        category={"id": sample_product_data["category_id"], "name": "Test Category"},
        dimensions=Dimensions(
            width=sample_product_data["width"],
            length=sample_product_data["length"],
            height=sample_product_data["height"],
            depth=sample_product_data["depth"],
            weight=sample_product_data["weight"]
        ),
        price=sample_product_data["price"],
        currency=sample_product_data["currency_code"],
        material=sample_product_data["material_id"],
        is_new=True,
        views=0,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )


@pytest.fixture
def sample_products_data() -> list:
    """Sample products data for parameterized tests."""
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
def product_service_with_mocks(mock_cache_service, mock_repository) -> ProductService:
    """Product service with mocked dependencies."""
    with pytest.MonkeyPatch().context() as m:
        m.setattr("services.product_service.ProductRepository", lambda: mock_repository)
        service = ProductService(cache_service=mock_cache_service)
        return service


@pytest.fixture
def real_product_service() -> ProductService:
    """Product service with real dependencies for integration tests."""
    return ProductService()


@pytest.fixture
async def test_database():
    """Test database setup and teardown."""
    # Setup test database
    # This would typically involve creating a test MongoDB instance
    # or using a test container
    
    yield
    
    # Teardown test database
    # Clean up test data


@pytest.fixture
def api_client():
    """FastAPI test client."""
    from fastapi.testclient import TestClient
    from main import app
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_headers():
    """Authentication headers for API tests."""
    return {"X-API-Key": "your-super-secret-api-key"}


@pytest.fixture
def admin_headers():
    """Admin authentication headers for API tests."""
    return {"X-API-Key": "admin-super-secret-api-key"}


# Test markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as an API test"
    )
    config.addinivalue_line(
        "markers", "cache: mark test as a cache test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as a database test"
    )


# Test utilities
class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_product_data(**kwargs) -> Dict[str, Any]:
        """Create product data with default values."""
        default_data = {
            "name": "Test Product",
            "short_name": "test-prod",
            "description": "A test product",
            "category_id": "test_category",
            "price": 100.0,
            "currency_code": "USD",
            "material_id": "test_material",
            "width": 50.0,
            "length": 100.0,
            "height": 75.0,
            "depth": 25.0,
            "weight": 500.0,
            "color_ids": ["color1"],
            "product_features": []
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_product_dto(**kwargs) -> ProductCreateDTO:
        """Create product DTO with default values."""
        data = TestDataFactory.create_product_data(**kwargs)
        return ProductCreateDTO(**data)
    
    @staticmethod
    def create_product_update_dto(**kwargs) -> ProductUpdateDTO:
        """Create product update DTO with default values."""
        return ProductUpdateDTO(**kwargs)
    
    @staticmethod
    def create_product(**kwargs) -> Product:
        """Create product instance with default values."""
        data = TestDataFactory.create_product_data(**kwargs)
        return Product(
            id=kwargs.get("id", "test_product_id"),
            name=data["name"],
            short_name=data["short_name"],
            description=data["description"],
            category={"id": data["category_id"], "name": "Test Category"},
            dimensions=Dimensions(
                width=data["width"],
                length=data["length"],
                height=data["height"],
                depth=data["depth"],
                weight=data["weight"]
            ),
            price=data["price"],
            currency=data["currency_code"],
            material=data["material_id"],
            is_new=kwargs.get("is_new", True),
            views=kwargs.get("views", 0),
            created_at=kwargs.get("created_at", "2024-01-01T00:00:00Z"),
            updated_at=kwargs.get("updated_at", "2024-01-01T00:00:00Z")
        )


# Test assertions
class TestAssertions:
    """Custom assertions for tests."""
    
    @staticmethod
    def assert_product_equal(actual: Product, expected: Product):
        """Assert that two products are equal."""
        assert actual.id == expected.id
        assert actual.name == expected.name
        assert actual.short_name == expected.short_name
        assert actual.description == expected.description
        assert actual.price == expected.price
        assert actual.currency == expected.currency
        assert actual.material == expected.material
    
    @staticmethod
    def assert_product_data_valid(product_data: Dict[str, Any]):
        """Assert that product data is valid."""
        assert "name" in product_data
        assert "short_name" in product_data
        assert "description" in product_data
        assert "price" in product_data
        assert "currency_code" in product_data
        assert "material_id" in product_data
        assert "width" in product_data
        assert "length" in product_data
        assert "height" in product_data
        
        assert product_data["price"] > 0
        assert product_data["width"] > 0
        assert product_data["length"] > 0
        assert product_data["height"] > 0
        assert len(product_data["name"]) >= 3
        assert len(product_data["short_name"]) >= 2
        assert len(product_data["description"]) >= 10


# Performance testing utilities
class PerformanceTest:
    """Utilities for performance testing."""
    
    @staticmethod
    async def measure_execution_time(func, *args, **kwargs):
        """Measure execution time of a function."""
        import time
        
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        
        return result, end_time - start_time
    
    @staticmethod
    async def benchmark_operation(operation_func, iterations: int = 100):
        """Benchmark an operation multiple times."""
        import time
        
        times = []
        for _ in range(iterations):
            start_time = time.time()
            await operation_func()
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
            "median": sorted(times)[len(times) // 2]
        }