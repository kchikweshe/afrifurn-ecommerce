import logging
from typing import Generic, TypeVar, List, Optional, Type, Union
from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from database import db
T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T], collection_name: str):
        self.db = db
        self.model_class = model_class
        self.collection_name = collection_name
    async def insert_one(self, data: T, id: Optional[str] = None) ->str:
        try:
            collection = self.db[self.collection_name]


            # If no ID is provided, insert a new document
            result =  collection.insert_one(data)
            return result.inserted_id   # True if the document was inserted

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Repository error: Failed to create or update {self.collection_name}. {e}"
            )
    async def fetch_all(self) -> List[T]:
        try:
            docs =  self.db[self.collection_name].find()
            return [self.model_class(**doc) for doc in docs]
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to fetch {self.collection_name}. {e}")
    async def get_by_id(self, id: str) -> Optional[T]:
        try:
            doc =  self.db[self.collection_name].find_one({"_id": ObjectId(id)})
            if doc:
                return self.model_class(**doc)
            return None
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to fetch {self.collection_name}. {e}")

    async def find_one(self, filter_query: dict) -> Optional[T]:
        try:
            doc =  self.db[self.collection_name].find_one(filter_query)
            if doc:
                return self.model_class(**doc)
            return None
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to fetch {self.collection_name}: {e}")

    def filter(
        self,
        filter_query: dict,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "_id",
        sort_order: int = 1
    ) -> List[T]:
        try:
            cursor =  self.db[self.collection_name].find(filter_query)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            if sort_by:
                cursor = cursor.sort(sort_by, sort_order)
            
            results= [self.model_class(**item) for item in  cursor]
            # validate the type of the results
            if not all(isinstance(item, self.model_class) for item in results):
                
                raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to filter {self.collection_name}")
            return results
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to filter {self.collection_name}. {e}")

    async def update(self, id: str, update_data: dict) -> bool:
        try:
            result =  self.db[self.collection_name].update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to update {self.collection_name} \n {e}") 
        
    # delete method should be a soft delete
    async def delete(self, id: str) -> bool:
        try:
            result =  self.db[self.collection_name].update_one(
                {"_id": ObjectId(id)}, {"$set": {"is_archived": True}})
            return result.modified_count > 0
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Repository error: Failed to delete {self.collection_name}")

    # async def find_one(self, filter_query: dict) -> Optional[T]:
    #     """Fetch a single document from specified collection using filter query"""
    #     try:
    #         # Convert _id to ObjectId if present in filter
    #         if '_id' in filter_query:
    #             filter_query['_id'] = ObjectId(filter_query['_id'])
            
    #         doc =  self.db[self.collection_name].find_one(filter_query)
    #         if doc:
    #             return self.model_class(**doc)
    #         return None
    #     except Exception as e:
    #         raise HTTPException(status_code=404, 
    #                           detail=f"Document not found in {self.collection_name}")
    async def aggregate(self, pipeline: list) -> list:
        """
        Execute an aggregation pipeline on the products collection.

        Args:
            pipeline (list): The aggregation pipeline to execute.

        Returns:
            list: The results of the aggregation.
        """
        try:
            results =  list(self.db[self.collection_name].aggregate(pipeline))
            return results
        except Exception as e:
            logging.error(f"Error executing aggregation: {e}")
            raise