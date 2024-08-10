import io
from typing import Any
from bson import ObjectId
from fastapi import UploadFile
from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch, MagicMock

from models.product_attributes import Material
from models.products import Color, Currency, Dimensions, Level2Category, Product


file_path_1 = 'static/product/663e74a7f859d62c6fe1c23bimage0.webp'
file_path_2 = 'static/product/663e74a7f859d62c6fe1c23bimage1.webp'
@pytest.fixture
def client():
    # Create a test client using your framework's test utilities
    # Replace this with the appropriate code for your framework
    from main import app as app
    with TestClient(app) as client:
        yield client

@patch('routers.products.extract_data')
@patch('routers.products.insert_into_db')
# @patch('routers.products.process_image')

def test_create_product_fail_no_images(mock_insert_into_db, mock_extract_data,client):
    # Mock the extract_data function
    color = MagicMock(spec=Color)
    parent_category = MagicMock(spec=Level2Category)
    currency = MagicMock(spec=Currency)
    material = MagicMock(spec=Material)
    mock_extract_data.return_value = (parent_category, currency, material, color)
   
    # mock_process_image.return_value=[file_path_1,file_path_2]
    # Mock the insert_into_db function
    inserted_product_id = "663e74a7f859d62c6fe1c23p"
    mock_insert_into_db.return_value = MagicMock(spec=Product,inserted_id=inserted_product_id,
                        name="Test Product",
        color=color,
        description="Test description",
        currency=currency,
        material=material,
        quantity_in_stock=100,
        category=parent_category,
        price=10.99,
        dimensions=MagicMock(spec=Dimensions,depth=5.0, height=20.0, weight=2.0, width=10.0, length=30.0)                         
                                                 )
    # Mock the image file
    # Send a POST request with valid data
# Create a mock object for UploadFile
    # Create a mock UploadFile object
    mock_upload_file = Mock(spec=UploadFile)
    mock_upload_file.filename = "test_image.jpg"
    mock_upload_file.content_type = "image/jpeg"

    data = {
        "name": "Test Product",
        "category": "663e74a7f859d62c6fe1c26b",
        "price": 10.99,
        "description": "Test description",
        "currency_code": "USD",
        "width": 10.0,
        "color_code": "#0d0d0d",
        "quantity": 100,
        "images": [],
        "height": 20.0,
        "length": 30.0,
        "depth": 5.0,
        "weight": 2.0,
        "material_id": "663e74a7f859d62c6fe1c69b"
    }
    response = client.post("/api/v1/products", data=data)
    print(response.json())
    # Assert the response
    assert response.json()['code'] == 400

    assert response.json() == {
        "data": {},
        "code": 400,
        "message": "No images provided for the product"
    }

    # Assert that the mocked functions were called with the expected arguments
    # mock_process_image.assert_called_once_with(MagicMock(spec=UploadFile),[i for i in enumerate(data['images'])],MagicMock(spec=Any))
    # mock_insert_into_db.assert_called_once_with(name="products", product=MagicMock(
    #     name="Test Product",
    #     color=color,
    #     description="Test description",
    #     currency=currency,
    #     material=material,
    #     quantity_in_stock=100,
    #     category=parent_category,
    #     price=10.99,
    #     dimensions=MagicMock(spec=Dimensions,depth=5.0, height=20.0, weight=2.0, width=10.0, length=30.0)
    # ))

# Add more mocked unit tests as needed