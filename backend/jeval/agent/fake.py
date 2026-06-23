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
    Magnitude,
    ManagerialKnowHow,
    NonQuantitativeImpact,
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


def _profile_from_dossier(dossier: JobDossier) -> dict:
    """Подбирает уровни факторов на основе признаков из досье.

    Логика простая, но создаёт разные оценки для разных должностей,
    чтобы сравнение якорей было осмысленным в тестовой среде.
    """
    opex = dossier.scope.annual_opex or 0
    headcount = dossier.scope.headcount or 0
    subordinates = len(dossier.reporting.subordinates)
    decisions = len(dossier.authorities.decides_alone)
    cases = len(dossier.problem_cases) + len(dossier.problem_cases_structured)

    # Know-How: специализация по сложности контекста
    kh_spec_levels = [
        SpecializedKnowHow.B,
        SpecializedKnowHow.C,
        SpecializedKnowHow.D,
        SpecializedKnowHow.E,
        SpecializedKnowHow.F,
        SpecializedKnowHow.G,
    ]
    spec_idx = 0
    if opex > 20_000_000_000:    spec_idx = 5
    elif opex > 5_000_000_000:   spec_idx = 4
    elif opex > 1_000_000_000:   spec_idx = 3
    elif opex > 100_000_000:     spec_idx = 2
    elif opex > 0:               spec_idx = 1
    kh_spec = kh_spec_levels[spec_idx]

    # Know-How: управление по подчинённым
    if subordinates >= 4 or headcount >= 100:
        kh_mgmt = ManagerialKnowHow.III
    elif subordinates >= 2 or headcount >= 20:
        kh_mgmt = ManagerialKnowHow.II
    else:
        kh_mgmt = ManagerialKnowHow.I

    # Know-How: коммуникации по стейкхолдерам
    kh_comm = Communication.THREE if len(dossier.stakeholders) >= 5 else Communication.TWO

    # Problem Solving: область по сложности решений
    ps_area_levels = [
        ProblemArea.B, ProblemArea.C, ProblemArea.D, ProblemArea.E, ProblemArea.F
    ]
    ps_idx = min(cases, len(ps_area_levels) - 1)
    ps_area = ps_area_levels[ps_idx]

    # Problem Solving: сложность по разнообразию кейсов
    if cases >= 3:
        ps_complexity = ProblemComplexity.ADAPTIVE
    elif cases >= 1:
        ps_complexity = ProblemComplexity.VARIABLE
    else:
        ps_complexity = ProblemComplexity.PATTERNED

    # Accountability: свобода действий по полномочиям
    fa_levels = [
        FreedomToAct.B, FreedomToAct.C, FreedomToAct.D,
        FreedomToAct.E, FreedomToAct.F, FreedomToAct.G,
    ]
    fa_idx = min(decisions + (1 if headcount > 50 else 0), len(fa_levels) - 1)
    freedom = fa_levels[fa_idx]

    # Без утверждённой корпоративной матрицы в ₸ офлайн-эвристика не имеет
    # права переводить денежную сумму в уровень 1–4.
    magnitude = Magnitude.N

    # Неколичественная ветка I–VI: организационный охват, а не доход/выручка.
    scope_score = min(5, subordinates + cases + (1 if len(dossier.stakeholders) >= 4 else 0))
    non_quantitative_impact = list(NonQuantitativeImpact)[scope_score]

    return dict(
        kh_spec=kh_spec, kh_mgmt=kh_mgmt, kh_comm=kh_comm,
        ps_area=ps_area, ps_complexity=ps_complexity,
        freedom=freedom, magnitude=magnitude,
        non_quantitative_impact=non_quantitative_impact,
    )


class FakeAgent:
    """Имитирует ответ Claude: уровни выводятся из признаков досье, не фиксированы."""

    def select_factors(self, dossier: JobDossier) -> AgentOutput:
        p = _profile_from_dossier(dossier)
        return AgentOutput(
            role_summary=(dossier.purpose or f"Роль «{dossier.name}» (резюме не предоставлено).")
            + " [Офлайн-режим: уровни выбраны эвристикой, не реальным агентом.]",
            overall_confidence=Confidence.MEDIUM,
            reasoning=(
                "ОФЛАЙН-РЕЖИМ: уровни факторов выбраны эвристикой на основе масштаба, "
                "полномочий и кейсов из досье. Не является реальной оценкой по Hay Group. "
                "Для точной оценки обратитесь к администратору системы — нужно подключить "
                "реальный AI-агент."
            ),
            clarifying_questions=["Какой годовой CAPEX находится в зоне влияния роли?"],
            recommendation="Провести реальную оценку агентом перед комитетом.",
            is_test_data=True,
            selections=FactorSelections(
                know_how=KnowHowSelection(
                    specialization=p["kh_spec"],
                    management=p["kh_mgmt"],
                    communication=p["kh_comm"],
                    evidence=_first(dossier.responsibilities, 3, "Обязанности не детализированы"),
                ),
                problem_solving=ProblemSolvingSelection(
                    area=p["ps_area"],
                    complexity=p["ps_complexity"],
                    evidence=_first(dossier.problem_cases, 3, "Типовые кейсы не предоставлены"),
                ),
                accountability=AccountabilitySelection(
                    freedom=p["freedom"],
                    magnitude=p["magnitude"],
                    non_quantitative_impact=p["non_quantitative_impact"],
                    evidence=_first(dossier.authorities.decides_alone, 3, "Полномочия не детализированы"),
                ),
            ),
        )
