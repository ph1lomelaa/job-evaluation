"""Тесты Gate 0."""

from jeval.domain.enums import EvaluationStatus
from jeval.domain.models import JobDossier
from jeval.gate import evaluate_gate


def test_full_dossier_ready(full_dossier):
    result = evaluate_gate(full_dossier)
    assert result.status == EvaluationStatus.READY
    assert result.can_evaluate
    assert not result.missing_fields


def test_empty_dossier_cannot_evaluate():
    result = evaluate_gate(JobDossier(name="Без данных"))
    assert result.status == EvaluationStatus.CANNOT_EVALUATE
    assert not result.can_evaluate
    assert "Цель должности" in result.missing_fields
    assert "Масштаб воздействия" in result.missing_fields


def test_missing_recommended_needs_clarification(full_dossier):
    full_dossier.anchor_roles = []
    full_dossier.stakeholders = []
    result = evaluate_gate(full_dossier)
    assert result.status == EvaluationStatus.NEEDS_CLARIFICATION
    assert result.can_evaluate
    assert "Якорные должности" in result.warnings


def test_role_core_with_missing_authorities_is_estimated(full_dossier):
    full_dossier.authorities.decides_alone = []
    full_dossier.authorities.requires_approval = []
    full_dossier.authorities.recommends = []
    result = evaluate_gate(full_dossier)
    assert result.status == EvaluationStatus.NEEDS_CLARIFICATION
    assert result.can_evaluate
    assert "Полномочия (сам/согласует/рекомендует)" in result.missing_fields
