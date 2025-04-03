from .products_route import router as product_router
from .users import router as user_router
from .currencies import router as currency_router
from .categories_router import router as category_router
from .material import router as materials_router
from.colors import router as color_router
from .product_variants import router as product_variant_router
from fastapi import APIRouter
from .cart import router as cart_router

api_router = APIRouter(prefix="/product-service/api/v1")
api_router.include_router(cart_router)
api_router.include_router(product_router)
api_router.include_router(user_router)
api_router.include_router(currency_router)
api_router.include_router(category_router)
api_router.include_router(product_variant_router)
api_router.include_router(color_router)
api_router.include_router(materials_router)




