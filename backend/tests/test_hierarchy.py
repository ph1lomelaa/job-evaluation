"""Тесты проверки иерархии (раздел 9.5) и новых QC-флагов."""

from __future__ import annotations

from jeval.domain.enums import (
    EvaluationStatus,
    Magnitude,
    ImpactType,
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


def test_expected_magnitude_is_disabled_without_verified_kzt_matrix():
    assert expected_magnitude(None) is None
    assert expected_magnitude(50_000_000) is None
    assert expected_magnitude(50_000_000_000) is None


def test_qc_magnitude_without_annual_figure(full_dossier, sample_output):
    sample_output.selections.accountability.magnitude = Magnitude.THREE
    sample_output.selections.accountability.impact = ImpactType.C
    full_dossier.scope.annual_opex = None  # численность остаётся, денег нет
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    f = _flag(flags, "magnitude_annual_figure")
    assert f is not None and f.status == QCStatus.WARN


def test_qc_magnitude_requires_amount_source(full_dossier, sample_output):
    sample_output.selections.accountability.magnitude = Magnitude.THREE
    sample_output.selections.accountability.impact = ImpactType.C
    full_dossier.scope.source = None
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    f = _flag(flags, "magnitude_annual_figure")
    assert f is not None and f.status == QCStatus.WARN


def test_qc_support_function_company_scale(full_dossier, sample_output):
    full_dossier.function = "HR / кадровая политика"
    sample_output.selections.accountability.magnitude = Magnitude.FOUR
    sample_output.selections.accountability.impact = ImpactType.C
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
        full_dossier, sample_output.selections, score, [(manager, mgr_eval)]
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
        full_dossier, sample_output.selections, score, [(manager, mgr_eval)]
    )
    f = _flag(flags, "subordinate_not_above_manager")
    assert f is not None and f.status == QCStatus.PASS


def test_specialized_knowledge_above_manager_is_not_blocking(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    mgr_selections = sample_output.selections.model_copy(deep=True)
    mgr_selections.know_how.specialization = type(
        mgr_selections.know_how.specialization
    ).D
    manager = JobDossier(id="mgr-1", name="Директор по производству")
    mgr_eval = _evaluation_for(mgr_selections, compute_score(mgr_selections))
    flags = run_hierarchy_qc(
        full_dossier, sample_output.selections, score, [(manager, mgr_eval)]
    )
    f = _flag(flags, "hierarchy_sensitive_factors")
    assert f is not None and f.status == QCStatus.PASS


def test_anchor_grade_gap_and_calibration(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    anchor = JobDossier(id="a-1", name="Главный инженер")
    anchor_score = score.model_copy(
        update={"grade": score.grade + 4, "total_points": score.total_points * 2}
    )
    anchor_eval = _evaluation_for(sample_output.selections, anchor_score)
    flags = run_hierarchy_qc(
        full_dossier, sample_output.selections, score, [(anchor, anchor_eval)]
    )
    assert _flag(flags, "anchor_grade_gap") is not None
    calibration = _flag(flags, "anchor_calibration")
    assert calibration is not None and calibration.status == QCStatus.PASS


def test_anchor_grade_gap_not_flagged_for_compensating_factor_shifts(full_dossier, sample_output):
    """ФАЗА 6: backend-контракт, который теперь зеркалит ComparisonPage.tsx
    (buildComparison/steps15pct) — компенсирующие сдвиги по факторам (+30
    Know-How / −30 Accountability) с тем же total_points не считаются разрывом,
    потому что anchor_grade_gap смотрит только на total_points, а не на факторы
    по отдельности."""
    score = compute_score(sample_output.selections)
    anchor_score = score.model_copy(
        update={
            "know_how": score.know_how.model_copy(update={"points": score.know_how.points + 30}),
            "accountability": score.accountability.model_copy(
                update={"points": score.accountability.points - 30}
            ),
        }
    )
    assert anchor_score.total_points == score.total_points

    anchor = JobDossier(id="a-2", name="Иной профиль, тот же total")
    anchor_eval = _evaluation_for(sample_output.selections, anchor_score)
    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score, [(anchor, anchor_eval)])
    assert _flag(flags, "anchor_grade_gap") is None


def test_anchors_not_in_system_warns(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    flags = run_hierarchy_qc(full_dossier, sample_output.selections, score, [])
    f = _flag(flags, "anchors_not_in_system")
    assert f is not None and f.status == QCStatus.WARN
