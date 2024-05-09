import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import database, redis
from src.config import app_configs, settings
from src.routes import root_router
from src.tgbot.app import start_telegram

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    logger.info("Initializing database...")
    await database.init()

    logger.info("Initializing telegram stuff...")
    await start_telegram()
    yield

    if settings.ENVIRONMENT.is_testing:
        return

    # Shutdown
    logger.info("Disconnecting from redis...")
    await redis.pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )

app.include_router(root_router)
