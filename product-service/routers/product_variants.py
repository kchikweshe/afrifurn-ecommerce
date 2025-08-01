from datetime import datetime
from functools import wraps
import io
import os
from typing import Any, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from typing import List
from bson import ObjectId
import asyncio
import logging

from fastapi.responses import FileResponse
import httpx
import pandas as pd

from models.common import ResponseModel
from models.products import Color, ProductVariant
from database import db
from constants.paths import PRODUCT_IMAGES_DIR
from services.image_processor import WebPImageProcessor
from services.repository.product_variant_repository import ProductVariantRepository
from services.repository.product_repository import ProductRepository
from services.repository.color_repository import ColorRepository

collection=db["products"]
variants = db["variants"]
colors = db["colors"]

image_processor = WebPImageProcessor()

router = APIRouter(
    prefix="/product/variant", 
    tags=["Product Variant"]
)

# Initialize repositories and processors
variant_repository = ProductVariantRepository()
product_repository = ProductRepository()
color_repository = ColorRepository()

# Mock database functions
async def insert_variant_into_db(product_id: ObjectId, variant: ProductVariant):
    # Mock implementation of inserting a variant into the database.
    return {"inserted_id": ObjectId()}

async def update_variant_in_db(product_id: ObjectId, variant_id: ObjectId, variant_data: dict):
    # Mock implementation of updating a variant in the database.
    return {"modified_count": 1}

async def archive(collection_name:str,item_id: ObjectId):
    # Updated implementation to archive a variant in the database.
    result =  db[collection_name].update_one(
        {"_id": item_id},
        {"$set": {f"is_archived": True}}
    )
    if result.modified_count == 0:
        return {"message": "Variant not found or already archived"}
    return {"message": "Variant archived successfully"}

async def process_images(images: List[UploadFile], product_id: str, color_code: str) -> List[str]:
    """Process multiple images in parallel using the WebP image processor"""
    return await asyncio.gather(
        *[image_processor.process_image(image, i, product_id, PRODUCT_IMAGES_DIR,color_code) 
          for i, image in enumerate(images)]
    )

