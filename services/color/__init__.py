import os
import re
from fastapi import UploadFile
from uuid import uuid4

from services.product import COLORS_IMAGE_DIR

# Define the directory to store images

# Ensure the directory exists
os.makedirs(COLORS_IMAGE_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    # Replace spaces and special characters with hyphens
    sanitized_name = re.sub(r'[^a-zA-Z0-9]', '-', name).lower()
    return sanitized_name

async def save_image(image: UploadFile, color_name: str) -> str:
    # Sanitize the color name to create a valid filename
    filename = f"{sanitize_filename(color_name)}.jpg"
    file_path = os.path.join(COLORS_IMAGE_DIR, filename)

    # Save the file to the specified directory
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    return file_path
