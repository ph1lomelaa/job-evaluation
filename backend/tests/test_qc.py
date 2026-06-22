"""Тесты движка QC-флагов."""

from jeval.domain.enums import (
    Communication,
    FreedomToAct,
    ImpactType,
    Magnitude,
    ManagerialKnowHow,
    ProblemArea,
    ProblemComplexity,
    QCStatus,
    SpecializedKnowHow,
)
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


def test_authorities_assumed_template_fails(full_dossier, sample_output):
    """UX: шаблон полномочий по умолчанию (jeval/importer/authorities.py) не
    может пройти как подтверждённый факт — должен форсировать needs_clarification."""
    from jeval.qc import AUTHORITY_ASSUMPTION_MARKER

    full_dossier.authorities.decides_alone = [f"{AUTHORITY_ASSUMPTION_MARKER} тестовый текст"]
    full_dossier.authorities.requires_approval = []
    full_dossier.authorities.recommends = []
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    flag = _flag(flags, "authorities_assumed")
    assert flag.status == QCStatus.FAIL
    assert flag.factor_groups == ["accountability"]


def test_authorities_from_document_passes(full_dossier, sample_output):
    """full_dossier фикстуры — реальные (не шаблонные) полномочия → PASS."""
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "authorities_assumed").status == QCStatus.PASS


def test_missing_authorities_fails_but_allows_preliminary_score(full_dossier, sample_output):
    full_dossier.authorities.decides_alone = []
    full_dossier.authorities.requires_approval = []
    full_dossier.authorities.recommends = []
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    flag = _flag(flags, "authorities_assumed")
    assert flag.status == QCStatus.FAIL
    assert "рассчитана предварительно" in flag.message


def test_impact_s_without_documented_joint_result_warns(full_dossier, sample_output):
    sample_output.selections.accountability.impact = ImpactType.S
    full_dossier.kpis = ["Исполнение бюджета ТОиР"]
    sample_output.selections.accountability.evidence = ["Влияет на готовность оборудования"]
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "impact_s_requires_joint_kpi").status == QCStatus.WARN


def test_impact_s_with_joint_result_passes(full_dossier, sample_output):
    sample_output.selections.accountability.impact = ImpactType.S
    full_dossier.kpis = ["Совместный KPI с добычей по готовности оборудования"]
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "impact_s_requires_joint_kpi").status == QCStatus.PASS


# ── WARN-ветки раздела 9.4, ранее не покрытые тестами ────────────────────────


def test_comm3_without_resistance_cases_warns(full_dossier, sample_output):
    sample_output.selections.know_how.communication = Communication.THREE
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "comm3_needs_resistance").status == QCStatus.WARN


def test_low_kh_high_mgmt_warns(full_dossier, sample_output):
    sample_output.selections.know_how.specialization = SpecializedKnowHow.B
    sample_output.selections.know_how.management = ManagerialKnowHow.III
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "low_kh_high_mgmt").status == QCStatus.WARN


def test_easy_area_high_complexity_warns(full_dossier, sample_output):
    sample_output.selections.problem_solving.area = ProblemArea.A
    sample_output.selections.problem_solving.complexity = ProblemComplexity.ADAPTIVE
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "easy_area_high_complexity").status == QCStatus.WARN


def test_high_complexity_few_cases_warns(full_dossier, sample_output):
    sample_output.selections.problem_solving.complexity = ProblemComplexity.ADAPTIVE
    full_dossier.problem_cases = full_dossier.problem_cases[:2]  # < 3 типовых кейсов
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "high_complexity_few_cases").status == QCStatus.WARN


def test_low_freedom_primary_impact_warns(full_dossier, sample_output):
    sample_output.selections.accountability.freedom = FreedomToAct.A
    sample_output.selections.accountability.magnitude = Magnitude.ONE
    sample_output.selections.accountability.impact = ImpactType.P
    sample_output.selections.accountability.non_quantitative_impact = None
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "low_freedom_primary_impact").status == QCStatus.WARN


def test_high_freedom_low_thinking_warns(full_dossier, sample_output):
    sample_output.selections.accountability.freedom = FreedomToAct.G
    sample_output.selections.problem_solving.area = ProblemArea.B
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "high_freedom_low_thinking").status == QCStatus.WARN


def test_profile_out_of_range_warns(full_dossier, sample_output):
    # Огромный разрыв Accountability/Problem Solving: H/4/P против A/1 —
    # больше PROFILE_MAX_STEPS=4 шагов по 15%.
    sample_output.selections.problem_solving.area = ProblemArea.A
    sample_output.selections.problem_solving.complexity = ProblemComplexity.REPETITIVE
    sample_output.selections.accountability.freedom = FreedomToAct.H
    sample_output.selections.accountability.magnitude = Magnitude.FOUR
    sample_output.selections.accountability.impact = ImpactType.P
    sample_output.selections.accountability.non_quantitative_impact = None
    score = compute_score(sample_output.selections)
    assert score.profile_steps > 4
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "profile_out_of_range").status == QCStatus.WARN


# ── factor_groups: UI P1.4 привязывает QC-флаг к нужному факторному блоку ────


def test_flags_carry_factor_groups_for_ui_linking(full_dossier, sample_output):
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert _flag(flags, "accountability_non_quantitative_policy").factor_groups == ["accountability"]
    # Не привязан к конкретному фактору — про резюме роли целиком.
    assert _flag(flags, "person_not_role").factor_groups == []


def test_high_freedom_low_thinking_spans_two_factor_groups(full_dossier, sample_output):
    sample_output.selections.accountability.freedom = FreedomToAct.G
    sample_output.selections.problem_solving.area = ProblemArea.B
    score = compute_score(sample_output.selections)
    flags = run_qc(full_dossier, sample_output.selections, score)
    assert set(_flag(flags, "high_freedom_low_thinking").factor_groups) == {
        "accountability", "problem_solving",
    }
