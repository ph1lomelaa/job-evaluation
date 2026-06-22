"""Запуск и просмотр предварительных оценок Hay."""

from __future__ import annotations

import uuid
from typing import Literal, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError

from ...domain.models import (
    AccountabilitySelection,
    Evaluation,
    JobDossier,
    KnowHowSelection,
    ProblemSolvingSelection,
)
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
