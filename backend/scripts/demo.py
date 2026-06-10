"""Демо сквозного потока БЕЗ обращения к Claude.

Показывает: JE-досье → Gate 0 → (фейковые уровни) → движок → QC → карточка.
Запуск:  python scripts/demo.py
"""

from __future__ import annotations

from datetime import date

from jeval.agent import FakeAgent
from jeval.domain.models import ApprovalItem, Authorities, JobDossier, Scope
from jeval.orchestrator import JobEvaluator


def _sample_dossier() -> JobDossier:
    return JobDossier(
        id="pos-demo",
        name="Начальник управления ТОиР актива",
        dzo="ДЗО Добыча",
        snapshot_date=date(2026, 6, 10),
        purpose="Обеспечивать надёжность и готовность оборудования актива.",
        key_results=["План ТОиР выполнен", "Аварийность снижена", "Бюджет ТОиР в лимите"],
        responsibilities=["Планирование ТОиР", "Управление подрядчиками", "Контроль HSE"],
        kpis=["Коэффициент готовности", "Исполнение бюджета ТОиР", "LTIFR"],
        authorities=Authorities(
            decides_alone=["Оперативные решения по ремонту"],
            requires_approval=[ApprovalItem(item="CAPEX свыше лимита", approver="Комитет")],
        ),
        scope=Scope(annual_opex=4_000_000_000, headcount=120, source="Бюджет 2026"),
        stakeholders=["Производство", "Подрядчики", "HSE"],
        organizational_context="Операторская модель, CAPEX утверждает комитет.",
        anchor_roles=["Начальник ТОиР другого актива", "Главный инженер"],
        problem_cases=["Внеплановый отказ", "Конфликт сроков", "Нехватка ЗИП"],
    )


def main() -> None:
    ev = JobEvaluator(agent=FakeAgent()).evaluate(_sample_dossier())
    print(f"Статус:      {ev.status.value}")
    print(f"Уверенность: {ev.confidence.value}")
    if ev.score:
        s = ev.score
        print(
            f"Know-How={s.know_how.points}  "
            f"PS={s.problem_solving.points} ({s.problem_solving.percentage}%)  "
            f"Acc={s.accountability.points}"
        )
        print(f"ИТОГО: {s.total_points}  →  Грейд {s.grade}  ·  Профиль {s.profile.value}")
    print("\nQC-флаги:")
    for f in ev.qc_flags:
        print(f"  [{f.status.value.upper():4}] {f.code}: {f.message}")
    print(f"\nРекомендация: {ev.recommendation}")


if __name__ == "__main__":
    main()
