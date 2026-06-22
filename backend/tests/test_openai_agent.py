"""Тесты OpenAIAgent._parse: разбор function/tool-call ответа без обращения к сети."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from jeval.agent.agent import TOOL_NAME
from jeval.agent.openai_agent import OpenAIAgent


def _response_with_tool_calls(*calls) -> SimpleNamespace:
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(tool_calls=list(calls)))])


def _tool_call(name: str, arguments: dict) -> SimpleNamespace:
    return SimpleNamespace(function=SimpleNamespace(name=name, arguments=json.dumps(arguments)))


def test_parse_extracts_tool_call_arguments(sample_output):
    response = _response_with_tool_calls(
        _tool_call(TOOL_NAME, sample_output.model_dump(mode="json"))
    )

    parsed = OpenAIAgent._parse(response)

    assert parsed.role_summary == sample_output.role_summary
    assert parsed.selections.know_how.specialization == sample_output.selections.know_how.specialization


def test_parse_ignores_tool_call_with_other_name():
    response = _response_with_tool_calls(_tool_call("other_tool", {"foo": "bar"}))

    with pytest.raises(RuntimeError, match="submit_evaluation"):
        OpenAIAgent._parse(response)


def test_parse_raises_without_tool_calls():
    response = _response_with_tool_calls()

    with pytest.raises(RuntimeError, match="submit_evaluation"):
        OpenAIAgent._parse(response)


def test_parse_raises_on_invalid_json_in_arguments():
    bad_call = SimpleNamespace(function=SimpleNamespace(name=TOOL_NAME, arguments="{not valid json"))
    response = _response_with_tool_calls(bad_call)

    with pytest.raises(RuntimeError, match="невалидный JSON"):
        OpenAIAgent._parse(response)


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
