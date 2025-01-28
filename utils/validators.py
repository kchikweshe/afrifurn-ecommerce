from typing import Dict, List, Tuple
from bson import ObjectId
from fastapi import HTTPException

from services.product_service import ProductService

def validate_object_ids(*ids: str) -> Dict[str, ObjectId]:
    """Validate and convert string IDs to ObjectIds"""
    try:
        return {f"{id_name}_id": ObjectId(id_val) 
                for id_name, id_val in zip(['category', 'material'], ids)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

async def validate_product_data(
    currency_code: str,
    material_id: ObjectId,
    category_id: ObjectId,
    colors: List[str],
    product_service: ProductService
) -> Dict:
    """Validate and retrieve related product data"""
    # Get all related data
    category ,currency, material, product_colors = await product_service.get_product_references(category_id=str(category_id),material_id=str(material_id)    ,currency_code=currency_code,colors=colors)


    
    # Validate existence
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    if not material:
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")
    
    # Validate colors
    # for color in colors:
    #     if not await product_service.get_color(color):
    #         raise HTTPException(status_code=404, detail=f"Color {color} not found")
    
    return {
        "category": category,
        "currency": currency,
        "material": material,
        "colors": product_colors
    } 