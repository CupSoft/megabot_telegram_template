from aiogram import types
from aiogram.utils.i18n import FSMI18nMiddleware, I18n


class CustomFSMI18nMiddleware(FSMI18nMiddleware):
    async def get_locale(self, event: types.TelegramObject, data) -> str:
        user_id = None

        if isinstance(event, types.Message):
            user_id = event.from_user.id
        elif isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id

        if not user_id:
            return self.i18n.default_locale
        # user_language = await get_user_language(user_id)
        user_language = None  # TODO: Implement get_user_language
        return user_language if user_language else self.i18n.default_locale


i18n_middleware = CustomFSMI18nMiddleware(
    I18n(path="locales", default_locale="en", domain="messages")
)
