
from typing import List, Optional

from fastapi.logger import logger
from models.cart import Cart, CartItem
from models.common import ErrorResponseModel, ResponseModel
from models.products import Product
from services.cart.exceptions import CartNotFoundException, UpdateFailedException
from services.generic import CartItemRepository, CartRepository



class CartService:
    def __init__(self, cart_repository: CartRepository, cart_item_repository: CartItemRepository):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
    async def user_cart_exists(self, user_id: str) -> Optional[bool]:
        '''
    Asynchronously checks if a cart exists for a specific user.

    Args:
        user_id (str): The ID of the user to check for cart existence.

    Returns:
        Optional[bool]: True if the cart exists, False if not found, or None if an error occurs.
    '''
        try:
            cart = await self.cart_repository.find_by_id(key="user_id", item_id=user_id)
            return cart is not None
        except CartNotFoundException as e:
            logger.debug(f"Cart not found: {e}")
            

       
    async def create_cart(self, user_id: str) -> Optional[str]:
        """
        Asynchronously creates a new cart for a user if one does not already exist.

        Args:
            user_id (str): The ID of the user for whom the cart is being created.

        Returns:
            Optional[str]: The result_id if cart creation is successful, else a ResponseModel.
        """
        if not user_id:
            logger.info(f"Invalid user_id: {user_id}")
            return None

        try:
            if await self.user_cart_exists(user_id=user_id):
                logger.info(f"Cart already exists for user: {user_id}")
                return None

            cart = Cart(user_id=user_id)
            result_id = await self.cart_repository.create(item=cart)
            logger.info(f"Cart created successfully for user: {user_id}")
            return result_id
        except Exception as e:
            return None
    async def add_product_to_cart(self, cart_id: str, product: Product, quantity: int):
        try:
            cart = await self.cart_repository.find_by_id(cart_id)
            if cart is None:
                raise Exception("Cart not found")

            for item in cart.items:
                if item.product.name == product.name:
                    item.quantity += quantity
                    await self.cart_item_repository.update(item_id=str(item.id), updates=item.model_dump())
                    break
            else:
                cart_item = CartItem(product=product, quantity=quantity)
                cart_item_saved_id = await self.cart_item_repository.create(cart_item)
                cart_item.id = cart_item_saved_id
                cart.items.append(cart_item)

        except Exception as e:
            raise e

        updated = await self.cart_repository.update(item_id=cart_id, updates=cart.model_dump())

        return updated

        # Business logic for adding product to cart
        # Use the repositories to manage Cart and CartItem entities

   
    async def remove_products_from_cart(self, cart_id: str, product_ids: List[str]) -> bool:
        try:
            logger.info(f"Removing products from cart with ID: {cart_id}")
            cart_repo = self.cart_repository
            cart: Cart = await cart_repo.find_by_id(cart_id)

            if cart is None:
                logger.error("Cart not found")
                raise CartNotFoundException("Cart not found")
            existing_list = cart.pop_cart_items_by_ids(ids_to_pop=product_ids)
            logger.info(f"Products removed from cart: {product_ids}")
            updated: bool = await cart_repo.update(item_id=cart_id, updates={"cart_items": existing_list})
            if not updated == True:
                logger.error("Failed to update cart")
                raise UpdateFailedException("Failed to update")
            logger.info("Cart update successful")
            return updated
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e
 