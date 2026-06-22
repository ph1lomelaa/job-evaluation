"""ФАЗА 2: версионирование таблиц Hay (table_version) — реестр, движок, иерархия."""

from __future__ import annotations

import pytest

from jeval.domain.enums import EvaluationStatus
from jeval.domain.models import Evaluation, GateResult, JobDossier
from jeval.hierarchy import run_hierarchy_qc
from jeval.scoring import compute_score, tables
from jeval.scoring.versions import ACTIVE_TABLE_VERSION, get_table_set


def _evaluation_for(selections, score) -> Evaluation:
    return Evaluation(
        status=EvaluationStatus.READY,
        gate=GateResult(status=EvaluationStatus.READY),
        selections=selections,
        score=score,
    )


def test_get_table_set_unknown_version_raises():
    with pytest.raises(ValueError):
        get_table_set("does-not-exist")


def test_table_functions_accept_explicit_version():
    """know_how_points/problem_solving_points/accountability_points читают таблицы
    по параметру table_version, а не модульной константой напрямую."""
    explicit = tables.know_how_points("H", "T", "1", table_version=ACTIVE_TABLE_VERSION)
    default = tables.know_how_points("H", "T", "1")
    assert explicit == default == 304


def test_table_functions_reject_unknown_version():
    with pytest.raises(ValueError):
        tables.know_how_points("H", "T", "1", table_version="does-not-exist")
    with pytest.raises(ValueError):
        tables.accountability_points("D", "3", impact="C", table_version="does-not-exist")


def test_compute_score_stamps_active_table_version(sample_output):
    score = compute_score(sample_output.selections)
    assert score.table_version == ACTIVE_TABLE_VERSION


def test_methodology_basis_is_not_exposed_in_user_result(sample_output):
    score = compute_score(sample_output.selections)
    assert score.methodology_basis == ""


def test_orchestrator_evaluation_carries_table_version(full_dossier, fake_agent):
    from jeval.orchestrator import JobEvaluator

    evaluation = JobEvaluator(agent=fake_agent).evaluate(full_dossier)
    assert evaluation.table_version == ACTIVE_TABLE_VERSION
    assert evaluation.score is not None
    assert evaluation.table_version == evaluation.score.table_version


def test_orchestrator_cannot_evaluate_still_stamps_table_version(fake_agent):
    from jeval.orchestrator import JobEvaluator

    bare_dossier = JobDossier(name="Должность без досье")
    evaluation = JobEvaluator(agent=fake_agent).evaluate(bare_dossier)
    assert evaluation.status == EvaluationStatus.CANNOT_EVALUATE
    assert evaluation.table_version == ACTIVE_TABLE_VERSION


def test_hierarchy_flags_table_version_mismatch_with_manager(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    mismatched_score = score.model_copy(update={"table_version": "some-other-version"})
    manager = JobDossier(id="mgr-1", name="Директор по производству")
    mgr_eval = _evaluation_for(sample_output.selections, mismatched_score)

    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score, [(manager, mgr_eval)])

    f = next((x for x in flags if x.code == "table_version_mismatch"), None)
    assert f is not None
    assert f.status.value == "warn"
    assert score.table_version in f.message
    assert "some-other-version" in f.message


def test_hierarchy_no_mismatch_flag_when_versions_match(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    manager = JobDossier(id="mgr-1", name="Директор по производству")
    mgr_eval = _evaluation_for(sample_output.selections, score)

    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score, [(manager, mgr_eval)])

    assert all(f.code != "table_version_mismatch" for f in flags)


def test_hierarchy_flags_table_version_mismatch_with_anchor(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    anchor_score = score.model_copy(
        update={"table_version": "some-other-version", "grade": score.grade + 4}
    )
    anchor = JobDossier(id="a-1", name="Главный инженер")
    anchor_eval = _evaluation_for(sample_output.selections, anchor_score)

    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score, [(anchor, anchor_eval)])

    f = next((x for x in flags if x.code == "table_version_mismatch"), None)
    assert f is not None
    assert f.status.value == "warn"
