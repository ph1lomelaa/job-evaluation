"""Справочные эндпоинты: детерминированный расчёт по таблицам Hay, шкала грейдов."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...domain.models import FactorSelections, QCFlag, ScoreResult
from ...qc import run_qc
from ...reference import factor_level_reference, factor_level_rules
from ...scoring import compute_score
from ...scoring.grades import GRADE_MATRIX
from ..deps import WorkspaceContext, workspace_context

router = APIRouter(prefix="/api/reference", tags=["reference"])


class CalculateResponse(BaseModel):
    score: ScoreResult
    qc_flags: list[QCFlag]


@router.post("/calculate", response_model=CalculateResponse)
def calculate_hay_score(
    selections: FactorSelections,
    _: WorkspaceContext = Depends(workspace_context),
) -> CalculateResponse:
    """Детерминированный расчёт по подстановочным таблицам Hay.

    Калькулятор работает без JE-досье, поэтому ``run_qc`` вызывается с
    ``dossier=None`` — это даёт только те QC-правила, которые проверяют сами
    уровни факторов (несостыковки, профиль вне диапазона, необоснованные
    модификаторы), без правил, которым нужны KPI/масштаб/текст досье.
    """
    score = compute_score(selections)
    qc_flags = run_qc(None, selections, score)
    return CalculateResponse(score=score, qc_flags=qc_flags)


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


@router.get("/level-rules")
def level_rules_reference() -> dict[str, list[str]]:
    """Калибровочные анти-паттерны по подфактору (раздел 9.4) — те же правила,
    что уже идут в промпт агента, теперь доступные и эксперту-рецензенту в UI."""
    return factor_level_rules()
