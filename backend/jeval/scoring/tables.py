"""Точные расчётные таблицы из ``Калькулятор Hay Group.xlsm``.

Формулы воспроизводят XLM-функции COMP, IC, PTSIC и FINALITE листа
``macro d'éval``. Значения не аппроксимируются арифметическим умножением.

ПРОВЕРКА: ``macro d'éval`` — лист Excel4 XLM-макросов (не VBA), поэтому он не
декомпилируется как обычный VBA-модуль; его формулы извлечены напрямую из
``xl/macrosheets/sheet1.xml`` через ``oletools``/``zipfile`` и пересчитаны
вручную для конкретных комбинаций уровней. Соответствие данного модуля
формулам книги построчно подтверждено в ``tests/test_tables_match_xlsm.py``
(индекс ряда ``pas_hay`` = 'macro d''éval'!$A$2:$B$60, формулы COMP/IC/PTSIC/
FINALITE = ячейки D1/G1/J1/M1 того же листа). Ветка ``backup-old-tables``
(старый ``HAY_SERIES``, начинавшийся с 38) не совпадает с книгой и неверна.
"""

from __future__ import annotations

TABLES_VERIFIED = True

# ``pas_hay`` / ``Valeurs_hay`` из макролиста ('macro d''éval'!$A$2:$B$60).
# Старая реализация (ветка backup-old-tables) ошибочно начинала ряд с 38 —
# это была позиция 16 настоящего ряда, не его начало. См. ПРОВЕРКА выше.
HAY_SERIES: tuple[int, ...] = (
    4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 19, 22, 25, 29, 33, 38, 43, 50,
    57, 66, 76, 87, 100, 115, 132, 152, 175, 200, 230, 264, 304, 350,
    400, 460, 528, 608, 700, 800, 920, 1056, 1216, 1400, 1600, 1840,
    2112, 2432, 2800, 3200, 3680, 4224, 4864, 5600, 6400, 7360, 8448,
    9728, 11200, 12800, 14720,
)
STEP_RATIO = 1.15


def _series_at_clamped(index: int) -> int:
    return HAY_SERIES[min(max(index, 0), len(HAY_SERIES) - 1)]


_SPEC_INDEX = {letter: i for i, letter in enumerate("ABCDEFGH")}
_MGMT_INDEX = {level: i for i, level in enumerate(("T", "I", "II", "III", "IV"))}
_AREA_INDEX = _SPEC_INDEX
_FREEDOM_INDEX = _SPEC_INDEX
_MAG_INDEX = {"N": 0, "1": 1, "2": 2, "3": 3, "4": 4}
_IMPACT_INDEX = {"R": 0, "C": 1, "S": 2, "P": 3}
_NON_QUANT_IMPACT_INDEX = {
    level: i for i, level in enumerate(("I", "II", "III", "IV", "V", "VI"))
}


def know_how_points(spec: str, mgmt: str, comm: str, plus_minus: int = 0) -> int:
    """COMP: A/T/1 = 43; специализация и управление = 2 шага, общение = 1."""
    # COMP normalises A/T/1 to key 17 in ``pas_hay`` => 43. A suffix ``-``
    # shifts it to 38 and ``+`` to 50.
    index = 16 + 2 * _SPEC_INDEX[spec] + 2 * _MGMT_INDEX[mgmt] + (int(comm) - 1)
    return _series_at_clamped(index + plus_minus)


PS_PERCENT_SERIES: tuple[int, ...] = (
    10, 12, 14, 16, 19, 22, 25, 29, 33, 38, 43, 50, 57, 66, 76, 87,
)


def problem_solving_percent(area: str, complexity: int, plus_minus: int = 0) -> int:
    """IC: точка пересечения области и сложности с пограничным шагом +/-.

    В XLSM суффиксы обоих подфакторов сводятся к одному шагу -1/0/+1.
    API хранит уже агрегированный модификатор.
    """
    # XLM IC uses MAX(0, plus + minus): a trailing ``+`` advances one
    # percentage step; ``-`` marks the lower edge but does not decrement it.
    idx = _AREA_INDEX[area] + 2 * (complexity - 1) + max(0, plus_minus)
    return PS_PERCENT_SERIES[min(max(idx, 0), len(PS_PERCENT_SERIES) - 1)]


def problem_solving_points(
    know_how: int, area: str, complexity: int, plus_minus: int = 0
) -> int:
    """PTSIC: сдвиг Know-How по ряду Hay, как в макросе, без float-округления."""
    kh_idx = series_index_of(know_how)
    pct = problem_solving_percent(area, complexity, plus_minus)
    pct_steps_below_100 = _steps_below_100(pct)
    return _series_at_clamped(kh_idx - pct_steps_below_100)


def _steps_below_100(pct: int) -> int:
    # Процентный ряд является фрагментом того же 15%-ряда: 10 находится за
    # 16 шагов до 100, 87 — за один шаг.
    pct_to_steps = {10: 16, 12: 15, 14: 14, 16: 13, 19: 12, 22: 11,
                    25: 10, 29: 9, 33: 8, 38: 7, 43: 6, 50: 5,
                    57: 4, 66: 3, 76: 2, 87: 1}
    return pct_to_steps[pct]


def accountability_points(
    freedom: str,
    magnitude: str,
    impact: str | None = None,
    plus_minus: int = 0,
    non_quantitative_impact: str | None = None,
) -> int:
    """FINALITE для количественной и неколичественной веток.

    При ``magnitude == N`` используется отдельная шкала I–VI. ``impact`` с N
    оставлен лишь для чтения ранее сохранённых оценок и не должен создаваться
    новыми оценками.
    """
    if magnitude == "N" and non_quantitative_impact:
        index = (
            5
            + 3 * _FREEDOM_INDEX[freedom]
            + 2 * _NON_QUANT_IMPACT_INDEX[non_quantitative_impact]
            + plus_minus
        )
        return _series_at_clamped(index)

    if impact is None:
        branch = "I–VI" if magnitude == "N" else "R/C/S/P"
        raise ValueError(f"Для Accountability требуется уровень воздействия {branch}")

    # Формула макроса: freedom*3 + magnitude*2 + impact*2 + modifier - 1,
    # где кодирование начинается с единицы. В нулевых индексах это 5 + ...
    index = (
        5
        + 3 * _FREEDOM_INDEX[freedom]
        + 2 * _MAG_INDEX[magnitude]
        + 2 * _IMPACT_INDEX[impact]
        + plus_minus
    )
    return _series_at_clamped(index)


# Денежные границы в предоставленной постановочной таблице выражены в российских
# рублях и относятся к конкретной версии таблицы. Корпоративной калибровки для
# тенге в материалах нет, поэтому автоматически выводить уровень Magnitude из ₸
# методологически нельзя.
MAGNITUDE_RANGES_VERIFIED = False
MAGNITUDE_RANGES_KZT: tuple[tuple[float, str], ...] = ()


def expected_magnitude(annual_amount_kzt: float | None) -> str | None:
    """Не выводит Magnitude без утверждённой корпоративной матрицы в тенге."""
    del annual_amount_kzt
    return None


def series_index_of(value: int) -> int:
    try:
        return HAY_SERIES.index(value)
    except ValueError:
        return min(range(len(HAY_SERIES)), key=lambda i: abs(HAY_SERIES[i] - value))
