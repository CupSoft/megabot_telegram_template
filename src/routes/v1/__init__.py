from fastapi import APIRouter

from .ping import router as ping_router

router = APIRouter(prefix="/ping")
router.include_router(ping_router)
