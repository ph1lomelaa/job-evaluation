"""Справочные эндпоинты: детерминированный расчёт по таблицам Hay, шкала грейдов."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ...domain.models import FactorSelections, ScoreResult
from ...reference import factor_level_reference
from ...scoring import compute_score
from ...scoring.grades import GRADE_MATRIX
from ..deps import WorkspaceContext, workspace_context

router = APIRouter(prefix="/api/reference", tags=["reference"])


@router.post("/calculate", response_model=ScoreResult)
def calculate_hay_score(
    selections: FactorSelections,
    _: WorkspaceContext = Depends(workspace_context),
) -> ScoreResult:
    """Детерминированный расчёт по функциям COMP/IC/PTSIC/FINALITE из XLSM."""
    return compute_score(selections)


@router.get("/grades")
def grade_reference() -> list[dict[str, int]]:
    return [
        {"grade": band.grade, "lower": band.lower, "mid": band.mid, "upper": band.upper}
        for band in GRADE_MATRIX
    ]


@router.get("/levels")
def levels_reference() -> dict[str, dict[str, str]]:
    """Описания уровней подфакторов — единый источник для UI и промпта агента."""
    return factor_level_reference()
