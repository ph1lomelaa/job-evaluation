"""Этап 0 — допуск к оценке. Правило «нет понимания — нет оценки» (раздел 3.2).

Критические блоки: их отсутствие → CANNOT_EVALUATE (уровни и грейд не присваиваются).
Рекомендуемые блоки: их отсутствие → NEEDS_CLARIFICATION (можно дать предварительную
оценку с пометкой о низкой уверенности).
"""

from __future__ import annotations

from collections.abc import Callable

from .domain.enums import EvaluationStatus, QCStatus
from .domain.models import GateCheck, GateResult, JobDossier, Scope


def _scope_has_magnitude(scope: Scope) -> bool:
    """Есть ли хоть один измеритель масштаба (количественный или качественный)."""
    return any(
        v is not None
        for v in (
            scope.annual_opex,
            scope.annual_capex,
            scope.annual_revenue,
            scope.function_budget,
            scope.project_portfolio,
            scope.headcount,
            scope.assets,
        )
    )


def _has_decision_split(d: JobDossier) -> bool:
    """Понятно ли, что роль решает сама / согласует / рекомендует."""
    a = d.authorities
    return bool(a.decides_alone or a.requires_approval or a.recommends)


# (ключ блока, критичность, предикат наличия) — порядок = порядок вывода.
_CRITICAL: list[tuple[str, Callable[[JobDossier], bool]]] = [
    ("Цель должности", lambda d: bool(d.purpose and d.purpose.strip())),
    ("Ключевые результаты", lambda d: len(d.key_results) > 0),
    ("Описание функций", lambda d: len(d.responsibilities) > 0),
    ("Оргконтекст", lambda d: bool(d.organizational_context and d.organizational_context.strip())),
    ("Полномочия (сам/согласует/рекомендует)", _has_decision_split),
    ("Масштаб воздействия", lambda d: _scope_has_magnitude(d.scope)),
    ("KPI / показатели блока", lambda d: len(d.kpis) > 0),
]

_RECOMMENDED: list[tuple[str, Callable[[JobDossier], bool]]] = [
    ("Стейкхолдеры", lambda d: len(d.stakeholders) > 0),
    ("Якорные должности", lambda d: len(d.anchor_roles) > 0),
    (
        "Типовые кейсы (Problem Solving)",
        lambda d: len(d.problem_cases) + len(d.problem_cases_structured) >= 3,
    ),
    ("Дата среза", lambda d: d.snapshot_date is not None),
    ("Лимиты (бюджет, закупки, штат, stop-work)", lambda d: len(d.limits) > 0),
    (
        "Подтверждение руководителя / HR",
        lambda d: bool(d.confirmed_by and d.confirmed_by.strip()),
    ),
]


def evaluate_gate(dossier: JobDossier) -> GateResult:
    """Проверить полноту JE-досье и вернуть статус допуска к оценке."""
    checks: list[GateCheck] = []
    missing_critical: list[str] = []
    warnings: list[str] = []

    for block, present in _CRITICAL:
        ok = present(dossier)
        checks.append(
            GateCheck(
                block=block,
                status=QCStatus.PASS if ok else QCStatus.FAIL,
                note=None if ok else "Критический блок отсутствует",
            )
        )
        if not ok:
            missing_critical.append(block)

    for block, present in _RECOMMENDED:
        ok = present(dossier)
        checks.append(
            GateCheck(
                block=block,
                status=QCStatus.PASS if ok else QCStatus.WARN,
                note=None if ok else "Желательно для надёжной оценки",
            )
        )
        if not ok:
            warnings.append(block)

    if missing_critical:
        status = EvaluationStatus.CANNOT_EVALUATE
    elif warnings:
        status = EvaluationStatus.NEEDS_CLARIFICATION
    else:
        status = EvaluationStatus.READY

    return GateResult(
        status=status,
        checks=checks,
        missing_fields=missing_critical,
        warnings=warnings,
    )
