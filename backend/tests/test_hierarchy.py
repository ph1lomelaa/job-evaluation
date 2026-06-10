"""Тесты проверки иерархии (раздел 9.5) и новых QC-флагов."""

from __future__ import annotations

from jeval.domain.enums import (
    EvaluationStatus,
    Magnitude,
    ManagerialKnowHow,
    QCStatus,
)
from jeval.domain.models import Evaluation, GateResult, JobDossier
from jeval.hierarchy import run_hierarchy_qc
from jeval.qc import run_qc
from jeval.scoring import compute_score, expected_magnitude, long_profile
from jeval.scoring.engine import PROFILE_MAX_STEPS


def _evaluation_for(selections, score) -> Evaluation:
    return Evaluation(
        status=EvaluationStatus.READY,
        gate=GateResult(status=EvaluationStatus.READY),
        selections=selections,
        score=score,
    )


def _flag(flags, code):
    return next((f for f in flags if f.code == code), None)


# ── Magnitude: диапазоны и QC ─────────────────────────────────────────────────


def test_expected_magnitude_bands():
    assert expected_magnitude(None) is None
    assert expected_magnitude(50_000_000) == "1"
    assert expected_magnitude(500_000_000) == "2"
    assert expected_magnitude(4_000_000_000) == "3"
    assert expected_magnitude(50_000_000_000) == "4"


def test_qc_magnitude_without_annual_figure(full_dossier, sample_output):
    full_dossier.scope.annual_opex = None  # численность остаётся, денег нет
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    f = _flag(flags, "magnitude_annual_figure")
    assert f is not None and f.status == QCStatus.WARN


def test_qc_magnitude_mismatch_with_scope(full_dossier, sample_output):
    sample_output.selections.accountability.magnitude = Magnitude.ONE  # OPEX 4 млрд → ждём 3
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    f = _flag(flags, "magnitude_scope_mismatch")
    assert f is not None and f.status == QCStatus.WARN


def test_qc_support_function_company_scale(full_dossier, sample_output):
    full_dossier.function = "HR / кадровая политика"
    sample_output.selections.accountability.magnitude = Magnitude.FOUR
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    f = _flag(flags, "support_function_company_scale")
    assert f is not None and f.status == QCStatus.WARN


def test_qc_neutral_summary_epithets(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    flags = run_qc(
        full_dossier, sample_output.selections, score,
        agent_text="Это стратегическая роль с высокой ответственностью.",
    )
    f = _flag(flags, "neutral_summary")
    assert f is not None and f.status == QCStatus.WARN


# ── Длинный профиль ───────────────────────────────────────────────────────────


def test_long_profile_continuum():
    from jeval.domain.enums import Profile

    assert long_profile(Profile.L, 0) == "L"
    assert long_profile(Profile.A, 2) == "A2"
    assert long_profile(Profile.P, PROFILE_MAX_STEPS) == f"P{PROFILE_MAX_STEPS}"
    assert long_profile(Profile.A, PROFILE_MAX_STEPS + 2) == f"A{PROFILE_MAX_STEPS}*"


def test_compute_score_sets_long_profile(sample_output):
    score = compute_score(sample_output.selections)
    assert score.profile_long.startswith(score.profile.value) or score.profile_long == "L"


# ── Иерархия 9.5 ──────────────────────────────────────────────────────────────


def test_subordinate_not_above_manager(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    # Руководитель оценён с управленческим уровнем III — как у подчинённого.
    manager = JobDossier(id="mgr-1", name="Директор по производству")
    mgr_eval = _evaluation_for(sample_output.selections, score)
    flags = run_hierarchy_qc(
        full_dossier, sample_output.selections, score.grade, [(manager, mgr_eval)]
    )
    f = _flag(flags, "subordinate_not_above_manager")
    assert f is not None and f.status == QCStatus.WARN


def test_subordinate_below_manager_passes(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    mgr_selections = sample_output.selections.model_copy(deep=True)
    mgr_selections.know_how.management = ManagerialKnowHow.IV
    manager = JobDossier(id="mgr-1", name="Директор по производству")
    mgr_eval = _evaluation_for(mgr_selections, compute_score(mgr_selections))
    flags = run_hierarchy_qc(
        full_dossier, sample_output.selections, score.grade, [(manager, mgr_eval)]
    )
    f = _flag(flags, "subordinate_not_above_manager")
    assert f is not None and f.status == QCStatus.PASS


def test_anchor_grade_gap_and_calibration(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    anchor = JobDossier(id="a-1", name="Главный инженер")
    anchor_score = score.model_copy(update={"grade": score.grade + 4})
    anchor_eval = _evaluation_for(sample_output.selections, anchor_score)
    flags = run_hierarchy_qc(
        full_dossier, sample_output.selections, score.grade, [(anchor, anchor_eval)]
    )
    assert _flag(flags, "anchor_grade_gap") is not None
    calibration = _flag(flags, "anchor_calibration")
    assert calibration is not None and calibration.status == QCStatus.PASS


def test_anchors_not_in_system_warns(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score.grade, [])
    f = _flag(flags, "anchors_not_in_system")
    assert f is not None and f.status == QCStatus.WARN
