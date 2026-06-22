"""Тесты OpenAIAgent._parse: разбор ответа Structured Outputs без обращения к сети.

Раньше (function/tool calling без strict-схемы) OpenAI мог пропускать
обязательные поля selections.* — отсюда переход на
client.chat.completions.parse(response_format=AgentOutput), см. комментарий
в jeval/agent/openai_agent.py. Эти тесты бьют по _parse, а не по реальному
SDK-вызову, поэтому форму ответа (message.parsed/.refusal) задаём вручную.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from jeval.agent.openai_agent import OpenAIAgent


def _completion(parsed=None, refusal=None) -> SimpleNamespace:
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(parsed=parsed, refusal=refusal))])


def test_parse_returns_parsed_agent_output(sample_output):
    completion = _completion(parsed=sample_output)

    parsed = OpenAIAgent._parse(completion)

    assert parsed is sample_output
    assert parsed.selections.know_how.specialization == sample_output.selections.know_how.specialization


def test_parse_raises_on_refusal():
    completion = _completion(refusal="не могу выполнить запрос")

    with pytest.raises(RuntimeError, match="отказался"):
        OpenAIAgent._parse(completion)


def test_parse_raises_when_parsed_is_none():
    completion = _completion(parsed=None)

    with pytest.raises(RuntimeError, match="submit_evaluation"):
        OpenAIAgent._parse(completion)


def test_select_factors_requires_api_key(full_dossier, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from jeval.config import get_settings

    get_settings.cache_clear()
    try:
        agent = OpenAIAgent()  # без явного api_key — берёт (пустой) settings.openai_api_key
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
            agent.select_factors(full_dossier)
    finally:
        get_settings.cache_clear()
