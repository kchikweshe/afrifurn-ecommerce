"""
Authentication utilities for the AfriFurn product service.
"""
import os
from typing import Optional
from fastapi import HTTPException, status, Header
from core.exceptions import AuthenticationError, AuthorizationError


def verify_api_key(x_api_key: str = Header(..., description="API Key")) -> str:
    """
    Verify API key for authentication.
    
    Args:
        x_api_key: API key from header
        
    Returns:
        Verified API key
        
    Raises:
        AuthenticationError: If API key is invalid
    """
    expected_api_key = os.getenv("API_KEY", "your-super-secret-api-key")
    
    if not x_api_key:
        raise AuthenticationError("API key is required")
    
    if x_api_key != expected_api_key:
        raise AuthenticationError("Invalid API key")
    
    return x_api_key


def verify_admin_access(api_key: str) -> bool:
    """
    Verify admin access level.
    
    Args:
        api_key: Verified API key
        
    Returns:
        True if admin access is granted
        
    Raises:
        AuthorizationError: If admin access is denied
    """
    admin_api_key = os.getenv("ADMIN_API_KEY")
    
    if not admin_api_key:
        # If no admin key is set, all valid API keys have admin access
        return True
    
    if api_key != admin_api_key:
        raise AuthorizationError("Admin access required")
    
    return True


def verify_write_access(api_key: str) -> bool:
    """
    Verify write access level.
    
    Args:
        api_key: Verified API key
        
    Returns:
        True if write access is granted
    """
    # For now, any valid API key has write access
    # This can be extended with role-based access control
    return True


def get_user_from_token(token: str) -> Optional[dict]:
    """
    Extract user information from JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        User information if valid, None otherwise
    """
    # TODO: Implement JWT token validation
    # This is a placeholder for future JWT implementation
    return None


def verify_user_permission(user_id: str, resource_id: str, action: str) -> bool:
    """
    Verify user permission for specific action on resource.
    
    Args:
        user_id: User ID
        resource_id: Resource ID
        action: Action to perform
        
    Returns:
        True if permission is granted
        
    Raises:
        AuthorizationError: If permission is denied
    """
    # TODO: Implement permission checking logic
    # This is a placeholder for future permission system
    return True 