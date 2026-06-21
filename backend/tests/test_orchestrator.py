"""Тесты оркестратора (с фейковым агентом, без сети)."""

import pytest

from jeval.domain.enums import Confidence, EvaluationStatus
from jeval.domain.models import JobDossier
from jeval.orchestrator import JobEvaluator, _downgrade


def test_full_flow_produces_score_and_is_ready(full_dossier, fake_agent):
    """С чистыми фикстурами Gate 0 проходит без замечаний и QC не даёт FAIL —
    ветка детерминированно READY (anchors_not_in_system — единственный флаг,
    он WARN, а не FAIL, и не входит в gate.warnings)."""
    ev = JobEvaluator(agent=fake_agent).evaluate(full_dossier)
    assert ev.status == EvaluationStatus.READY
    assert ev.score is not None
    assert ev.score.total_points == (
        ev.score.know_how.points
        + ev.score.problem_solving.points
        + ev.score.accountability.points
    )
    assert 0 <= ev.score.grade <= 38
    assert ev.selections is not None


def test_qc_failure_forces_needs_clarification(full_dossier, fake_agent):
    """person_not_role FAIL (раздел 9.2) переводит готовый Gate 0 в NEEDS_CLARIFICATION."""
    full_dossier.purpose = (
        "Незаменимый сотрудник с большим стажем, выполняет работу лучше других."
    )
    ev = JobEvaluator(agent=fake_agent).evaluate(full_dossier)
    assert ev.status == EvaluationStatus.NEEDS_CLARIFICATION
    fail_flags = [f for f in ev.qc_flags if f.status.value == "fail"]
    assert any(f.code == "person_not_role" for f in fail_flags)
    assert "Не утверждать до закрытия" in ev.recommendation
    assert str(len(fail_flags) + sum(1 for f in ev.qc_flags if f.status.value == "warn")) in ev.recommendation


def test_gate_fail_skips_agent(fake_agent):
    ev = JobEvaluator(agent=fake_agent).evaluate(JobDossier(name="Пустая"))
    assert ev.status == EvaluationStatus.CANNOT_EVALUATE
    assert ev.score is None
    assert ev.selections is None
    assert ev.clarifying_questions  # есть что запросить


# ── _downgrade(): понижение уверенности при QC-замечаниях ────────────────────


def test_downgrade_has_fail_forces_low():
    assert _downgrade(Confidence.HIGH, has_warn=True, has_fail=True) == Confidence.LOW
    assert _downgrade(Confidence.MEDIUM, has_warn=False, has_fail=True) == Confidence.LOW


def test_downgrade_warn_on_high_drops_to_medium():
    assert _downgrade(Confidence.HIGH, has_warn=True, has_fail=False) == Confidence.MEDIUM


@pytest.mark.parametrize("confidence", [Confidence.HIGH, Confidence.MEDIUM, Confidence.LOW])
def test_downgrade_clean_leaves_confidence_unchanged(confidence):
    assert _downgrade(confidence, has_warn=False, has_fail=False) == confidence
