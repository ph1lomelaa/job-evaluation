"""Запуск и просмотр предварительных оценок Hay."""

from __future__ import annotations

import uuid
from itertools import product
from typing import Literal, Optional, Union
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field, ValidationError

from ...domain.models import (
    AccountabilitySelection,
    Evaluation,
    JobDossier,
    KnowHowSelection,
    ProblemSolvingSelection,
    FactorSelections,
)
from ...domain.enums import (
    Communication,
    FreedomToAct,
    ImpactType,
    ManagerialKnowHow,
    NonQuantitativeImpact,
    ProblemArea,
    ProblemComplexity,
    SpecializedKnowHow,
)
from ...export.pdf import build_evaluation_pdf
from ...hierarchy import run_hierarchy_qc
from ...orchestrator import JobEvaluator, _committee_recommendation, _downgrade, decide_status
from ...qc import has_blocking_failures, run_qc
from ...scoring import compute_score
from ...store import Store
from ..deps import WorkspaceContext, get_evaluator, get_store, workspace_context, write_workspace_context

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])

FactorGroupName = Literal["know_how", "problem_solving", "accountability"]

_SELECTION_MODEL_BY_GROUP = {
    "know_how": KnowHowSelection,
    "problem_solving": ProblemSolvingSelection,
    "accountability": AccountabilitySelection,
}

# Поля, которые эксперт может точечно скорректировать на каждом подфакторе —
# то же, что выбирает агент в FactorSelections, без evidence/doubts/confidence
# (те трогаются отдельно: evidence дополняется пометкой о правке, см. ниже).
_OVERRIDABLE_FIELDS: dict[FactorGroupName, set[str]] = {
    "know_how": {"specialization", "management", "communication", "plus_minus"},
    "problem_solving": {"area", "complexity", "plus_minus"},
    "accountability": {"freedom", "magnitude", "impact", "non_quantitative_impact", "plus_minus"},
}


class EvaluateRequest(BaseModel):
    position_id: str


class EvaluationRangeResponse(BaseModel):
    base_points: int
    base_grade: int
    min_points: int
    min_grade: int
    max_points: int
    max_grade: int
    uncertain_groups: list[FactorGroupName]
    scenarios_checked: int


@router.post("", response_model=Evaluation, status_code=201)
def create_evaluation(
    req: EvaluateRequest,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
    evaluator: JobEvaluator = Depends(get_evaluator),
) -> Evaluation:
    pos = store.get_position(req.position_id, ctx.company_id)
    if not pos:
        raise HTTPException(404, "Должность не найдена")
    peers = _collect_peers(store, exclude_id=pos.id, company_id=ctx.company_id)
    try:
        evaluation = evaluator.evaluate(pos, peers=peers)
    except RuntimeError as exc:
        raise HTTPException(502, f"Ошибка агента: {exc}") from exc
    evaluation.id = evaluation.id or str(uuid.uuid4())
    evaluation.company_id = ctx.company_id
    evaluation.created_by_user_id = ctx.user_id
    result = store.save_evaluation(evaluation, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "evaluation.create", "evaluation", evaluation.id, {"position_id": pos.id})
    return _with_author_name(result, store)


