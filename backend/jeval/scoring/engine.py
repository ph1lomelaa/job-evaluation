"""Сборка итогового расчёта из выбранных уровней факторов.

    Total = Know-How + Problem Solving + Accountability
    Профиль = знак разницы (Accountability − Problem Solving) в шагах 15%.
"""

from __future__ import annotations

from ..domain.enums import Profile
from ..domain.models import (
    AccountabilityResult,
    AccountabilitySelection,
    FactorSelections,
    KnowHowResult,
    ProblemSolvingResult,
    ScoreResult,
)
from . import tables
from .grades import grade_band_for_points, grade_position, steps_15pct
from .versions import ACTIVE_TABLE_VERSION, get_table_set

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


def compute_score(
    selections: FactorSelections, table_version: str | None = None
) -> ScoreResult:
    """Полный детерминированный расчёт по выбранным уровням факторов.

    ``table_version`` фиксирует, по какой версии подстановочных таблиц считалась
    эта оценка (по умолчанию — активная версия), и сохраняется в результате —
    см. ``ScoreResult.table_version`` и предупреждение в ``hierarchy.py`` при
    сравнении оценок разных версий.
    """
    version = table_version or ACTIVE_TABLE_VERSION
    table_set = get_table_set(version)
    kh = selections.know_how
    ps = selections.problem_solving
    acc = selections.accountability

    # 1. Know-How
    kh_points = tables.know_how_points(
        kh.specialization.value, kh.management.value, kh.communication.value,
        kh.plus_minus, version,
    )

    # 2. Problem Solving (% от Know-How)
    ps_percent = tables.problem_solving_percent(
        ps.area.value, int(ps.complexity.value), ps.plus_minus, version
    )
    ps_points = tables.problem_solving_points(
        kh_points, ps.area.value, int(ps.complexity.value), ps.plus_minus, version
    )

    # 3. Accountability
    acc_points = tables.accountability_points(
        acc.freedom.value,
        acc.magnitude.value,
        acc.impact.value if acc.impact else None,
        acc.plus_minus,
        acc.non_quantitative_impact.value if acc.non_quantitative_impact else None,
        version,
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

    band = grade_band_for_points(total, version)
    zone, color = grade_position(total, band)

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
        grade=band.grade,
        grade_lower=band.lower,
        grade_mid=band.mid,
        grade_upper=band.upper,
        grade_zone=zone,
        grade_color=color,
        calculation_explanation=[
            f"1. Знания и умения (Know-How): специальные знания {kh.specialization.value}, "
            f"управленческие знания {kh.management.value}, коммуникации "
            f"{kh.communication.value}{_pm(kh.plus_minus)} вместе определяют одну ячейку в "
            f"подстановочной таблице Know-How → {kh_points} баллов.",
            f"2. Решение вопросов (Problem Solving): область {ps.area.value} и сложность "
            f"{ps.complexity.value}{_pm(ps.plus_minus)} по таблице пересечения дают "
            f"{ps_percent}% — именно от Know-How ({kh_points} баллов). Итоговые "
            f"{ps_points} баллов взяты по шагам геометрического ряда Hay (шаг ≈15%), "
            f"а не прямым умножением {ps_percent}% × {kh_points} — поэтому простое "
            "умножение в столбик даст немного другое число.",
            f"3. Ответственность (Accountability): свобода действий {acc.freedom.value}, "
            f"{_accountability_branch_text(acc)} по таблице пересечения дают "
            f"{acc_points} баллов.",
            f"4. Итог: {kh_points} (Know-How) + {ps_points} (Problem Solving) + "
            f"{acc_points} (Accountability) = {total} баллов → грейд {band.grade} "
            f"(диапазон {band.lower}–{band.upper}, {zone.lower()} зона).",
        ],
        methodology_basis="",
        table_version=table_set.table_version,
    )


def _accountability_branch_text(acc: AccountabilitySelection) -> str:
    modifier = _pm(acc.plus_minus)
    if acc.magnitude.value == "N" and acc.non_quantitative_impact is not None:
        return f"неколичественный уровень воздействия {acc.non_quantitative_impact.value}{modifier}"
    return f"величина {acc.magnitude.value} и тип влияния {acc.impact.value if acc.impact else '—'}{modifier}"


def _pm(value: int) -> str:
    return "+" if value > 0 else "−" if value < 0 else ""
