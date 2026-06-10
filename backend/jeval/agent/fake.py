"""Офлайн-агент: детерминированные уровни без обращения к Claude.

Используется в демо, тестах и при JEVAL_FAKE_AGENT=1 (разработка без API-ключа).
Уровни фиксированы, но доказательства берутся из самого досье, чтобы карточка
выглядела осмысленно. НЕ предназначен для боевой оценки.
"""

from __future__ import annotations

from .agent import AgentOutput
from ..domain.enums import (
    Communication,
    Confidence,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ManagerialKnowHow,
    ProblemArea,
    ProblemComplexity,
    SpecializedKnowHow,
)
from ..domain.models import (
    AccountabilitySelection,
    FactorSelections,
    JobDossier,
    KnowHowSelection,
    ProblemSolvingSelection,
)


def _first(items: list[str], n: int, fallback: str) -> list[str]:
    return items[:n] if items else [fallback]


class FakeAgent:
    """Имитирует ответ Claude: уровни фиксированы, доказательства — из досье."""

    def select_factors(self, dossier: JobDossier) -> AgentOutput:
        magnitude = Magnitude.THREE if dossier.scope.annual_opex else Magnitude.N
        return AgentOutput(
            role_summary=(dossier.purpose or f"Роль «{dossier.name}» (резюме не предоставлено).")
            + " [Офлайн-режим: уровни выбраны заглушкой, не Claude.]",
            overall_confidence=Confidence.MEDIUM,
            reasoning=(
                "ОФЛАЙН-РЕЖИМ (JEVAL_FAKE_AGENT=1): уровни факторов выбраны "
                "детерминированной заглушкой для проверки конвейера, а не моделью. "
                "Для реальной предварительной оценки укажите ANTHROPIC_API_KEY."
            ),
            clarifying_questions=["Какой годовой CAPEX находится в зоне влияния роли?"],
            recommendation="Провести реальную оценку агентом перед комитетом.",
            selections=FactorSelections(
                know_how=KnowHowSelection(
                    specialization=SpecializedKnowHow.E,
                    management=ManagerialKnowHow.II,
                    communication=Communication.TWO,
                    evidence=_first(dossier.responsibilities, 3, "Обязанности не детализированы"),
                ),
                problem_solving=ProblemSolvingSelection(
                    area=ProblemArea.E,
                    complexity=ProblemComplexity.VARIABLE,
                    evidence=_first(dossier.problem_cases, 3, "Типовые кейсы не предоставлены"),
                ),
                accountability=AccountabilitySelection(
                    freedom=FreedomToAct.E,
                    magnitude=magnitude,
                    impact=ImpactType.C,
                    evidence=_first(dossier.authorities.decides_alone, 3, "Полномочия не детализированы"),
                ),
            ),
        )
