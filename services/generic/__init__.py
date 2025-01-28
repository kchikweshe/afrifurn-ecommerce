# from abc import ABC, abstractmethod
# from typing import Dict, List

# from bson import ObjectId
# from database import db

# # Base repository interface for common CRUD operations
# class IRepository(ABC):
#     collection_name:str

#     def __init__(self,collection_name:str) -> None:
#         self.collection_name=collection_name
#         self.collection=db[self.collection_name]

    
#     async def create(self, item) -> str:
#         result_id=await create_document(
#             collection_name=self.collection_name,
#             document=item)
#         return result_id


#     async def find_by_id(self,key:str, item_id: str="_id"):
#       return  await fetch_one(
#             collection_name=self.collection_name,
#             key=key,
#             value=item_id
#         )
#     async def find_with_filters(self, filters: Dict, skip: int, limit: int, 
#                               sort_by: str, sort_order: int) -> List[Dict]:
#         return await self.collection.find(filters)\
#             .skip(skip)\
#             .limit(limit)\
#             .sort(sort_by, sort_order)\
#             .to_list(length=None)
#     # async def find_all(self) -> List:
#     #   items=await filter_items(
#     #     collection_name=self.collection_name
#     #     )
#     #   return items

#     async def update(self, item_id: str, updates: dict) -> bool:
#         filter_criteria = {"_id": ObjectId(item_id)}
#         updated=await update_document(collection_name=self.collection_name,
                        
#                      filter_criteria= filter_criteria,
#                      update_data=  updates
#                         )
#         if updated is None:
#             return False
#         return updated


#     async def delete(self, item_id: str):
#         pass

# # Repository interfaces for each entity
# class IProductRepository(IRepository):
#     def __init__(self) -> None:
#         super().__init__(collection_name="products")
        



# class CartItemRepository(IRepository):
#     def __init__(self) -> None:
#         super().__init__(collection_name="cart_items")

 

# class CartRepository(IRepository):
#        def __init__(self) -> None:
#         super().__init__(collection_name="cart")

# class ICategoryRepository(IRepository):
#        def __init__(self) -> None:
#         super().__init__(collection_name="categories")
        
# class ILevel1CategoryRepository(IRepository):
#        def __init__(self) -> None:
#         super().__init__(collection_name="level1_categories")

# class ILevel2CategoryRepository(IRepository):
#        def __init__(self) -> None:
#         super().__init__(collection_name="level2_categories")

# class IMaterialRepository(IRepository):
#        def __init__(self) -> None:
#         super().__init__(collection_name="materials")
