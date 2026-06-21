"""Золотые значения сверены напрямую с «Калькулятор Hay Group.xlsm».

Числа в этом файле НЕ выведены из текущего `tables.py` — они посчитаны вручную
по реальному алгоритму макролиста ``macro d'éval``, который декомпилирован из
``xl/macrosheets/sheet1.xml`` (формулы Excel4 XLM, не VBA). Сами функции COMP /
IC / PTSIC / FINALITE — это просто способ записи Excel-формул на листе
``macro d'éval``, видны напрямую в значениях ячеек книги:

    COMP    = 'macro d''éval'!$D$1   (Know-How,        тело D2:D18)
    IC      = 'macro d''éval'!$G$1   (Problem Solving %,тело G2:G14)
    PTSIC   = 'macro d''éval'!$J$1   (Problem Solving б.,тело J2:J12)
    FINALITE= 'macro d''éval'!$M$1   (Accountability,   тело M2:M22)
    pas_hay = 'macro d''éval'!$A$2:$B$60   (геометрический ряд Hay, шаг 15%)

Для каждого случая ниже приведён путь по реальным формулам книги, чтобы
результат можно было пересчитать вручную по xlsm без доверия к этому файлу.

Формулы (выведены из ячеек, не из кода jeval):
    COMP:     index = comm + 2*MATCH(mgmt, [T,I,II,III,IV,V,VI,...,XII]) \
                       + 2*(CODE(spec)-64) + modifier + 12   [1-based позиция в pas_hay]
    IC:       index = 2*complexity + (CODE(area)-64) + modifier + 4   [1-based]
    PTSIC:    index = MATCH(know_how, Valeurs_hay) - (MATCH(100, Valeurs_hay) - MATCH(pct, Valeurs_hay))
    FINALITE: index = modifier + 3*(CODE(freedom)-64) + 2*magnitude_rank + 2*impact_rank + 4   [1-based]

`tables.py` реализует те же формулы в 0-based индексации (см. там же).
"""

import pytest

from jeval.scoring import tables


def test_hay_series_matches_pas_hay_named_range():
    """``pas_hay`` = 'macro d''éval'!$A$2:$B$60, столбец B построчно.

    Строки 2..60 книги: B2=4, B3=5, ... B32=304, ... B60=14720 (59 значений).
    Старая реализация (ветка backup-old-tables) начинала ряд с 38 — это была
    подстрока ряда начиная с позиции 16, не сам ряд.
    """
    assert tables.HAY_SERIES[0] == 4  # 'macro d''éval'!B2
    assert tables.HAY_SERIES[30] == 304  # 'macro d''éval'!B32
    assert tables.HAY_SERIES[-1] == 14720  # 'macro d''éval'!B60
    assert len(tables.HAY_SERIES) == 59


def test_know_how_ht1_matches_comp_macro():
    """COMP(H,T,1): D14=(CODE('H')-64)*2=16, D15=MATCH('T',...)*2=2, D16=1+2+16+0+12=31.

    VLOOKUP(31,pas_hay,2) -> строка 32 книги ('macro d''éval'!A32=31, B32=304).
    Это пример из аудита: H/T/1 Know-How.
    """
    assert tables.know_how_points("H", "T", "1") == 304


def test_know_how_boundary_modifier_matches_comp_macro():
    """COMP(C+,II,2): D14=(CODE('C')-64)*2=6, D15=MATCH('II',...)*2=6, D13(модификатор)=+1.

    D16 = 2 + 6 + 6 + 1 + 12 = 27 -> 'macro d''éval'!A28=27, B28=175.
    Проверяет границу: суффикс «+» на Connaissances даёт D11=1, D12=0,
    D13=MAX(MIN(1+0,1),-1)=1 — комбинированный модификатор клампится к [-1,1].
    """
    assert tables.know_how_points("C", "II", "2", plus_minus=1) == 175


def test_problem_solving_percent_f4_matches_ic_macro():
    """IC(F,4): G10=CODE('F')-64=6, G11=4*2=8, G12=8+6+0+4=18.

    VLOOKUP(18,pas_hay,2) -> 'macro d''éval'!A19=18, B19=50. Аудитный пример F/4.
    """
    assert tables.problem_solving_percent("F", 4) == 50


