from fastapi import APIRouter

from .webhook import router as telegram_router

router = APIRouter(prefix="/telegram")
router.include_router(telegram_router)
