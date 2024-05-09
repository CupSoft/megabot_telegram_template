from tortoise import Tortoise

from src.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": (
            f"asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
