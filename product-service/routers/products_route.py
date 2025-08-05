from fastapi import APIRouter, Depends, Form, HTTPException, Header, Query, Body, UploadFile, File
from typing import List, Optional
from bson import ObjectId
import logging
import io
import logging
from typing import List, Optional
from functools import wraps
from datetime import datetime
import pandas as pd
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
from decorators.decorator import cache_response
from models.products import CategoryProducts, Dimensions, Product, ProductFeature, ProductPipeline
from models.common import ResponseModel
from utils.query_builder import build_product_query
from database import db


API_KEY = "your-super-secret-api-key"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/filter", response_model=List[Product])
@cache_response(
    key="products:{start_price}:{end_price}:{short_name}:{colors}:{materials}:{width}:{length}:{depth}:{height}:{weight}:{category_short_name}:{level1_category_name}:{page}:{page_size}:{sort_by}:{sort_order}:{name}",
    response_model=Product,
    ttl_seconds=300
)

async def filter_products_route(
    start_price: Optional[float] = Query(None, description="Minimum price"),
    end_price: Optional[float] = Query(None, description="Maximum price"),
    short_name: Optional[str] = Query(None, description="Short name"),
    colors: str = Query('[]', description="Colors (JSON array) of hex codes"),
    materials: str = Query('[]', description="Materials (JSON array)"),
    width: float = Query(None, description="Product width"),
    length: Optional[float] = Query(None, description="Product length"), 
    depth: Optional[float] = Query(None, description="Product depth"),
    height: Optional[float] = Query(None, description="Product height"),
    weight: Optional[float] = Query(None, description="Product weight"),
    category_short_name: Optional[str] = Query(None, description="Category short name"),
    level1_category_name: Optional[str] = Query(None, description="Level 1 category name"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)"),
    name: Optional[str] = Query(None, description="Product name")
):
    """Filter products based on various criteria"""
    try:
        skip = (page - 1) * page_size

        query_criteria = build_product_query(
            start_price=start_price,
            end_price=end_price,
            name=name,
            short_name=short_name,
            colors=colors,
            materials=materials,
            dimensions={
                "length":length,
                "width":width,
                "height":height,
                "depth":depth

            },
            category_short_name=category_short_name,
            level1_category_name=level1_category_name
        )
        
        # Add default criteria
        query_criteria["is_archived"] = False
        
        logging.info(f"Query criteria: {query_criteria}")

        # Get products with a pipeline to properly handle nested objects
        pipeline = [
            {"$match": query_criteria},
            {
                "$addFields": {
                    "category._id": "$category.id",
                    "category.level_one_category._id": "$category.level_one_category.id",
                    "category.level_one_category.category._id": "$category.level_one_category.category.id",
                    "dimensions._id": "$dimensions.id"
                }
            },
            {"$sort": {sort_by: sort_order}},
            {"$skip": skip},
            {"$limit": page_size}
        ]
        
        logging.info(f"Pipeline: {pipeline}")
        cursor = db['products'].aggregate(pipeline)
        products = [Product(**item)  for item in cursor]
        logging.info(f"Found {len(products)} products")
            
        return products
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error filtering products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/filter-one", response_model=Product)
@cache_response(
    key="filtered-product:{id}:{short_name}:{name}",
    response_model=Product,
    ttl_seconds=300
)
async def filter_product(
    id: str = Query(None, description="Product ID"),
    short_name: Optional[str] = Query(None, description="Short name"),
    name: Optional[str] = Query(None, description="Product name")
):
    """Get a single product by various criteria"""
    query_criteria = {
        k: v for k, v in {
            "name": {"$regex": name, "$options": "i"} if name else None,
            "_id": id,
            "short_name": {"$regex": short_name, "$options": "i"}
        }.items() if v is not None
    }

    try:
        product:Product|None =  db["products"].find_one(query_criteria)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        updated= db["products"].update_one({"_id":product["_id"]}, {"$inc": {"views": 1}})

        if not updated:
            logging.error(f"Error updating product views: {updated}")
            raise HTTPException(status_code=500, detail="Internal server error")
        product["_id"]= str(product["_id"])
        return product
    except Exception as e:
        logging.error(f"Error retrieving product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: "+str(e))

