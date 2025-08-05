"""
Custom exceptions for the AfriFurn product service.
"""
from typing import Optional, Dict, Any


class AfriFurnException(Exception):
    """Base exception for AfriFurn application."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AfriFurnException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        details = {"field": field, "value": value} if field else {}
        super().__init__(message, "VALIDATION_ERROR", details)


class NotFoundError(AfriFurnException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, "NOT_FOUND", {"resource_type": resource_type, "resource_id": resource_id})


class DuplicateError(AfriFurnException):
    """Raised when trying to create a duplicate resource."""
    
    def __init__(self, resource_type: str, field: str, value: str):
        message = f"{resource_type} with {field} '{value}' already exists"
        super().__init__(message, "DUPLICATE", {"resource_type": resource_type, "field": field, "value": value})


class DatabaseError(AfriFurnException):
    """Raised when database operations fail."""
    
    def __init__(self, operation: str, details: str = None):
        message = f"Database {operation} failed"
        if details:
            message += f": {details}"
        super().__init__(message, "DATABASE_ERROR", {"operation": operation, "details": details})


class CacheError(AfriFurnException):
    """Raised when cache operations fail."""
    
    def __init__(self, operation: str, key: str = None, details: str = None):
        message = f"Cache {operation} failed"
        if key:
            message += f" for key '{key}'"
        if details:
            message += f": {details}"
        super().__init__(message, "CACHE_ERROR", {"operation": operation, "key": key, "details": details})


class AuthenticationError(AfriFurnException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR")


class AuthorizationError(AfriFurnException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message, "AUTHORIZATION_ERROR")


class BusinessLogicError(AfriFurnException):
    """Raised when business logic validation fails."""
    
    def __init__(self, message: str, business_rule: str = None):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", {"business_rule": business_rule})


class ExternalServiceError(AfriFurnException):
    """Raised when external service calls fail."""
    
    def __init__(self, service_name: str, operation: str, details: str = None):
        message = f"External service '{service_name}' {operation} failed"
        if details:
            message += f": {details}"
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", {
            "service_name": service_name,
            "operation": operation,
            "details": details
        }) 