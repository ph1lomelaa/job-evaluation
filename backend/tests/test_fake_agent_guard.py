"""ФАЗА 5: FakeAgent не должен молча включаться в production.

get_evaluator() резолвит провайдера из настроек лениво (``app.state.evaluator``
кэшируется при первом запросе) — здесь дёргаем его напрямую с управляемым
``app.state``/``settings``, без полноценного HTTP-клиента.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from jeval import config
from jeval.agent.fake import FakeAgent
from jeval.api.deps import get_evaluator


def _request_with_no_cached_evaluator() -> SimpleNamespace:
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(evaluator=None)))


def test_fake_agent_blocked_in_production_without_override(monkeypatch):
    settings = config.get_settings()
    monkeypatch.setattr(settings, "jeval_fake_agent", True)
    monkeypatch.setattr(settings, "jeval_env", "production")
    monkeypatch.setattr(settings, "jeval_allow_fake_in_prod", False)

    with pytest.raises(HTTPException) as exc_info:
        get_evaluator(_request_with_no_cached_evaluator())
    assert exc_info.value.status_code == 503


def test_fake_agent_allowed_in_production_with_explicit_override(monkeypatch):
    settings = config.get_settings()
    monkeypatch.setattr(settings, "jeval_fake_agent", True)
    monkeypatch.setattr(settings, "jeval_env", "production")
    monkeypatch.setattr(settings, "jeval_allow_fake_in_prod", True)

    evaluator = get_evaluator(_request_with_no_cached_evaluator())
    assert isinstance(evaluator._agent, FakeAgent)


def test_fake_agent_allowed_outside_production(monkeypatch):
    settings = config.get_settings()
    monkeypatch.setattr(settings, "jeval_fake_agent", True)
    monkeypatch.setattr(settings, "jeval_env", "development")
    monkeypatch.setattr(settings, "jeval_allow_fake_in_prod", False)

    evaluator = get_evaluator(_request_with_no_cached_evaluator())
    assert isinstance(evaluator._agent, FakeAgent)
