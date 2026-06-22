"""ИИ-импорт документов: OpenAI должен быть такой же веткой, как groq/anthropic
(регрессия — раньше provider=openai падал в RuntimeError "provider=fake" и
роутер маскировал это 503 "ИИ-импорт временно недоступен")."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from jeval.importer.agent import DossierExtractionAgent


def _fake_openai_response(arguments: dict) -> SimpleNamespace:
    tool_call = SimpleNamespace(
        function=SimpleNamespace(name="submit_dossier_draft", arguments=json.dumps(arguments))
    )
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(tool_calls=[tool_call]))])


def test_extract_openai_parses_tool_call(monkeypatch):
    monkeypatch.setenv("JEVAL_AGENT_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    from jeval.config import get_settings

    get_settings.cache_clear()
    try:
        captured = {}

        class FakeCompletions:
            def create(self, **kwargs):
                captured.update(kwargs)
                return _fake_openai_response(
                    {"name": "Начальник отдела", "key_results": ["Результат 1"], "missing_fields": ["KPI"]}
                )

        class FakeChat:
            completions = FakeCompletions()

        class FakeOpenAI:
            def __init__(self, api_key):
                self.chat = FakeChat()

        # _extract_openai делает `from openai import OpenAI` внутри метода —
        # подменяем сам модуль в sys.modules, чтобы не тянуть реальный SDK/сеть.
        import sys

        monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

        agent = DossierExtractionAgent()
        result = agent.extract("текст должности про начальника отдела")

        assert result.position.name == "Начальник отдела"
        assert result.position.key_results == ["Результат 1"]
        assert result.missing_fields == ["KPI"]
        assert captured["model"] == "gpt-4o-mini"
        assert captured["tools"][0]["function"]["name"] == "submit_dossier_draft"
    finally:
        get_settings.cache_clear()


def test_extract_unknown_provider_raises_with_provider_name(monkeypatch):
    monkeypatch.setenv("JEVAL_AGENT_PROVIDER", "fake")
    from jeval.config import get_settings

    get_settings.cache_clear()
    try:
        agent = DossierExtractionAgent()
        with pytest.raises(RuntimeError, match="provider=fake"):
            agent.extract("любой текст")
    finally:
        get_settings.cache_clear()
