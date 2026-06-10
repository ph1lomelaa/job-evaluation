"""Подстановочные таблицы Hay Group и доступ к ним.

СТАТУС ТОЧНОСТИ
--------------
* `HAY_SERIES`     — стандартный геометрический ряд Hay с шагом ~15%. Стабилен.
* `PS_PERCENT`     — матрица «Решение вопросов %» (Area × Complexity). Сверена
                     со страницей 5 PDF и совпадает со стандартным чартом.
* Know-How и Accountability собраны по ДОКУМЕНТИРОВАННОЙ аддитивно-шаговой
  модели Hay (каждый уровень фактора = смещение на N шагов ряда). Якорные
  смещения (`*_OFFSET`, `*_ANCHOR`) ПРЕДВАРИТЕЛЬНЫ и подлежат сверке с
  официальным чартом Korn Ferry перед боевым использованием. См. `TABLES_VERIFIED`.

Заменить таблицы на выверенные значения = поправить константы в этом одном файле.
"""

from __future__ import annotations

# Функции работают со строковыми ключами (значениями enum-ов), что позволяет
# держать модуль таблиц независимым от моделей предметной области.

# Выставить True только после сверки Know-How/Accountability с официальным чартом.
TABLES_VERIFIED = False


# ── Геометрический ряд Hay (шаг ~15%) ─────────────────────────────────────────
# Каждое значение ≈ предыдущее × 1.15 с округлением по конвенции Hay.
HAY_SERIES: tuple[int, ...] = (
    38, 43, 50, 57, 66, 76, 87, 100, 115, 132, 152, 175, 200, 230, 264, 304,
    350, 400, 460, 528, 608, 700, 800, 920, 1056, 1216, 1400, 1600, 1840,
    2112, 2432, 2800, 3216, 3696, 4256, 4896, 5632,
)
STEP_RATIO = 1.15


def series_at(index: int) -> int:
    """Значение ряда по индексу с защитой от выхода за границы."""
    if index < 0:
        raise ValueError(f"Индекс ряда не может быть отрицательным: {index}")
    if index >= len(HAY_SERIES):
        raise ValueError(f"Индекс ряда вне диапазона таблицы: {index}")
    return HAY_SERIES[index]


def _series_at_clamped(index: int) -> int:
    """Значение ряда с мягким зажимом на границах.

    Используется для boundary `plus_minus`, чтобы крайние ячейки не приводили к падению
    расчета, если агент или пользовательское досье выбрали уже максимальный / минимальный
    шаг и попросили сдвиг дальше.
    """
    if index < 0:
        return HAY_SERIES[0]
    if index >= len(HAY_SERIES):
        return HAY_SERIES[-1]
    return HAY_SERIES[index]


# ── Фактор 1. Know-How ────────────────────────────────────────────────────────
# index = SPEC_OFFSET + MGMT_OFFSET + COMM_OFFSET + KH_ANCHOR
SPEC_OFFSET: dict[str, int] = {"A": 0, "B": 3, "C": 6, "D": 9, "E": 12, "F": 15, "G": 18, "H": 21}
MGMT_OFFSET: dict[str, int] = {"T": 0, "I": 1, "II": 2, "III": 3, "IV": 4}
COMM_OFFSET: dict[str, int] = {"1": 0, "2": 1, "3": 2}
KH_ANCHOR = 0  # A / T / 1 → HAY_SERIES[0] = 38


def know_how_points(spec: str, mgmt: str, comm: str, plus_minus: int = 0) -> int:
    """Баллы Know-How по уровням специальных/управленческих знаний и коммуникаций.

    `plus_minus` (-1/0/+1) сдвигает результат на один шаг ряда — модификатор
    пограничности «+»/«−», применяется только если уровень на границе ячейки.
    """
    index = SPEC_OFFSET[spec] + MGMT_OFFSET[mgmt] + COMM_OFFSET[comm] + KH_ANCHOR + plus_minus
    return _series_at_clamped(index)