@router.post("/", response_model=ResponseModel)
async def create_product(
    product_features: List[ProductFeature] | None = None,
    name: str = Query(...),
    short_name: str = Query(...),
    category: str = Query( description="ID of Level2Category"),
    price: float = Query(...),
    description: str = Query( description="Description of product"),
    currency_code: str = Form(...),
    width: float = Query(...),
    length: float = Query(...),
    weight: float = Query(None, description="Weight in grams"),
    height: float = Query( description="Height in mm"),
    depth: float = Query(None, description= "Depth in mm"),
    colors: List[str] = Query( description="Weight in grams"),
    material_id: str = Query(...),
) -> ResponseModel:
    """Create a new product"""
    try:
        category_id = ObjectId(category)
        material_data = ObjectId(material_id)
        
        # Get related data
        level2_category =   db["level2_categories"].find_one({"_id":category_id})
        if not level2_category:
            raise HTTPException(status_code=400, detail="Invalid category ID")

        dimensions = Dimensions(width=width,
                                 length=length, 
                                 height=height,
                                   depth=depth, weight=weight)
        
       

        product = Product(
            name=name,
            description=description,
            short_name=short_name,
            currency=currency_code,
            material=material_id,
            color_codes=colors,
            category=level2_category,
            price=price,
            dimensions=dimensions,
            product_features=product_features or []
        )

        inserted_product =  db["products"].insert_one(product.model_dump())
        if not inserted_product:
            raise HTTPException(status_code=500, detail="Failed to create product")

        return ResponseModel.create(
            class_name="Product",
            status_code=201,
            message="Product added successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/by-level-two-category/filter", response_model=List[Product])
@cache_response(key="level-two-products:{short_name}:{limit}:{skip}:{sort_by}:{sort_order}",response_model=Product,ttl_seconds=300)
async def get_products_by_level_two_category(
    short_name: str = Query(..., description="Level 2 category name"),
    limit: int = Query(10, description="Number of products to return"),
    skip: int = Query(0, description="Number of products to skip"),
    sort_by: str = Query("_id", description="Field to sort by"),
    sort_order: int = Query(1, description="Sort order (1 for ascending, -1 for descending)")
):
    """Get products by Level 2 category name"""
    try:
        # Use aggregation pipeline for better performance and flexibility
        pipeline = [
            {"$match": {
                "category.short_name": short_name,
                "is_archived": False  # Add this if you want to exclude archived products
            }},
            {"$sort": {sort_by: sort_order}},
            {"$skip": skip},
            {"$limit": limit}
        ]
        
        products =  db["products"].aggregate(pipeline)
        data = [Product(**product) for product in products]
        
        return data
    except Exception as e:
        logging.error(f"Error retrieving products by level two category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
@router.get("/by-level-one-category", response_model=List[Product])
@cache_response(key="level-one-products:{name}",response_model=Product,ttl_seconds=300)

async def get_products_by_level_one_category(
    name: str = Query(..., description="Level 1 category name"),
    limit: int = Query(10, description="Number of products to return")
):
    """Get products by Level 1 category name"""
    try:
        pipeline = ProductPipeline.get_products_by_level_one_category_name(name, limit)
        products =  db["products"].aggregate(pipeline)
        products= [CategoryProducts(**product) for product in products]
        return products
    except Exception as e:
        logging.error(f"Error retrieving products by level one category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/by-category", response_model=CategoryProducts)
@cache_response(key="category-products:{category_name}",response_model=CategoryProducts,ttl_seconds=300)

async def get_products_by_category(category_name:str):
    """Get products grouped by category"""
    try:
        pipeline = ProductPipeline.get_products_by_category(name=category_name)
        category_products =  db["products"].aggregate(pipeline)
        
        if category_products is None:
            raise HTTPException(status_code=404, detail="No products found for the specified category")

        return ResponseModel.create(
            class_name="Product",
            data=category_products or [],
            message="Products grouped by category retrieved successfully"
        )
    except Exception as e:
        logging.error(f"Error retrieving products by category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/products/{product_id}")
async def update_product(product_id: str, update_data: dict = Body(...)):
    # Validate product_id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    # Remove fields you don't want to allow updating, if any
    # update_data.pop("id", None)
    # update_data.pop("_id", None)
    # Update only the provided fields
    result =  db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"msg": "Product updated with details:"+str(update_data)}


@router.get("/products/{product_id}/reviews")
async def get_reviews(
    product_id: str,
    page: int = 1,
    page_size: int = 5,
    stars: int | None = None
):
    match = {"_id": ObjectId(product_id)}
    project = {"reviews": 1}
    product = db["products"].find_one(match, project)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    reviews = product.get("reviews", [])
    if stars:
        reviews = [r for r in reviews if r.get("rating") == stars]
    total = len(reviews)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "reviews": reviews[start:end],
        "total": total,
        "page": page,
        "page_size": page_size
    }
# Validation decorators
def validate_csv_file(func):
    """Decorator to validate CSV file format and content"""
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

