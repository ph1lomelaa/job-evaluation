"""Детерминированный движок расчёта баллов и грейда.

Здесь НЕТ обращений к LLM. На вход — выбранные уровни факторов, на выход —
баллы, профиль и грейд строго по подстановочным таблицам.
"""

from .engine import PROFILE_MAX_STEPS, compute_score, long_profile
from .grades import GRADE_MATRIX, grade_for_points, steps_15pct
from .tables import expected_magnitude

__all__ = [
    "compute_score",
    "grade_for_points",
    "steps_15pct",
    "GRADE_MATRIX",
    "long_profile",
    "PROFILE_MAX_STEPS",
    "expected_magnitude",
]
