import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
# Import your main application

# Global test client
@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)

# Async database session fixture
@pytest.fixture(scope="function")
async def async_session():
    # Configure your async database engine
    engine = create_async_engine("your_async_database_url", future=True)
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        yield session

# Authentication fixture (example)
@pytest.fixture
def authenticated_client(test_client):
    # Simulate authentication logic
    token = "mock_authentication_token"
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client

# Performance and logging fixtures
@pytest.fixture(autouse=True)
def _slow_test_marker(request):
    marker = request.node.get_closest_marker("slow")
    if marker is not None:
        print(f"\n⏳ Running slow test: {request.node.name}")

# Logging fixture
def pytest_configure(config):
    config.addinivalue_line(
        "markers", 
        "slow: mark test as slow-running"
    )