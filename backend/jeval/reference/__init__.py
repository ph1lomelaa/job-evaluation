"""Справочные материалы для агента: уровни подфакторов и корпоративные документы."""

from .levels import build_levels_reference, factor_level_reference, factor_level_rules
from .standards import STANDARDS_VERIFIED, build_standards_reference

__all__ = [
    "build_levels_reference",
    "build_standards_reference",
    "factor_level_reference",
    "factor_level_rules",
    "STANDARDS_VERIFIED",
]


def build_reference_text() -> str:
    """Полный справочный блок, добавляемый к системному промпту агента."""
    return build_levels_reference() + "\n\n" + build_standards_reference()
