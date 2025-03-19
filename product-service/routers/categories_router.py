from fastapi import APIRouter
from .category_routes import router as category_router
from .level1_routes import router as level1_router
from .level2_routes import router as level2_router

router = APIRouter(prefix="/categories", tags=["Categories"])

router.include_router(category_router)
router.include_router(level1_router, prefix="/level-1", tags=["Level 1 Categories"])
router.include_router(level2_router, prefix="/level-2", tags=["Level 2 Categories"])
