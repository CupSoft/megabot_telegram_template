import logging
from typing import Any, Dict

from aiogram.types import Update
from fastapi import APIRouter, status

from src.config import settings
from src.tgbot.app import bot, dp

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    f"/webhook/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}",
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
