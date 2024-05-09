from fastapi import APIRouter

from .telegram import router as telegram_router
from .v1 import router as v1_router

root_router = APIRouter(prefix="/api")
root_router.include_router(v1_router)
root_router.include_router(telegram_router)


@root_router.get("/healthcheck", include_in_schema=True)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
