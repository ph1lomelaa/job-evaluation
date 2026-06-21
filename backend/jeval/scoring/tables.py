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

ФАЗА 2: сами числовые ряды живут в ``scoring/data/<table_version>.json`` и
читаются через ``scoring.versions.get_table_set`` по параметру
``table_version`` — функции ниже не обращаются к глобальному тюплу напрямую.
``HAY_SERIES``/``PS_PERCENT_SERIES`` ниже — это вид активной версии для
обратной совместимости (интроспекция в тестах/скриптах), а не источник данных.
"""

from __future__ import annotations

from .versions import ACTIVE_TABLE_VERSION, TableSet, get_table_set

TABLES_VERIFIED = True

# Вид активной версии таблиц — для обратной совместимости существующих
# тестов/скриптов, которые читают эти имена напрямую. Источник истины —
# ``scoring/data/<table_version>.json`` через ``get_table_set``.
HAY_SERIES: tuple[int, ...] = get_table_set(ACTIVE_TABLE_VERSION).hay_series
STEP_RATIO = 1.15


def _series_at_clamped(table_set: TableSet, index: int) -> int:
    series = table_set.hay_series
    return series[min(max(index, 0), len(series) - 1)]


_SPEC_INDEX = {letter: i for i, letter in enumerate("ABCDEFGH")}
_MGMT_INDEX = {level: i for i, level in enumerate(("T", "I", "II", "III", "IV"))}
_AREA_INDEX = _SPEC_INDEX
_FREEDOM_INDEX = _SPEC_INDEX
_MAG_INDEX = {"N": 0, "1": 1, "2": 2, "3": 3, "4": 4}
_IMPACT_INDEX = {"R": 0, "C": 1, "S": 2, "P": 3}
_NON_QUANT_IMPACT_INDEX = {
    level: i for i, level in enumerate(("I", "II", "III", "IV", "V", "VI"))
}


def know_how_points(
    spec: str, mgmt: str, comm: str, plus_minus: int = 0, table_version: str | None = None
) -> int:
    """COMP: A/T/1 = 43; специализация и управление = 2 шага, общение = 1."""
    # COMP normalises A/T/1 to key 17 in ``pas_hay`` => 43. A suffix ``-``
    # shifts it to 38 and ``+`` to 50.
    table_set = get_table_set(table_version)
    index = 16 + 2 * _SPEC_INDEX[spec] + 2 * _MGMT_INDEX[mgmt] + (int(comm) - 1)
    return _series_at_clamped(table_set, index + plus_minus)


# Вид активной версии для обратной совместимости — см. примечание к HAY_SERIES.
PS_PERCENT_SERIES: tuple[int, ...] = get_table_set(ACTIVE_TABLE_VERSION).ps_percent_series


def problem_solving_percent(
    area: str, complexity: int, plus_minus: int = 0, table_version: str | None = None
) -> int:
    """IC: точка пересечения области и сложности с пограничным шагом +/-.

    В XLSM суффиксы обоих подфакторов сводятся к одному шагу -1/0/+1.
    API хранит уже агрегированный модификатор.
    """
    # XLM IC uses MAX(0, plus + minus): a trailing ``+`` advances one
    # percentage step; ``-`` marks the lower edge but does not decrement it.
    series = get_table_set(table_version).ps_percent_series
    idx = _AREA_INDEX[area] + 2 * (complexity - 1) + max(0, plus_minus)
    return series[min(max(idx, 0), len(series) - 1)]


def problem_solving_points(
    know_how: int,
    area: str,
    complexity: int,
    plus_minus: int = 0,
    table_version: str | None = None,
) -> int:
    """PTSIC: сдвиг Know-How по ряду Hay, как в макросе, без float-округления."""
    table_set = get_table_set(table_version)
    kh_idx = series_index_of(know_how, table_version)
    pct = problem_solving_percent(area, complexity, plus_minus, table_version)
    pct_steps_below_100 = _steps_below_100(pct, table_version)
    return _series_at_clamped(table_set, kh_idx - pct_steps_below_100)


def _steps_below_100(pct: int, table_version: str | None = None) -> int:
    # Процентный ряд является фрагментом того же 15%-ряда: позиция каждого
    # процента в pas_hay вычисляется относительно позиции 100, а не хардкодом.
    series = get_table_set(table_version).hay_series
    return series.index(100) - series.index(pct)


def accountability_points(
    freedom: str,
    magnitude: str,
    impact: str | None = None,
    plus_minus: int = 0,
    non_quantitative_impact: str | None = None,
    table_version: str | None = None,
) -> int:
    """FINALITE для количественной и неколичественной веток.

    При ``magnitude == N`` используется отдельная шкала I–VI. ``impact`` с N
    оставлен лишь для чтения ранее сохранённых оценок и не должен создаваться
    новыми оценками.
    """
    table_set = get_table_set(table_version)

    if magnitude == "N" and non_quantitative_impact:
        index = (
            5
            + 3 * _FREEDOM_INDEX[freedom]
            + 2 * _NON_QUANT_IMPACT_INDEX[non_quantitative_impact]
            + plus_minus
        )
        return _series_at_clamped(table_set, index)

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
    return _series_at_clamped(table_set, index)


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


def series_index_of(value: int, table_version: str | None = None) -> int:
    """Позиция значения в ряду Hay указанной версии.

    Nearest-match fallback ниже недостижим из живого пути: ``value`` всегда —
    результат ``know_how_points``/``problem_solving_points`` той же версии
    таблиц, т. е. уже сам является элементом ``hay_series``. Он остаётся как
    защита от рассинхронизации данных (например, при ручном вызове с
    посторонним числом или при правке JSON), а не как часть штатной формулы;
    зафиксировано тестом ``test_series_index_of_nearest_match_fallback``.
    """
    series = get_table_set(table_version).hay_series
    try:
        return series.index(value)
    except ValueError:
        return min(range(len(series)), key=lambda i: abs(series[i] - value))
