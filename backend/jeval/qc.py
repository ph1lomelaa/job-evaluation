"""Контроль качества оценки (раздел 9 инструкции).

Проверяет: персонализацию, влияние оплаты, нелогичные связки факторов и жёсткие
правила типа влияния. Возвращает список QC-флагов со статусами PASS/WARN/FAIL.
Запускается ПОСЛЕ выбора уровней и расчёта баллов.
"""

from __future__ import annotations

import re

from .domain.enums import (
    Communication,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ProblemArea,
    ProblemComplexity,
    QCSeverity,
    QCStatus,
    SpecializedKnowHow,
)
from .domain.models import FactorSelections, JobDossier, QCFlag, ScoreResult
from .scoring import PROFILE_MAX_STEPS

# Слова-маркеры (раздел 9.2 и 9.3) — нормализуем регистр.
_PERSON_MARKERS = (
    "стаж", "незаменим", "лучший эксперт", "фактически делает больше",
    "замещает руководител", "опытный сотрудник", "много лет",
)
_PAY_MARKERS = (
    "зарплат", "оклад", "ниже рынка", "рыночн", "надбавк", "текущий грейд",
    "поднять грейд",
)
_INFLUENCE_MARKERS = ("переговор", "сопротивлен", "конфликт интерес", "убежд", "торг")

# Запрещённые эпитеты в резюме роли (раздел 4, шаг 2): формулировки без доказательств.
_EPITHET_MARKERS = (
    "стратегическая роль", "стратегическая должность", "очень важная", "ключевая позиция",
    "ключевая должность", "ключевая роль", "высокая ответственность", "важная должность",
)

# Маркеры поддерживающих функций (раздел 9.4: «Magnitude всей компании у
# поддерживающей функции — требует декомпозиции»).
_SUPPORT_FUNCTION_MARKERS = (
    "hr", "кадр", "финанс", "бухгалт", "юрид", "правов", "комплаенс", "compliance",
    "ит", "it", "информацион", "закуп", "снабжен", "администрат", "делопроизвод",
    "документооборот", "pr", "связи с общественностью", "корпоративное управление",
)


def _dossier_text(d: JobDossier) -> str:
    parts: list[str] = [d.purpose or "", d.organizational_context or ""]
    parts += d.key_results + d.responsibilities + d.stakeholders
    return " ".join(parts).lower()


def _selection_text(sel: FactorSelections) -> str:
    chunks: list[str] = []
    for s in (sel.know_how, sel.problem_solving, sel.accountability):
        chunks += s.evidence + s.doubts
    return " ".join(chunks).lower()


def _flag(
    code: str, sev: QCSeverity, status: QCStatus, msg: str, rec: str,
    factors: tuple[str, ...] = (),
) -> QCFlag:
    return QCFlag(
        code=code, severity=sev, status=status, message=msg, recommendation=rec,
        factor_groups=list(factors),
    )


def _marker_pattern(marker: str) -> re.Pattern[str]:
    # \b только перед маркером (без хвоста): "стаж" должен матчить "стажем",
    # "стажировка", но "ит" не должен матчить середину слова "капитал"/"кредит".
    return re.compile(rf"\b{re.escape(marker)}", re.UNICODE)


def _find_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    """Маркеры, найденные с начала слова — а не как сырая подстрока."""
    return [m for m in markers if _marker_pattern(m).search(text)]


def _has_marker(text: str, markers: tuple[str, ...]) -> bool:
    return any(_marker_pattern(m).search(text) for m in markers)


