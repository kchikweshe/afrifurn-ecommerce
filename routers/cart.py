from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.cart import Cart, CartItem
from models.common import ResponseModel
from models.products import Product
from services.cart import CartService
from services.cart.exceptions import CartNotFoundException, UpdateFailedException
from services.generic import CartItemRepository, CartRepository

router = APIRouter()

# Dependency to get CartService instance
async def get_cart_service():
    # Initialize and return CartService instance
    # You may need to adjust this based on your dependency injection setup
    cart_repository = CartRepository()  # Initialize CartRepository
    cart_item_repository = CartItemRepository()  # Initialize CartItemRepository
    return CartService(cart_repository, cart_item_repository)

@router.post("/cart/{cart_id}/add-product")
async def add_product_to_cart(
    cart_id: str,
    product: Product,
    quantity: int,
    cart_service: CartService = Depends(get_cart_service)
)  : # type: ignore
    try:
        updated = await cart_service.add_product_to_cart(cart_id, product, quantity)
        if updated:
            return ResponseModel(message="Product added to cart successfully")
        else:
            # raise HTTPException(status_code=400, detail="Failed to add product to cart")
            return ResponseModel(message="Failed to add product to cart")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cart/{user_id}")
async def create_cart(
    user_id:str,
    cart_service: CartService = Depends(get_cart_service)
):
    
    try:
      cart= await cart_service.user_cart_exists(user_id)
      if cart is Cart :
          return ResponseModel(message="Cart for this user already exists",code=99)
 
      response=await cart_service.create_cart(user_id)
      
      
      return ResponseModel(message="Cart created successfully")
    except CartNotFoundException:
        raise HTTPException(status_code=404, detail="Cart not found")
    
@router.post("/cart/{cart_id}/remove-products")
async def remove_products_from_cart(
    cart_id: str,
    product_ids: List[str],
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        updated = await cart_service.remove_products_from_cart(cart_id, product_ids)
        if updated:
            return {"message": "Products removed from cart successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to remove products from cart")
    except CartNotFoundException:
        raise HTTPException(status_code=404, detail="Cart not found")
    except UpdateFailedException:
        raise HTTPException(status_code=400, detail="Failed to update cart")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))