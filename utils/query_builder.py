import json
from typing import Any, Dict, Optional

def build_product_query(
    start_price: Optional[float],
    end_price: Optional[float],
    name: Optional[str],
    short_name: Optional[str],
    colors: str,
    materials: str,
    dimensions: Dict[str, float|None],
    category: Optional[str]
) -> Dict[str, Any]:
    """Build MongoDB query criteria for product filtering"""
    query_criteria = {}
    
    # Price range
    if start_price is not None and end_price is not None:
        if start_price >= end_price:
            raise ValueError("Start price cannot be greater than or equal to end price")
        query_criteria["price"] = {"$gte": start_price, "$lte": end_price}
    
    # Text searches
    if name:
        query_criteria["name"] = {"$regex": name, "$options": "i"}
    if short_name:
        query_criteria["category.short_name"] = {"$regex": short_name, "$options": "i"}
    
    # Arrays
    colors_list = json.loads(colors)
    materials_list = json.loads(materials)
    
    if colors_list:
        query_criteria["variants.color.name"] = {"$in": colors_list}
    if materials_list:
        query_criteria["material.name"] = {"$in": materials_list}
    
    # Dimensions
    for dim, value in dimensions.items():
        if value is not None:
            query_criteria[f"dimensions.{dim}"] = value
    
    # Category
    if category:
        query_criteria["category.short_name"] = category
        
    return query_criteria 