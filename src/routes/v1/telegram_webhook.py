from fastapi import status, APIRouter

router = APIRouter(prefix="/telegram-webhook/")


@router.post(
    f"/webhook/telegram/{settings.TELEGRAM_BOT_TOKEN}",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def handle_telegram_update(payload: Dict[Any, Any]):
    try:
        update = Update(**payload)
    except Exception:
        logger.warning(f"Bad tg update. Payload: {payload}")
        return {"status": "error"}
    return await dp.feed_update(bot, update)
