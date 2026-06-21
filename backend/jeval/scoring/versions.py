"""Реестр версионированных подстановочных таблиц Hay.

ФАЗА 2: HAY_SERIES/PS_PERCENT_SERIES/GRADE_MATRIX больше не хардкод в
``tables.py``/``grades.py`` — они читаются из JSON-файлов в ``scoring/data/``
по ``table_version``. Это позволяет хранить, какой версией таблиц посчитана
каждая ``Evaluation`` (поле ``table_version``), и явно предупреждать при
сравнении оценок, посчитанных разными версиями (см. ``hierarchy.py``).

Новую калибровку таблиц добавляют новым JSON-файлом + записью в
``TABLE_VERSIONS_AVAILABLE``, не правкой существующего файла — старые
``Evaluation`` должны навсегда оставаться воспроизводимыми по своей версии.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

_DATA_DIR = Path(__file__).parent / "data"

# Активная версия таблиц для новых расчётов. Смена этого значения не должна
# сопровождаться правкой JSON уже выпущенных версий — только добавлением новой.
ACTIVE_TABLE_VERSION = "hay-xlsm-v1"

TABLE_VERSIONS_AVAILABLE: tuple[str, ...] = ("hay-xlsm-v1",)


class GradeBandData(NamedTuple):
    grade: int
    lower: int
    mid: int
    upper: int


class TableSet(NamedTuple):
    table_version: str
    source: str
    verified_date: str
    hay_series: tuple[int, ...]
    ps_percent_series: tuple[int, ...]
    grade_matrix: tuple[GradeBandData, ...]


@lru_cache
def get_table_set(table_version: str | None = None) -> TableSet:
    """Таблицы указанной версии (по умолчанию — активная версия)."""
    version = table_version or ACTIVE_TABLE_VERSION
    path = _DATA_DIR / f"{version}.json"
    if not path.exists():
        raise ValueError(f"Неизвестная версия таблиц Hay: {version!r}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return TableSet(
        table_version=raw["table_version"],
        source=raw["source"],
        verified_date=raw["verified_date"],
        hay_series=tuple(raw["hay_series"]),
        ps_percent_series=tuple(raw["ps_percent_series"]),
        grade_matrix=tuple(GradeBandData(*row) for row in raw["grade_matrix"]),
    )
