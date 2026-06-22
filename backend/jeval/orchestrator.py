"""Оркестратор: связывает все шаги в одну предварительную оценку.

    JE-досье → Gate 0 → агент (уровни) → движок (баллы/грейд) → QC → карточка.

Если Gate 0 не пройден, агент не вызывается («нет понимания — нет оценки»).
"""

from __future__ import annotations

from typing import Optional, Protocol

from .agent import AgentOutput, EvaluationAgent
from .domain.enums import Confidence, EvaluationStatus, QCStatus
from .domain.models import Evaluation, JobDossier, QCFlag
from .gate import evaluate_gate
from .hierarchy import run_hierarchy_qc
from .qc import has_blocking_failures, run_qc
from .scoring import compute_score
from .scoring.versions import ACTIVE_TABLE_VERSION


class _AgentLike(Protocol):
    def select_factors(self, dossier: JobDossier) -> AgentOutput: ...


def decide_status(gate_status: EvaluationStatus, flags: list[QCFlag]) -> EvaluationStatus:
    """FAIL или Gate 0 «нужны уточнения» → NEEDS_CLARIFICATION, иначе READY.

    Единая точка решения — используется и полным циклом оценки
    (``JobEvaluator.evaluate``), и точечной правкой подфактора
    (``api/routers/evaluations.py::patch_evaluation``), чтобы оба пути не
    могли разойтись в трактовке одних и тех же флагов.
    """
    if has_blocking_failures(flags) or gate_status == EvaluationStatus.NEEDS_CLARIFICATION:
        return EvaluationStatus.NEEDS_CLARIFICATION
    return EvaluationStatus.READY


def _downgrade(confidence: Confidence, has_warn: bool, has_fail: bool) -> Confidence:
    """Понизить уверенность при наличии предупреждений/ошибок QC."""
    if has_fail:
        return Confidence.LOW
    if has_warn and confidence == Confidence.HIGH:
        return Confidence.MEDIUM
    return confidence


class JobEvaluator:
    """Главный сценарий предварительной оценки. Агент инъектируется (удобно для тестов)."""

    def __init__(self, agent: Optional[_AgentLike] = None) -> None:
        self._agent = agent or EvaluationAgent()

    def evaluate(
        self,
        dossier: JobDossier,
        peers: Optional[list[tuple[JobDossier, Evaluation]]] = None,
    ) -> Evaluation:
        """Полная предварительная оценка.

        `peers` — другие должности системы с их последними оценками; используются
        для проверки иерархии (раздел 9.5): якоря и руководитель.
        """
        gate = evaluate_gate(dossier)

        # Gate 0 не пройден — оценку не проводим.
        if gate.status == EvaluationStatus.CANNOT_EVALUATE:
            return Evaluation(
                position_id=dossier.id,
                status=EvaluationStatus.CANNOT_EVALUATE,
                gate=gate,
                confidence=Confidence.LOW,
                reasoning="Оценка не может быть завершена: не хватает критических данных.",
                clarifying_questions=[f"Предоставьте: {b}" for b in gate.missing_fields],
                recommendation="Вернуть JE-досье на доработку.",
                table_version=ACTIVE_TABLE_VERSION,
            )

        # Агент выбирает уровни факторов.
        out = self._agent.select_factors(dossier)

        # Детерминированный расчёт.
        score = compute_score(out.selections)

        # Контроль качества (раздел 9) + проверка иерархии (раздел 9.5).
        agent_text = f"{out.role_summary} {out.reasoning}"
        flags = run_qc(dossier, out.selections, score, agent_text=agent_text)
        flags += run_hierarchy_qc(dossier, out.selections, score, peers or [])
        has_fail = has_blocking_failures(flags)
        has_warn = any(f.status == QCStatus.WARN for f in flags)
        status = decide_status(gate.status, flags)
        recommendation = _committee_recommendation(status, score, flags)

        return Evaluation(
            position_id=dossier.id,
            status=status,
            gate=gate,
            selections=out.selections,
            score=score,
            qc_flags=flags,
            confidence=_downgrade(out.overall_confidence, has_warn, has_fail),
            is_test_data=out.is_test_data,
            role_summary=out.role_summary,
            reasoning=out.reasoning,
            clarifying_questions=out.clarifying_questions,
            recommendation=recommendation,
            table_version=score.table_version,
        )


def _committee_recommendation(status, score, flags) -> str:
    """Фактическая рекомендация вместо общей фразы, не помогающей комитету."""
    kh = score.know_how.selection
    ps = score.problem_solving.selection
    acc = score.accountability.selection
    codes = (
        f"Know-How {kh.specialization.value}/{kh.management.value}/{kh.communication.value}, "
        f"Problem Solving {ps.area.value}/{ps.complexity.value}, "
        f"Accountability {acc.freedom.value}/{acc.magnitude.value}/"
        f"{(acc.non_quantitative_impact or acc.impact).value}"
    )
    unresolved = [f for f in flags if f.status in {QCStatus.FAIL, QCStatus.WARN}]
    if status == EvaluationStatus.NEEDS_CLARIFICATION:
        return (
            f"Предварительно зафиксировать {codes}: {score.total_points} баллов, грейд "
            f"{score.grade}, профиль {score.profile_long}. Не утверждать до закрытия "
            f"{len(unresolved)} замечаний QC и калибровки спорных подфакторов."
        )
    return (
        f"Вынести на Оценочный комитет {codes}: {score.total_points} баллов, "
        f"грейд {score.grade}, профиль {score.profile_long}; подтвердить сравнением "
        "с якорными должностями той же семьи."
    )
