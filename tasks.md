# Project Tasks

## Tortoise

- Replace `sqlalchemy` with `tortoise-orm`.
- Replace `alembic` with `aerich`.
- Rewrite models using `tortoise-orm`.

## Aiogram

- Replace `python-telegram-bot` with `aiogram`.

## Internationalization

- Use `pybabel`, `i18n` in `aiogram` for language detection.

## Remove the unnecessary

- Leave only the minimally necessary handlers
  - /start - registration, greeting
  - /help - help
  - /settings - settings
    - Language change
  - Processing of inline requests

## Telegram admin panel

- Message distribution
  - Pictures
  - Keyboard setup (for start, button-links)
- Ban users

## Web admin panel

- Authentication through Telegram
- FastApi Admin Panel
- Close interactive documentation for unauthorized users

## Deployment

- MetaBase
  - Default requests and dashboards
- Sentry
- Prefect