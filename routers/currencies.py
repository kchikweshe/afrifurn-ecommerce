import logging
from typing import List, Any
from fastapi import APIRouter, Form, HTTPException
from bson import ObjectId

from models.products import Currency
from models.common import ResponseModel
from services.repository.currency_repository import CurrencyRepository

router = APIRouter(
    prefix="/currencies",
    tags=["Currencies"]
)

# Initialize repository
currency_repository = CurrencyRepository()

@router.post("/", response_model=Any)
async def create_currency(
    code: str = Form(..., min_length=0),
    symbol: str = Form(..., min_length=1)
):
    """Create a new currency"""
    try:
        # Create currency
        currency = Currency(code=code, symbol=symbol)
        
        # Save currency
        created = await currency_repository.create_currency(currency)
        if not created:
            raise HTTPException(status_code=500, detail="Failed to save currency")

        return ResponseModel.create(
            class_name="Currency",
            status_code=201,
            message="Currency saved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to create currency: {e}")
        raise HTTPException(status_code=500, detail="Failed to create currency")

@router.get("/{currency_id}", response_model=Currency)
async def get_currency(currency_id: str):
    """Get a currency by ID"""
    try:
        # Validate currency ID
        try:
            currency_obj_id = ObjectId(currency_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid currency ID")

        # Get currency
        currency = await currency_repository.get_currency(currency_obj_id)
        if not currency:
            raise HTTPException(status_code=404, detail="Currency not found")

        return currency
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get currency: {e}")
        raise HTTPException(status_code=500, detail="Failed to get currency")

@router.get("/", response_model=List[Currency])
async def get_currencies():
    """Get all currencies"""
    try:
        currencies = await currency_repository.fetch_all()
        return currencies
    except Exception as e:
        logging.error(f"Failed to get currencies: {e}")
        raise HTTPException(status_code=500, detail="Failed to get currencies")

@router.put("/{currency_id}", response_model=Currency)
async def update_currency(currency_id: str, currency_updates: Currency):
    """Update a currency"""
    try:
        # Validate currency ID
        try:
            currency_obj_id = ObjectId(currency_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid currency ID")

        # Update currency
        updated = await currency_repository.update_currency(
            currency_obj_id,
            currency_updates.model_dump(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Currency not found")

        # Get updated currency
        currency = await currency_repository.get_currency(currency_obj_id)
        if not currency:
            raise HTTPException(status_code=404, detail="Currency not found")

        return currency
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to update currency: {e}")
        raise HTTPException(status_code=500, detail="Failed to update currency")
