"""Groq-агент: вызов LLM через Groq API (llama-3.3-70b и др.).

Groq не поддерживает tool_use в том же формате, что Anthropic,
поэтому используем JSON-режим: просим модель вернуть структуру напрямую.
"""

from __future__ import annotations

import json
import re
from typing import Optional

from ..config import get_settings
from ..domain.models import JobDossier
from .agent import AgentOutput, TOOL_NAME
from .prompt import SYSTEM_PROMPT, build_user_message

_JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def _extract_json(text: str) -> dict:
    """Вытащить JSON из ответа — либо из блока, либо напрямую."""
    m = _JSON_BLOCK.search(text)
    raw = m.group(1) if m else text.strip()
    # Убираем trailing comma перед } / ] — частая ошибка LLM
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    return json.loads(raw)


_JSON_INSTRUCTION = """
Верни ТОЛЬКО валидный JSON-объект без каких-либо пояснений до или после.
Не оборачивай в markdown. Структура объекта:
{
  "role_summary": "...",
  "overall_confidence": "high|medium|low",
  "reasoning": "...",
  "clarifying_questions": ["..."],
  "recommendation": "...",
  "selections": {
    "know_how": {
      "specialization": "A|B|C|D|E|F|G|H",
      "management": "T|I|II|III|IV",
      "communication": "1|2|3",
      "plus_minus": 0,
      "modifier_reason": null,
      "adjacent_level": null,
      "evidence": ["..."],
      "doubts": [],
      "confidence": "high|medium|low"
    },
    "problem_solving": {
      "area": "A|B|C|D|E|F|G|H",
      "complexity": 1,
      "plus_minus": 0,
      "modifier_reason": null,
      "adjacent_level": null,
      "evidence": ["..."],
      "doubts": [],
      "confidence": "high|medium|low"
    },
    "accountability": {
      "freedom": "A|B|C|D|E|F|G|H",
      "magnitude": "N",
      "impact": null,
      "non_quantitative_impact": "I|II|III|IV|V|VI",
      "plus_minus": 0,
      "modifier_reason": null,
      "adjacent_level": null,
      "evidence": ["..."],
      "doubts": [],
      "confidence": "high|medium|low"
    }
  }
}
"""


class GroqAgent:
    """Обёртка над Groq API. LLM выбирает уровни; баллы считает движок."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.groq_api_key
        self._model = model or settings.groq_model

    def select_factors(self, dossier: JobDossier, max_tokens: int = 4096) -> AgentOutput:
        if not self._api_key:
            raise RuntimeError(
                "GROQ_API_KEY не задан. Укажите ключ в .env (GROQ_API_KEY=gsk_...)."
            )

        from groq import Groq

        client = Groq(api_key=self._api_key)

        system = SYSTEM_PROMPT + "\n\n" + _JSON_INSTRUCTION
        user_msg = build_user_message(dossier)

        from groq import RateLimitError

        try:
            response = client.chat.completions.create(
                model=self._model,
                max_tokens=max_tokens,
                temperature=0.1,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
            )
        except RateLimitError as exc:
            msg = str(exc)
            wait = ""
            if "Please try again in" in msg:
                wait = msg.split("Please try again in")[1].split(".")[0].strip()
                wait = f" Попробуйте через {wait}."
            raise RuntimeError(
                f"Groq: дневной лимит токенов исчерпан.{wait} "
                "Для продолжения работы переключитесь на офлайн-режим: "
                "установите JEVAL_AGENT_PROVIDER=fake в backend/.env и перезапустите сервер."
            ) from exc

        raw_text = response.choices[0].message.content or ""
        try:
            data = _extract_json(raw_text)
        except (json.JSONDecodeError, AttributeError) as exc:
            raise RuntimeError(
                f"Groq вернул невалидный JSON: {exc}\n--- ответ ---\n{raw_text[:500]}"
            ) from exc

        return AgentOutput.model_validate(data)
