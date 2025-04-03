# from typing import List, Optional

# from fastapi import HTTPException
# from fastapi.logger import logger
# from models.cart import Cart, CartItem
# from models.common import ErrorResponseModel, ResponseModel
# from models.products import Product
# from services.cart.exceptions import CartNotFoundException, UpdateFailedException
# from services.generic import CartItemRepository, CartRepository



# class CartService:
#     def __init__(self, cart_repository: CartRepository, cart_item_repository: CartItemRepository):
#         self.cart_repository = cart_repository
#         self.cart_item_repository = cart_item_repository
#     async def user_cart_exists(self, user_id: str) -> Optional[bool]:
#         '''
#     Asynchronously checks if a cart exists for a specific user.

#     Args:
#         user_id (str): The ID of the user to check for cart existence.

#     Returns:
#         Optional[bool]: True if the cart exists, False if not found, or None if an error occurs.
#     '''
#         try:
#             cart = await self.cart_repository.find_by_id(key="user_id", item_id=user_id)
#             return cart is not None
#         except CartNotFoundException as e:
#             logger.debug(f"Cart not found: {e}")
            

       
#     async def create_cart(self, user_id: str) -> Optional[str]:
#         """
#         Asynchronously creates a new cart for a user if one does not already exist.

#         Args:
#             user_id (str): The ID of the user for whom the cart is being created.

#         Returns:
#             Optional[str]: The result_id if cart creation is successful, else a ResponseModel.
#         """
#         if not user_id:
#             logger.info(f"Invalid user_id: {user_id}")
#             return None

#         try:
#             if await self.user_cart_exists(user_id=user_id):
#                 logger.info(f"Cart already exists for user: {user_id}")
#                 return None

#             cart = Cart(user_id=user_id)
#             result_id = await self.cart_repository.create(item=cart)
#             logger.info(f"Cart created successfully for user: {user_id}")
#             return result_id
#         except Exception as e:
#             return None
#     async def add_product_to_cart(self, cart_id: str, product: Product, quantity: int,selected_color: str):
#         try:
#             cart = await self.cart_repository.find_by_id(cart_id)
#             if cart is None:
#                 raise Exception("Cart not found")

#             for item in cart.items:
#                 if item.product.name == product.name:
#                     item.quantity += quantity
#                     await self.cart_item_repository.update(item_id=str(item.id), updates=item.model_dump())
#                     break
#             else:
#                 cart_item = CartItem(
#                     product=product,
#                     quantity=quantity,
                
#                     selected_color=selected_color,
#                     unit_price=product.price,
#                     total_price=product.price * quantity
#                 )
#                 cart_item_saved_id = await self.cart_item_repository.create(cart_item)
#                 cart_item.id = cart_item_saved_id
#                 cart.items.append(cart_item)

#         except Exception as e:
#             raise e

#         updated = await self.cart_repository.update(item_id=cart_id, updates=cart.model_dump())

#         return updated

#         # Business logic for adding product to cart
#         # Use the repositories to manage Cart and CartItem entities

   
#     async def remove_products_from_cart(self, cart_id: str, product_ids: List[str]) -> bool:
#         try:
#             logger.info(f"Removing products from cart with ID: {cart_id}")
#             cart_repo = self.cart_repository
#             cart: Cart = await cart_repo.find_by_id(cart_id)

#             if cart is None:
#                 logger.error("Cart not found")
#                 raise CartNotFoundException("Cart not found")
#             # Filter out items with IDs in product_ids
#             existing_list = [item for item in cart.items if str(item.id) not in product_ids]
#             logger.info(f"Products removed from cart: {product_ids}")
#             updated: bool = await cart_repo.update(item_id=cart_id, updates={"cart_items": existing_list})
#             if not updated == True:
#                 logger.error("Failed to update cart")
#                 raise UpdateFailedException("Failed to update")
#             logger.info("Cart update successful")
#             return updated
#         except Exception as e:
#             logger.error(f"An error occurred: {e}")
#             raise e
 
#     async def update_item_quantity(
#             self, 
#             cart_id: str, 
#             item_id: str, 
#             quantity: int
#         ) -> bool:
#             cart = await self.get_cart(cart_id)
#             if not cart:
#                 raise HTTPException(status_code=404, detail="Cart not found")

#             item = next((item for item in cart.items if str(item.id) == item_id), None)
#             if not item:
#                 raise HTTPException(status_code=404, detail="Item not found in cart")

#             # Validate new quantity against stock
#             if not item.product.is_variant_available(item.selected_color, quantity):
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Requested quantity not available in stock"
#                 )

#             item.quantity = quantity
#             item.calculate_total()
#             cart.calculate_total()

#             result = await self.cart_repository.update_one(
#                 {"_id": cart_id},
#                 {"$set": cart.dict()}
#             )

#             return result.modified_count > 0 
        

#     async def get_cart(self, cart_id: str) -> Optional[Cart]:
#         cart_data =  await self.cart_repository.find_by_id(cart_id)
#         return Cart(**cart_data) if cart_data else None

#     async def clear_cart(self, cart_id: str) -> dict:
#         """
#         Asynchronously clears all items from a cart.

#         Args:
#             cart_id (str): The ID of the cart to clear.

#         Returns:
#             dict: Operation result containing success status and details.

#         Raises:
#             CartNotFoundException: If the cart is not found.
#             UpdateFailedException: If the cart update fails.
#         """
#         try:
#             logger.info(f"Clearing cart with ID: {cart_id}")
#             cart = await self.get_cart(cart_id)
            
#             if not cart:
#                 logger.error("Cart not found")
#                 raise CartNotFoundException("Cart not found")
            
#             items_removed = len(cart.items)
#             cart.items = []
#             cart.calculate_total()  # Assuming Cart model has this method
            
#             updated = await self.cart_repository.update(
#                 item_id=cart_id, 
#                 updates=cart.model_dump()
#             )
            
#             if not updated:
#                 logger.error("Failed to clear cart")
#                 raise UpdateFailedException("Failed to update cart")
                
#             logger.info(f"Successfully cleared cart {cart_id}, removed {items_removed} items")
#             return {
#                 "success": True,
#                 "items_removed": items_removed,
#                 "cart_id": cart_id,
#                 "new_total": cart.total_amount
#             }
            
#         except (CartNotFoundException, UpdateFailedException) as e:
#             logger.error(f"Error clearing cart: {str(e)}")
#             raise e
#         except Exception as e:
#             logger.error(f"Unexpected error clearing cart: {str(e)}")
#             raise e
