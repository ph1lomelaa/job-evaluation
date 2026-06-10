"""Оркестратор: связывает все шаги в одну предварительную оценку.

    JE-досье → Gate 0 → агент (уровни) → движок (баллы/грейд) → QC → карточка.

Если Gate 0 не пройден, агент не вызывается («нет понимания — нет оценки»).
"""

from __future__ import annotations

from typing import Optional, Protocol

from .agent import AgentOutput, EvaluationAgent
from .domain.enums import Confidence, EvaluationStatus, QCStatus
from .domain.models import Evaluation, JobDossier
from .gate import evaluate_gate
from .hierarchy import run_hierarchy_qc
from .qc import has_blocking_failures, run_qc
from .scoring import compute_score


class _AgentLike(Protocol):
    def select_factors(self, dossier: JobDossier) -> AgentOutput: ...


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
            )

        # Агент выбирает уровни факторов.
        out = self._agent.select_factors(dossier)

        # Детерминированный расчёт.
        score = compute_score(out.selections)

        # Контроль качества (раздел 9) + проверка иерархии (раздел 9.5).
        agent_text = f"{out.role_summary} {out.reasoning}"
        flags = run_qc(dossier, out.selections, score, agent_text=agent_text)
        flags += run_hierarchy_qc(dossier, out.selections, score.grade, peers or [])
        has_fail = has_blocking_failures(flags)
        has_warn = any(f.status == QCStatus.WARN for f in flags)

        if has_fail or gate.status == EvaluationStatus.NEEDS_CLARIFICATION:
            status = EvaluationStatus.NEEDS_CLARIFICATION
        else:
            status = EvaluationStatus.READY

        recommendation = out.recommendation or _default_recommendation(status, has_fail)

        return Evaluation(
            position_id=dossier.id,
            status=status,
            gate=gate,
            selections=out.selections,
            score=score,
            qc_flags=flags,
            confidence=_downgrade(out.overall_confidence, has_warn, has_fail),
            role_summary=out.role_summary,
            reasoning=out.reasoning,
            clarifying_questions=out.clarifying_questions,
            recommendation=recommendation,
        )


def _default_recommendation(status: EvaluationStatus, has_fail: bool) -> str:
    if has_fail:
        return "Вынести спорный фактор отдельно и уточнить данные перед комитетом."
    if status == EvaluationStatus.NEEDS_CLARIFICATION:
        return "Провести интервью с руководителем / калибровку с якорными должностями."
    return "Рассмотреть на Оценочном комитете."
