"""Шаблон 'Полномочия' по умолчанию — детерминированный, не LLM (см.
jeval/importer/authorities.py). Должен помечать себя маркером-предположением,
который jeval/qc.py::authorities_assumed обязан находить и заваливать FAIL."""

from jeval.domain.models import Authorities, JobDossier, Reporting
from jeval.importer.authorities import default_authorities_note, infer_default_authorities
from jeval.qc import AUTHORITY_ASSUMPTION_MARKER


def test_infer_default_authorities_requires_manager():
    dossier = JobDossier(name="Без руководителя", reporting=Reporting(manager=None))
    assert infer_default_authorities(dossier) is None


def test_infer_default_authorities_does_not_overwrite_existing():
    dossier = JobDossier(
        name="С полномочиями",
        reporting=Reporting(manager="Директор"),
        authorities=Authorities(decides_alone=["Реальное полномочие из документа"]),
    )
    assert infer_default_authorities(dossier) is None


def test_infer_default_authorities_marks_assumption():
    dossier = JobDossier(name="Начальник цеха", reporting=Reporting(manager="Директор завода"))
    result = infer_default_authorities(dossier)
    assert result is not None
    assert all(AUTHORITY_ASSUMPTION_MARKER in item for item in result.decides_alone)
    assert all(AUTHORITY_ASSUMPTION_MARKER in item.item for item in result.requires_approval)
    assert result.requires_approval[0].approver == "Директор завода"


def test_default_authorities_note_mentions_manager():
    note = default_authorities_note("Директор завода")
    assert AUTHORITY_ASSUMPTION_MARKER in note
    assert "Директор завода" in note
