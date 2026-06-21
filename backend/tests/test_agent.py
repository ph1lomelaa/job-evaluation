"""Тесты EvaluationAgent._parse: разбор ответа Claude без обращения к сети."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from jeval.agent.agent import TOOL_NAME, EvaluationAgent


def _response_with_blocks(*blocks) -> SimpleNamespace:
    return SimpleNamespace(content=list(blocks))


def test_parse_extracts_tool_use_block(sample_output):
    tool_block = SimpleNamespace(
        type="tool_use", name=TOOL_NAME, input=sample_output.model_dump(mode="json")
    )
    response = _response_with_blocks(
        SimpleNamespace(type="text", text="промежуточные рассуждения"), tool_block
    )

    parsed = EvaluationAgent._parse(response)

    assert parsed.role_summary == sample_output.role_summary
    assert parsed.selections.know_how.specialization == sample_output.selections.know_how.specialization


def test_parse_ignores_tool_use_with_other_name(sample_output):
    other_tool = SimpleNamespace(type="tool_use", name="other_tool", input={"foo": "bar"})
    response = _response_with_blocks(other_tool)

    with pytest.raises(RuntimeError, match="submit_evaluation"):
        EvaluationAgent._parse(response)


def test_parse_raises_without_tool_use_block():
    response = _response_with_blocks(SimpleNamespace(type="text", text="нет вызова инструмента"))

    with pytest.raises(RuntimeError, match="submit_evaluation"):
        EvaluationAgent._parse(response)
