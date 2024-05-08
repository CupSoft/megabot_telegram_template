import logging

from aiogram import F, Router, types
from aiogram.filters import Command

logger = logging.getLogger(__name__)
router = Router(name="Start router")


@router.message(Command(commands=["start"]), F.chat.type == "private")
async def start_handler(message: types.Message):
    await message.answer("/start")
