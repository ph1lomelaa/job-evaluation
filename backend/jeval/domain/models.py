"""Pydantic-модели предметной области.

Разделение ответственности:
  * `JobDossier`        — вход: описание должности (JE-досье, раздел 3.1 инструкции).
  * `FactorSelection`-ы — что выбирает LLM-агент (уровни + доказательства).
  * `Evaluation`        — итог: уровни + рассчитанные движком баллы, грейд, профиль.
  * `GateResult`/`QCFlag` — проверки полноты и качества.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

from .enums import (
    Communication,
    Confidence,
    DossierReviewStatus,
    EvaluationStatus,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ManagerialKnowHow,
    NonQuantitativeImpact,
    ProblemArea,
    ProblemComplexity,
    Profile,
    QCSeverity,
    QCStatus,
    SpecializedKnowHow,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── JE-досье (вход) ───────────────────────────────────────────────────────────


class ApprovalItem(BaseModel):
    item: str
    approver: str


class Authorities(BaseModel):
    """Что роль решает сама / согласует / только рекомендует."""

    decides_alone: list[str] = Field(default_factory=list)
    requires_approval: list[ApprovalItem] = Field(default_factory=list)
    recommends: list[str] = Field(default_factory=list)


class Scope(BaseModel):
    """Масштаб. Все денежные величины — годовые, в тенге, в зоне роли."""

    annual_opex: Optional[float] = None
    annual_capex: Optional[float] = None
    annual_revenue: Optional[float] = None
    function_budget: Optional[float] = None
    project_portfolio: Optional[float] = None
    headcount: Optional[int] = None
    assets: Optional[str] = None
    source: Optional[str] = Field(
        default=None, description="Источник цифр: бюджет, бизнес-план, упр. отчётность"
    )


class Reporting(BaseModel):
    manager: Optional[str] = None
    subordinates: list[str] = Field(default_factory=list)
    matrix_links: list[str] = Field(default_factory=list)


class ProblemCase(BaseModel):
    """Структурированный кейс Problem Solving (раздел 6.2 инструкции).

    Минимальный пакет доказательств сложности: что было задано, что неизвестно,
    какие альтернативы, был ли tradeoff, как проверялся результат.
    """

    summary: str
    given: Optional[str] = Field(default=None, description="Что было задано")
    unknown: Optional[str] = Field(default=None, description="Что было неизвестно")
    alternatives: Optional[str] = Field(default=None, description="Какие альтернативы рассматривались")
    tradeoff: Optional[str] = Field(default=None, description="Был ли tradeoff и какой")
    verification: Optional[str] = Field(default=None, description="Как проверялся результат")
    is_typical: bool = Field(default=True, description="Кейс типовой, а не исключительный")


class ImportMetadata(BaseModel):
    """Метаданные черновика, созданного из документа.

    Важно: `missing_fields` означает "не найдено в источнике", а не "не важно".
    Агент/парсер не должен заполнять эти поля догадками.
    """

    source_filename: Optional[str] = None
    source_type: str = "manual"
    source_mime_type: Optional[str] = None
    source_size_bytes: Optional[int] = None
    source_sha256: Optional[str] = None
    extraction_method: str = "manual"
    confidence: Confidence = Confidence.LOW
    notes: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    field_sources: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Откуда взялось каждое поле: заголовок, строка таблицы, секция или цитата",
    )
    raw_text_preview: Optional[str] = None


class JobDossier(BaseModel):
    """Описание должности на дату среза. Оцениваем РОЛЬ, не работника."""

    id: Optional[str] = None
    company_id: Optional[str] = None
    created_by_user_id: Optional[str] = None
    review_status: DossierReviewStatus = DossierReviewStatus.MANUAL_DRAFT
    import_metadata: Optional[ImportMetadata] = None
    name: str
    dzo: Optional[str] = Field(default=None, description="ДЗО / организация")
    department: Optional[str] = None
    function: Optional[str] = None

    snapshot_date: Optional[date] = Field(default=None, description="Дата среза оценки")

    purpose: Optional[str] = Field(default=None, description="Зачем существует роль (1–2 предложения)")
    key_results: list[str] = Field(default_factory=list, description="5–10 результатов, не процессов")
    responsibilities: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)

    reporting: Reporting = Field(default_factory=Reporting)
    authorities: Authorities = Field(default_factory=Authorities)
    scope: Scope = Field(default_factory=Scope)
    limits: list[str] = Field(
        default_factory=list,
        description="Лимиты: бюджет, закупки, договоры, штат, stop-work, технические решения",
    )

    stakeholders: list[str] = Field(default_factory=list)
    organizational_context: Optional[str] = None
    anchor_roles: list[str] = Field(default_factory=list, description="2–3 сопоставимые должности")
    problem_cases: list[str] = Field(
        default_factory=list, description="Типовые нестандартные кейсы для Problem Solving"
    )
    problem_cases_structured: list[ProblemCase] = Field(
        default_factory=list, description="Структурированные кейсы (минимальный пакет доказательств)"
    )
    documents: list[str] = Field(default_factory=list, description="ДИ, оргструктура, RACI, DoA…")
    confirmed_by: Optional[str] = Field(
        default=None, description="Кто подтвердил досье (руководитель / HR)"
    )

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


# ── Выбор уровней факторов (выход LLM-агента) ─────────────────────────────────


class FactorEvidence(BaseModel):
    """Общая обвязка к выбранному уровню: доказательства, сомнения, уверенность."""

    evidence: list[str] = Field(default_factory=list, description="2–3 факта из досье")
    doubts: list[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.MEDIUM
    modifier_reason: Optional[str] = Field(
        default=None,
        description="Почему выбран пограничный модификатор; обязателен по QC для +/−",
    )
    adjacent_level: Optional[str] = Field(
        default=None, description="Соседняя ячейка таблицы, с которой сравнивался уровень"
    )


class KnowHowSelection(FactorEvidence):
    specialization: SpecializedKnowHow
    management: ManagerialKnowHow
    communication: Communication
    plus_minus: int = Field(default=0, ge=-1, le=1, description="Модификатор пограничности: -1/0/+1")


class ProblemSolvingSelection(FactorEvidence):
    area: ProblemArea
    complexity: ProblemComplexity
    plus_minus: int = Field(default=0, ge=-1, le=1)


class AccountabilitySelection(FactorEvidence):
    freedom: FreedomToAct
    magnitude: Magnitude
    impact: Optional[ImpactType] = Field(
        default=None, description="R/C/S/P — только для количественной ветки Magnitude 1–4"
    )
    non_quantitative_impact: Optional[NonQuantitativeImpact] = Field(
        default=None, description="I–VI — объединённый уровень воздействия при Magnitude N"
    )
    plus_minus: int = Field(default=0, ge=-1, le=1)


class FactorSelections(BaseModel):
    """Полный набор уровней, которые выдаёт агент перед расчётом."""

    know_how: KnowHowSelection
    problem_solving: ProblemSolvingSelection
    accountability: AccountabilitySelection


# ── Рассчитанные результаты (выход движка) ────────────────────────────────────


class KnowHowResult(BaseModel):
    selection: KnowHowSelection
    points: int


class ProblemSolvingResult(BaseModel):
    selection: ProblemSolvingSelection
    percentage: float
    points: int


class AccountabilityResult(BaseModel):
    selection: AccountabilitySelection
    points: int


class ScoreResult(BaseModel):
    """Полный детерминированный расчёт по выбранным уровням."""

    know_how: KnowHowResult
    problem_solving: ProblemSolvingResult
    accountability: AccountabilityResult
    total_points: int
    profile: Profile
    profile_steps: int = Field(description="Шаги (по 15%) между PS и Accountability")
    profile_long: str = Field(
        default="",
        description="Длинный профиль (континуум P4…P1, L, A1…A4); * — вне допустимых пределов",
    )
    grade: int
    grade_lower: int = 0
    grade_mid: int = 0
    grade_upper: int = 0
    grade_zone: str = Field(default="Средняя", description="Положение внутри диапазона грейда")
    grade_color: str = Field(default="green", description="Цвет зоны: blue/green/orange")
    calculation_explanation: list[str] = Field(default_factory=list)
    methodology_basis: str = ""
    table_version: str = Field(
        default="",
        description="Версия подстановочных таблиц Hay, по которой посчитан результат",
    )


# ── Проверки ──────────────────────────────────────────────────────────────────


class GateCheck(BaseModel):
    block: str
    status: QCStatus  # pass / warn / fail
    note: Optional[str] = None


class GateResult(BaseModel):
    """Этап 0: допуск к оценке («нет понимания — нет оценки»)."""

    status: EvaluationStatus
    checks: list[GateCheck] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def can_evaluate(self) -> bool:
        return self.status != EvaluationStatus.CANNOT_EVALUATE


class QCFlag(BaseModel):
    code: str
    severity: QCSeverity
    status: QCStatus
    message: str
    recommendation: str


# ── Итоговая карточка оценки ──────────────────────────────────────────────────


class Evaluation(BaseModel):
    """Итог работы агента — карточка для Оценочного комитета (раздел 10)."""

    id: Optional[str] = None
    position_id: Optional[str] = None
    company_id: Optional[str] = None
    created_by_user_id: Optional[str] = None

    status: EvaluationStatus
    gate: GateResult

    selections: Optional[FactorSelections] = None
    score: Optional[ScoreResult] = None

    qc_flags: list[QCFlag] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    is_test_data: bool = Field(
        default=False,
        description=(
            "Уровни выбраны заглушкой (FakeAgent), а не реальным агентом/экспертом — "
            "ФАЗА 5: такую оценку нельзя показывать как готовую для Оценочного комитета "
            "(см. guard в api/deps.get_evaluator и баннер EvaluationCardPage)."
        ),
    )
    role_summary: str = Field(default="", description="Нейтральное резюме роли (раздел 10.2)")
    reasoning: str = ""
    clarifying_questions: list[str] = Field(default_factory=list)
    recommendation: str = ""
    table_version: str = Field(
        default="",
        description=(
            "Версия таблиц Hay, действовавшая на момент оценки — даже если "
            "score не посчитан (Gate 0 не пройден). Дублирует score.table_version "
            "при наличии score; нужно для предупреждений в сравнении (hierarchy.py)."
        ),
    )

    created_at: datetime = Field(default_factory=_now)


class DossierImportResult(BaseModel):
    """Ответ API импорта документа в черновик JE-досье."""

    position: JobDossier
    raw_text: str = Field(default="", description="Извлеченный текст документа")
    extracted_fields: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


# ── Публичные формы сбора описания должности ─────────────────────────────────


class PublicFormCreate(BaseModel):
    """Параметры одноразовой ссылки на стандартизированную форму JE-досье."""

    title: str = Field(min_length=1, max_length=200)
    recipient: Optional[str] = Field(default=None, max_length=200)
    expires_in_days: int = Field(default=7, ge=1, le=90)


class PublicJobForm(BaseModel):
    id: str
    token: str
    company_id: Optional[str] = None
    created_by_user_id: Optional[str] = None
    title: str
    recipient: Optional[str] = None
    status: Literal["active", "submitted", "expired"] = "active"
    is_read: bool = False
    position_id: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    expires_at: datetime
    submitted_at: Optional[datetime] = None


class PublicFormInfo(BaseModel):
    """Безопасное публичное представление формы без внутренних идентификаторов."""

    title: str
    recipient: Optional[str] = None
    status: Literal["active", "submitted", "expired"]
    expires_at: datetime
