# MegaBot Telegram template
## 🚧 DEVELOPMENT IN PROGRESS, NOTHING WORKS YET 🚧

### Powerful Telegram bot template with async support

Inspired by FastFoodMemes telegram bot

➡️ https://t.me/megabotbot ⬅️

## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker network create ffmemes_network`
3. `docker-compose up -d --build`

Don't forget to fill the local `.env` file with all envs you need.

### Test local changes

Before sending a PR you must test your new code. The easiest way is to run `ipython` shell, then import the functions you may need and test them. Note that ipython can run async functions without wrapping them with `asyncio.run(...)`.

``` shell
docker compose exec app ipython
```

### Linters
Format the code with `ruff --fix` and `ruff format`
```shell
docker compose exec app format
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
docker compose exec app makemigrations *migration_name*
```
- Run migrations
```shell
docker compose exec app migrate
```
- Downgrade migrations
```shell
docker compose exec app downgrade -1  # or -2 or base or hash of the migration
```
