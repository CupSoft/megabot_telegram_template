from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional


class WLUIMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(WLUIMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WLUIContextVar(metaclass=WLUIMeta):
    def __init__(self):
        self.ctx_chat_id = ContextVar("wn_ctx_chat_id", default=None)
        self.ctx_bot_id = ContextVar("wn_ctx_bot_id", default=None)
        self.ctx_message_id = ContextVar("wn_ctx_message_id", default=None)
        self.ctx_chat_type = ContextVar("wn_ctx_chat_type", default=None)

    @property
    def current_chat_id(self) -> Optional[int]:
        return self.ctx_chat_id.get()

    @current_chat_id.setter
    def current_chat_id(self, user_id: Optional[int] = None) -> None:
        self.ctx_chat_id.set(user_id)

    @property
    def current_bot_id(self) -> Optional[int]:
        return self.ctx_bot_id.get()

    @current_bot_id.setter
    def current_bot_id(self, bot_id: Optional[int] = None) -> None:
        self.ctx_bot_id.set(bot_id)

    @property
    def current_message_id(self) -> Optional[int]:
        return self.ctx_message_id.get()

    @current_message_id.setter
    def current_message_id(self, message_id: Optional[int] = None) -> None:
        self.ctx_message_id.set(message_id)

    @property
    def current_chat_type(self) -> Optional[str]:
        return self.ctx_chat_type.get()

    @current_chat_type.setter
    def current_chat_type(self, chat_type: Optional[str] = None) -> None:
        self.ctx_chat_type.set(chat_type)

    @contextmanager
    def use_chat_id(self, value: Optional[int] = None):
        ctx_token = self.ctx_chat_id.set(value)
        try:
            yield
        finally:
            self.ctx_chat_id.reset(ctx_token)

    @contextmanager
    def use_bot_id(self, value: Optional[int] = None):
        ctx_token = self.ctx_bot_id.set(value)
        try:
            yield
        finally:
            self.ctx_bot_id.reset(ctx_token)

    @contextmanager
    def use_message_id(self, value: Optional[int] = None):
        ctx_token = self.ctx_message_id.set(value)
        try:
            yield
        finally:
            self.ctx_message_id.reset(ctx_token)

    @contextmanager
    def use_chat_type(self, value: Optional[str] = None):
        ctx_token = self.ctx_chat_type.set(value)
        try:
            yield
        finally:
            self.ctx_chat_type.reset(ctx_token)