@router.get("", response_model=list[Evaluation])
def list_evaluations(
    position_id: Optional[str] = None,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> list[Evaluation]:
    return [_with_author_name(ev, store) for ev in store.list_evaluations(position_id, ctx.company_id)]


@router.get("/{evaluation_id}", response_model=Evaluation)
def get_evaluation(
    evaluation_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> Evaluation:
    ev = store.get_evaluation(evaluation_id, ctx.company_id)
    if not ev:
        raise HTTPException(404, "Оценка не найдена")
    return _with_author_name(ev, store)


@router.get("/{evaluation_id}/export.pdf")
def export_evaluation_pdf(
    evaluation_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> Response:
    """Подписываемый PDF карточки оценки для досье Оценочного комитета —
    альтернатива `window.print()` на EvaluationCardPage.tsx (раздел 10)."""
    evaluation = store.get_evaluation(evaluation_id, ctx.company_id)
    if not evaluation:
        raise HTTPException(404, "Оценка не найдена")
    if not evaluation.position_id:
        raise HTTPException(400, "У оценки нет привязанной должности")
    position = store.get_position(evaluation.position_id, ctx.company_id)
    if not position:
        raise HTTPException(404, "Должность для этой оценки не найдена")

    evaluation = _with_author_name(evaluation, store)
    try:
        pdf_bytes = build_evaluation_pdf(position, evaluation)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc

    # Content-Disposition должен быть latin-1 — имя должности почти всегда
    # кириллица, поэтому ASCII-имя в filename — запасной вариант для старых
    # клиентов, а реальное читаемое имя передаётся через filename* (RFC 5987).
    encoded_name = quote(f"otsenka-{position.name}-{evaluation_id}.pdf")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=\"evaluation-{evaluation_id}.pdf\"; filename*=UTF-8''{encoded_name}"
        },
    )


@router.get("/{evaluation_id}/range", response_model=EvaluationRangeResponse)
def get_evaluation_range(
    evaluation_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> EvaluationRangeResponse:
    """Диапазон результата при сдвиге неподтверждённых подфакторов на один
    соседний уровень. Это не новый грейд, а прозрачная чувствительность текущей
    оценки: показывает HR, насколько незакрытые вопросы реально влияют на итог."""
    evaluation = store.get_evaluation(evaluation_id, ctx.company_id)
    if not evaluation or evaluation.selections is None or evaluation.score is None:
        raise HTTPException(404, "Оценка с рассчитанными уровнями не найдена")

    uncertain = _uncertain_factor_groups(evaluation)
    dimensions = _adjacent_dimensions(evaluation.selections, uncertain)
    scores = [evaluation.score]
    for values in product(*(dimension[2] for dimension in dimensions)):
        selections = evaluation.selections.model_copy(deep=True)
        for (group, field, _), value in zip(dimensions, values):
            selection = getattr(selections, group)
            setattr(selection, field, value)
        scores.append(compute_score(selections))

    lowest = min(scores, key=lambda item: item.total_points)
    highest = max(scores, key=lambda item: item.total_points)
    return EvaluationRangeResponse(
        base_points=evaluation.score.total_points,
        base_grade=evaluation.score.grade,
        min_points=lowest.total_points,
        min_grade=lowest.grade,
        max_points=highest.total_points,
        max_grade=highest.grade,
        uncertain_groups=sorted(uncertain),
        scenarios_checked=len(scores),
    )


@router.post("/{evaluation_id}/finalize", response_model=Evaluation)
def finalize_evaluation(
    evaluation_id: str,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> Evaluation:
    """Согласованный результат сверки нескольких независимых оценок одной
    должности (раздел 9.5 / UX «консенсус экспертов»). Финальная — не более
    одной версии на должность одновременно: помечая эту, снимаем флаг с
    остальных версий той же должности."""
    evaluation = store.get_evaluation(evaluation_id, ctx.company_id)
    if not evaluation:
        raise HTTPException(404, "Оценка не найдена")
    if not evaluation.position_id:
        raise HTTPException(400, "У оценки нет привязанной должности")

    for other in store.list_evaluations(evaluation.position_id, ctx.company_id):
        if other.id != evaluation.id and other.is_final:
            other.is_final = False
            store.save_evaluation(other, ctx.company_id)

    evaluation.is_final = True
    result = store.save_evaluation(evaluation, ctx.company_id)
    store.record_audit(
        ctx.company_id, ctx.user_id, "evaluation.finalize", "evaluation", evaluation.id,
        {"position_id": evaluation.position_id},
    )
    return _with_author_name(result, store)


class FactorOverrideRequest(BaseModel):
    """Точечная правка одного подфактора в уже сохранённой оценке — без
    повторного вызова агента и без потери обоснования по остальным факторам."""

    factor_group: FactorGroupName
    field: str
    value: Union[str, int]
    reason: str = Field(min_length=1, description="Почему эксперт корректирует уровень вручную")


@router.patch("/{evaluation_id}", response_model=Evaluation)
def patch_evaluation_factor(
    evaluation_id: str,
    req: FactorOverrideRequest,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> Evaluation:
    """Скорректировать один подфактор существующей оценки и пересчитать
    score/qc_flags/status/confidence через те же детерминированные
    compute_score()/run_qc(), что и полный цикл оценки — без LLM."""
    evaluation = store.get_evaluation(evaluation_id, ctx.company_id)
    if not evaluation:
        raise HTTPException(404, "Оценка не найдена")
    if evaluation.selections is None:
        raise HTTPException(400, "У этой оценки нет уровней факторов — нечего корректировать")

    allowed_fields = _OVERRIDABLE_FIELDS[req.factor_group]
    if req.field not in allowed_fields:
        raise HTTPException(
            400,
            f"Поле '{req.field}' не относится к '{req.factor_group}'. "
            f"Допустимые поля: {sorted(allowed_fields)}",
        )

    pos = store.get_position(evaluation.position_id, ctx.company_id) if evaluation.position_id else None
    if not pos:
        raise HTTPException(404, "Должность для этой оценки не найдена")

    actor = store.get_user(ctx.user_id) if ctx.user_id else None
    actor_name = actor.display_name if actor else "неизвестный эксперт"

    selections = evaluation.selections.model_copy(deep=True)
    current_selection = getattr(selections, req.factor_group)
    selection_data = current_selection.model_dump(mode="json")
    selection_data[req.field] = req.value
    selection_data["evidence"] = [
        *selection_data.get("evidence", []),
        f"[Скорректировано экспертом {actor_name}]: {req.reason}",
    ]
    try:
        new_selection = _SELECTION_MODEL_BY_GROUP[req.factor_group].model_validate(selection_data)
    except ValidationError as exc:
        raise HTTPException(400, f"Недопустимое значение '{req.value}' для '{req.field}': {exc}") from exc
    setattr(selections, req.factor_group, new_selection)

    score = compute_score(selections)
    agent_text = f"{evaluation.role_summary} {evaluation.reasoning}"
    peers = _collect_peers(store, exclude_id=pos.id, company_id=ctx.company_id)
    flags = run_qc(pos, selections, score, agent_text=agent_text)
    flags += run_hierarchy_qc(pos, selections, score, peers)
    has_fail = has_blocking_failures(flags)
    has_warn = any(f.status.value == "warn" for f in flags)
    status = decide_status(evaluation.gate.status, flags)

    evaluation.selections = selections
    evaluation.score = score
    evaluation.qc_flags = flags
    evaluation.status = status
    evaluation.confidence = _downgrade(evaluation.confidence, has_warn, has_fail)
    evaluation.recommendation = _committee_recommendation(status, score, flags)

    result = store.save_evaluation(evaluation, ctx.company_id)
    store.record_audit(
        ctx.company_id, ctx.user_id, "evaluation.patch_factor", "evaluation", evaluation.id,
        {"factor_group": req.factor_group, "field": req.field},
    )
    return _with_author_name(result, store)


_GROUP_GATE_MARKERS: dict[FactorGroupName, tuple[str, ...]] = {
    "know_how": ("Цель должности", "Описание функций", "Оргконтекст"),
    "problem_solving": ("Типовые кейсы", "Описание функций", "Оргконтекст"),
    "accountability": ("Полномочия", "Масштаб воздействия", "KPI", "Лимиты"),
}


def _uncertain_factor_groups(evaluation: Evaluation) -> set[FactorGroupName]:
    groups: set[FactorGroupName] = set()
    if evaluation.selections is None:
        return groups
    for group in ("know_how", "problem_solving", "accountability"):
        selection = getattr(evaluation.selections, group)
        if selection.confidence.value != "high" or selection.doubts:
            groups.add(group)
    for flag in evaluation.qc_flags:
        if flag.status.value == "pass":
            continue
        groups.update(group for group in flag.factor_groups if group in _SELECTION_MODEL_BY_GROUP)
    for check in evaluation.gate.checks:
        if check.status.value == "pass":
            continue
        for group, markers in _GROUP_GATE_MARKERS.items():
            if any(marker in check.block for marker in markers):
                groups.add(group)
    return groups


def _neighbors(current, ordered: list) -> list:
    index = ordered.index(current)
    start = max(0, index - 1)
    end = min(len(ordered), index + 2)
    return ordered[start:end]


def _adjacent_dimensions(
    selections: FactorSelections,
    uncertain: set[FactorGroupName],
) -> list[tuple[FactorGroupName, str, list]]:
    dimensions: list[tuple[FactorGroupName, str, list]] = []
    if "know_how" in uncertain:
        dimensions.extend((
            ("know_how", "specialization", _neighbors(selections.know_how.specialization, list(SpecializedKnowHow))),
            ("know_how", "management", _neighbors(selections.know_how.management, list(ManagerialKnowHow))),
            ("know_how", "communication", _neighbors(selections.know_how.communication, list(Communication))),
        ))
    if "problem_solving" in uncertain:
        dimensions.extend((
            ("problem_solving", "area", _neighbors(selections.problem_solving.area, list(ProblemArea))),
            ("problem_solving", "complexity", _neighbors(selections.problem_solving.complexity, list(ProblemComplexity))),
        ))
    if "accountability" in uncertain:
        dimensions.append((
            "accountability", "freedom",
            _neighbors(selections.accountability.freedom, list(FreedomToAct)),
        ))
        if selections.accountability.non_quantitative_impact is not None:
            dimensions.append((
                "accountability", "non_quantitative_impact",
                _neighbors(
                    selections.accountability.non_quantitative_impact,
                    list(NonQuantitativeImpact),
                ),
            ))
        elif selections.accountability.impact is not None:
            dimensions.append((
                "accountability", "impact",
                _neighbors(selections.accountability.impact, list(ImpactType)),
            ))
    return dimensions


def _with_author_name(evaluation: Evaluation, store: Store) -> Evaluation:
    """Подставляет имя автора версии в ответ API, не трогая хранение (см.
    Evaluation.created_by_name) — резолвится из created_by_user_id на каждый
    запрос, чтобы переименование пользователя не требовало пересчёта истории."""
    if evaluation.created_by_user_id:
        user = store.get_user(evaluation.created_by_user_id)
        evaluation.created_by_name = user.display_name if user else None
    return evaluation


def _collect_peers(store: Store, exclude_id: Optional[str], company_id: Optional[str] = None) -> list[tuple[JobDossier, Evaluation]]:
    peers: list[tuple[JobDossier, Evaluation]] = []
    for position in store.list_positions(company_id):
        if not position.id or position.id == exclude_id:
            continue
        evaluations = store.list_evaluations(position.id, company_id)
        if evaluations:
            peers.append((position, max(evaluations, key=lambda item: item.created_at)))
    return peers