def run_qc(
    dossier: JobDossier | None,
    selections: FactorSelections,
    score: ScoreResult,
    agent_text: str = "",
) -> list[QCFlag]:
    """QC-проверки (раздел 9). `agent_text` — резюме/обоснование агента для
    проверки запрещённых эпитетов и маркеров персонализации/оплаты.

    ``dossier`` опционален: без него правила, читающие текст/масштаб/KPI
    досье (раздел 9.2/9.3/9.4 про персонализацию, оплату, impact P/S, типовые
    кейсы, Magnitude и поддерживающие функции), пропускаются целиком, а не
    молча проходят как PASS без реальной проверки — это используется
    отдельным от полной оценки калькулятором (`/api/reference/calculate`),
    где никакого досье ещё нет, только уровни факторов.
    """
    kh = selections.know_how
    ps = selections.problem_solving
    acc = selections.accountability
    flags: list[QCFlag] = []
    text = (
        _dossier_text(dossier) + " " + _selection_text(selections) + " " + agent_text.lower()
        if dossier is not None
        else ""
    )

    # Пограничный модификатор не является способом выразить неуверенность.
    # Для каждого +/- нужны соседний уровень и проверяемое объяснение границы.
    for factor_code, selection in (
        ("know_how", kh), ("problem_solving", ps), ("accountability", acc)
    ):
        if selection.plus_minus:
            documented = bool(selection.modifier_reason and selection.adjacent_level)
            flags.append(
                _flag(
                    f"{factor_code}_modifier_boundary",
                    QCSeverity.MEDIUM,
                    QCStatus.PASS if documented else QCStatus.WARN,
                    (
                        f"Модификатор {selection.plus_minus:+d} подтверждён сравнением "
                        f"с {selection.adjacent_level}"
                        if documented
                        else f"Модификатор {selection.plus_minus:+d} не имеет обоснования границы"
                    ),
                    "Указать соседнюю ячейку и факты: для '+' — что выше базы, но ниже "
                    "следующего уровня; для '−' — что базовый уровень достигнут лишь по нижней границе.",
                    factors=(factor_code,),
                )
            )

    # В KMG DIGITAL финансовая величина не участвует: применяется только N/I–VI.
    non_quant_ok = acc.magnitude == Magnitude.N and acc.non_quantitative_impact is not None
    flags.append(
        _flag(
            "accountability_non_quantitative_policy",
            QCSeverity.HIGH,
            QCStatus.PASS if non_quant_ok else QCStatus.FAIL,
            (
                f"Применена неколичественная ветка N/{acc.non_quantitative_impact.value}"
                if non_quant_ok
                else "Accountability должна использовать корпоративную ветку N и уровень I–VI"
            ),
            "Не использовать доход, выручку или денежные диапазоны; выбрать N и подтвердить "
            "организационный уровень воздействия I–VI.",
            factors=("accountability",),
        )
    )

    if dossier is not None:
        # 9.2 Должность, а не человек
        hits = _find_markers(text, _PERSON_MARKERS)
        flags.append(
            _flag(
                "person_not_role", QCSeverity.HIGH,
                QCStatus.FAIL if hits else QCStatus.PASS,
                f"Признаки оценки работника, а не должности: {', '.join(hits)}" if hits
                else "Оценивается роль, не работник",
                "Исключить аргументы про конкретного работника или подтвердить, что это "
                "постоянное требование должности.",
            )
        )

        # 9.3 Независимость от оплаты
        pay = _find_markers(text, _PAY_MARKERS)
        flags.append(
            _flag(
                "pay_independence", QCSeverity.HIGH,
                QCStatus.FAIL if pay else QCStatus.PASS,
                f"Аргументы про оплату/грейд: {', '.join(pay)}" if pay
                else "Нет аргументов про оплату",
                "Убрать ссылки на зарплату, рынок и текущий грейд из обоснования.",
            )
        )

        # 9.4 Impact P без KPI и ресурсов → FAIL
        has_resource = _scope_has_resource(dossier)
        if acc.impact == ImpactType.P:
            ok = bool(dossier.kpis) and has_resource
            flags.append(
                _flag(
                    "impact_p_requires_kpi_resource", QCSeverity.HIGH,
                    QCStatus.PASS if ok else QCStatus.FAIL,
                    "Тип влияния P подтверждён KPI и ресурсным рычагом" if ok
                    else "Тип влияния P без KPI результата и/или ресурсного рычага",
                    "Для P нужны KPI результата и управление ресурсами (люди/бюджет/лимиты). "
                    "Иначе понизить до S или C.",
                    factors=("accountability",),
                )
            )

        # Shared impact требует документированного совместного результата. Сам факт
        # наличия руководителя не запрещает S: матричные и проектные роли могут иметь
        # совместное влияние при явно разделённой ответственности.
        if acc.impact == ImpactType.S:
            shared_text = " ".join(dossier.kpis + dossier.key_results + acc.evidence).lower()
            has_joint_result = _has_marker(
                shared_text,
                ("совмест", "разделенн", "совлад", "joint", "общий kpi", "общего результата"),
            )
            flags.append(
                _flag(
                    "impact_s_requires_joint_kpi", QCSeverity.MEDIUM,
                    QCStatus.PASS if has_joint_result else QCStatus.WARN,
                    "Тип влияния S подтверждён совместным результатом"
                    if has_joint_result
                    else "Тип влияния S не подтверждён совместным результатом или разделённой ответственностью",
                    "Указать общий конечный результат, других совладельцев и границы ответственности; "
                    "иначе пересмотреть тип влияния C или P.",
                    factors=("accountability",),
                )
            )

        # 9.4 Коммуникации 3 без кейсов влияния/сопротивления
        if kh.communication == Communication.THREE:
            has_cases = _has_marker(text, _INFLUENCE_MARKERS)
            flags.append(
                _flag(
                    "comm3_needs_resistance", QCSeverity.MEDIUM,
                    QCStatus.PASS if has_cases else QCStatus.WARN,
                    "Коммуникации 3 подтверждены кейсами переговоров/сопротивления" if has_cases
                    else "Коммуникации 3 без кейсов сопротивления/переговоров — вероятное завышение",
                    "Подтвердить изменение позиции/поведения, устойчивое сопротивление или "
                    "конфликт интересов. Иначе понизить до 2.",
                    factors=("know_how",),
                )
            )

    # 9.4 Know-How низкий + управление широкое
    if kh.specialization in {SpecializedKnowHow.A, SpecializedKnowHow.B, SpecializedKnowHow.C} \
            and kh.management.value in {"III", "IV"}:
        flags.append(
            _flag(
                "low_kh_high_mgmt", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Несостыковка: специальные знания {kh.specialization.value} при "
                f"управлении {kh.management.value}",
                "Проверить логику: широкая интеграция обычно требует более высоких знаний.",
                factors=("know_how",),
            )
        )

    # 9.4 Problem Solving: простая область + высокая сложность
    if ps.area in {ProblemArea.A, ProblemArea.B} \
            and ps.complexity in {ProblemComplexity.ADAPTIVE, ProblemComplexity.UNCHARTED}:
        flags.append(
            _flag(
                "easy_area_high_complexity", QCSeverity.HIGH, QCStatus.WARN,
                f"Область {ps.area.value} (по шаблону) при сложности {ps.complexity.value} "
                "почти всегда ошибка без сильного кейса",
                "Подтвердить нестандартность сильным кейсом или пересмотреть область/сложность.",
                factors=("problem_solving",),
            )
        )

    # 9.4 Высокая сложность без типовых кейсов
    if dossier is not None and ps.complexity.value >= 4 and len(dossier.problem_cases) < 3:
        flags.append(
            _flag(
                "high_complexity_few_cases", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Сложность {ps.complexity.value} при < 3 типовых кейсов",
                "Запросить минимум 3 типовых нестандартных кейса (раздел 6.2).",
                factors=("problem_solving",),
            )
        )

    # 9.4 Freedom A/B + Impact P
    if acc.freedom in {FreedomToAct.A, FreedomToAct.B} and acc.impact == ImpactType.P:
        flags.append(
            _flag(
                "low_freedom_primary_impact", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Свобода действий {acc.freedom.value} при типе влияния P требует пересмотра",
                "Строго контролируемая роль редко владеет KPI результата. Проверить.",
                factors=("accountability",),
            )
        )

    # Высокая свобода действий при низкой свободе мышления
    if acc.freedom in {FreedomToAct.F, FreedomToAct.G, FreedomToAct.H} \
            and ps.area in {ProblemArea.A, ProblemArea.B, ProblemArea.C}:
        flags.append(
            _flag(
                "high_freedom_low_thinking", QCSeverity.LOW, QCStatus.WARN,
                f"Высокая свобода действий {acc.freedom.value} при узкой свободе мышления "
                f"{ps.area.value}",
                "Объяснить расхождение Freedom to Act и области Problem Solving.",
                factors=("accountability", "problem_solving"),
            )
        )

    if dossier is not None:
        # 7.2 / 10.7 Magnitude: количественный уровень должен опираться на годовой показатель
        annual = _max_annual_amount(dossier)
        if acc.magnitude != Magnitude.N:
            has_source = bool(dossier.scope.source and dossier.scope.source.strip())
            magnitude_ok = annual is not None and has_source
            flags.append(
                _flag(
                    "magnitude_annual_figure", QCSeverity.MEDIUM,
                    QCStatus.PASS if magnitude_ok else QCStatus.WARN,
                    (
                        f"Количественная Magnitude подтверждена годовым показателем "
                        f"({annual:,.0f} ₸; источник: {dossier.scope.source})"
                        if magnitude_ok
                        else f"Magnitude {acc.magnitude.value} требует годового показателя в зоне роли и источника"
                    ),
                    "Указать годовой OPEX/CAPEX/выручку/бюджет в зоне роли и источник цифры; "
                    "если деньги искажают характер влияния, обосновать неколичественную ветку N.",
                    factors=("accountability",),
                )
            )

        # 9.4 «Масштаб всей компании» у поддерживающей функции
        func_text = " ".join(filter(None, (dossier.function, dossier.department, ""))).lower()
        if acc.magnitude == Magnitude.FOUR and _has_marker(func_text, _SUPPORT_FUNCTION_MARKERS):
            flags.append(
                _flag(
                    "support_function_company_scale", QCSeverity.MEDIUM, QCStatus.WARN,
                    "Большая величина воздействия (4) у поддерживающей функции — требует декомпозиции",
                    "Привязать масштаб к зоне ответственности роли (бюджет функции, охват), "
                    "а не ко всей компании «по привычке».",
                    factors=("accountability",),
                )
            )

    # Шаг 2 раздела 4: запрещённые эпитеты в резюме/обосновании агента
    if agent_text:
        epithets = _find_markers(agent_text.lower(), _EPITHET_MARKERS)
        flags.append(
            _flag(
                "neutral_summary", QCSeverity.LOW,
                QCStatus.WARN if epithets else QCStatus.PASS,
                f"Оценочные эпитеты без доказательств: {', '.join(epithets)}" if epithets
                else "Резюме роли нейтральное, без оценочных эпитетов",
                "Заменить эпитеты фактами: за что отвечает роль, какой бюджет, кто утверждает.",
            )
        )

    # 8.4 Профиль вне допустимых пределов континуума (P4…A4)
    if score.profile_steps > PROFILE_MAX_STEPS:
        flags.append(
            _flag(
                "profile_out_of_range", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Профиль {score.profile_long}: разрыв PS/Accountability "
                f"{score.profile_steps} шагов — за пределами континуума P4…A4",
                "Проверить уровни Problem Solving и Accountability: такой разрыв "
                "обычно означает ошибку выбора уровней.",
                factors=("problem_solving", "accountability"),
            )
        )

    return flags


def _max_annual_amount(d: JobDossier) -> float | None:
    """Максимальный годовой денежный показатель в зоне роли (₸)."""
    amounts = [
        v for v in (
            d.scope.annual_opex, d.scope.annual_capex, d.scope.annual_revenue,
            d.scope.function_budget, d.scope.project_portfolio,
        )
        if v is not None and v > 0
    ]
    return max(amounts) if amounts else None


def _scope_has_resource(d: JobDossier) -> bool:
    s = d.scope
    return any(
        v is not None
        for v in (s.annual_opex, s.annual_capex, s.annual_revenue, s.function_budget,
                  s.project_portfolio, s.headcount)
    )


def has_blocking_failures(flags: list[QCFlag]) -> bool:
    """Есть ли FAIL — основание не выдавать оценку как готовую."""
    return any(f.status == QCStatus.FAIL for f in flags)
