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
    # На малых баллах округление сильнее; с 10 шаг близок к 15%.
    start = tables.HAY_SERIES.index(10)
    for a, b in zip(tables.HAY_SERIES[start:], tables.HAY_SERIES[start + 1:]):
        assert 1.10 <= b / a <= 1.20


@pytest.mark.parametrize(
    "spec,mgmt,comm,points",
    [("A", "T", "1", 43), ("B", "T", "1", 57), ("E", "III", "2", 350),
     ("H", "IV", "3", 1216)],
)
def test_know_how_matches_xlsm_comp(spec, mgmt, comm, points):
    assert tables.know_how_points(spec, mgmt, comm) == points


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
    assert score.know_how.points == 38
    assert score.accountability.points == 8


def test_problem_solving_plus_minus_and_ptsic_match_xlsm():
    assert tables.problem_solving_percent("E", 4) == 43
    assert tables.problem_solving_percent("E", 4, -1) == 43
    assert tables.problem_solving_percent("E", 4, 1) == 50
    assert tables.problem_solving_points(304, "E", 4) == 132


@pytest.mark.parametrize(
    "freedom,magnitude,impact,points",
    [("A", "N", "R", 9), ("A", "1", "P", 29), ("E", "3", "S", 200),
     ("H", "4", "P", 1216)],
)
def test_accountability_matches_xlsm_finalite(freedom, magnitude, impact, points):
    assert tables.accountability_points(freedom, magnitude, impact) == points


@pytest.mark.parametrize(
    "freedom,level,points",
    [("A", "I", 9), ("A", "VI", 38), ("E", "I", 50), ("E", "IV", 115),
     ("E", "VI", 200), ("H", "VI", 700)],
)
def test_accountability_non_quantitative_branch_matches_xlsm(freedom, level, points):
    assert tables.accountability_points(
        freedom, "N", non_quantitative_impact=level
    ) == points


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
    assert 0 <= score.grade <= 38


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


def test_full_control_row_from_evaluation_template():
    """F+/II+/3, E/4, E/4-/S = 460+200+230=890, grade 21, A1."""
    selections = FactorSelections(
        know_how=KnowHowSelection(
            specialization=SpecializedKnowHow.F,
            management=ManagerialKnowHow.II,
            communication=Communication.THREE,
            plus_minus=1,
        ),
        problem_solving=ProblemSolvingSelection(
            area=ProblemArea.E,
            complexity=ProblemComplexity.ADAPTIVE,
        ),
        accountability=AccountabilitySelection(
            freedom=FreedomToAct.E,
            magnitude=Magnitude.FOUR,
            impact=ImpactType.S,
            plus_minus=-1,
        ),
    )
    score = compute_score(selections)
    assert score.know_how.points == 460
    assert score.problem_solving.percentage == 43
    assert score.problem_solving.points == 200
    assert score.accountability.points == 230
    assert score.total_points == 890
    assert score.grade == 21
    assert score.profile_long == "A1"
