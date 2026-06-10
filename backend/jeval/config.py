"""Конфигурация сервиса из переменных окружения (.env)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    # Anthropic
    anthropic_api_key: str = ""
    jeval_model: str = "claude-opus-4-8"

    # Офлайн-режим: вместо Claude уровни выбирает детерминированная заглушка.
    # Только для разработки/демо без API-ключа.
    jeval_fake_agent: bool = False

    # Сервис
    jeval_host: str = "127.0.0.1"
    jeval_port: int = 8000
    jeval_env: str = "development"

    # Хранилище
    jeval_db_url: str = "sqlite:///./jeval.db"
    jeval_upload_dir: str = "uploads"  # файлы JE-досье (ДИ, RACI, DoA…)


@lru_cache
def get_settings() -> Settings:
    return Settings()
