"""Общие фикстуры: полное досье, фейковый агент (без сети)."""

from __future__ import annotations

from datetime import date

import pytest

from jeval.agent import AgentOutput
from jeval.domain.enums import (
    Communication,
    Confidence,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ManagerialKnowHow,
    NonQuantitativeImpact,
    ProblemArea,
    ProblemComplexity,
    SpecializedKnowHow,
)
from jeval.domain.models import (
    AccountabilitySelection,
    ApprovalItem,
    Authorities,
    FactorSelections,
    JobDossier,
    KnowHowSelection,
    ProblemSolvingSelection,
    Reporting,
    Scope,
)


@pytest.fixture
def full_dossier() -> JobDossier:
    """Должность, проходящая Gate 0 (все критические блоки заполнены)."""
    return JobDossier(
        id="pos-1",
        name="Начальник управления ТОиР актива",
        dzo="ДЗО Добыча",
        function="Производство / ТОиР",
        snapshot_date=date(2026, 6, 10),
        purpose="Обеспечивать надёжность и готовность оборудования актива.",
        key_results=[
            "Годовой план ТОиР выполнен",
            "Аварийность снижена",
            "Бюджет ТОиР исполнен в лимите",
        ],
        responsibilities=["Планирование ТОиР", "Управление подрядчиками", "Контроль HSE"],
        kpis=["Коэффициент готовности", "Исполнение бюджета ТОиР", "LTIFR"],
        reporting=Reporting(manager="Директор по производству", subordinates=["Мастера", "Инженеры"]),
        authorities=Authorities(
            decides_alone=["Оперативные решения по ремонту"],
            requires_approval=[ApprovalItem(item="CAPEX свыше лимита", approver="Комитет")],
            recommends=["Стратегия обновления парка"],
        ),
        scope=Scope(annual_opex=4_000_000_000, headcount=120, source="Бюджет 2026"),
        limits=["Закупки до 50 млн ₸", "Stop-work при угрозе аварии"],
        stakeholders=["Производство", "Подрядчики", "HSE", "Снабжение"],
        organizational_context="Операторская модель, решения по CAPEX утверждает комитет.",
        anchor_roles=["Начальник ТОиР другого актива", "Главный инженер"],
        problem_cases=[
            "Внеплановый отказ ключевого оборудования",
            "Конфликт сроков ремонта и плана добычи",
            "Нехватка ЗИП в пик ремонтной кампании",
        ],
        documents=["ДИ", "Оргструктура", "RACI", "DoA"],
        confirmed_by="HR-директор ДЗО",
    )


@pytest.fixture
def sample_output() -> AgentOutput:
    """Фиксированный ответ агента — для тестов без обращения к Claude."""
    return AgentOutput(
        role_summary="Роль отвечает за годовой план ТОиР актива и бюджет OPEX.",
        overall_confidence=Confidence.MEDIUM,
        reasoning="Профессиональные знания, межфункциональная интеграция, joint KPI с добычей.",
        clarifying_questions=["Какой годовой CAPEX в зоне влияния роли?"],
        recommendation="Рассмотреть на Оценочном комитете.",
        selections=FactorSelections(
            know_how=KnowHowSelection(
                specialization=SpecializedKnowHow.E,
                management=ManagerialKnowHow.III,
                communication=Communication.TWO,
                evidence=["Управляет ТОиР", "Координирует подрядчиков"],
                confidence=Confidence.MEDIUM,
            ),
            problem_solving=ProblemSolvingSelection(
                area=ProblemArea.E,
                complexity=ProblemComplexity.ADAPTIVE,
                evidence=["Внеплановые отказы", "Конфликт сроков"],
                confidence=Confidence.MEDIUM,
            ),
            accountability=AccountabilitySelection(
                freedom=FreedomToAct.E,
                magnitude=Magnitude.N,
                non_quantitative_impact=NonQuantitativeImpact.V,
                evidence=["joint KPI с добычей по готовности"],
                confidence=Confidence.MEDIUM,
            ),
        ),
    )


class FakeAgent:
    """Заглушка агента: возвращает заранее заданный результат."""

    def __init__(self, output: AgentOutput) -> None:
        self._output = output

    def select_factors(self, dossier: JobDossier) -> AgentOutput:  # noqa: ARG002
        return self._output


@pytest.fixture
def fake_agent(sample_output: AgentOutput) -> FakeAgent:
    return FakeAgent(sample_output)
