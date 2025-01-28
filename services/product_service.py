import os
from typing import List, Tuple, Optional
import logging

from bson import ObjectId
from fastapi import HTTPException, UploadFile
from constants.paths import PRODUCT_IMAGES_DIR
from models.product_attributes import Material
from models.products import CategoryProducts, Color, Currency, Level2Category, Product
from services.base_service import BaseService
from services.image import ImageProcessor, WebPImageProcessor
from services.repository.product_repository import ProductRepository
from services.repository.color_repository import ColorRepository
from services.repository.material_repository import MaterialRepository
from services.repository.currency_repository import CurrencyRepository
from services.repository.level2_category_repository import Level2CategoryRepository
from pymongo import MongoClient
from database import db

class ProductService(BaseService[Product]):

    def __init__(
        self,
        repository: ProductRepository,
        color_repository: ColorRepository,
        material_repository: MaterialRepository,
        currency_repository: CurrencyRepository,
        level2category_repository: Level2CategoryRepository,
        image_processor: ImageProcessor = WebPImageProcessor()
    ):
        super().__init__(repository=repository)
        self.image_processor = image_processor
        self.color_repository = color_repository
        self.material_repository = material_repository
        self.currency_repository = currency_repository
        self.level2category_repository = level2category_repository

    async def increment_product_views(self, product_id: str) -> bool:
        try:
            result = await db["products"].update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"views": 1}}
            )
            return result.modified_count > 0
        except Exception as e:
            raise HTTPException(status_code=500, 
                              detail=f"Repository error: Failed to update: {e}") 


    async def get_product_references(
        self, 
        currency_code: str, 
        material_id: str, 
        category_id: str,
        colors: List[str]
    ) -> Tuple[Level2Category, Currency, Material, List[Color]]:
        """Fetch all referenced documents for a product"""
        try:
            parent_category = await self.level2category_repository.get_category(filter_query={"id":category_id})
            currency = await self.currency_repository.get_currency(filter_query={"code":currency_code})
            material = await self.material_repository.get_material(filter_query={"id":material_id})
            
            color_docs = []
            for color in colors:
                color_doc = await self.color_repository.get_color(filter_query={"color_id":color})
                color_docs.append(color_doc)
            #if any of the documents are not found, raise an error
            if not parent_category or not currency or not material:
                raise HTTPException(status_code=404, detail="One or more referenced documents not found")
            return parent_category, currency, material, color_docs
        except Exception as e:
            raise HTTPException(status_code=404, 
                              detail="Failed to fetch referenced documents")

    async def get_products_by_category(self, level2_category_name: str,limit:int=20,page:int=1,skip:int=0,sort_by:str="views",sort_order:int=1) -> List[Product]:
       
       products_by_category =  self.repository.filter({
          "category":level2_category_name,
          
          "is_archived":False
       },
       skip=skip,
       limit=limit,
       sort_by=sort_by,
       sort_order=sort_order
       )
    #  TODO: add the logic to get the products by the level 2 category name          
       return products_by_category

    async def delete_product(self, product_id: str) -> bool:
        return await self.repository.delete(product_id)

    async def save_product_images(self, images: List[UploadFile], product_id: str) -> List[str]:
        """Process and save product images"""
        saved_paths = []
        product_folder = os.path.join(PRODUCT_IMAGES_DIR, str(product_id))
        
        for i, image in enumerate(images):
            file_path = await self.image_processor.process_image(
                image=image,
                i=i,
                inserted_item=product_id,
                directory=product_folder
            )
            saved_paths.append(file_path)

        return saved_paths

    async def aggregate(self, pipeline: list) -> Optional[CategoryProducts]:
        """
        Execute an aggregation pipeline on the products collection and return a single CategoryProducts.

        Args:
            pipeline (list): The aggregation pipeline to execute.

        Returns:
            Optional[CategoryProducts]: The result of the aggregation structured as CategoryProducts, or None if no results.
        """
        try:
            # Use the aggregate method from the repository
            results =await db['products'].aggregate(pipeline).to_list(length=None)
            
            if not results:
                return None  # Return None if no results

            # Assuming the first result contains the category name and products
            first_result = results[0]


            
            category_products = CategoryProducts(
                category_name=first_result['category_name'],
                products=first_result['products']
            )

            return category_products
        except Exception as e:
            logging.error(f"Error executing aggregation: {e}")
            raise