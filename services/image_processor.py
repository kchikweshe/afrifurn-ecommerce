from abc import ABC, abstractmethod
import asyncio
from io import BytesIO
import os
from pathlib import Path
import re
from typing import Any, List, Optional
from PIL import Image
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

from constants.paths import COLOR_IMAGES_DIR
load_dotenv()
class ImageProcessor(ABC):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    @abstractmethod
    def convert_image(self, img: Image.Image) -> bytes:
        """Convert the image to desired format."""
        pass
    
    @abstractmethod
    def save_image(self, contents: bytes, file_path: str) -> None:
        """Save the image to the specified path."""
        pass
    
    def _allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def _read_image(self, contents: bytes) -> Image.Image:
        return Image.open(BytesIO(contents))
    
    async def process_image(self, image: UploadFile, i: int, inserted_item: Any, directory: str,color_code: str) -> str:
        """Process an uploaded image file and save it in a product-specific folder."""
        if not image.filename or not self._allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

        contents = await image.read()
        img = self._read_image(contents)
        converted_contents = self.convert_image(img)
        color_folder = os.path.join(directory, color_code.replace("#", ""))

        os.makedirs(color_folder, exist_ok=True)

        folder = os.path.join(color_folder, str(inserted_item))
        os.makedirs(folder, exist_ok=True)

        filename = f"{i}.webp"
        file_path = os.path.join(folder, filename)

        self.save_image(converted_contents, file_path)
        return file_path
    async def process_images(self,images: List[UploadFile], product_id: str,folder,color_code: str) -> List[str]:
        """Process multiple images in parallel using the WebP image processor"""
        return await asyncio.gather(
            *[self.process_image(image, i, product_id, folder,color_code) 
            for i, image in enumerate(images)]
        )


class WebPImageProcessor(ImageProcessor):
    def convert_image(self, img: Image.Image) -> bytes:
        output_buffer = BytesIO()
        img.save(output_buffer, format="WEBP")
        return output_buffer.getvalue()
    
    def save_image(self, contents: bytes, file_path: str) -> None:
        with open(file_path, "wb") as f:
            f.write(contents)
    # TODO: add a concrete implementation for saving the image in the cloud
class ColorImageProcessor(WebPImageProcessor):
        
    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a filename by replacing special characters with hyphens.
        
        Args:
            name: The original filename to sanitize
            
        Returns:
            A sanitized filename string
        """
        return re.sub(r'[^a-zA-Z0-9]', '-', name).lower()

    async def save_image(
        self,
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
            
            filename = f"{self._sanitize_filename(color_name)}.{extension}"
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


