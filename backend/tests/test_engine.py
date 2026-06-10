"""Тесты движка расчёта: таблицы, суммирование, профиль."""

import pytest

from jeval.domain.enums import (
    Communication,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ManagerialKnowHow,
    ProblemArea,
    ProblemComplexity,
    Profile,
    SpecializedKnowHow,
)
from jeval.domain.models import (
    AccountabilitySelection,
    FactorSelections,
    KnowHowSelection,
    ProblemSolvingSelection,
)
from jeval.scoring import compute_score, tables


def test_series_monotonic():
    assert list(tables.HAY_SERIES) == sorted(tables.HAY_SERIES)
    # шаг близок к 15%
    for a, b in zip(tables.HAY_SERIES, tables.HAY_SERIES[1:]):
        assert 1.10 <= b / a <= 1.20


@pytest.mark.parametrize(
    "area,complexity,pct",
    [("A", 1, 10), ("H", 5, 87), ("E", 3, 33), ("B", 1, 12)],
)
def test_ps_percent_matches_chart(area, complexity, pct):
    assert tables.problem_solving_percent(area, complexity) == pct


def test_know_how_monotonic_in_each_dimension():
    base = tables.know_how_points("C", "II", "2")
    assert tables.know_how_points("D", "II", "2") > base   # выше специализация
    assert tables.know_how_points("C", "III", "2") > base  # шире управление
    assert tables.know_how_points("C", "II", "3") > base   # выше коммуникации


def test_plus_minus_shifts_one_step():
    base = tables.know_how_points("E", "II", "2", plus_minus=0)
    assert tables.know_how_points("E", "II", "2", plus_minus=1) > base
    assert tables.know_how_points("E", "II", "2", plus_minus=-1) < base


def test_plus_minus_is_clamped_at_lower_boundary():
    selections = FactorSelections(
        know_how=KnowHowSelection(
            specialization=SpecializedKnowHow.A,
            management=ManagerialKnowHow.T,
            communication=Communication.ONE,
            plus_minus=-1,
        ),
        problem_solving=ProblemSolvingSelection(
            area=ProblemArea.A, complexity=ProblemComplexity.REPETITIVE
        ),
        accountability=AccountabilitySelection(
            freedom=FreedomToAct.A,
            magnitude=Magnitude.N,
            impact=ImpactType.R,
            plus_minus=-1,
        ),
    )
    score = compute_score(selections)
    assert score.know_how.points == tables.HAY_SERIES[0]
    assert score.accountability.points == tables.HAY_SERIES[0]


def _selections(area="E", complexity=4, impact=ImpactType.S) -> FactorSelections:
    return FactorSelections(
        know_how=KnowHowSelection(
            specialization=SpecializedKnowHow.E,
            management=ManagerialKnowHow.III,
            communication=Communication.TWO,
        ),
        problem_solving=ProblemSolvingSelection(
            area=ProblemArea(area), complexity=ProblemComplexity(complexity)
        ),
        accountability=AccountabilitySelection(
            freedom=FreedomToAct.E, magnitude=Magnitude.THREE, impact=impact
        ),
    )


def test_total_is_sum_of_factors():
    score = compute_score(_selections())
    assert score.total_points == (
        score.know_how.points + score.problem_solving.points + score.accountability.points
    )
    assert 0 <= score.grade <= 31


def test_profile_direction():
    # Сильное Accountability (P, большой масштаб) → профиль A.
    high_acc = FactorSelections(
        know_how=KnowHowSelection(
            specialization=SpecializedKnowHow.D,
            management=ManagerialKnowHow.II,
            communication=Communication.ONE,
        ),
        problem_solving=ProblemSolvingSelection(
            area=ProblemArea.B, complexity=ProblemComplexity.REPETITIVE
        ),
        accountability=AccountabilitySelection(
            freedom=FreedomToAct.G, magnitude=Magnitude.FOUR, impact=ImpactType.P
        ),
    )
    assert compute_score(high_acc).profile == Profile.A
