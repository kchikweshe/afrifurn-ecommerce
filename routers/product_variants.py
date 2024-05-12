from io import BytesIO
import os
from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image

from models.products import Variant
from  models.common import ErrorResponseModel, ResponseModel
from database import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
collection=db["products"]
variants = db["variants"]
colors = db["colors"]

router = APIRouter(
    prefix="/product/variant", 
    tags=["Product Variant"]
)
def convert_to_webp(img: Image.Image) -> bytes: # type: ignore
    """
    Convert the image to WEBP format.

    Args:
        img (Image): The image to be converted.

    Returns:
        bytes: The converted image in WEBP format.
    """
    output_buffer = BytesIO()
    img.save(output_buffer, format="WEBP") # type: ignore
    return output_buffer.getvalue()


def save_image(contents: bytes, file_path: str) -> None:
    """
    Save the image to the specified file path.

    Args:
        contents (bytes): The image contents.
        file_path (str): The file path to save the image to.

    Returns:
        None
    """
    with open(file_path, "wb") as f:
        f.write(contents)

def readImage(contents)->Image.Image:
    return Image.open(BytesIO(contents))

