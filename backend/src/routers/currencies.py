import os
from typing import Dict, List, Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import BaseModel

from models.products import Category, Currency, Dimensions, Level1Category, Level2Category, Product, Variant
from  models.common import CommonModel
from database import db
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/currencies", 
    tags=["Currencies"]
)
@router.post("/currencies/", response_model=Currency)
async def create_currency(currency: Currency):
    insert_result = await db["currencies"].insert_one(currency.dict(exclude_unset=True))
    inserted_id = insert_result.inserted_id
    return currency.copy(update={"id": inserted_id})
@router.get("/currencies/{currency_id}", response_model=Currency)
async def get_currency(currency_id: str):
    currency = await db["currencies"].find_one({"_id": ObjectId(currency_id)})
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency
@router.get("/currencies/", response_model=List[Currency])
async def get_currencies():
    currencies = await db["currencies"].find().to_list(length=None)
    return currencies
@router.put("/currencies/{currency_id}", response_model=Currency)
async def update_currency(currency_id: str, currency_updates: Currency):
    update_result = await db["currencies"].update_one(
      {"_id": ObjectId(currency_id)}, {"$set": currency_updates.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Currency not found")
    updated_currency = await db["currencies"].find_one({"_id": ObjectId(currency_id)})
    return updated_currency
