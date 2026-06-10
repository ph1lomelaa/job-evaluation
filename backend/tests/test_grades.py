"""Тесты грейд-матрицы и правила 15% — значения точные, проверяем дословно."""

import pytest

from jeval.scoring.grades import GRADE_MATRIX, grade_for_points, steps_15pct


def test_matrix_is_contiguous_and_ordered():
    """Полосы грейдов идут подряд без разрывов и без пересечений."""
    for prev, cur in zip(GRADE_MATRIX, GRADE_MATRIX[1:]):
        assert cur.grade == prev.grade + 1
        assert cur.lower == prev.upper + 1
        assert prev.lower <= prev.mid <= prev.upper


@pytest.mark.parametrize(
    "points,grade",
    [
        (0, 0), (14, 0), (29, 0),
        (30, 1), (39, 1),
        (40, 2), (46, 2),
        (192, 12), (209, 12), (227, 12),
        (1056, 22), (1260, 22),
        (6020, 31),
    ],
)
def test_grade_boundaries(points, grade):
    assert grade_for_points(points) == grade


def test_out_of_range():
    assert grade_for_points(-100) == 0
    assert grade_for_points(99_999) == 31


def test_steps_15pct():
    assert steps_15pct(200, 200) == 0
    assert steps_15pct(230, 200) == 1   # один шаг ряда Hay
    assert steps_15pct(400, 200) == 5   # 1.15**5 ≈ 2.01
    assert steps_15pct(0, 200) == 0     # защита от нуля
