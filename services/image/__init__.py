from io import BytesIO
import os
from typing import Any
from PIL import Image
from fastapi import HTTPException, UploadFile
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

async def process_image(image: UploadFile, i: int, inserted_item: Any,directory:str):
    """Process an uploaded image file and save it in a product-specific folder."""
    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

    contents = await image.read()
    img = readImage(contents)
    webp_contents = convert_to_webp(img)

    # Create product folder if it doesn't exist
    folder = os.path.join(directory, str(inserted_item))
    os.makedirs(folder, exist_ok=True)  

    filename = f"{i}.webp"  # Removed product ID from filename
    file_path = os.path.join(folder, filename)

    save_image(webp_contents, file_path)
    return file_path