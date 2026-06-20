"""LLM-агент: выбирает УРОВНИ факторов и доказательства. Баллы он не считает."""

from .agent import AgentOutput, EvaluationAgent
from .fake import FakeAgent
from .groq_agent import GroqAgent

__all__ = ["EvaluationAgent", "AgentOutput", "FakeAgent", "GroqAgent"]
