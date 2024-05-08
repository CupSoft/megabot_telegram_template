from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import BackgroundTasks, Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src import database, redis
from src.config import app_configs, settings
from src.tgbot.app import bot, process_event, start_telegram
from src.tgbot.dependencies import validate_webhook_secret


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    await start_telegram()

    yield

    if settings.ENVIRONMENT.is_testing:
        return

    # Shutdown
    await redis.pool.disconnect()


async def on_startup():
    await database.init()


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


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/webhook",
    dependencies=[Depends(validate_webhook_secret)],
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def tgbot_webhook_events(
    payload: dict,
    worker: BackgroundTasks,
) -> dict:
    worker.add_task(process_event, payload=payload, bot=bot)

    return {
        "ok:": True,
    }
