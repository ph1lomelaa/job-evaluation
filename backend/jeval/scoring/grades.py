"""Матрица Jobgrades из предоставленного XLSM и правило шага 15%.

ФАЗА 2: ``GRADE_MATRIX`` читается версионированно через
``scoring.versions.get_table_set`` (см. примечание в ``tables.py``).
``GRADE_MATRIX`` ниже — вид активной версии для обратной совместимости.
"""

from __future__ import annotations

import math

from .versions import ACTIVE_TABLE_VERSION, GradeBandData as GradeBand, get_table_set

# (grade, lower, mid, upper) — вид активной версии; источник —
# ``scoring/data/<table_version>.json``.
GRADE_MATRIX: tuple[GradeBand, ...] = get_table_set(ACTIVE_TABLE_VERSION).grade_matrix


def grade_for_points(points: int, table_version: str | None = None) -> int:
    """Грейд по суммарным баллам должности.

    За пределами числовой таблицы XLSM (XX) возвращается максимальный грейд 38,
    так как доменная модель хранит числовой грейд; такой случай отдельно виден
    по превышению ``grade_upper``.
    """
    matrix = get_table_set(table_version).grade_matrix
    if points <= matrix[0].upper:
        return matrix[0].grade
    for band in matrix:
        if band.lower <= points <= band.upper:
            return band.grade
    return matrix[-1].grade


def grade_band_for_points(points: int, table_version: str | None = None) -> GradeBand:
    """Полный диапазон грейда для результата."""
    return grade_band(grade_for_points(points, table_version), table_version)


def grade_position(points: int, band: GradeBand) -> tuple[str, str]:
    """Положение результата внутри диапазона и цвет для таблицы/карточки.

    Нижняя, средняя и верхняя зоны разделены относительно midpoint. Цвета —
    визуальная легенда приложения; сами границы и midpoint взяты из XLSM.
    """
    if points < band.mid:
        return "Нижняя", "blue"
    if points > band.mid:
        return "Верхняя", "orange"
    return "Средняя", "green"


def grade_band(grade: int, table_version: str | None = None) -> GradeBand:
    for band in get_table_set(table_version).grade_matrix:
        if band.grade == grade:
            return band
    raise ValueError(f"Неизвестный грейд: {grade}")


def steps_15pct(points_a: int, points_b: int) -> int:
    """Число «шагов» по 15% между двумя суммами баллов.

    0 — роли практически равны; 1 — едва уловимая разница; 2 — очевидная;
    3+ — существенная (возможен структурный разрыв). См. раздел 8.3 инструкции.

    Не версионируется: 15% — методологическая константа самого шага ряда Hay
    (тот же коэффициент, которым построен ``hay_series`` в любой версии таблиц),
    а не калибровочное значение, которое может отличаться между версиями.
    """
    if points_a <= 0 or points_b <= 0:
        return 0
    hi, lo = max(points_a, points_b), min(points_a, points_b)
    return round(math.log(hi / lo) / math.log(1.15))
