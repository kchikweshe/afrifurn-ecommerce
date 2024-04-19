from io import BytesIO
import os
from typing import Any, List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image

from .products import IMAGES_DIR
from models.products import Variant
from  models.common import ErrorResponseModel, ResponseModel
from database import db
from bson import ObjectId
os.makedirs(IMAGES_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

router = APIRouter(
    prefix="/product/variant", 
    tags=["Product Variant"]
)
@router.post("/", response_model=Any)
async def create_product_variant(product_id: str = Form(..., min_length=0),
    color_code: str = Form(...),
    quantity: str = Form(..., min_length=1),
   images:List[UploadFile]=[File]

    )->Any:

    product = await db["products"].find_one({"_id": ObjectId(product_id)})
    if product is None:
        return ErrorResponseModel(
            error="",
            code=404,
            message="Product not found."
        )

    file_paths=[]
    for image in images:
        if not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")
 
        contents = await image.read()
        img = Image.open(BytesIO(contents))

        # Create image directory if it doesn't exist

 
        # Convert the image to WEBP format
        output_buffer = BytesIO()
        img.save(output_buffer, format="WEBP")
        webp_contents = output_buffer.getvalue()
       # Generate a unique filename for the image
        filename = f"{image.filename}_{color_code}.webp"  # Example filename format
        file_path = os.path.join(IMAGES_DIR, filename)

        file_paths.append(file_path)
          # Save the WEBP image
        with open(file_path, "wb") as f:
            f.write(webp_contents)


    color = await db["colors"].find_one({"color_code": color_code})
    if color is None:
        return ErrorResponseModel(
        error=color_code,
        code=404,
        message="Color not found."
    )

    
    variant=Variant(color=color,
                    quantity_in_stock=quantity,
                    product_id=str(product['_id']),
                    images=file_paths)
    
    try:
         await db["variants"].insert_one(variant.dict())
    except Exception as e:
        raise HTTPException(status_code='500',detail=f"Failed to save{e}")
    return ResponseModel(data=None,code=200,message="Product variant saved successfully")
@router.get("/{product_id}", response_model=Variant)
async def get_product_variants(product_id: str):
    variants = await db["variants"].find({"product_id": product_id}).to_list(length=None)
    return variants

# @router.put("/currencies/{currency_id}", response_model=Currency)
# async def update_currency(currency_id: str, currency_updates: Currency):
#     update_result = await db["currencies"].update_one(
#       {"_id": ObjectId(currency_id)}, {"$set": currency_updates.dict(exclude_unset=True)}
#     )
#     if update_result.modified_count == 0:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     updated_currency = await db["currencies"].find_one({"_id": ObjectId(currency_id)})
#     return updated_currency
