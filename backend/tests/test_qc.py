"""Тесты движка QC-флагов."""

from jeval.domain.enums import ImpactType, QCStatus
from jeval.qc import run_qc
from jeval.scoring import compute_score


def _flag(flags, code):
    return next(f for f in flags if f.code == code)


def test_clean_case_has_no_failures(full_dossier, sample_output):
    clean_output = sample_output.model_copy(deep=True)
    clean_output.selections.accountability.impact = ImpactType.C
    score = compute_score(clean_output.selections)
    flags = run_qc(full_dossier, clean_output.selections, score)
    assert not any(f.status == QCStatus.FAIL for f in flags)


def test_impact_p_without_resources_fails(full_dossier, sample_output):
    sample_output.selections.accountability.impact = ImpactType.P
    full_dossier.kpis = []          # нет KPI результата
    full_dossier.scope.headcount = None
    full_dossier.scope.annual_opex = None
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "impact_p_requires_kpi_resource").status == QCStatus.FAIL


def test_personalization_detected(full_dossier, sample_output):
    full_dossier.purpose = "Незаменимый сотрудник с большим стажем, фактически делает больше."
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "person_not_role").status == QCStatus.FAIL


def test_pay_argument_detected(full_dossier, sample_output):
    full_dossier.organizational_context = "Нужно поднять грейд, потому что оклад ниже рынка."
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "pay_independence").status == QCStatus.FAIL


def test_impact_s_in_vertical_fails(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "impact_s_requires_joint_kpi").status == QCStatus.FAIL
