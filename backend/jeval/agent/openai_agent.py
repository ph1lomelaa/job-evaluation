"""OpenAI-агент: выбор уровней факторов через function/tool calling.

В отличие от Groq (который не гарантирует структурированный вывод и требует
вытаскивать JSON из текста), Chat Completions API OpenAI поддерживает то же
строгое tool-calling, что и Anthropic — модель обязана вернуть аргументы,
соответствующие схеме AgentOutput, а не текст с JSON внутри.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from ..config import get_settings
from ..domain.models import JobDossier
from .agent import AgentOutput, TOOL_NAME, _tool_schema
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
        response = client.chat.completions.create(
            model=self._model,
            max_completion_tokens=max_tokens,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_message(dossier)},
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": TOOL_NAME,
                        "description": "Вернуть выбранные уровни факторов, доказательства, "
                        "резюме, обоснование, вопросы и рекомендацию.",
                        "parameters": _tool_schema(),
                    },
                }
            ],
            tool_choice={"type": "function", "function": {"name": TOOL_NAME}},
        )

        return self._parse(response)

    @staticmethod
    def _parse(response: Any) -> AgentOutput:
        message = response.choices[0].message
        for call in message.tool_calls or []:
            if call.function.name == TOOL_NAME:
                try:
                    data = json.loads(call.function.arguments)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        f"OpenAI вернул невалидный JSON в аргументах инструмента: {exc}"
                    ) from exc
                return AgentOutput.model_validate(data)
        raise RuntimeError("OpenAI не вернул вызов инструмента submit_evaluation.")
