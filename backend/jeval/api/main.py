"""FastAPI: фабрика приложения.

Сама бизнес-логика — в ``jeval/api/routers/*`` (auth, companies, admin,
positions, evaluations, public_forms, reference). Здесь только сборка:
middleware, общее состояние приложения (store/evaluator/auth_required) и
подключение роутеров.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import get_settings
from ..orchestrator import JobEvaluator
from ..store import Store, build_store
from .deps import configure_rate_limits, now
from .routers import admin, auth, companies, evaluations, positions, public_forms, reference

logger = logging.getLogger(__name__)


def create_app(
    store: Optional[Store] = None,
    evaluator: Optional[JobEvaluator] = None,
    auth_required: Optional[bool] = None,
) -> FastAPI:
    """Фабрика приложения.

    При инъекции store старые domain/API-тесты работают без auth. Новые auth-
    тесты передают `auth_required=True`; runtime по умолчанию защищён.
    """
    settings = get_settings()
    if settings.jeval_disable_access_gate:
        logger.warning(
            "ACCESS GATE DISABLED — DEV ONLY: JEVAL_DISABLE_ACCESS_GATE=1 пропускает "
            "allowlist-проверку при первом входе через Google. Не использовать в проде."
        )
    app = FastAPI(title="Платформа оценки должностей (Hay Group)", version="0.2.0")
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=settings.jeval_cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.store = store or build_store(settings.jeval_db_url)
    app.state.evaluator = evaluator
    app.state.auth_required = (
        settings.jeval_auth_required if auth_required is None and store is None else bool(auth_required)
    )
    configure_rate_limits(app)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "timestamp": now().isoformat()}

    app.include_router(reference.router)
    app.include_router(auth.router)
    app.include_router(companies.router)
    app.include_router(admin.router)
    app.include_router(positions.router)
    app.include_router(positions.import_router)
    app.include_router(evaluations.router)
    app.include_router(public_forms.router)
    app.include_router(public_forms.public_router)

    return app


app = create_app()
