import logging

from src.wlui.context import WLUIContextVar

wnl = WLUIContextVar()


class WLUIFilter(logging.Filter):
    def filter(self, record):
        record.message_id = wnl.current_message_id
        record.bot_id = wnl.current_bot_id
        record.chat_id = wnl.current_chat_id
        record.chat_type = wnl.current_chat_type
        return True
