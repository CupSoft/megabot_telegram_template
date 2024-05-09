from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Update, WebhookInfo

from src.config import settings
from src.tgbot.middlewares import i18n, logging

base_router = Router(name="telegram")

base_router.message.middleware(i18n.i18n_middleware)
base_router.edited_message.middleware(logging.WnLoggingUserIdMiddleware)

dp = Dispatcher()
dp.include_router(base_router)
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML
)


async def set_webhook(my_bot: Bot) -> None:
    async def check_webhook() -> WebhookInfo | None:
        webhook_info = await my_bot.get_webhook_info()
        return webhook_info

    current_webhook_info = await check_webhook()

    await bot.set_webhook(
        f"https://{settings.SITE_DOMAIN}/webhook",
        secret_token=settings.TELEGRAM_BOT_WEBHOOK_SECRET.get_secret_value(),
        drop_pending_updates=current_webhook_info.pending_update_count > 0,
        max_connections=40,
    )


async def set_bot_commands_menu(my_bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description="Get help"),
    ]

    await my_bot.set_my_commands(commands)


async def start_telegram():
    await set_webhook(bot)
    await set_bot_commands_menu(bot)


async def process_event(bot: Bot, payload: dict) -> None:
    await dp.feed_update(bot, Update(**payload))
