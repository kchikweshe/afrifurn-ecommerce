"""
Improved base repository implementation following SOLID principles.
"""
import logging
from typing import Generic, TypeVar, List, Optional, Type, Dict, Any
from pydantic import BaseModel
from bson import ObjectId
from database import db
from core.interfaces import IRepository
from core.exceptions import DatabaseError, NotFoundError, DuplicateError
from core.dto import PaginationParams, SortParams

T = TypeVar('T', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseRepository(IRepository[T]):
    """
    Base repository implementation following the Repository pattern.
    
    This class provides common CRUD operations and follows SOLID principles:
    - Single Responsibility: Only handles data access
    - Open/Closed: Extensible through inheritance
    - Liskov Substitution: Can be replaced with any IRepository implementation
    - Interface Segregation: Implements only necessary methods
    - Dependency Inversion: Depends on abstractions
    """
    
    def __init__(self, model_class: Type[T], collection_name: str):
        """
        Initialize the repository.
        
        Args:
            model_class: The Pydantic model class for this repository
            collection_name: The MongoDB collection name
        """
        self.db = db
        self.model_class = model_class
        self.collection_name = collection_name
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    async def create(self, data: CreateSchema) -> str:
        """
        Create a new entity.
        
        Args:
            data: The data to create
            
        Returns:
            The ID of the created entity
            
        Raises:
            DatabaseError: If database operation fails
            DuplicateError: If entity already exists
        """
        try:
            collection = self.db[self.collection_name]
            
            # Check for duplicates if unique fields exist
            await self._check_duplicates(data)
            
            # Convert to dict and insert
            data_dict = data.dict()
            result = collection.insert_one(data_dict)
            
            self.logger.info(f"Created {self.collection_name} with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except DuplicateError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to create {self.collection_name}: {e}")
            raise DatabaseError("create", str(e))
    
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Get entity by ID.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            The entity if found, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            if not ObjectId.is_valid(entity_id):
                return None
                
            doc = self.db[self.collection_name].find_one({"_id": ObjectId(entity_id)})
            
            if doc:
                return self.model_class(**doc)
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get {self.collection_name} by ID {entity_id}: {e}")
            raise DatabaseError("get_by_id", str(e))
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all entities with pagination.
        
        Args:
            skip: Number of entities to skip
            limit: Maximum number of entities to return
            
        Returns:
            List of entities
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            cursor = self.db[self.collection_name].find().skip(skip).limit(limit)
            return [self.model_class(**doc) for doc in cursor]
            
        except Exception as e:
            self.logger.error(f"Failed to get all {self.collection_name}: {e}")
            raise DatabaseError("get_all", str(e))
    
    async def update(self, entity_id: str, data: UpdateSchema) -> bool:
        """
        Update an entity.
        
        Args:
            entity_id: The entity ID
            data: The update data
            
        Returns:
            True if updated, False otherwise
            
        Raises:
            DatabaseError: If database operation fails
            NotFoundError: If entity not found
        """
        try:
            if not ObjectId.is_valid(entity_id):
                raise NotFoundError(self.collection_name, entity_id)
            
            # Remove None values from update data
            update_data = {k: v for k, v in data.dict().items() if v is not None}
            
            if not update_data:
                return False
            
            result = self.db[self.collection_name].update_one(
                {"_id": ObjectId(entity_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError(self.collection_name, entity_id)
            
            self.logger.info(f"Updated {self.collection_name} with ID: {entity_id}")
            return result.modified_count > 0
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to update {self.collection_name} {entity_id}: {e}")
            raise DatabaseError("update", str(e))
    
    async def delete(self, entity_id: str) -> bool:
        """
        Soft delete an entity.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            True if deleted, False otherwise
            
        Raises:
            DatabaseError: If database operation fails
            NotFoundError: If entity not found
        """
        try:
            if not ObjectId.is_valid(entity_id):
                raise NotFoundError(self.collection_name, entity_id)
            
            result = self.db[self.collection_name].update_one(
                {"_id": ObjectId(entity_id)},
                {"$set": {"is_archived": True}}
            )
            
            if result.matched_count == 0:
                raise NotFoundError(self.collection_name, entity_id)
            
            self.logger.info(f"Soft deleted {self.collection_name} with ID: {entity_id}")
            return result.modified_count > 0
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to delete {self.collection_name} {entity_id}: {e}")
            raise DatabaseError("delete", str(e))
    
    async def find_by_criteria(
        self, 
        criteria: Dict[str, Any], 
        skip: int = 0, 
        limit: int = 100,
        sort_by: str = "_id",
        sort_order: int = 1
    ) -> List[T]:
        """
        Find entities by criteria.
        
        Args:
            criteria: Search criteria
            skip: Number of entities to skip
            limit: Maximum number of entities to return
            sort_by: Field to sort by
            sort_order: Sort order (1=asc, -1=desc)
            
        Returns:
            List of entities matching criteria
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            cursor = self.db[self.collection_name].find(criteria)
            
            if sort_by:
                cursor = cursor.sort(sort_by, sort_order)
            
            cursor = cursor.skip(skip).limit(limit)
            
            return [self.model_class(**doc) for doc in cursor]
            
        except Exception as e:
            self.logger.error(f"Failed to find {self.collection_name} by criteria: {e}")
            raise DatabaseError("find_by_criteria", str(e))
    
    async def count(self, criteria: Dict[str, Any] = None) -> int:
        """
        Count entities matching criteria.
        
        Args:
            criteria: Search criteria (optional)
            
        Returns:
            Number of entities matching criteria
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            filter_criteria = criteria or {}
            return self.db[self.collection_name].count_documents(filter_criteria)
            
        except Exception as e:
            self.logger.error(f"Failed to count {self.collection_name}: {e}")
            raise DatabaseError("count", str(e))
    
    async def exists(self, entity_id: str) -> bool:
        """
        Check if entity exists.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            if not ObjectId.is_valid(entity_id):
                return False
            
            return self.db[self.collection_name].count_documents({"_id": ObjectId(entity_id)}) > 0
            
        except Exception as e:
            self.logger.error(f"Failed to check existence of {self.collection_name} {entity_id}: {e}")
            return False
    
    async def _check_duplicates(self, data: CreateSchema) -> None:
        """
        Check for duplicate entities.
        
        Args:
            data: The data to check
            
        Raises:
            DuplicateError: If duplicate found
        """
        # Override in subclasses to implement duplicate checking
        pass
    
    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute aggregation pipeline.
        
        Args:
            pipeline: MongoDB aggregation pipeline
            
        Returns:
            Aggregation results
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            cursor = self.db[self.collection_name].aggregate(pipeline)
            return list(cursor)
            
        except Exception as e:
            self.logger.error(f"Failed to execute aggregation on {self.collection_name}: {e}")
            raise DatabaseError("aggregate", str(e)) 