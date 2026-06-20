"""Запуск и просмотр предварительных оценок Hay."""

from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ...domain.models import Evaluation, JobDossier
from ...orchestrator import JobEvaluator
from ...store import Store
from ..deps import WorkspaceContext, get_evaluator, get_store, workspace_context, write_workspace_context

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


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
    return result


@router.get("", response_model=list[Evaluation])
def list_evaluations(
    position_id: Optional[str] = None,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> list[Evaluation]:
    return store.list_evaluations(position_id, ctx.company_id)


@router.get("/{evaluation_id}", response_model=Evaluation)
def get_evaluation(
    evaluation_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> Evaluation:
    ev = store.get_evaluation(evaluation_id, ctx.company_id)
    if not ev:
        raise HTTPException(404, "Оценка не найдена")
    return ev


def _collect_peers(store: Store, exclude_id: Optional[str], company_id: Optional[str] = None) -> list[tuple[JobDossier, Evaluation]]:
    peers: list[tuple[JobDossier, Evaluation]] = []
    for position in store.list_positions(company_id):
        if not position.id or position.id == exclude_id:
            continue
        evaluations = store.list_evaluations(position.id, company_id)
        if evaluations:
            peers.append((position, max(evaluations, key=lambda item: item.created_at)))
    return peers