def test_problem_solving_percent_b2_matches_ic_macro():
    """IC(B,2): G10=CODE('B')-64=2, G11=2*2=4, G12=4+2+0+4=10.

    VLOOKUP(10,pas_hay,2) -> 'macro d''éval'!A11=10, B11=16.
    """
    assert tables.problem_solving_percent("B", 2) == 16


def test_problem_solving_points_matches_ptsic_macro():
    """PTSIC(know_how=304, F/4 -> pct=50): J4 = MATCH(304,Valeurs_hay) - (MATCH(100,..)-MATCH(50,..)).

    Valeurs_hay='macro d''éval'!$B$2:$B$51: позиция 304 = 31, позиция 100 = 23,
    позиция 50 = 18. J4 = 31-(23-18) = 26 -> VLOOKUP(26,pas_hay,2) ->
    'macro d''éval'!A27=26, B27=152. Завершает аудитный пример: KH H/T/1 (304) +
    PS F/4 (50%) = 152 баллов Problem Solving.
    """
    assert tables.problem_solving_points(304, "F", 4) == 152


def test_problem_solving_points_b2_matches_ptsic_macro():
    """PTSIC(know_how=175, B/2 -> pct=16): позиция 175=27, 100=23, 16=10.

    J4 = 27-(23-10) = 14 -> VLOOKUP(14,pas_hay,2) -> 'macro d''éval'!A15=14, B15=29.
    """
    assert tables.problem_solving_points(175, "B", 2) == 29


def test_accountability_d3c_matches_finalite_macro():
    """FINALITE(D,3,C): M15=(CODE('D')-64)*3=12, M16=VLOOKUP('3',N25:O34,2)*2=8.

    M17=VLOOKUP('C',N36:O45,2,FALSE)*2=4 (N43=C -> O43=2). M20=SUM(0,12,8,4)-1=23.
    VLOOKUP(23,pas_hay,2) -> 'macro d''éval'!A24=23, B24=100. Аудитный пример D/3/C.
    """
    assert tables.accountability_points("D", "3", impact="C") == 100


def test_accountability_points_requires_impact_for_quantitative_branch():
    """Без impact и без non_quantitative_impact для количественного Magnitude

    (1-4) формула не определена — функция должна явно отказать, а не молча
    посчитать что-то по ``_MAG_INDEX`` (там у "N" тоже есть индекс 0)."""
    with pytest.raises(ValueError, match="R/C/S/P"):
        tables.accountability_points("D", "3")


def test_accountability_points_requires_level_for_non_quantitative_branch():
    """То же для Magnitude=N без non_quantitative_impact: ветка I-VI обязательна."""
    with pytest.raises(ValueError, match="I–VI"):
        tables.accountability_points("D", "N")


def test_series_index_of_exact_match():
    assert tables.series_index_of(304) == 30


def test_series_index_of_nearest_match_fallback():
    """Fallback недостижим из живого пути (см. docstring ``series_index_of``):

    ``problem_solving_points`` всегда передаёт значение Know-How, которое само
    вернула ``know_how_points`` той же версии таблиц, то есть уже есть в ряду.
    303 искусственно выбрано как число между 304 (idx 30) и 264 (idx 29) —
    ближе к 304, поэтому fallback должен вернуть индекс 304, а не упасть.
    """
    assert 303 not in tables.HAY_SERIES
    assert tables.series_index_of(303) == tables.series_index_of(304) == 30


def test_accountability_non_quantitative_matches_finalite_macro():
    """FINALITE(F,N,IV): M15=(CODE('F')-64)*3=18, M16=VLOOKUP('N',N25:O34,2)*2=2
    (N34=N -> O34=1).

    M17=VLOOKUP('IV',N36:O45,2,FALSE)*2=8 (N39=IV -> O39=4). M20=SUM(0,18,2,8)-1=27.
    VLOOKUP(27,pas_hay,2) -> 'macro d''éval'!A28=27, B28=175. Покрывает корпоративную
    ветку N + I-VI, обязательную по qc.py (accountability_non_quantitative_policy).
    """
    assert (
        tables.accountability_points("F", "N", non_quantitative_impact="IV") == 175
    )
