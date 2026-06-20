"""Матрица Jobgrades из предоставленного XLSM и правило шага 15%."""

from __future__ import annotations

import math
from typing import NamedTuple


class GradeBand(NamedTuple):
    grade: int
    lower: int
    mid: int
    upper: int


# (grade, lower, mid, upper) — точные значения из инструкции (раздел 8.2).
GRADE_MATRIX: tuple[GradeBand, ...] = (
    GradeBand(0, 0, 14, 29),
    GradeBand(1, 30, 34, 39),
    GradeBand(2, 40, 43, 46),
    GradeBand(3, 47, 50, 53),
    GradeBand(4, 54, 58, 62),
    GradeBand(5, 63, 67, 72),
    GradeBand(6, 73, 78, 84),
    GradeBand(7, 85, 91, 97),
    GradeBand(8, 98, 105, 113),
    GradeBand(9, 114, 124, 134),
    GradeBand(10, 135, 147, 160),
    GradeBand(11, 161, 176, 191),
    GradeBand(12, 192, 209, 227),
    GradeBand(13, 228, 248, 268),
    GradeBand(14, 269, 291, 313),
    GradeBand(15, 314, 342, 370),
    GradeBand(16, 371, 404, 438),
    GradeBand(17, 439, 478, 518),
    GradeBand(18, 519, 566, 613),
    GradeBand(19, 614, 674, 734),
    GradeBand(20, 735, 807, 879),
    GradeBand(21, 880, 967, 1055),
    GradeBand(22, 1056, 1158, 1260),
    GradeBand(23, 1261, 1384, 1507),
    GradeBand(24, 1508, 1654, 1800),
    GradeBand(25, 1801, 1970, 2140),
    GradeBand(26, 2141, 2345, 2550),
    GradeBand(27, 2551, 2785, 3020),
    GradeBand(28, 3021, 3300, 3580),
    GradeBand(29, 3581, 3915, 4250),
    GradeBand(30, 4251, 4655, 5060),
    GradeBand(31, 5061, 5540, 6020),
    GradeBand(32, 6021, 6590, 7160),
    GradeBand(33, 7161, 7740, 8320),
    GradeBand(34, 8321, 8980, 9640),
    GradeBand(35, 9641, 10410, 11180),
    GradeBand(36, 11181, 12080, 12980),
    GradeBand(37, 12981, 14030, 15080),
    GradeBand(38, 15081, 16310, 17540),
)


def grade_for_points(points: int) -> int:
    """Грейд по суммарным баллам должности.

    За пределами числовой таблицы XLSM (XX) возвращается максимальный грейд 38,
    так как доменная модель хранит числовой грейд; такой случай отдельно виден
    по превышению ``grade_upper``.
    """
    if points <= GRADE_MATRIX[0].upper:
        return GRADE_MATRIX[0].grade
    for band in GRADE_MATRIX:
        if band.lower <= points <= band.upper:
            return band.grade
    return GRADE_MATRIX[-1].grade


def grade_band_for_points(points: int) -> GradeBand:
    """Полный диапазон грейда для результата."""
    return grade_band(grade_for_points(points))


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


def grade_band(grade: int) -> GradeBand:
    for band in GRADE_MATRIX:
        if band.grade == grade:
            return band
    raise ValueError(f"Неизвестный грейд: {grade}")


def steps_15pct(points_a: int, points_b: int) -> int:
    """Число «шагов» по 15% между двумя суммами баллов.

    0 — роли практически равны; 1 — едва уловимая разница; 2 — очевидная;
    3+ — существенная (возможен структурный разрыв). См. раздел 8.3 инструкции.
    """
    if points_a <= 0 or points_b <= 0:
        return 0
    hi, lo = max(points_a, points_b), min(points_a, points_b)
    return round(math.log(hi / lo) / math.log(1.15))
