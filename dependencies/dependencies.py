from fastapi import Depends
from database import db
from models.cart import Cart
from services.cart_service import CartService
from services.category_service import CategoryService
from services.color_service import ColorService
from services.image_processor import WebPImageProcessor
from services.level_1_category_service import Level1CategoryService
from services.level_2_category_service import Level2CategoryService
from services.material_service import MaterialService
from services.product_service import ProductService
from services.product_variant_service import ProductVariantService
from services.repository.cart_repository import CartItemRepository, CartRepository
from services.repository.category_repository import CategoryRepository
from services.repository.color_repository import ColorRepository
from services.repository.currency_repository import CurrencyRepository
from services.repository.level2_category_repository import Level2CategoryRepository
from services.repository.level_1_category_repository import Level1CategoryRepository
from services.repository.material_repository import MaterialRepository
from services.repository.product_repository import ProductRepository
from services.repository.product_variant_repository import ProductVariantRepository
async def get_cart_service() -> CartService:
    return CartService(repository=CartRepository(),
                       product_repository=ProductRepository(),
                       product_variant_repository=ProductVariantRepository(),
                     cart_item_repository=CartItemRepository()) 
# product variant service
async def get_product_variant_service() -> ProductVariantService:
    return ProductVariantService(repository=ProductVariantRepository()) 
# color service
async def get_color_service() -> ColorService:
    return ColorService(repository=ColorRepository())
# category service
async def get_category_service() -> CategoryService:
    return CategoryService(repository=CategoryRepository(),image_processor=WebPImageProcessor()) 
# product service
async def get_product_service() -> ProductService:
    return ProductService(repository=ProductRepository(), color_repository=ColorRepository(), material_repository=MaterialRepository(), currency_repository=CurrencyRepository(), level2category_repository=Level2CategoryRepository())   

# level 1 category service
async def get_level_1_category_service() -> Level1CategoryService:
    return Level1CategoryService(repository=Level1CategoryRepository(),image_proccessor=WebPImageProcessor())
async def get_level_2_category_service() -> Level2CategoryService:
    return Level2CategoryService(repository=Level2CategoryRepository(),image_processor=WebPImageProcessor())
async def get_material_service() -> MaterialService:
    return MaterialService(repository=MaterialRepository())
