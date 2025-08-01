from abc import ABC, abstractmethod
from typing import Any, Optional


class ICacheProvider(ABC):
    """Interface for cache providers"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass