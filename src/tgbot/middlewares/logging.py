import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types

from src.wlui.context import WLUIContextVar

logger = logging.getLogger(__name__)


class WnLoggingUserIdMiddleware(BaseMiddleware):
    def __init__(self, wlui: WLUIContextVar):
        self.wlui = wlui

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event (Subclass of :class:`aiogram.types.base.TelegramObject`)
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """
        try:
            message_id, bot_id, chat_type, chat_id = self.get_event_info(event, data)
        except Exception as e:
            logger.exception("WnLoggingUserIdMiddleware", exc_info=e)
            message_id, bot_id, chat_type, chat_id = None, None, None, None
        with self.wlui.use_message_id(message_id), self.wlui.use_bot_id(
            bot_id
        ), self.wlui.use_chat_id(chat_id), self.wlui.use_chat_type(chat_type):
            return await handler(event, data)

    def get_event_info(self, event: types.Update, data: dict):
        if isinstance(event, types.Update):
            if event.message:
                return self.on_pre_process_message(event.message, data)
            elif event.edited_message:
                return self.on_pre_process_edited_message(event.edited_message, data)
            elif event.channel_post:
                return self.on_pre_process_channel_post(event.channel_post, data)
            elif event.edited_channel_post:
                return self.on_pre_process_edited_channel_post(
                    event.edited_channel_post, data
                )
            elif event.inline_query:
                return self.on_pre_process_inline_query(event.inline_query, data)
            elif event.chosen_inline_result:
                return self.on_pre_process_chosen_inline_result(
                    event.chosen_inline_result, data
                )
        return None, None, None, None

    def on_pre_process_message(self, message: types.Message, data: dict):
        return (
            message.message_id,
            data.get("bot").id,
            message.chat.type,
            message.chat.id,
        )

    def on_pre_process_edited_message(self, edited_message, data: dict):
        return (
            edited_message.message_id,
            data.get("bot").id,
            edited_message.chat.type,
            edited_message.chat.id,
        )

    def on_pre_process_channel_post(self, channel_post: types.Message, data: dict):
        return (
            channel_post.message_id,
            data.get("bot").id,
            channel_post.chat.type,
            channel_post.chat.id,
        )

    def on_pre_process_edited_channel_post(
        self, edited_channel_post: types.Message, data: dict
    ):
        return (
            edited_channel_post.message_id,
            data.get("bot").id,
            edited_channel_post.chat.type,
            edited_channel_post.chat.id,
        )

    def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        return (
            inline_query.message_id,
            data.get("bot").id,
            inline_query.chat.type,
            inline_query.chat.id,
        )

    def on_pre_process_chosen_inline_result(
        self, chosen_inline_result: types.ChosenInlineResult, data: dict
    ):
        return (
            chosen_inline_result.message_id,
            data.get("bot").id,
            chosen_inline_result.chat.type,
            chosen_inline_result.chat.id,
        )
