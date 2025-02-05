FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Install & setup Poetry
RUN pip install -U pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /src
COPY pyproject.toml poetry.lock /src/

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-dev --no-root

# Copying the rest of the project
COPY . /src

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

USER app

ENTRYPOINT ["./scripts/start-dev.sh"]