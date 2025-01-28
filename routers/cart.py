from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.cart import Cart, CartItem
from models.common import ResponseModel
from models.products import Product, ProductVariant
from dependencies.dependencies import get_cart_service, get_product_service, get_product_variant_service
from services.cart_service import CartService
from database import db
from services.product_service import ProductService
from services.product_variant_service import ProductVariantService
router = APIRouter(tags=["Cart"])

@router.post("/cart/create/{user_id}", response_model=ResponseModel)
async def create_cart(
    user_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    is_done = await cart_service.create(item=Cart(user_id=user_id))
    if not is_done or is_done==None:
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

@router.get("/cart/{cart_id}", response_model=Cart)
async def get_cart(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.get_one(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/cart/add-product/{cart_id}/",response_model=ResponseModel)
async def add_product_to_cart(
    cart_id:str,
    user_id: str=Query(None, description="User ID"),
    product_id: str= Query(None, description="Product ID"),
    quantity: int= Query(None, description="Quantity"),
    variant_id:str= Query(None, description="Variant ID"),
    cart_service: CartService = Depends(get_cart_service),
    product_service: ProductService = Depends(get_product_service),
    product_variant_service: ProductVariantService = Depends(get_product_variant_service)

): 
    try:
        product_variant=await product_variant_service.get_one(item_id=variant_id)
        if not isinstance(product_variant,ProductVariant):
             return ResponseModel.create(
                status_code=-1,
                message="Error. Product variant is not found.",
            )

        product = await product_service.get_one(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Check if the item already exists in the cart
        existing_item = await cart_service.get_cart_item(cart_id, product_id, variant_id)
        if existing_item is not None:
            # Update the quantity of the existing item
            cart_item_updated = await cart_service.update_item_quantity(cart_id, existing_item._id, existing_item.quantity + quantity)

            if not cart_item_updated:
                return ResponseModel.create(
                    status_code=500,
                    message=f"Product quantity update failed. Please try again",
                    data={"cart_id": cart_id}
                )
            return ResponseModel.create(
                    status_code=200,
                    message=f"Product quantity updated successfully",
                    data={"cart_id": cart_id}
                )
          
        else:
            # Add new item to the cart
            updated = await cart_service.add_to_cart(
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
            message="Failed to update product in cart",
        )
                
        
    
        return ResponseModel.create(
                        status_code=200,
                        message="Product added to cart successfully",
                        data={"cart_id": cart_id}
                    )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cart/{cart_id}/items/{item_id}")
async def remove_from_cart(
    cart_id: str,
    item_ids: List[str],
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        updated = await cart_service.remove_from_cart(cart_id, item_ids)
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
            message="Failed to remove item from cart",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cart/{cart_id}/items/{item_id}")
async def update_item_quantity(
    cart_id: str,
    item_id: str,
    quantity: int,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        updated = await cart_service.update_item_quantity(cart_id, item_id, quantity)
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
            message="Failed to update cart item quantity",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cart/{cart_id}/clear")
async def clear_cart(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        updated = await cart_service.clear_cart(cart_id)    
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
            message="Failed to clear cart",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
