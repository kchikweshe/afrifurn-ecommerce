"""Color service module for handling color-related image operations."""

import os
import re
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from uuid import uuid4

from constants.paths import COLOR_IMAGES_DIR


# Ensure the directory exists
os.makedirs(COLOR_IMAGES_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    """
    Sanitize a filename by replacing special characters with hyphens.
    
    Args:
        name: The original filename to sanitize
        
    Returns:
        A sanitized filename string
    """
    return re.sub(r'[^a-zA-Z0-9]', '-', name).lower()

async def save_image(
    image: UploadFile, 
    color_name: str,
    extension: Optional[str] = None
) -> str:
    """
    Save a color image file to the colors directory.
    
    Args:
        image: The uploaded image file
        color_name: Name of the color for the filename
        extension: Optional file extension (defaults to original file extension or jpg)
        
    Returns:
        The path to the saved image file
        
    Raises:
        HTTPException: If there's an error saving the file
    """
    try:
        # Get file extension from original file or use provided/default
        if not extension:
            extension = Path(str(image.filename)).suffix or '.jpg'
        extension = extension.lstrip('.')
        
        filename = f"{sanitize_filename(color_name)}.{extension}"
        file_path = Path(COLOR_IMAGES_DIR) / filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
            
        return str(file_path)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving color image: {str(e)}"
        )
