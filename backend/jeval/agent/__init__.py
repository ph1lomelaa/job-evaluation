"""LLM-агент: выбирает УРОВНИ факторов и доказательства. Баллы он не считает."""

from .agent import AgentOutput, EvaluationAgent
from .fake import FakeAgent

__all__ = ["EvaluationAgent", "AgentOutput", "FakeAgent"]
