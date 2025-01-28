from typing import Any, Dict, List, Optional
from pydantic import  BaseModel, Field
from pymongo import ASCENDING, IndexModel


from .common import CommonModel


class Dimensions(CommonModel):
    width: float 
    height: float 
    depth: Optional[float]=None   # Optional depth
    length: float  
    weight: Optional[float]=None 
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
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None)
    images: Optional[List[str]] = Field(default_factory=list)
    class Settings:
        name = "categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("category_id", ASCENDING)])
        ]
class Level1Category(CommonModel):
    category: Category  # Reference to Category._id
    # TODO: Add a field to store the images of the category 
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None)
    images: Optional[List[str]] = Field(default_factory=list)
    class Settings:
        name = "level1_categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            # IndexModel([("category.id", ASCENDING)])  # Index for foreign key
        ]
class Level2Category(CommonModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None)
    images: Optional[List[str]] = Field(default_factory=list)
    level_one_category:Level1Category  # Reference to Level1Category._id
    class Settings:
        name = "level2_categories"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            # IndexModel([("category._id", ASCENDING)])  # Index for foreign key
        ]

class ProductVariant(CommonModel):
    color_id: str  # Reference to Color._id
    quantity_in_stock: int
    product_id: str 
    images: List[str] = []

class Product(CommonModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3)
    category: Level2Category  # Reference to Level2Category._id, lowercase only
    dimensions: Dimensions = Field(...)
    is_new: bool = True
    price: float = Field(gt=0)
    currency: str  # Reference to Currency._id
    color_codes: List[str] = []  # References to Color._id
    product_variants: List[ProductVariant] = []  # References to ProductVariant._id

    discount: Optional[float] = None
    views: int = 0
    material: str

    async def get_variant_by_color(self, color_id: str, db) -> Optional[ProductVariant]:
        """
        Find a product variant by color ID
        Returns None if variant doesn't exist
        Args:
            color_id: The ID of the color to search for
            db: Database connection
        Returns:
            ProductVariant or None if not found
        """
        variants_collection = db["variants"]
        variant = await variants_collection.find_one({
            "product_id": self.id,
            "color_id": color_id
        })
        return ProductVariant(**variant) if variant else None

    async def is_variant_available(self, color_id: str, quantity: int, db) -> bool:
        """
        Check if a variant has enough quantity in stock
        """
        variant = await self.get_variant_by_color(color_id, db)
        if not variant:
            return False
        return variant.quantity_in_stock >= quantity

    def updateViews(self):
        self.views += 1
        
   
    class Settings:
        name = "products"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("short_name", ASCENDING)], unique=True),
            # IndexModel([("category", ASCENDING)], unique=True)  # Added unique index for category
        ]



class CategoryProducts(BaseModel):
    category_name: str
    products: List[Product]

# Pipeline abstraction
class ProductPipeline:
    
    @staticmethod
    def get_products_by_level_two_category_name(name:str,limit:int=10):
        return [
    
                {
                    "$match": {
                    "category.short_name":name}},
                {
                    "$group": {
                        "_id": "$category.name",
                    "category_name": {
                        "$first": "$category.name"
                        },
                    "products": {
                        "$push": "$$ROOT"
                    }
                    }
                },
                {
                    "$skip": 0
                },
                {
                    "$limit": limit
                }

]
        
   
    
    @staticmethod
    def get_products_by_level_one_category_name(name:str,limit:int=10):
        return [
    
                {
                    "$match": {
                    "category.level_one_category.name":name}},
                {
                    "$group": {
                        "_id": "$category.level_one_category.name",
                    "category_name": {
                        "$first": "$category.level_one_category.name"
                        },
                    "products": {
                        "$push": "$$ROOT"
                    }
                    }
                },
                {
                    "$skip": 0
                },
                {
                    "$limit": limit
                }

]
        
    
    @staticmethod
    def get_products_by_category(name:str,limit:int=10) -> List[Dict[str, Any]]:
        return [
    {
        '$group': {
            '_id': '$category.name', 
            'products': {
                '$push': {
                    'is_new': '$is_new', 
                    'created_at': '$created_at', 
                    'description': '$description', 
                    'discount': '$discount', 
                    'variants': '$variants', 
                    'colors': '$colors', 
                    'is_archived': '$is_archived', 
                    'updated_at': '$updated_at', 
                    'material': '$material', 
                    'price': '$price', 
                    'name': '$name', 
                    'currency': '$currency', 
                    'short_name': '$short_name', 
                    '_id': '$_id', 
                    'category': '$category', 
                    'views': '$views', 
                    'dimensions': '$dimensions'
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'category': '$_id', 
            'products': 1
        }
    }
]