# ── Фактор 2. Problem Solving % (Area × Complexity) ───────────────────────────
# Сверено с PDF (стр. 5): A1=10%, H5=87%. Ряд процентов и аддитивная модель:
#   pct_index = area_index + 2*(complexity-1)
PS_PERCENT_SERIES: tuple[int, ...] = (
    10, 12, 14, 16, 19, 22, 25, 29, 33, 38, 43, 50, 57, 66, 76, 87,
)
PS_AREA_INDEX: dict[str, int] = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}


def problem_solving_percent(area: str, complexity: int) -> int:
    """Процент Problem Solving по области и сложности (целое, напр. 43)."""
    idx = PS_AREA_INDEX[area] + 2 * (complexity - 1)
    return PS_PERCENT_SERIES[idx]


def problem_solving_points(know_how: int, area: str, complexity: int) -> int:
    """Баллы PS = Know-How × PS% (округление до ближайшего значения ряда Hay)."""
    raw = know_how * problem_solving_percent(area, complexity) / 100.0
    return _nearest_series(raw)


# ── Фактор 3. Accountability (Freedom × Magnitude × Impact) ───────────────────
# index = FREEDOM_OFFSET + MAG_OFFSET + IMPACT_OFFSET + ACC_ANCHOR
FREEDOM_OFFSET: dict[str, int] = {"A": 0, "B": 3, "C": 6, "D": 9, "E": 12, "F": 15, "G": 18, "H": 21}
MAG_OFFSET: dict[str, int] = {"N": 0, "1": 0, "2": 1, "3": 2, "4": 3}
IMPACT_OFFSET: dict[str, int] = {"R": 0, "C": 1, "S": 2, "P": 3}
ACC_ANCHOR = 0  # A / 1 / R → HAY_SERIES[0] = 38


def accountability_points(
    freedom: str, magnitude: str, impact: str, plus_minus: int = 0
) -> int:
    """Баллы Accountability по свободе действий, величине и типу воздействия."""
    index = (
        FREEDOM_OFFSET[freedom]
        + MAG_OFFSET[magnitude]
        + IMPACT_OFFSET[impact]
        + ACC_ANCHOR
        + plus_minus
    )
    return _series_at_clamped(index)


# ── Денежные диапазоны Magnitude (ПРЕДВАРИТЕЛЬНЫЕ / МОК) ──────────────────────
# Годовые показатели в тенге для количественной ветки Magnitude (раздел 7.2).
# ВНИМАНИЕ: границы — заглушка до получения утверждённой таблицы КМГ
# (в методике Hay диапазоны индексируются и утверждаются компанией).
# Замена = поправить границы здесь. См. MAGNITUDE_RANGES_VERIFIED.
MAGNITUDE_RANGES_VERIFIED = False

# (верхняя граница диапазона ₸/год, уровень Magnitude)
MAGNITUDE_RANGES_KZT: tuple[tuple[float, str], ...] = (
    (100_000_000, "1"),        # до 100 млн — очень незначительная
    (1_000_000_000, "2"),      # 100 млн – 1 млрд — незначительная
    (10_000_000_000, "3"),     # 1 – 10 млрд — средняя
    (float("inf"), "4"),       # свыше 10 млрд — большая
)


def expected_magnitude(annual_amount_kzt: float | None) -> str | None:
    """Ожидаемый уровень Magnitude по годовому денежному показателю.

    None — нет денежного показателя (количественная ветка неприменима,
    Magnitude остаётся N или обосновывается качественно).
    """
    if annual_amount_kzt is None or annual_amount_kzt <= 0:
        return None
    for upper, level in MAGNITUDE_RANGES_KZT:
        if annual_amount_kzt <= upper:
            return level
    return "4"  # pragma: no cover — недостижимо из-за inf


# ── Вспомогательное ───────────────────────────────────────────────────────────


def _nearest_series(value: float) -> int:
    """Ближайшее значение геометрического ряда Hay к произвольному числу."""
    return min(HAY_SERIES, key=lambda v: abs(v - value))


def series_index_of(value: int) -> int:
    """Индекс ближайшего значения ряда (для подсчёта шагов профиля)."""
    return min(range(len(HAY_SERIES)), key=lambda i: abs(HAY_SERIES[i] - value))
