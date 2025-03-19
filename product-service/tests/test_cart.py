# import pytest
# from unittest.mock import AsyncMock, Mock, patch
# from models.cart import Cart, CartItem
# from models.products import Product, ProductVariant
# from routers.cart import add_product_to_cart  # Import the function directly
# from models.common import ResponseModel
# from services.cart_service import CartService
# from services.product_service import ProductService
# from services.product_variant_service import ProductVariantService
# from services.repository.product_variant_repository import ProductVariantRepository


# cart_service = Mock(spec=CartService)
# product_service = Mock(spec=ProductService)
# variant_service = Mock(spec=ProductVariantService)


# async def get_one_variant( item_id: str):
#     mock= Mock(spec=ProductVariant) 
#     mock._id=item_id
#     mock.product_id="product_789" 
#         # return None
#     return mock
# async def get_one_product( item_id: str):
#     mock= Mock(spec=Product) 
#     mock._id=item_id
#     return mock
# async def get_cart_item( cart_id:str, product_id:str, variant_id:str):
#     mock= Mock(spec=CartItem) 
#     mock._id="item_id"
#     mock.quantity=1
#     return mock
# async def get_cart_item_none( cart_id:str, product_id:str, variant_id:str):
#     return None

#     return mock
# async def update_item_quantity( 
#              cart_id: str, 
#             item_id: str, 
#             quantity: int
# ):
#     mock= Mock(spec=CartItem) 
#     mock._id=item_id
#     return mock

# async def add_to_cart_mock(   user_id:str,
#         product_id:str,

#         variant_id:str,
#         quantity:int):
#     mock= Mock(spec=Cart) 
#     return mock  


# @pytest.mark.asyncio
# async def test_add_product_to_cart_success():
#     """Test successful product addition to cart"""


#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="product_789",
#         quantity=2,
#         variant_id="variant_001",
#         cart_service=cart_service,
#         product_service=product_service,
#         product_variant_service=variant_service
#     )

#     assert response.status_code == 200
#     assert response.message == "Product added to cart successfully"
#     assert response.data['cart_id'] == "test_cart_123"
# @pytest.mark.asyncio
# async def test_add_product_to_cart_success_same_product(monkeypatch):
#     """Test successful product addition to cart"""

#     monkeypatch.setattr(variant_service, "get_one", get_one_variant
#                         )
#     monkeypatch.setattr(cart_service, "get_cart_item", get_cart_item_none
                        
#                         )
#     monkeypatch.setattr(cart_service, "update_item_quantity", update_item_quantity)

#     monkeypatch.setattr(cart_service, "add_to_cart", add_to_cart_mock)

#     monkeypatch.setattr(product_service, "get_one", get_one_product
#                         )
#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="product_789",
#         quantity=1,
#         variant_id="variant_001",
#         cart_service=cart_service,
#         product_service=product_service,
#         product_variant_service=variant_service
#     )

#     assert response.status_code == 200
#     assert response.message == "Product added to cart successfully"
#     assert response.data['cart_id'] == "test_cart_123"

#     monkeypatch.setattr(variant_service, "get_one", get_one_variant
#                         )
#     monkeypatch.setattr(cart_service, "get_cart_item", get_cart_item
                        
#                         )
#     monkeypatch.setattr(cart_service, "update_item_quantity", update_item_quantity)

#     monkeypatch.setattr(cart_service, "add_to_cart", add_to_cart_mock)

#     monkeypatch.setattr(product_service, "get_one", get_one_product
#                         )
#     response_two = await add_product_to_cart(
#     cart_id="test_cart_123",
#     user_id="user_456",
#     product_id="product_789",
#     quantity=1,
#     variant_id="variant_001",
#     cart_service=cart_service,
#     product_service=product_service,
#     product_variant_service=variant_service
# )

#     assert response_two.status_code == 200
#     assert response_two.message == "Product quantity updated successfully"
#     assert response_two.data['cart_id'] == "test_cart_123"

# @pytest.mark.asyncio
# async def test_add_product_to_cart_missing_variant(monkeypatch):
#     """Test scenario where product variant is not found"""
#        # variant_service.get_one = AsyncMock(return_value=None)  # Simulate variant not found
#     monkeypatch.setattr(variant_service, "get_one", get_one_variant
#                         )
#     monkeypatch.setattr(cart_service, "add_to_cart", add_to_cart_mock
#                         )
#     monkeypatch.setattr(product_service, "get_one", get_one_product
#                         )

#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="product_789",
#         quantity=2,
#         variant_id="variant_001",
#         product_variant_service=variant_service,
#         cart_service=cart_service,
#         product_service=product_service
   
#     )

#     assert response.status_code == -1
#     assert response.message == "Error. Product variant is not found."

# @pytest.mark.asyncio
# async def test_add_product_to_cart_missing_product():
#     """Test scenario where product is not found"""
#     product_service.get_one = AsyncMock(return_value=None)  # Simulate product not found

#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="nonexistent_product",
#         quantity=2,
#         variant_id="variant_001",
      
#     )

#     assert response.status_code == 404
#     assert "Product not found" in response.message

# @pytest.mark.asyncio
# async def test_add_product_to_cart_cart_addition_failure():
#     """Test scenario where cart addition fails"""


#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="product_789",
#         quantity=2,
#         variant_id="variant_001",
#         cart_service=cart_service,
#         product_service=product_service,
#         product_variant_service=variant_service
#     )

#     assert response.status_code == 500
#     assert response.message == "Failed to add product to cart"

# @pytest.mark.asyncio
# async def test_add_product_to_cart_invalid_quantity():
#     """Test adding product with invalid quantity"""
 

#     response = await add_product_to_cart(
#         cart_id="test_cart_123",
#         user_id="user_456",
#         product_id="product_789",
#         quantity=-1,  # Invalid quantity
#         variant_id="variant_001",

#     )

#     assert response.status_code in [400, 422]  # Adjust based on your validation logic