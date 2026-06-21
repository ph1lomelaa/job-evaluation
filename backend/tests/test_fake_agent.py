"""ФАЗА 5: golden-тесты порогов FakeAgent (jeval/agent/fake.py).

FakeAgent — офлайн-заглушка без калибровки источником методики: пороги
(opex, headcount, число кейсов и т. п.) подобраны "на глаз", чтобы разные
должности получали разные уровни в демо. Эти тесты не утверждают, что пороги
методологически верны — они фиксируют ТЕКУЩИЕ границы, чтобы случайное
изменение константы в ``_profile_from_dossier`` было заметно в diff тестов,
а не тихо меняло поведение демо-режима.
"""

from __future__ import annotations

import pytest

from jeval.agent.fake import FakeAgent
from jeval.domain.enums import (
    Communication,
    FreedomToAct,
    Magnitude,
    ManagerialKnowHow,
    NonQuantitativeImpact,
    ProblemArea,
    ProblemComplexity,
    SpecializedKnowHow,
)
from jeval.domain.models import Authorities, JobDossier, Reporting, Scope


def _dossier(
    opex: float = 0,
    headcount: int = 0,
    subordinates: int = 0,
    decisions: int = 0,
    stakeholders: int = 0,
    cases: int = 0,
) -> JobDossier:
    return JobDossier(
        name="Тестовая должность",
        scope=Scope(annual_opex=opex or None, headcount=headcount or None),
        reporting=Reporting(subordinates=[f"п{i}" for i in range(subordinates)]),
        authorities=Authorities(decides_alone=[f"р{i}" for i in range(decisions)]),
        stakeholders=[f"с{i}" for i in range(stakeholders)],
        problem_cases=[f"кейс {i}" for i in range(cases)],
    )


def test_output_is_marked_as_test_data():
    out = FakeAgent().select_factors(_dossier())
    assert out.is_test_data is True


@pytest.mark.parametrize(
    "opex,expected",
    [
        (0, SpecializedKnowHow.B),
        (1, SpecializedKnowHow.C),
        (100_000_000, SpecializedKnowHow.C),
        (100_000_001, SpecializedKnowHow.D),
        (1_000_000_000, SpecializedKnowHow.D),
        (1_000_000_001, SpecializedKnowHow.E),
        (5_000_000_000, SpecializedKnowHow.E),
        (5_000_000_001, SpecializedKnowHow.F),
        (20_000_000_000, SpecializedKnowHow.F),
        (20_000_000_001, SpecializedKnowHow.G),
    ],
)
def test_specialization_opex_breakpoints(opex, expected):
    out = FakeAgent().select_factors(_dossier(opex=opex))
    assert out.selections.know_how.specialization == expected


@pytest.mark.parametrize(
    "subordinates,headcount,expected",
    [
        (0, 0, ManagerialKnowHow.I),
        (1, 19, ManagerialKnowHow.I),
        (2, 0, ManagerialKnowHow.II),
        (0, 20, ManagerialKnowHow.II),
        (3, 0, ManagerialKnowHow.II),
        (0, 99, ManagerialKnowHow.II),
        (4, 0, ManagerialKnowHow.III),
        (0, 100, ManagerialKnowHow.III),
    ],
)
def test_management_subordinate_headcount_breakpoints(subordinates, headcount, expected):
    out = FakeAgent().select_factors(_dossier(subordinates=subordinates, headcount=headcount))
    assert out.selections.know_how.management == expected


@pytest.mark.parametrize(
    "stakeholders,expected", [(4, Communication.TWO), (5, Communication.THREE)]
)
def test_communication_stakeholder_breakpoint(stakeholders, expected):
    out = FakeAgent().select_factors(_dossier(stakeholders=stakeholders))
    assert out.selections.know_how.communication == expected


@pytest.mark.parametrize(
    "cases,area,complexity",
    [
        (0, ProblemArea.B, ProblemComplexity.PATTERNED),
        (1, ProblemArea.C, ProblemComplexity.VARIABLE),
        (2, ProblemArea.D, ProblemComplexity.VARIABLE),
        (3, ProblemArea.E, ProblemComplexity.ADAPTIVE),
        (4, ProblemArea.F, ProblemComplexity.ADAPTIVE),
        (5, ProblemArea.F, ProblemComplexity.ADAPTIVE),  # клампится на последнем уровне area
    ],
)
def test_problem_solving_case_count_breakpoints(cases, area, complexity):
    out = FakeAgent().select_factors(_dossier(cases=cases))
    assert out.selections.problem_solving.area == area
    assert out.selections.problem_solving.complexity == complexity


@pytest.mark.parametrize(
    "decisions,headcount,expected",
    [
        (0, 0, FreedomToAct.B),
        (0, 50, FreedomToAct.B),   # граница headcount>50 не строгая >=, а строгая >
        (0, 51, FreedomToAct.C),
        (5, 0, FreedomToAct.G),
        (6, 0, FreedomToAct.G),    # клампится на последнем уровне
        (4, 51, FreedomToAct.G),
    ],
)
def test_freedom_decisions_headcount_breakpoints(decisions, headcount, expected):
    out = FakeAgent().select_factors(_dossier(decisions=decisions, headcount=headcount))
    assert out.selections.accountability.freedom == expected


def test_magnitude_is_always_non_quantitative():
    """Без утверждённой корпоративной матрицы в ₸ FakeAgent не имеет права
    выводить количественный Magnitude — даже при огромном opex."""
    out = FakeAgent().select_factors(_dossier(opex=999_999_999_999))
    assert out.selections.accountability.magnitude == Magnitude.N
    assert out.selections.accountability.non_quantitative_impact is not None


@pytest.mark.parametrize(
    "subordinates,cases,stakeholders,expected",
    [
        (0, 0, 0, NonQuantitativeImpact.I),
        (2, 1, 4, NonQuantitativeImpact.V),   # 2+1+1(стейкхолдеры>=4) = 4 -> индекс 4
        (10, 10, 10, NonQuantitativeImpact.VI),  # клампится на min(5, ...) -> индекс 5
    ],
)
def test_non_quantitative_impact_scope_score_breakpoints(subordinates, cases, stakeholders, expected):
    out = FakeAgent().select_factors(
        _dossier(subordinates=subordinates, cases=cases, stakeholders=stakeholders)
    )
    assert out.selections.accountability.non_quantitative_impact == expected
