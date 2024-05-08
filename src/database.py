from tortoise import Tortoise, fields, models

from src.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class UserTg(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255, null=True)
    is_premium = fields.BooleanField(default=False)
    language_code = fields.CharField(
        max_length=10, null=True
    )  # IETF language tag from telegram
    deep_link = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_tg"


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
