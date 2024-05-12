from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel, ValidationError


class ProductFilter(BaseModel):
    startPrice: Optional[float]
    endPrice: Optional[float]
    width: Optional[float]
    height: Optional[float]
    length: Optional[float]
    depth:Optional[float]
    categories: Optional[List[str]] 

    material:Optional[str]
    