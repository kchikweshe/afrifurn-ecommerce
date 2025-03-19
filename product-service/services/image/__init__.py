from abc import ABC, abstractmethod
from io import BytesIO
import os
from typing import Any
from PIL import Image
from fastapi import HTTPException, UploadFile

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
    
    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def read_image(self, contents: bytes) -> Image.Image:
        return Image.open(BytesIO(contents))
    
    async def process_image(self, image: UploadFile, i: int, inserted_item: Any, directory: str) -> str:
        """Process an uploaded image file and save it in a product-specific folder."""
        if not image.filename or not self.allowed_file(image.filename): 
            raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

        contents = await image.read()
        img = self.read_image(contents)
        converted_contents = self.convert_image(img)

        folder = os.path.join(directory, str(inserted_item))
        os.makedirs(folder, exist_ok=True)

        filename = f"{i}.webp"
        file_path = os.path.join(folder, filename)

        self.save_image(converted_contents, file_path)
        return file_path

class WebPImageProcessor(ImageProcessor):
    def convert_image(self, img: Image.Image) -> bytes:
        output_buffer = BytesIO()
        img.save(output_buffer, format="WEBP")
        return output_buffer.getvalue()
    
    def save_image(self, contents: bytes, file_path: str) -> None:
        with open(file_path, "wb") as f:
            f.write(contents)