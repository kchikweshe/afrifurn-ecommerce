"""
Validation utilities for the AfriFurn product service.
"""
import csv
import io
from typing import List, Dict, Any
from functools import wraps
from fastapi import HTTPException, status, UploadFile
from core.exceptions import ValidationError


def validate_csv_file(func):
    """
    Decorator to validate CSV file upload.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get('file')
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is required"
            )
        
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a CSV file"
            )
        
        # Check file size (max 10MB)
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        return await func(*args, **kwargs)
    
    return wrapper


def validate_csv_headers(func):
    """
    Decorator to validate CSV headers.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get('file')
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is required"
            )
        
        # Read first line to check headers
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV headers
        csv_reader = csv.reader(io.StringIO(csv_content))
        headers = next(csv_reader, [])
        
        # Required headers for product import
        required_headers = [
            'name', 'short_name', 'description', 'category_id',
            'price', 'currency_code', 'material_id', 'width',
            'length', 'height'
        ]
        
        missing_headers = [header for header in required_headers if header not in headers]
        
        if missing_headers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required headers: {', '.join(missing_headers)}"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        return await func(*args, **kwargs)
    
    return wrapper


def validate_product_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate product data.
    
    Args:
        data: Product data to validate
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Required fields
    required_fields = ['name', 'short_name', 'description', 'price']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # Validate price
    price = data.get('price')
    if price is not None and (not isinstance(price, (int, float)) or price <= 0):
        errors.append("Price must be a positive number")
    
    # Validate dimensions
    dimensions = ['width', 'length', 'height']
    for dim in dimensions:
        value = data.get(dim)
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            errors.append(f"{dim} must be a positive number")
    
    # Validate optional dimensions
    optional_dimensions = ['depth', 'weight']
    for dim in optional_dimensions:
        value = data.get(dim)
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            errors.append(f"{dim} must be a positive number")
    
    # Validate string lengths
    string_fields = {
        'name': (3, 100),
        'short_name': (2, 50),
        'description': (10, 1000)
    }
    
    for field, (min_len, max_len) in string_fields.items():
        value = data.get(field)
        if value and (len(value) < min_len or len(value) > max_len):
            errors.append(f"{field} must be between {min_len} and {max_len} characters")
    
    return errors


def validate_pagination_params(page: int, page_size: int) -> List[str]:
    """
    Validate pagination parameters.
    
    Args:
        page: Page number
        page_size: Items per page
        
    Returns:
        List of validation errors
    """
    errors = []
    
    if page < 1:
        errors.append("Page number must be greater than 0")
    
    if page_size < 1 or page_size > 100:
        errors.append("Page size must be between 1 and 100")
    
    return errors


def validate_sort_params(sort_by: str, sort_order: int) -> List[str]:
    """
    Validate sorting parameters.
    
    Args:
        sort_by: Field to sort by
        sort_order: Sort order
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Allowed sort fields
    allowed_fields = [
        '_id', 'name', 'short_name', 'price', 'created_at',
        'updated_at', 'views', 'discount'
    ]
    
    if sort_by not in allowed_fields:
        errors.append(f"Invalid sort field. Allowed fields: {', '.join(allowed_fields)}")
    
    if sort_order not in [-1, 1]:
        errors.append("Sort order must be -1 (descending) or 1 (ascending)")
    
    return errors


def validate_filter_params(filters: Dict[str, Any]) -> List[str]:
    """
    Validate filter parameters.
    
    Args:
        filters: Filter parameters
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Validate price range
    start_price = filters.get('start_price')
    end_price = filters.get('end_price')
    
    if start_price is not None and (not isinstance(start_price, (int, float)) or start_price < 0):
        errors.append("Start price must be a non-negative number")
    
    if end_price is not None and (not isinstance(end_price, (int, float)) or end_price < 0):
        errors.append("End price must be a non-negative number")
    
    if start_price is not None and end_price is not None and end_price < start_price:
        errors.append("End price must be greater than or equal to start price")
    
    # Validate dimension ranges
    dimension_fields = ['width', 'height', 'depth', 'length', 'weight']
    for field in dimension_fields:
        min_value = filters.get(f'min_{field}')
        max_value = filters.get(f'max_{field}')
        
        if min_value is not None and (not isinstance(min_value, (int, float)) or min_value < 0):
            errors.append(f"Min {field} must be a non-negative number")
        
        if max_value is not None and (not isinstance(max_value, (int, float)) or max_value < 0):
            errors.append(f"Max {field} must be a non-negative number")
        
        if min_value is not None and max_value is not None and max_value < min_value:
            errors.append(f"Max {field} must be greater than or equal to min {field}")
    
    return errors


def validate_object_id(object_id: str, field_name: str = "ID") -> bool:
    """
    Validate MongoDB ObjectId format.
    
    Args:
        object_id: ObjectId string to validate
        field_name: Name of the field for error messages
        
    Returns:
        True if valid, False otherwise
    """
    from bson import ObjectId
    
    try:
        if not ObjectId.is_valid(object_id):
            return False
        return True
    except Exception:
        return False


def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        input_string: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not input_string:
        return input_string
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', '[', ']']
    sanitized = input_string
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip() 