from typing import Any, List

from bson import ObjectId
from models.common import ErrorResponseModel, ResponseModel
from fastapi import APIRouter, Form, HTTPException

from models.products import Category, Level1Category, Level2Category
from database import db
from services.product import filter_one

router = APIRouter(prefix="/categories", tags=["Categories"]
)

categories_collection = db.get_collection("categories")

@router.post("/", response_model=Any,    response_model_by_alias=False,
)
async def create_category(name:str)->Any:
    cat=Category(name=name)
    insert_result = await categories_collection.insert_one(cat.model_dump(
        by_alias=True, exclude=["id"] # type: ignore
    ))
    if insert_result==None:
        return ResponseModel(code=500,message="Failed to save category")
    inserted_id = insert_result.inserted_id
    data = cat.model_copy(update={"id": str(inserted_id)})

    return ResponseModel(data=data.model_dump(),message=f"Category {name} added successfully!!!")


@router.post("/level-1/", response_model=Any)
async def create_level1_category(name: str=Form(...),
                                 category_id: str=Form(...)
                                 ) -> Any:
    try:
        category_id = ObjectId(category_id) # type: ignore
      
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    parent_category = await categories_collection.find_one({"_id": category_id})
    if parent_category is None:
        return ErrorResponseModel(error="Category not found", message="Category not found", code=404)

    level1_category = Level1Category(name=name, category=parent_category)
    insert_result = await db["level1_categories"].insert_one(level1_category.model_dump(
        by_alias=True, exclude=["id"])) # type: ignore
    inserted_id = insert_result.inserted_id
    
    data = level1_category.copy(update={"id": str(inserted_id)})
    return ResponseModel(data=data.model_dump(), message=f"Category {name} added successfully!!!")
@router.post("/level-2", response_model=Any)
async def create_level2_category(name:str=Form(min_length=3),
                              level_1_category_id:str=Form(min_length=1)

                                 ):
        try:
            level_1_category_idx = ObjectId(level_1_category_id)
            parent_category=await  db["level1_categories"].find_one({"_id": level_1_category_idx})
            if parent_category is None:
                return ErrorResponseModel(error="",message="Category not found", code="404")

    
        except ValueError:
         raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        level2_category=Level2Category(name=name,category=parent_category)

    
        insert_result = await db["level2_categories"].insert_one(level2_category.model_dump(
        by_alias=True, exclude=["id"])) # type: ignore
        inserted_id = insert_result.inserted_id
        return level2_category
@router.get("/", response_model=List[Category])
async def get_categories():
    categories = await categories_collection.find().to_list(length=None)
    return categories


@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    try:
        # Convert the provided category_id to ObjectId
        obj_id = ObjectId(category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    # Query the category using the converted ObjectId
    category = await categories_collection.find_one({"_id": obj_id})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category
@router.get("/categories/{name}", response_model=Category)
async def filter_category(name: str):
    try:
      category=  await filter_one(filters={"name":name},collection_name="categories")

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Query the category using the converted ObjectId
     

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category


@router.get("/level1-categories/{name}", response_model=Level1Category)
async def filter_level_one_level_one_category(name: str):
    try:
      category=await filter_one(filters={"name":name},collection_name="level1_categories")

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid category")
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category
@router.get("/level2-categories/{name}", response_model=Level2Category)
async def filter_level_two_category(name: str):
    try:
      category=  await filter_one(filters={"name":name},collection_name="level2_categories")

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid category")

     

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return category
@router.get("/level-2", response_model=List[Level2Category])
async def get_level2_categories():
    level2_categories = await db["level2_categories"].find().to_list(length=None)
    
    return level2_categories

@router.get("/level-1", response_model=List[Level1Category])
async def get_level1_categories():
    level1_categories = await db["level1_categories"].find().to_list(length=None)
    return level1_categories

@router.get("/level-1/{category_id}", response_model=List[Level1Category])
async def get_level1_categories_by_category(category_id:str):
    cid=ObjectId(category_id)
    level1_categories = await db["level1_categories"].find({'category._id':category_id}).to_list(length=None)
    return level1_categories
@router.get("/level-2/{category_id}", response_model=List[Level2Category])
async def get_level2_categories_by_level_one_category(category_id:str):
    cid=ObjectId(category_id)

    level2_categories = await db["level2_categories"].find({'category._id':category_id}).to_list(length=None)
    return level2_categories
