"""Сборка итогового расчёта из выбранных уровней факторов.

    Total = Know-How + Problem Solving + Accountability
    Профиль = знак разницы (Accountability − Problem Solving) в шагах 15%.
"""

from __future__ import annotations

from ..domain.enums import Profile
from ..domain.models import (
    AccountabilityResult,
    FactorSelections,
    KnowHowResult,
    ProblemSolvingResult,
    ScoreResult,
)
from . import tables
from .grades import grade_for_points, steps_15pct

# Порог в шагах 15%, ниже которого профиль считается сбалансированным (L).
PROFILE_BALANCED_STEPS = 1

# Допустимый предел континуума профиля (P4…P1, L, A1…A4). Больше — оценка
# выходит за пределы методики и помечается «*» (проверяется QC).
PROFILE_MAX_STEPS = 4


def long_profile(profile: Profile, steps: int) -> str:
    """Длинный профиль: L, A1…A4, P1…P4; «*» — вне допустимых пределов."""
    if profile == Profile.L:
        return "L"
    capped = min(steps, PROFILE_MAX_STEPS)
    suffix = "*" if steps > PROFILE_MAX_STEPS else ""
    return f"{profile.value}{capped}{suffix}"


def compute_score(selections: FactorSelections) -> ScoreResult:
    """Полный детерминированный расчёт по выбранным уровням факторов."""
    kh = selections.know_how
    ps = selections.problem_solving
    acc = selections.accountability

    # 1. Know-How
    kh_points = tables.know_how_points(
        kh.specialization.value, kh.management.value, kh.communication.value, kh.plus_minus
    )

    # 2. Problem Solving (% от Know-How)
    ps_percent = tables.problem_solving_percent(ps.area.value, int(ps.complexity.value))
    ps_points = tables.problem_solving_points(kh_points, ps.area.value, int(ps.complexity.value))

    # 3. Accountability
    acc_points = tables.accountability_points(
        acc.freedom.value, acc.magnitude.value, acc.impact.value, acc.plus_minus
    )

    total = kh_points + ps_points + acc_points

    # Профиль: сравнение Accountability и Problem Solving.
    steps = steps_15pct(acc_points, ps_points)
    if steps <= PROFILE_BALANCED_STEPS - 1:
        profile = Profile.L
    elif acc_points > ps_points:
        profile = Profile.A
    else:
        profile = Profile.P

    return ScoreResult(
        know_how=KnowHowResult(selection=kh, points=kh_points),
        problem_solving=ProblemSolvingResult(
            selection=ps, percentage=ps_percent, points=ps_points
        ),
        accountability=AccountabilityResult(selection=acc, points=acc_points),
        total_points=total,
        profile=profile,
        profile_steps=steps,
        profile_long=long_profile(profile, steps),
        grade=grade_for_points(total),
    )
