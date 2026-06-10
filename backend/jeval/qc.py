"""Контроль качества оценки (раздел 9 инструкции).

Проверяет: персонализацию, влияние оплаты, нелогичные связки факторов и жёсткие
правила типа влияния. Возвращает список QC-флагов со статусами PASS/WARN/FAIL.
Запускается ПОСЛЕ выбора уровней и расчёта баллов.
"""

from __future__ import annotations

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
from .scoring import PROFILE_MAX_STEPS, expected_magnitude

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


def _flag(code: str, sev: QCSeverity, status: QCStatus, msg: str, rec: str) -> QCFlag:
    return QCFlag(code=code, severity=sev, status=status, message=msg, recommendation=rec)


def run_qc(
    dossier: JobDossier,
    selections: FactorSelections,
    score: ScoreResult,
    agent_text: str = "",
) -> list[QCFlag]:
    """QC-проверки (раздел 9). `agent_text` — резюме/обоснование агента для
    проверки запрещённых эпитетов и маркеров персонализации/оплаты."""
    kh = selections.know_how
    ps = selections.problem_solving
    acc = selections.accountability
    flags: list[QCFlag] = []
    text = _dossier_text(dossier) + " " + _selection_text(selections) + " " + agent_text.lower()

    # 9.2 Должность, а не человек
    hits = [m for m in _PERSON_MARKERS if m in text]
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
    pay = [m for m in _PAY_MARKERS if m in text]
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
            )
        )

    # 9.4 Impact S без joint KPI → для вертикали manager/subordinate это FAIL.
    if acc.impact == ImpactType.S:
        vertical = bool(dossier.reporting.manager or dossier.reporting.subordinates)
        status = QCStatus.FAIL if vertical else QCStatus.WARN
        flags.append(
            _flag(
                "impact_s_requires_joint_kpi", QCSeverity.MEDIUM, status,
                "Тип влияния S требует совместного (joint) KPI с равноправными владельцами"
                if not vertical
                else "Тип влияния S в вертикали «руководитель–подчинённый» недопустим",
                "Подтвердить наличие joint KPI. S в вертикали «руководитель–подчинённый» — FAIL."
                if not vertical
                else "Понизить до C или P; в вертикали S не применяется.",
            )
        )

    # 9.4 Коммуникации 3 без кейсов влияния/сопротивления
    if kh.communication == Communication.THREE:
        has_cases = any(m in text for m in _INFLUENCE_MARKERS)
        flags.append(
            _flag(
                "comm3_needs_resistance", QCSeverity.MEDIUM,
                QCStatus.PASS if has_cases else QCStatus.WARN,
                "Коммуникации 3 подтверждены кейсами переговоров/сопротивления" if has_cases
                else "Коммуникации 3 без кейсов сопротивления/переговоров — вероятное завышение",
                "Подтвердить изменение позиции/поведения, устойчивое сопротивление или "
                "конфликт интересов. Иначе понизить до 2.",
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
            )
        )

    # 9.4 Высокая сложность без типовых кейсов
    if ps.complexity.value >= 4 and len(dossier.problem_cases) < 3:
        flags.append(
            _flag(
                "high_complexity_few_cases", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Сложность {ps.complexity.value} при < 3 типовых кейсов",
                "Запросить минимум 3 типовых нестандартных кейса (раздел 6.2).",
            )
        )

    # 9.4 Freedom A/B + Impact P
    if acc.freedom in {FreedomToAct.A, FreedomToAct.B} and acc.impact == ImpactType.P:
        flags.append(
            _flag(
                "low_freedom_primary_impact", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Свобода действий {acc.freedom.value} при типе влияния P требует пересмотра",
                "Строго контролируемая роль редко владеет KPI результата. Проверить.",
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
            )
        )

    # 7.2 / 10.7 Magnitude: количественный уровень должен опираться на годовой показатель
    annual = _max_annual_amount(dossier)
    if acc.magnitude != Magnitude.N:
        flags.append(
            _flag(
                "magnitude_annual_figure", QCSeverity.MEDIUM,
                QCStatus.PASS if annual is not None else QCStatus.WARN,
                "Magnitude подтверждена годовым денежным показателем" if annual is not None
                else f"Magnitude {acc.magnitude.value} без годового денежного показателя в досье",
                "Указать годовой OPEX/CAPEX/выручку/бюджет в зоне роли с источником, "
                "либо перейти на неколичественную ветку (N) с качественным обоснованием.",
            )
        )

    # 7.2 Magnitude против диапазонов (диапазоны ПРЕДВАРИТЕЛЬНЫЕ — см. tables.py)
    expected = expected_magnitude(annual)
    if expected is not None and acc.magnitude != Magnitude.N \
            and acc.magnitude.value != expected:
        flags.append(
            _flag(
                "magnitude_scope_mismatch", QCSeverity.MEDIUM, QCStatus.WARN,
                f"Выбрана Magnitude {acc.magnitude.value}, но по годовому показателю "
                f"({annual:,.0f} ₸) ожидается {expected} (диапазоны предварительные)",
                "Сверить объект воздействия и привязку к зоне роли; подтвердить выбор "
                "или скорректировать уровень.",
            )
        )

    # 9.4 «Масштаб всей компании» у поддерживающей функции
    func_text = " ".join(filter(None, (dossier.function, dossier.department, ""))).lower()
    if acc.magnitude == Magnitude.FOUR and any(m in func_text for m in _SUPPORT_FUNCTION_MARKERS):
        flags.append(
            _flag(
                "support_function_company_scale", QCSeverity.MEDIUM, QCStatus.WARN,
                "Большая величина воздействия (4) у поддерживающей функции — требует декомпозиции",
                "Привязать масштаб к зоне ответственности роли (бюджет функции, охват), "
                "а не ко всей компании «по привычке».",
            )
        )

    # Шаг 2 раздела 4: запрещённые эпитеты в резюме/обосновании агента
    if agent_text:
        epithets = [m for m in _EPITHET_MARKERS if m in agent_text.lower()]
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