@router.post("/product/{product_id}", response_model=ResponseModel, response_model_by_alias=False)
async def create_product_variant(
    product_id: str,
    color_code: str = Form(...),
    quantity_in_stock: int = Form(...),
    images: List[UploadFile] = File(...),
) -> Any:
    """Create a new product variant with associated images and color"""
    try:
        # Validate product ID
        try:
            product_obj_id = ObjectId(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product ID format")

    
        # Get color
        color = await color_repository.get_color_by_code(color_code)
        if not color:
            raise HTTPException(status_code=404, detail="Color not found")
    # Process images
        image_paths = await process_images(images, product_id,color.color_code)

        # Create variant
        variant = ProductVariant(
            product_id=str(product_obj_id),
            color_id=color.color_code,
            images=image_paths,
            quantity_in_stock=quantity_in_stock
        )

        # Save variant
        inserted_id =  db["variants"].insert_one(variant.model_dump())
        if not inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create variant")

        # Update product
        updated =  db["products"].update_one(
            {"_id": product_obj_id},    {"$push": {"product_variants": variant.model_dump()}})
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update product with variant")

        return ResponseModel.create(
            class_name="ProductVariant",
            data=variant.model_dump(),
            message="Product variant created successfully"
        )

    except Exception as e:
        logging.error(f"Failed to create product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product variant")

@router.get("{product_id}/variants/{variant_id}", response_model=ProductVariant)
async def get_product_variant(product_id: str, variant_id: str,
                              ):
    try:
        # Validate IDs
        try:
            product_obj_id = ObjectId(product_id)
            variant_obj_id = ObjectId(variant_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Get variant
        variant =  db["variants"].find_one({"_id": variant_obj_id})
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        return variant
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to get product variant")

@router.delete("{product_id}/variants/{variant_id}", response_model=ResponseModel)
async def soft_delete_product_variant(product_id: str, variant_id: str):
    """Soft delete a product variant"""
    try:
        # Validate IDs
        try:
            product_obj_id = ObjectId(product_id)
            variant_obj_id = ObjectId(variant_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Archive variant
        archived = await archive("variants",variant_obj_id)
        if not archived:
            raise HTTPException(status_code=404, detail="Variant not found or already archived")

        return ResponseModel.create(
            class_name="ProductVariant",
            message="Product variant archived successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to archive product variant: {e}")
        raise HTTPException(status_code=500, detail="Failed to archive product variant")
# Validation decorators for variant bulk import
def validate_variant_csv_file(func):
    """Decorator to validate CSV file format and content for variants"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get('file')
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size too large (max 10MB)")
        
        return await func(*args, **kwargs)
    return wrapper

def validate_variant_csv_headers(func):
    """Decorator to validate required CSV headers for variants"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get('file')
        if file is None:
            raise HTTPException(status_code=400, detail="No file provided")
            
        try:
            content = await file.read()
            await file.seek(0)  # Reset file pointer
            
            # Decode content with error handling
            try:
                content_str = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    content_str = content.decode('utf-8-sig')  # Handle BOM
                except UnicodeDecodeError:
                    content_str = content.decode('latin-1')  # Fallback encoding
            
            # Read CSV with additional parameters for better compatibility
            df = pd.read_csv(
                io.StringIO(content_str),
                dtype=str,  # Read all columns as strings initially
                na_values=['', 'NULL', 'null', 'None', 'none', 'N/A', 'n/a'],
                keep_default_na=False,  # Don't convert to NaN automatically
                skipinitialspace=True,  # Remove leading whitespace
                encoding_errors='ignore'
            )
            
            # Clean up column names (remove extra whitespace)
            df.columns = df.columns.str.strip()
            
            required_headers = [
                'product_id', 'color_code', 'quantity_in_stock', 'image_sources'
            ]
            
            missing_headers = [h for h in required_headers if h not in df.columns]
            if missing_headers:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required headers: {missing_headers}"
                )
            
            # Log DataFrame info for debugging
            logging.info(f"Variant CSV loaded successfully. Shape: {df.shape}, Columns: {list(df.columns)}")
            
            kwargs['df'] = df
            return await func(*args, **kwargs)
            
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error processing variant CSV: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    return wrapper

def log_bulk_variant_operation(func):
    """Decorator to log bulk variant operation details"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.info(f"Starting bulk variant import at {start_time}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logging.info(f"Bulk variant import completed successfully in {duration:.2f} seconds")
            logging.info(f"Results: {result}")
            
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logging.error(f"Bulk variant import failed after {duration:.2f} seconds: {str(e)}")
            raise
    return wrapper

async def process_image_sources(image_sources: List[str], product_id: str, color_code: str, pictures_folder: str ) -> List[str]:
    """Process images from URLs or local file paths"""
    image_paths = []
    
    for i, source in enumerate(image_sources):
        try:
            source = source.strip()
            
            # Check if it's a URL
            if source.startswith(('http://', 'https://')):
                # Download from URL
                async with httpx.AsyncClient() as client:
                    response = await client.get(source, timeout=30.0)
                    response.raise_for_status()
                    
                    # Get file extension from URL or content type
                    content_type = response.headers.get('content-type', '')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    elif 'webp' in content_type:
                        ext = '.webp'
                    else:
                        # Try to get extension from URL
                        ext = os.path.splitext(source.split('?')[0])[1]
                        if not ext:
                            ext = '.jpg'  # Default to jpg
                    
                    # Generate filename
                    filename = f"{product_id}_{color_code}_{i+1}{ext}"
                    file_path = os.path.join("uploads", "products", filename)
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # Save the image
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    image_paths.append(file_path)
                    logging.info(f"Downloaded image from {source} to {file_path}")
            
            else:
                # Handle local file path
                local_path = source
                
                # If pictures_folder is provided and source is not absolute, make it relative to pictures folder
                if pictures_folder and not os.path.isabs(local_path):
                    local_path = os.path.join(pictures_folder, source)
                
                # Check if file exists
                if not os.path.exists(local_path):
                    logging.error(f"Local image file not found: {local_path}")
                    continue
                
                # Validate it's an image file
                valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
                file_ext = os.path.splitext(local_path)[1].lower()
                if file_ext not in valid_extensions:
                    logging.error(f"Invalid image format: {local_path}")
                    continue
                
                # Copy to uploads directory
                filename = f"{product_id}_{color_code}_{i+1}{file_ext}"
                destination_path = os.path.join("uploads", "products", filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                # Copy the file
                import shutil
                shutil.copy2(local_path, destination_path)
                
                image_paths.append(destination_path)
                logging.info(f"Copied local image from {local_path} to {destination_path}")
                
        except Exception as e:
            logging.error(f"Failed to process image source {source}: {str(e)}")
            # Continue with other images instead of failing completely
            continue
    
    return image_paths

@router.post("/variants/bulk-import", response_model=None)
@validate_variant_csv_file
@validate_variant_csv_headers
@log_bulk_variant_operation
async def bulk_create_product_variants(
    file: UploadFile = File(...),
    pictures_folder: str = Form(None, description="Path to local pictures folder (optional)"),
    df=None  # Remove the type annotation here
):
    """
    Bulk create product variants from CSV file
    
    Expected CSV columns:
    - product_id: Product ObjectId
    - color_code: Color code (e.g., #ffffff)
    - quantity_in_stock: Integer quantity
    - image_urls: Semicolon or comma-separated list of image URLs to download
    
    Example CSV row:
    product_id,color_code,quantity_in_stock,image_urls
    507f1f77bcf86cd799439011,#ffffff,100,https://example.com/img1.jpg;https://example.com/img2.jpg
    """
    
    try:
        if df is None:
            raise HTTPException(status_code=400, detail="No data provided")
            
        # Log DataFrame info for debugging
        logging.info(f"Processing variant DataFrame with shape: {df.shape}")
        logging.info(f"DataFrame columns: {list(df.columns)}")
        
        # Clean the DataFrame
        df = df.copy()  # Create a copy to avoid modifying the original
        
        # Replace various null representations with empty string
        df = df.fillna('')
        df = df.replace(['NULL', 'null', 'None', 'none', 'N/A', 'n/a'], '')
        
        # Strip whitespace from all string columns
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        logging.info(f"Cleaned variant DataFrame shape: {df.shape}")
        
        # Data validation
        validation_errors = []
        valid_variants = []
        processed_variants = []
        
        for index, row in df.iterrows():
            try:
                # Ensure index is an integer for arithmetic
                row_num = int(index) + 2  # +2 because CSV is 1-indexed and we have headers
                
                logging.debug(f"Processing variant row {row_num}: {dict(row)}")
                
                # Validate required fields
                product_id_str = str(row['product_id']).strip()
                color_code_str = str(row['color_code']).strip()
                quantity_str = str(row['quantity_in_stock']).strip()
                image_urls_str = str(row['image_urls']).strip()
                
                if not product_id_str or not color_code_str or not quantity_str:
                    validation_errors.append(f"Row {row_num}: Missing required fields (product_id, color_code, or quantity_in_stock)")
                    continue
                
                # Validate product ID
                try:
                    product_obj_id = ObjectId(product_id_str)
                except Exception as e:
                    validation_errors.append(f"Row {row_num}: Invalid product ID format - {str(e)}")
                    continue
                
                # Check if product exists
                product = db["products"].find_one({"_id": product_obj_id})
                if not product:
                    validation_errors.append(f"Row {row_num}: Product not found")
                    continue
                
                # Validate quantity
                try:
                    quantity = int(quantity_str)
                    if quantity < 0:
                        validation_errors.append(f"Row {row_num}: Quantity must be non-negative")
                        continue
                except (ValueError, TypeError) as e:
                    validation_errors.append(f"Row {row_num}: Invalid quantity value - {str(e)}")
                    continue
                
                # Validate color code
                if not color_code_str.startswith('#') or len(color_code_str) not in [4, 7]:
                    validation_errors.append(f"Row {row_num}: Invalid color code format")
                    continue
                
                # Check if color exists
                color = await color_repository.get_color_by_code(color_code_str)
                if not color:
                    validation_errors.append(f"Row {row_num}: Color not found")
                    continue
                
                # Parse image URLs
                image_urls = []
                if image_urls_str:
                    # Check if it uses semicolons or commas as separators
                    if ';' in image_urls_str:
                        image_urls = [url.strip() for url in image_urls_str.split(';') if url.strip()]
                    else:
                        image_urls = [url.strip() for url in image_urls_str.split(',') if url.strip()]
                    
                    # Validate URLs
                    valid_urls = []
                    for url in image_urls:
                        if url.startswith(('http://', 'https://')):
                            valid_urls.append(url)
                        else:
                            logging.warning(f"Row {row_num}: Invalid URL '{url}' - skipping")
                    
                    image_urls = valid_urls
                
                if not image_urls:
                    validation_errors.append(f"Row {row_num}: At least one valid image URL is required")
                    continue
                
                # Store valid variant data for processing
                valid_variants.append({
                    'row_num': row_num,
                    'product_id': str(product_obj_id),
                    'product_obj_id': product_obj_id,
                    'color_code': color_code_str,
                    'color': color,
                    'quantity': quantity,
                    'image_urls': image_urls
                })
                
            except Exception as e:
                validation_errors.append(f"Row {row_num}: Unexpected error - {str(e)}")
                continue
        
        # If there are validation errors, return them
        if validation_errors:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Validation errors found",
                    "errors": validation_errors,
                    "valid_variants_count": len(valid_variants)
                }
            )
        
      
        else:
            raise HTTPException(
                status_code=400,
                detail="No valid variants found in CSV"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error in bulk variant import: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/variants/bulk-import/template")
async def download_bulk_variant_import_template():
    """
    Download CSV template for bulk variant import
    """
    template_path = "bulk_variant_import_template.csv"
    
    if not os.path.exists(template_path):
        # Create template file if it doesn't exist
        template_content = """product_id,color_code,quantity_in_stock,image_urls
507f1f77bcf86cd799439011,#ffffff,100,https://example.com/image1.jpg;https://example.com/image2.jpg
507f1f77bcf86cd799439012,#000000,50,https://example.com/image3.jpg;https://example.com/image4.jpg"""
        
        with open(template_path, 'w') as f:
            f.write(template_content)
    
    return FileResponse(
        path=template_path,
        filename="product_variant_bulk_import_template.csv",
        media_type="text/csv"
    )