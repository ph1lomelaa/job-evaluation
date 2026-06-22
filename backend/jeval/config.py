"""Конфигурация сервиса из переменных окружения (.env)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    # Anthropic
    anthropic_api_key: str = ""
    jeval_model: str = "claude-opus-4-8"

    # Groq (альтернатива Anthropic, быстрее и дешевле для разработки)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # OpenAI (альтернатива Anthropic/Groq)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Выбор провайдера: "anthropic" | "groq" | "openai" | "fake"
    # "fake" — офлайн-заглушка без API-ключа
    jeval_agent_provider: str = "anthropic"

    # Офлайн-режим: вместо LLM уровни выбирает детерминированная заглушка.
    # Только для разработки/демо без API-ключа.
    jeval_fake_agent: bool = False
    jeval_import_use_ai: bool = False

    # ФАЗА 5: FakeAgent выдаёт тестовые уровни, не пригодные для реального
    # Оценочного комитета (см. Evaluation.is_test_data). В jeval_env=production
    # его включение требует ВТОРОГО явного флага — одного JEVAL_FAKE_AGENT=1
    # недостаточно, чтобы тестовые данные не попали в прод по недосмотру.
    jeval_allow_fake_in_prod: bool = False

    # Сервис
    jeval_host: str = "127.0.0.1"
    jeval_port: int = 8000
    jeval_env: str = "development"

    # Авторизация. В production включена по умолчанию; тестовая фабрика может
    # явно отключить её для старых isolated unit-тестов.
    jeval_auth_required: bool = True
    jeval_session_days: int = 30
    jeval_frontend_url: str = "http://127.0.0.1:5173"

    # Google OAuth / OpenID Connect
    jeval_google_client_id: str = ""
    jeval_google_client_secret: str = ""
    jeval_google_enabled: bool = False
    jeval_google_redirect_uri: str = "http://127.0.0.1:8000/api/auth/google/callback"

    # ВРЕМЕННО для разработки, не включать в проде: пропускает allowlist-проверку
    # (приглашение/существующая компания) при первом входе через Google в
    # google_callback() — новый пользователь логинится без приглашения. RBAC
    # внутри приложения (роли owner/admin/evaluator/viewer) при этом не меняется —
    # это только про допуск к созданию аккаунта, не про права после входа.
    # Откатывается одной переменной: по умолчанию False.
    jeval_disable_access_gate: bool = False

    # CORS: разрешённые origin'ы фронтенда (regex). Дефолт — только localhost для
    # разработки; в проде задайте реальный домен через переменную окружения.
    jeval_cors_origin_regex: str = r"https?://(localhost|127\.0\.0\.1)(:\d+)?"

    # Хранилище
    jeval_db_url: str = "sqlite:///./jeval.db"
    jeval_upload_dir: str = "uploads"  # файлы JE-досье (ДИ, RACI, DoA…)


@lru_cache
def get_settings() -> Settings:
    return Settings()
