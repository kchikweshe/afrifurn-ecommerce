from typing import Any, List, Union
from uuid import UUID
import uuid

from bson import ObjectId
from bson.binary import Binary
from pydantic import Field
from models.common import ErrorResponseModel, PyObjectId, ResponseModel
from fastapi import APIRouter, Body, Form, HTTPException

from models.products import Category, Level1Category, Level2Category
from database import db

router = APIRouter(prefix="/categories", tags=["Categories"]
)

categories_collection = db.get_collection("categories")

@router.post("/", response_model=Any)
async def create_category(name:str)->Any:
    cat=Category(name=name)
    insert_result = await categories_collection.insert_one(cat.dict())
    if insert_result==None:
        return ErrorResponseModel(code=500,message="Failed to save category")

    return ResponseModel(data=cat,message=f"Category {name} added successfully!!!")


@router.post("/level1-categories/", response_model=Any)
async def create_level1_category(name: str=Form(...),
                                 category_id: str=Form(...)
                                 ) -> Any:
    try:
        category_id = ObjectId(category_id)
      
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    parent_category = await categories_collection.find_one({"_id": category_id})
    if parent_category is None:
        return ErrorResponseModel(error="Category not found", message="Category not found", code=404)

    level1_category = Level1Category(name=name, category=parent_category)
    insert_result = await db["level1_categories"].insert_one(level1_category.dict())
    inserted_id = insert_result.inserted_id
    
    data = level1_category.copy(update={"id": str(inserted_id)})
    return ResponseModel(data=data, message=f"Category {name} added successfully!!!")
@router.post("/level2-categories/", response_model=Any)
async def create_level2_category(name:str=Form(min_length=3),
                              level_1_category_id:str=Form(min_length=1)

                                 ):
        try:
            level_1_category_id = ObjectId(level_1_category_id)
    
        except ValueError:
         raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        parent_category=await  db["level1_categories"].find_one({"_id": level_1_category_id})
        if parent_category is None:
                return ErrorResponseModel(error="",message="Category not found", code="404")
        level2_category=Level2Category(name=name,category=parent_category)

        insert_result = await db["level2_categories"].insert_one(level2_category.dict(exclude_unset=True))
        inserted_id = insert_result.inserted_id
        return level2_category.copy(update={"id": inserted_id})
@router.get("/", response_model=List[Category])
async def get_categories():
    categories = await categories_collection.find().to_list(length=None)
    return categories

from bson import ObjectId

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    try:
        # Convert the provided category_id to ObjectId
        obj_id = ObjectId(category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    # Query the category using the converted ObjectId
    category = await categories_collection.find_one({"_id": obj_id})

    if category:
        return category
    else:
        raise HTTPException(status_code=404, detail="Category not found")

@router.get("/level2-categories/", response_model=List[Level2Category])
async def get_level2_categories():
    level2_categories = await db["level2_categories"].find().to_list(length=None)
    return level2_categories

@router.get("/level1-categories/", response_model=List[Level1Category])
async def get_level1_categories():
    level1_categories = await db["level1_categories"].find().to_list(length=None)
    return level1_categories
