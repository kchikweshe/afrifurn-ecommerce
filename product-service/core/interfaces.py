"""
Core interfaces following SOLID principles for the AfriFurn product service.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel

# Type variables for generic interfaces
T = TypeVar('T', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class IRepository(ABC, Generic[T]):
    """Repository interface following the Repository pattern."""
    
    @abstractmethod
    async def create(self, data: CreateSchema) -> str:
        """Create a new entity and return its ID."""
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, data: UpdateSchema) -> bool:
        """Update an entity."""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Soft delete an entity."""
        pass
    
    @abstractmethod
    async def find_by_criteria(self, criteria: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[T]:
        """Find entities by criteria."""
        pass


class IService(ABC, Generic[T]):
    """Service interface following the Service pattern."""
    
    @abstractmethod
    async def create_entity(self, data: CreateSchema) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def get_entity_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    async def get_all_entities(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    async def update_entity(self, entity_id: str, data: UpdateSchema) -> Optional[T]:
        """Update an entity."""
        pass
    
    @abstractmethod
    async def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity."""
        pass


class ICacheService(ABC):
    """Cache service interface."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Set value in cache."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass


class IValidator(ABC):
    """Validation interface."""
    
    @abstractmethod
    async def validate_create_data(self, data: CreateSchema) -> bool:
        """Validate create data."""
        pass
    
    @abstractmethod
    async def validate_update_data(self, data: UpdateSchema) -> bool:
        """Validate update data."""
        pass


class ILogger(ABC):
    """Logging interface."""
    
    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        pass
    
    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        pass
    
    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        pass
    
    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        pass 