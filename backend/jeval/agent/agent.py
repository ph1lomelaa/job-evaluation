"""Вызов Claude для выбора уровней факторов через структурированный tool-use."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..config import get_settings
from ..domain.enums import Confidence
from ..domain.models import FactorSelections, JobDossier
from .prompt import SYSTEM_PROMPT, build_user_message

TOOL_NAME = "submit_evaluation"


class AgentOutput(BaseModel):
    """Структурированный результат агента (без баллов — только уровни и тексты)."""

    role_summary: str = Field(description="Нейтральное резюме роли без оценочных эпитетов")
    selections: FactorSelections
    overall_confidence: Confidence = Confidence.MEDIUM
    reasoning: str = Field(
        default="",
        description="Структурированное обоснование по трём факторам: факт → вывод → ограничение",
    )
    clarifying_questions: list[str] = Field(
        default_factory=list,
        description="Вопросы, привязанные к спорному подфактору и соседним уровням",
    )
    recommendation: str = Field(
        default="",
        description="Что принять предварительно и что подтвердить до решения комитета",
    )
    is_test_data: bool = Field(
        default=False,
        description=(
            "True у заглушек (FakeAgent и т. п.): Evaluation.is_test_data копирует "
            "это значение, чтобы тестовый результат не прошёл за реальную оценку "
            "(см. ФАЗА 5 — guard в api/deps.py и баннер в EvaluationCardPage)."
        ),
    )


def _tool_schema() -> dict[str, Any]:
    """JSON-схема инструмента из Pydantic-модели AgentOutput."""
    return AgentOutput.model_json_schema()


class EvaluationAgent:
    """Обёртка над Anthropic SDK. LLM выбирает уровни; баллы считает движок."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.anthropic_api_key
        self._model = model or settings.jeval_model

    def select_factors(self, dossier: JobDossier, max_tokens: int = 4096) -> AgentOutput:
        """Запросить у Claude уровни факторов для одной должности."""
        if not self._api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY не задан. Укажите ключ в .env или передайте api_key."
            )

        # Импорт внутри метода: пакет не нужен для движка/тестов без сети.
        import anthropic

        client = anthropic.Anthropic(api_key=self._api_key)
        response = client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            tools=[
                {
                    "name": TOOL_NAME,
                    "description": "Вернуть выбранные уровни факторов, доказательства, "
                    "резюме, обоснование, вопросы и рекомендацию.",
                    "input_schema": _tool_schema(),
                }
            ],
            tool_choice={"type": "tool", "name": TOOL_NAME},
            messages=[{"role": "user", "content": build_user_message(dossier)}],
        )

        return self._parse(response)

    @staticmethod
    def _parse(response: Any) -> AgentOutput:
        for block in response.content:
            if getattr(block, "type", None) == "tool_use" and block.name == TOOL_NAME:
                return AgentOutput.model_validate(block.input)
        raise RuntimeError("Claude не вернул вызов инструмента submit_evaluation.")
