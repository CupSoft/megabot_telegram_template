from typing import Any
import logging
from fastapi import APIRouter, status
from typing import Dict

from src.config import settings

router = APIRouter(prefix="/telegram-webhook/")
logger = logging.getLogger(__name__)


@router.post(
    f"/webhook/telegram/{settings.TELEGRAM_BOT_TOKEN}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def handle_telegram_update(payload: Dict[Any, Any]):
    try:
        update = Update(**payload)
    except Exception as e:
        logger.exception(f"Bad tg update. Payload: {payload}", exc_info=e)
        return {"status": "error"}
    return await dp.feed_update(bot, update)
