"""OpenAI-агент: выбор уровней факторов через Structured Outputs.

Раньше использовался обычный function/tool calling без strict-схемы (см. git
history). В этом режиме OpenAI (в отличие от Anthropic tool_use) не гарантирует,
что модель заполнит ВСЕ обязательные поля схемы — на практике уровни факторов
(specialization/management/communication/area/complexity/freedom/magnitude)
иногда пропускались, оставляя только evidence, что валилось в
pydantic.ValidationError и превращалось в 500 при оценке (см. трейсбек:
"Field required [type=missing]" для всех обязательных полей selections.*).

client.chat.completions.parse(response_format=AgentOutput) — Structured
Outputs — заставляет OpenAI строго соответствовать JSON-схеме Pydantic-модели
на уровне API (strict-режим), а не только промпта, и сам валидирует/парсит
ответ. Пропущенные обязательные поля становятся невозможны.
"""

from __future__ import annotations

from typing import Any, Optional

from ..config import get_settings
from ..domain.models import JobDossier
from .agent import AgentOutput
from .prompt import SYSTEM_PROMPT, build_user_message


class OpenAIAgent:
    """Обёртка над OpenAI SDK. LLM выбирает уровни; баллы считает движок."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.openai_api_key
        self._model = model or settings.openai_model

    def select_factors(self, dossier: JobDossier, max_tokens: int = 4096) -> AgentOutput:
        if not self._api_key:
            raise RuntimeError(
                "OPENAI_API_KEY не задан. Укажите ключ в .env или передайте api_key."
            )

        # Импорт внутри метода: пакет не нужен для движка/тестов без сети.
        from openai import OpenAI

        client = OpenAI(api_key=self._api_key)
        completion = client.chat.completions.parse(
            model=self._model,
            max_completion_tokens=max_tokens,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_message(dossier)},
            ],
            response_format=AgentOutput,
        )

        return self._parse(completion)

    @staticmethod
    def _parse(completion: Any) -> AgentOutput:
        message = completion.choices[0].message
        if getattr(message, "refusal", None):
            raise RuntimeError(f"OpenAI отказался выполнить запрос: {message.refusal}")
        if message.parsed is None:
            raise RuntimeError("OpenAI не вернул структурированный ответ (submit_evaluation).")
        return message.parsed
