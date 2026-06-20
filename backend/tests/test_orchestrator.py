"""Тесты оркестратора (с фейковым агентом, без сети)."""

from jeval.domain.enums import EvaluationStatus
from jeval.domain.models import JobDossier
from jeval.orchestrator import JobEvaluator


def test_full_flow_produces_score(full_dossier, fake_agent):
    ev = JobEvaluator(agent=fake_agent).evaluate(full_dossier)
    assert ev.status in {EvaluationStatus.READY, EvaluationStatus.NEEDS_CLARIFICATION}
    assert ev.score is not None
    assert ev.score.total_points == (
        ev.score.know_how.points
        + ev.score.problem_solving.points
        + ev.score.accountability.points
    )
    assert 0 <= ev.score.grade <= 38
    assert ev.selections is not None


def test_gate_fail_skips_agent(fake_agent):
    ev = JobEvaluator(agent=fake_agent).evaluate(JobDossier(name="Пустая"))
    assert ev.status == EvaluationStatus.CANNOT_EVALUATE
    assert ev.score is None
    assert ev.selections is None
    assert ev.clarifying_questions  # есть что запросить
