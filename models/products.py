from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Request
from pydantic import  Field
import motor.motor_asyncio
from pymongo import ASCENDING, IndexModel

from models.product_attributes import Material

from .common import CommonModel


class Dimensions(CommonModel):
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    depth: Optional[float] = Field(gt=0)  # Optional depth
    length: float = Field(gt=0)  # Optional depth
    weight: Optional[float] = Field(gt=0)
class Color(CommonModel):
    name: str
    color_code: str
    image: Optional[str] 
    class Settings:
        name = "colors"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("short_name", ASCENDING)], unique=True)
        ]

class Currency(CommonModel):
    code: str = Field(..., min_length=3, max_length=3)
    symbol: str = Field(..., min_length=1)
    class Settings:
        name = "currencies"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("short_name", ASCENDING)], unique=True)
        ]


class Category(CommonModel):
    name:str=Field(..., min_length=3, max_length=50)
    class Settings:
        name = "categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]
class Level1Category(CommonModel):
    name:str=Field(..., min_length=3, max_length=50)
    category:Category=Field(...)
    class Settings:
        name = "level1_categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]
class Level2Category(CommonModel):
   name:str=Field(..., min_length=3, max_length=50,)
   category:Level1Category=Field(...)
   class Settings:
        name = "level2_categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]

class ProductVariant(CommonModel):
    color: Color 
    quantity_in_stock: int
    product_id:str 
    images: List[str] = []

class Product(CommonModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3)
    category: Level2Category = Field(...)
    dimensions: Dimensions=Field(...)
    is_new: bool = True
    price: float = Field(gt=0)
    currency: Currency
    colors: List[str] = []
    variants:List[ProductVariant]=[]

    discount: Optional[float] =None#
    views:int=0
    material:Optional[Material]
    
    def updateViews(self):
        self.views+=1
        
   
    class Settings:
        name = "products"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("short_name", ASCENDING)], unique=True)
        ]


