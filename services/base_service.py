from typing import Generic, TypeVar, List, Optional, Type, Any
from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from services.repository.base_repository import BaseRepository
from database import db
T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def create(self, item: T) -> bool|None:
        """Generic create method"""
        try:
            return await self.repository.insert_one(item.model_dump() )
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Service error: Failed to create item \n {e}")

    async def get_one(self, item_id: str) -> Optional[T]:
        """Generic method to get a single item"""
        try:
            doc = await self.repository.find_one({"_id":ObjectId(item_id)})
            if not doc:
                return None
            return self.repository.model_class(**doc)
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Service error: Failed to fetch item : {e}")

    async def filter(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "_id",
        sort_order: int = 1
    ) -> List[T]:
        """Generic filter method with pagination and sorting"""
        try:
            documents =  self.repository.filter(
                filters, skip, limit, sort_by, sort_order
            )
            return [doc for doc in documents]
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Service error: Failed to filter items,{e}")

    async def update(self, item_id: str, update_data: dict) -> bool:
        """Generic update method"""
        try:
            return await self.repository.update(item_id, update_data)
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail="Service error: Failed to update item")
    # TODO: add the logic to delete the item
    # TODO: add the logic to soft delete the item   
    async def soft_delete(self, item_id: str) -> bool:
        """Generic soft delete method"""
        return await self.repository.delete(item_id)
    # filter_one
    async def filter_one(self, filters: dict) -> Optional[T]:
        """Generic filter one method"""
        data:T|None =await self.repository.find_one(filters)
        return data

    async def update_related_document(
        self,
        collection_name: str,
        filter_query: dict,
        update_query: dict
    ) -> Any:
        """
        Update a related document in another collection
        """
        result = await db[collection_name].find_one_and_update(
            filter_query,
            update_query
        )
        return result