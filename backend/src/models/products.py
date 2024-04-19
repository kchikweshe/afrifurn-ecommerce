from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Request
from pydantic import  Field
import motor.motor_asyncio

from .common import CommonModel


class Dimensions(CommonModel):
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    depth: float = Field(gt=0, optional=True)  # Optional depth
    weight: float = Field(gt=0)
class Color(CommonModel):
    name:str
    color_code:str
class Variant(CommonModel):
    color: Color 
    quantity_in_stock: int = Field(gt=0)
    product_id:str
    images: List[str]|None = List[str]

class Currency(CommonModel):
    code: str = Field(..., min_length=3, max_length=3)
    symbol: str = Field(..., min_length=1)

class Price(CommonModel):
    value: float = Field(gt=0)
    currency: Currency
class Category(CommonModel):
    name:str=Field(..., min_length=3, max_length=50)
class Level1Category(CommonModel):
    name:str=Field(..., min_length=3, max_length=50)
    category:Category=Field(...)
class Level2Category(CommonModel):
   name:str=Field(..., min_length=3, max_length=50)
   category:Level1Category=Field(...)


class Product(CommonModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3)
    category: Level2Category = Field(...)
    dimensions: Dimensions=Field(...)
    # variants: list[Variant]
    is_new: bool = True
    is_archived:bool=False
    price: Price=Field(...)
    discount: Optional[float] =None#