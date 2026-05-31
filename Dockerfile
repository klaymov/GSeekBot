FROM python:3.13-slim

ARG APP_USER=appuser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 ${APP_USER} && \
    mkdir -p /app && \
    chown -R ${APP_USER}:${APP_USER} /app

WORKDIR /app

RUN mkdir -p /app/logs && chmod 777 /app/logs
RUN mkdir -p /app/secrets && chmod 777 /app/secrets

COPY --chown=${APP_USER}:${APP_USER} pyproject.toml ./

USER ${APP_USER}

RUN uv sync --no-dev

COPY --chown=${APP_USER}:${APP_USER} app/ ./app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/app:$PYTHONPATH"
