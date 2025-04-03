# import os
# from typing import List, Optional, Tuple
# from bson import ObjectId
# from fastapi import HTTPException, UploadFile
# from pydantic import ValidationError

# from database import db
# from models.products import Product, Color, Currency, Level2Category, Material
# from services.image import ImageProcessor
# class ProductService:
#     DEFAULT_IMAGES_DIR = "static/product/"
#     DEFAULT_COLORS_IMAGES_DIR = "static/colors/"
#     COLORS_IMAGE_DIR = os.getenv("COLORS_IMAGES_DIR", DEFAULT_COLORS_IMAGES_DIR)
#     IMAGES_DIR = os.getenv("COLORS_IMAGES_DIR", DEFAULT_COLORS_IMAGES_DIR)

#     def __init__(self, database=db):
#         self.db = database

#     async def create_product(self, product: Product) -> str:
#         """Create a new product in the database"""
#         try:
#             result = await self.db[Product.Settings.name].insert_one(
#                 product.model_dump(exclude=["id"])
#             )
#             return str(result.inserted_id)
#         except ValidationError as ve:
#             raise HTTPException(status_code=422, detail=str(ve))
#         except Exception as e:
#             raise HTTPException(status_code=500, 
#                               detail="An error occurred while creating the product.")

#     async def get_product_references(
#         self, 
#         currency_code: str, 
#         material_id: str, 
#         category_id: str,
#         colors: List[str]
#     ) -> Tuple[Level2Category, Currency, Material, List[Color]]:
#         """Fetch all referenced documents for a product"""
#         try:
#             parent_category = Level2Category(**(await self._fetch_one("level2_categories", value=category_id)))
#             currency = Currency(**(await self._fetch_one("currencies", key='code', value=currency_code)))
#             material = Material(**(await self._fetch_one('materials', value=material_id)))
#             color_docs = []
#             for color in colors:
#                 color_doc = Color(**(await self._fetch_one('colors', key='color_code', value=color)))
#                 color_docs.append(color_doc)

#             return parent_category, currency, material, color_docs
#         except Exception as e:
#             raise HTTPException(status_code=404, 
#                               detail="Failed to fetch referenced documents")

#     async def process_product_images(self, images: List[UploadFile], product_id: str) -> List[str]:
#         """Process and save product images"""
#         saved_paths = []
#         product_folder = os.path.join(self.IMAGES_DIR, str(product_id))
#         os.makedirs(product_folder, exist_ok=True)

#         for i, image in enumerate(images):
#             if not allowed_file(image.filename):
#                 raise HTTPException(status_code=400, 
#                                   detail="Only PNG, JPG, and JPEG files are allowed")

#             contents = await image.read()
#             img = readImage(contents)
#             webp_contents = convert_to_webp(img)

#             filename = f"image{i}.webp"
#             file_path = os.path.join(product_folder, filename)
#             save_image(webp_contents, file_path)
#             saved_paths.append(file_path)

#         return saved_paths

#     async def get_product(self, product_id: str) -> Optional[Product]:
#         """Get a single product by ID"""
#         try:
#             product_doc = await self._fetch_one("products", value=product_id)
#             if not product_doc:
#                 return None
#             return Product(**product_doc)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))

#     async def filter_products(
#         self,
#         filters: dict,
#         page: int,
#         page_size: int,
#         skip: int,
#         limit: int,
#         sort_by: str,
#         sort_order: int
#     ) -> List[Product]:
#         """Filter products with pagination and sorting"""
#         try:
#             products = await self.db["products"].find(filters)\
#                 .skip(skip)\
#                 .limit(limit)\
#                 .sort(sort_by, sort_order)\
#                 .to_list(length=None)
#             return [Product(**product) for product in products]
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))

#     async def update_product(self, product_id: str, update_data: dict) -> bool:
#         """Update a product's information"""
#         try:
#             result = await self.db[Product.Settings.name].update_one(
#                 {"_id": ObjectId(product_id)},
#                 {"$set": update_data}
#             )
#             return result.modified_count > 0
#         except Exception as e:
#             raise HTTPException(status_code=500, 
#                               detail=f"Failed to update product: {str(e)}")

#     async def _fetch_one(self, collection_name: str, key: str = "_id", value: str = '') -> dict:
#         """Internal method to fetch a single document"""
#         try:
#             if key == '_id':
#                 return await self.db[collection_name].find_one({key: ObjectId(value)})
#             return await self.db[collection_name].find_one({key: value})
#         except Exception as e:
#             raise HTTPException(status_code=404, 
#                               detail=f"Document not found in {collection_name}")


    