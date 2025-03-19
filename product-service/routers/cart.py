from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.cart import Cart, CartItem
from models.common import ResponseModel
from models.products import ProductVariant
from services.repository.cart_repository import CartRepository
from services.repository.product_repository import ProductRepository
from services.repository.product_variant_repository import ProductVariantRepository

router = APIRouter(tags=["Cart"])

# Initialize repositories
cart_repository = CartRepository()
product_repository = ProductRepository()
product_variant_repository = ProductVariantRepository()

@router.post("/cart/create/{user_id}", response_model=ResponseModel)
async def create_cart(user_id: str):
    """Create a new cart for a user"""
    try:
        cart = Cart(user_id=user_id)
        is_created = await cart_repository.insert_one(cart.model_dump())
        if not is_created:
            return ResponseModel(
                class_name="Cart",
                status_code=-1,
                number_of_data_items=1,
                message="Cart creation failed."
            )

        return ResponseModel(
            class_name="Cart",
            status_code=201,
            number_of_data_items=1,
            message="Cart created successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cart/{cart_id}", response_model=Cart)
async def get_cart(cart_id: str):
    """Get a cart by ID"""
    try:
        cart = await cart_repository.fetch_one({"_id": cart_id})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cart/add-product/{cart_id}/", response_model=ResponseModel)
async def add_product_to_cart(
    cart_id: str,
    user_id: str = Query(None, description="User ID"),
    product_id: str = Query(None, description="Product ID"),
    quantity: int = Query(None, description="Quantity"),
    variant_id: str = Query(None, description="Variant ID")
):
    """Add a product to a cart"""
    try:
        # Verify product variant exists
        product_variant = await product_variant_repository.fetch_one({"_id": variant_id})
        if not isinstance(product_variant, ProductVariant):
            return ResponseModel.create(
                status_code=-1,
                message="Error. Product variant is not found."
            )

        # Verify product exists
        product = await product_repository.fetch_one({"_id": product_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if item already exists in cart
        existing_item = await cart_repository.get_cart_item(cart_id, product_id, variant_id)
        if existing_item:
            # Update quantity of existing item
            updated = await cart_repository.update_item_quantity(
                cart_id,
                existing_item._id,
                existing_item.quantity + quantity
            )
            if not updated:
                return ResponseModel.create(
                    status_code=500,
                    message="Product quantity update failed. Please try again",
                    data={"cart_id": cart_id}
                )
            return ResponseModel.create(
                status_code=200,
                message="Product quantity updated successfully",
                data={"cart_id": cart_id}
            )
        else:
            # Add new item to cart
            updated = await cart_repository.add_to_cart(
                user_id=user_id,
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity
            )
            if not updated:
                return ResponseModel(
                    data={},
                    class_name="Cart",
                    status_code=500,
                    number_of_data_items=0,
                    message="Failed to update product in cart"
                )

            return ResponseModel.create(
                status_code=200,
                message="Product added to cart successfully",
                data={"cart_id": cart_id}
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cart/{cart_id}/items/{item_id}")
async def remove_from_cart(
    cart_id: str,
    item_ids: List[str]
):
    """Remove items from a cart"""
    try:
        updated = await cart_repository.remove_from_cart(cart_id, item_ids)
        if updated:
            return ResponseModel(
                class_name="Cart",
                status_code=200,
                number_of_data_items=1,
                message="Item removed from cart successfully",
                data={}
            )
        return ResponseModel(
            data={},
            class_name="Cart",
            status_code=500,
            number_of_data_items=0,
            message="Failed to remove item from cart"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cart/{cart_id}/items/{item_id}")
async def update_item_quantity(
    cart_id: str,
    item_id: str,
    quantity: int
):
    """Update the quantity of an item in a cart"""
    try:
        updated = await cart_repository.update_item_quantity(cart_id, item_id, quantity)
        if updated:
            return ResponseModel(
                class_name="Cart",
                status_code=200,
                number_of_data_items=1,
                message="Cart item quantity updated successfully",
                data={}
            )
        return ResponseModel(
            data={},
            class_name="Cart",
            status_code=500,
            number_of_data_items=0,
            message="Failed to update cart item quantity"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cart/{cart_id}/clear")
async def clear_cart(cart_id: str):
    """Clear all items from a cart"""
    try:
        updated = await cart_repository.clear_cart(cart_id)
        if updated:
            return ResponseModel(
                class_name="Cart",
                status_code=200,
                number_of_data_items=1,
                message="Cart cleared successfully",
                data={}
            )
        return ResponseModel(
            data={},
            class_name="Cart",
            status_code=500,
            number_of_data_items=0,
            message="Failed to clear cart"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