def validate_csv_headers(func):
    """Decorator to validate required CSV headers"""
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
                'name', 'short_name', 'category', 'price', 'description',
                'currency_code', 'width', 'length', 'height', 'depth',
                'weight', 'colors', 'material_id'
            ]
            
            missing_headers = [h for h in required_headers if h not in df.columns]
            if missing_headers:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required headers: {missing_headers}"
                )
            
            # Log DataFrame info for debugging
            logging.info(f"CSV loaded successfully. Shape: {df.shape}, Columns: {list(df.columns)}")
            
            kwargs['df'] = df
            return await func(*args, **kwargs)
            
        except HTTPException as e:
            logging.error(f"Error processing CSV: {str(e)}")

            raise
        except Exception as e:
            logging.error(f"Error processing CSV: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    return wrapper
def log_bulk_operation(func):
    """Decorator to log bulk operation details"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logging.info(f"Starting bulk product import at {start_time}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logging.info(f"Bulk import completed successfully in {duration:.2f} seconds")
            logging.info(f"Results: {result}")
            
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logging.error(f"Bulk import failed after {duration:.2f} seconds: {str(e)}")
            raise
    return wrapper

@router.post("/bulk-import", response_model=None)  # Add this parameter
@validate_csv_file
@validate_csv_headers
@log_bulk_operation
async def bulk_create_products(
    file: UploadFile = File(...),
    df=None  # Remove the type annotation here
):
    """
    Bulk create products from CSV file
    
    Expected CSV columns:
    - name: Product name
    - short_name: Product short name
    - category: Level2 category ID
    - price: Product price
    - description: Product description
    - currency_code: Currency code (USD, EUR, etc.)
    - width: Width in mm
    - length: Length in mm
    - height: Height in mm
    - depth: Depth in mm (optional)
    - weight: Weight in grams (optional)
    - colors: Comma-separated color codes
    - material_id: Material ID
    """
    
    try:
        if df is None:
            raise HTTPException(status_code=400, detail="No data provided")
            
        # Validate and clean data
        df = df.fillna('')  # Replace NaN with empty string
        
        # Data validation
        validation_errors = []
        valid_products = []
        
        for index, row in df.iterrows():
            try:
                # Ensure index is an integer for arithmetic
                row_num = int(index) + 2  # +2 because CSV is 1-indexed and we have headers
                # Validate required fields
                if not row['name'] or not row['short_name'] or not row['category']:
                    validation_errors.append(f"Row {row_num}: Missing required fields")
                    continue
                
                # Validate numeric fields
                try:
                    price = float(str(row['price']))
                    width = float(str(row['width']))
                    length = float(str(row['length']))
                    height = float(str(row['height']))
                    depth = float(str(row['depth'])) if row['depth'] else None
                    weight = float(str(row['weight'])) if row['weight'] else None
                except ValueError:
                    validation_errors.append(f"Row {row_num}: Invalid numeric values")
                    continue
                
                # Validate ObjectIds
                try:
                    category_id = ObjectId(str(row['category']))
                    material_id = ObjectId(str(row['material_id']))
                except Exception:
                    validation_errors.append(f"Row {row_num}: Invalid ObjectId format")
                    continue
                
                # Validate category exists
                category = db["level2_categories"].find_one({"_id": category_id})
                if not category:
                    validation_errors.append(f"Row {row_num}: Category not found")
                    continue
                
                # Validate material exists
                material = db["materials"].find_one({"_id": material_id})
                if not material:
                    validation_errors.append(f"Row {row_num}: Material not found")
                    continue
                
                # Parse colors
                colors = [c.strip() for c in str(row['colors']).split(';') if c.strip()]
                
                # Create dimensions
                dimensions = Dimensions(
                    width=width,
                    length=length,
                    height=height,
                    depth=depth,
                    weight=weight
                )
                
                # Create product
                product = Product(
                    name=str(row['name']),
                    description=str(row['description']),
                    short_name=str(row['short_name']),
                    currency=str(row['currency_code']),
                    material=str(material_id),
                    color_codes=colors,
                    category=category,
                    price=price,
                    dimensions=dimensions,
                    product_features=[]
                )
                
                valid_products.append(product.model_dump())
                
            except Exception as e:
                validation_errors.append(f"Row {row_num}: {str(e)}")
                continue
        
        # If there are validation errors, return them
        if validation_errors:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Validation errors found",
                    "errors": validation_errors,
                    "valid_products_count": len(valid_products)
                }
            )
        
        # Bulk insert valid products
        if valid_products:
            result = db["products"].insert_many(valid_products)
            
            # Log success
            logging.info(f"Successfully imported {len(valid_products)} products")
            
            return ResponseModel.create(
                class_name="BulkProductImport",
                status_code=201,
                message=f"Successfully imported {len(valid_products)} products",
                data={
                    "imported_count": len(valid_products),
                    "inserted_ids": [str(id) for id in result.inserted_ids]
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="No valid products found in CSV"
            )
            
    except HTTPException as e:
        logging.error(f"Unexpected error in bulk import: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error in bulk import: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error  {str(e)}")

@router.get("/bulk-import/template")
async def download_bulk_import_template():
    """
    Download CSV template for bulk product import
    """
    template_path = "bulk_import_template.csv"
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    return FileResponse(
        path=template_path,
        filename="product_bulk_import_template.csv",
        media_type="text/csv"
    )