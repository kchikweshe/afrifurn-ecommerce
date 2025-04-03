import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from models.products import Product
from services.product_service import ProductService

@pytest.fixture
def mock_repositories():
    return {
        'repository': AsyncMock(),
        'color_repository': AsyncMock(),
        'material_repository': AsyncMock(),
        'currency_repository': AsyncMock(),
        'level2category_repository': AsyncMock(),
        'image_processor': AsyncMock()
    }

@pytest.fixture
def product_service(mock_repositories):
    return ProductService(**mock_repositories)

class TestProductService:
    
    async def test_increment_product_views_success(self, product_service):
        # Arrange
        product_id = "test_id"
        product_service.repository.update.return_value = True
        
        # Act
        await product_service.increment_product_views(product_id)
        
        # Assert
        product_service.repository.update.assert_called_once_with(
            product_id,
            {"$inc": {"views": 1}}
        )

    async def test_get_product_references_success(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#fdgdgd', '#fffff']
        }
        
        product_service.level2category_repository.get_category.return_value = {'id': 'cat1'}
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        product_service.color_repository.get_color.return_value = {'color_id': '#fdgdgd'}
        
        # Act
        result = await product_service.get_product_references(**test_data)
        
        # Assert
        assert len(result) == 4
        assert result[0] == {'id': 'cat1'}
        assert result[1] == {'code': 'USD'}
        assert result[2] == {'id': 'mat1'}
        assert len(result[3]) == 2

    async def test_get_product_references_missing_category(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#fdgdgd', '#fffff']
        }
        
        product_service.level2category_repository.get_category.return_value = None
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        product_service.color_repository.get_color.return_value = {'color_id': 'red'}
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await product_service.get_product_references(**test_data)
        assert exc.value.status_code == 404

    async def test_get_product_references_repository_error(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#fdgdgd', '#fffff']
        }
        
        product_service.level2category_repository.get_category.side_effect = Exception("DB Error")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await product_service.get_product_references(**test_data)
        assert exc.value.status_code == 404

    async def test_get_products_by_category_success(self, product_service):
        # Arrange
        category_name = "test_category"
        expected_products = [{"id": "1", "name": "Product 1"}, {"id": "2", "name": "Product 2"}]
        product_service.repository.filter.return_value = expected_products
        
        # Act
        result = await product_service.get_products_by_category(category_name)
        
        # Assert
        assert result == expected_products
        product_service.repository.filter.assert_called_once_with(
            {
                "category": category_name,
                "is_archived": False
            },
            skip=0,
            limit=20,
            sort_by="views",
            sort_order=1
        )

    async def test_get_products_by_category_with_pagination(self, product_service):
        # Arrange
        category_name = "test_category"
        limit = 5
        page = 2
        skip = 5
        sort_by = "price"
        sort_order = -1
        
        # Act
        await product_service.get_products_by_category(
            category_name,
            limit=limit,
            page=page,
            skip=skip,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Assert
        product_service.repository.filter.assert_called_once_with(
            {
                "category": category_name,
                "is_archived": False
            },
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )

    @patch('os.path.join')
    async def test_save_product_images_success(self, mock_path_join, product_service):
        # Arrange
        mock_path_join.return_value = "/test/path"
        images = [AsyncMock(), AsyncMock()]
        product_id = "test_id"
        expected_paths = ["/test/path/1.webp", "/test/path/2.webp"]
        product_service.image_processor.process_image.side_effect = expected_paths
        
        # Act
        result = await product_service.save_product_images(images, product_id)
        
        # Assert
        assert result == expected_paths
        assert product_service.image_processor.process_image.call_count == 2

    async def test_delete_product_success(self, product_service):
        # Arrange
        product_id = "test_id"
        product_service.repository.delete.return_value = True
        
        # Act
        result = await product_service.delete_product(product_id)
        
        # Assert
        assert result is True
        product_service.repository.delete.assert_called_once_with(product_id)

    async def test_delete_product_failure(self, product_service):
        # Arrange
        product_id = "test_id"
        product_service.repository.delete.return_value = False
        
        # Act
        result = await product_service.delete_product(product_id)
        
        # Assert
        assert result is False
        product_service.repository.delete.assert_called_once_with(product_id)

    async def test_get_product_references_with_valid_colors(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#fec76j', '#ffffff']
        }
        
        product_service.level2category_repository.get_category.return_value = {'id': 'cat1'}
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        product_service.color_repository.get_color.return_value = {
            '_id': '66db2ba359c1f33bc0754e25',
            'name': 'Pine',
            'color_code': '#fec76j',
            'image': 'static/colors/pine.jpg',
            'is_archived': False
        }
        
        # Act
        result = await product_service.get_product_references(**test_data)
        
        # Assert
        assert len(result) == 4
        assert len(result[3]) == 2  # Two colors
        assert result[3][0]['color_code'] == '#fec76j'
        assert result[3][0]['image'] == 'static/colors/pine.jpg'
        
    async def test_get_product_references_with_archived_color(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#fec76j']
        }
        
        product_service.level2category_repository.get_category.return_value = {'id': 'cat1'}
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        product_service.color_repository.get_color.return_value = {
            '_id': '66db2ba359c1f33bc0754e25',
            'name': 'Pine',
            'color_code': '#fec76j',
            'image': 'static/colors/pine.jpg',
            'is_archived': True  # Archived color
        }
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await product_service.get_product_references(**test_data)
        assert exc.value.status_code == 404
        assert "archived color" in str(exc.value.detail).lower()

    async def test_get_product_references_with_nonexistent_color(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': ['#nonexistent']
        }
        
        product_service.level2category_repository.get_category.return_value = {'id': 'cat1'}
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        product_service.color_repository.get_color.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await product_service.get_product_references(**test_data)
        assert exc.value.status_code == 404
        assert "color not found" in str(exc.value.detail).lower()


    async def test_get_product_references_with_empty_colors(self, product_service):
        # Arrange
        test_data = {
            'currency_code': 'USD',
            'material_id': 'mat1',
            'category_id': 'cat1',
            'colors': []
        }
        
        product_service.level2category_repository.get_category.return_value = {'id': 'cat1'}
        product_service.currency_repository.get_currency.return_value = {'code': 'USD'}
        product_service.material_repository.get_material.return_value = {'id': 'mat1'}
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await product_service.get_product_references(**test_data)
        assert exc.value.status_code == 404
        assert "no colors" in str(exc.value.detail).lower()
    # test product service create product
    @pytest.mark.asyncio
    async def test_create_product_success(self, product_service):
        # Arrange
        product_data = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": 100,
            "currency": "USD",
            "material": "mat1",
            "category": "cat1",
            "colors": ["#fdgdgd", "#fffff"],
            "width": 600,
            "height": 300,
            "length": 1200,
            "depth": 100,
            "short_name": "test_short_name"




        }
        product_service.repository.create.return_value = True
        dimensions={"width": 600, "height": 300, "length": 1200,"depth":100,"weight":10}
        product_data["dimensions"]=dimensions
        product=Product(**product_data)
        # Act

        result = await product_service.create(product)

        
        # Assert
        assert result == True
        product_service.repository.create.assert_called_once()

   # test create product with depth and weight missing
    @pytest.mark.asyncio
    async def test_create_product_with_depth_and_weight_missing(self, product_service):
        # Arrange
        product_data = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": 100,
            "currency": "USD",
            "material": "mat1",
            "category": "cat1",
            "colors": ["#fdgdgd", "#fffff"],
            "short_name": "test_short_name"
        }
        product_service.repository.create.return_value = True
        dimensions={"width": 600, "height": 300, "length": 1200}
        product_data["dimensions"]=dimensions
        product=Product(**product_data)
        # Act
        result = await product_service.create(product)
        # Assert
        assert result == True
        product_service.repository.create.assert_called_once()

# when product is fetched from db it should have , product variant should be created,Level2Category should be fetched
