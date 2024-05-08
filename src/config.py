from typing import Any

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    REDIS_MAX_CONNECTIONS: int = 128

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str
    TELEGRAM_BOT_WEBHOOK_SECRET: str


settings = Config()

app_configs: dict[str, Any] = {"title": "MegaBot API"}
if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
    app_configs["debug"] = False
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None
