"""Общие зависимости FastAPI: store/evaluator, сессия, рабочее пространство, CSRF, rate-limit.

Вынесены сюда, чтобы не дублировать резолюцию сессии/CSRF в каждом роутере
(как было раньше: ``current_user`` и ``workspace_context`` независимо
перечитывали cookie, а несколько write-эндпоинтов вручную копировали проверку
CSRF вместо того, чтобы зависеть от общего ``write_workspace_context``).
"""

from __future__ import annotations

import hmac
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

from fastapi import Cookie, Depends, Header, HTTPException, Request
from pydantic import BaseModel

from ..agent import EvaluationAgent, FakeAgent, GroqAgent
from ..config import get_settings
from ..domain.identity import UserRecord
from ..orchestrator import JobEvaluator
from ..security import hash_session_token
from ..store import Store

SESSION_COOKIE_NAME = "jeval_session"
CSRF_COOKIE_NAME = "jeval_csrf"


class WorkspaceContext(BaseModel):
    company_id: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None


def now() -> datetime:
    return datetime.now(timezone.utc)


def get_store(request: Request) -> Store:
    return request.app.state.store


def get_evaluator(request: Request) -> JobEvaluator:
    app = request.app
    if app.state.evaluator is None:
        settings = get_settings()
        provider = settings.jeval_agent_provider
        if settings.jeval_fake_agent or provider == "fake":
            app.state.evaluator = JobEvaluator(agent=FakeAgent())
        elif provider == "groq":
            if not settings.groq_api_key:
                raise HTTPException(503, "Агент недоступен: GROQ_API_KEY не задан.")
            app.state.evaluator = JobEvaluator(agent=GroqAgent())
        else:
            if not settings.anthropic_api_key:
                raise HTTPException(
                    503,
                    "Агент недоступен: ANTHROPIC_API_KEY не задан. "
                    "Укажите ключ или включите JEVAL_FAKE_AGENT=1.",
                )
            app.state.evaluator = JobEvaluator(agent=EvaluationAgent())
    return app.state.evaluator


def _resolve_session_user(store: Store, session_cookie: Optional[str]) -> Optional[UserRecord]:
    token = session_cookie.strip() if session_cookie and session_cookie.strip() else None
    if not token:
        return None
    return store.get_user_by_session(hash_session_token(token), now())


def current_user(
    session_cookie: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    store: Store = Depends(get_store),
) -> UserRecord:
    user = _resolve_session_user(store, session_cookie)
    if not user:
        raise HTTPException(401, "Требуется вход в аккаунт")
    return user


def workspace_context(
    request: Request,
    session_cookie: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    company_id: Optional[str] = Header(default=None, alias="X-Company-ID"),
    store: Store = Depends(get_store),
) -> WorkspaceContext:
    if not request.app.state.auth_required:
        return WorkspaceContext(company_id=company_id)
    user = _resolve_session_user(store, session_cookie)
    if not user:
        raise HTTPException(401, "Требуется вход в аккаунт")
    if not company_id:
        raise HTTPException(400, "Не выбрана компания")
    membership = store.get_membership(user.id, company_id)
    if not membership:
        raise HTTPException(403, "Нет доступа к выбранной компании")
    return WorkspaceContext(company_id=company_id, user_id=user.id, role=membership.role)


def require_csrf(
    request: Request,
    csrf_cookie: Optional[str] = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    csrf_header: Optional[str] = Header(default=None, alias="X-CSRF-Token"),
) -> None:
    """Double-submit CSRF: только на изменяющих методах и только если auth включена.

    Единая точка проверки — раньше код проверки CSRF (``cookie != header``)
    был скопирован в нескольких местах вручную; здесь же сразу заменено на
    ``hmac.compare_digest`` вместо ``!=``.
    """
    if not request.app.state.auth_required:
        return
    if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
        return
    if not csrf_cookie or not csrf_header or not hmac.compare_digest(csrf_cookie.strip(), csrf_header.strip()):
        raise HTTPException(403, "Недействительный CSRF-токен")


def write_workspace_context(
    request: Request,
    ctx: WorkspaceContext = Depends(workspace_context),
    _csrf: None = Depends(require_csrf),
) -> WorkspaceContext:
    if request.app.state.auth_required and ctx.role not in {"owner", "admin", "evaluator"}:
        raise HTTPException(403, "Недостаточно прав для изменения данных")
    return ctx


def admin_workspace_context(
    request: Request,
    ctx: WorkspaceContext = Depends(workspace_context),
) -> WorkspaceContext:
    if request.app.state.auth_required and ctx.role not in {"owner", "admin"}:
        raise HTTPException(403, "Только админ может управлять доступом")
    return ctx


def admin_write_workspace_context(
    ctx: WorkspaceContext = Depends(admin_workspace_context),
    _csrf: None = Depends(require_csrf),
) -> WorkspaceContext:
    return ctx


# ── Rate limiting ────────────────────────────────────────────────────────────
# In-memory, per процесс — достаточно против тривиального brute force одним
# клиентом. Для нескольких реплик за балансировщиком нужен внешний стор
# (Redis и т.п.); это сознательно не делается сейчас, чтобы не тащить лишнюю
# инфраструктурную зависимость в MVP.


class _RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self._max = max_requests
        self._window = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def check(self, key: str) -> None:
        moment = time.monotonic()
        with self._lock:
            bucket = self._hits[key]
            cutoff = moment - self._window
            while bucket and bucket[0] < cutoff:
                bucket.pop(0)
            if len(bucket) >= self._max:
                raise HTTPException(429, "Слишком много попыток. Повторите позже.")
            bucket.append(moment)


def configure_rate_limits(app) -> None:
    """Лимитеры — состояние конкретного приложения, не модуля: иначе тесты,
    создающие много ``create_app()`` в одном процессе, делили бы счётчики."""
    app.state.login_limiter = _RateLimiter(max_requests=10, window_seconds=60)
    app.state.register_limiter = _RateLimiter(max_requests=5, window_seconds=60)
    app.state.public_form_limiter = _RateLimiter(max_requests=10, window_seconds=60)


def _client_key(request: Request) -> str:
    client = request.client
    return client.host if client else "unknown"


def limit_login(request: Request) -> None:
    request.app.state.login_limiter.check(_client_key(request))


def limit_register(request: Request) -> None:
    request.app.state.register_limiter.check(_client_key(request))


def limit_public_form(request: Request) -> None:
    request.app.state.public_form_limiter.check(_client_key(request))
