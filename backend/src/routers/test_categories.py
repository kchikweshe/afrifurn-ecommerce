# Return 404 error if level_1_category_id is empty
import pytest

from .categories import create_level2_category


@pytest.mark.asyncio
async def test_create_level2_category_empty_id( mocker):
    # Mock the db collection
    mocker.patch("database.db['level1_categories'].find_one", return_value=None)

    # Call the create_level2_category function
    response = await create_level2_category(name="valid_name", level_1_category_id="")

    # Assert the error response
    assert response["error"] == ""
    assert response["message"] == "Category not found"
    assert response["code"] == "404"