import os
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel, Field

from models.products import Category, Currency, Dimensions, Level1Category, Level2Category, Product, ProductVariant
from  models.common import CommonModel, ResponseModel
from database import db
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/currencies", 
    tags=["Currencies"]
)
@router.post("/currencies/", response_model=Any)
async def create_currency(code: str = Form(..., min_length=0),
    symbol: str = Form(..., min_length=1)):

    currency=Currency(code=code,symbol=symbol)
    try:
         await db["currencies"].insert_one(currency.model_dump(
        by_alias=True, exclude=["id"])) # type: ignore
    except:
        raise HTTPException(status_code=500,detail="Failed to save currency")
    return ResponseModel(data={},code=201,message="Currency saved successfully")
@router.get("/{currency_id}", response_model=Currency)
async def get_currency(currency_id: str):
    currency = await db["currencies"].find_one({"_id": ObjectId(currency_id)})
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency
@router.get("/", response_model=List[Currency])
async def get_currencies():
    currencies = await db["currencies"].find().to_list(length=None)
    return currencies
@router.put("/{currency_id}", response_model=Currency)
async def update_currency(currency_id: str, currency_updates: Currency):
    update_result = await db["currencies"].update_one(
      {"_id": ObjectId(currency_id)}, {"$set": currency_updates.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Currency not found")
    updated_currency = await db["currencies"].find_one({"_id": ObjectId(currency_id)})
    return updated_currency
