from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

from jeval.importer import build_dossier_from_text, extract_docx_text
from jeval.importer.agent import DossierDraftOutput


def _docx_bytes(body_xml: str) -> bytes:
    data = BytesIO()
    with ZipFile(data, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{body_xml}</w:body>
</w:document>""",
        )
    return data.getvalue()


def _p(text: str) -> str:
    return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"


def test_docx_parser_extracts_paragraphs_and_tables():
    raw = _docx_bytes(
        _p("Описание должности")
        + _p("Директор департамента")
        + """
<w:tbl>
  <w:tr>
    <w:tc><w:p><w:r><w:t>Название должности:</w:t></w:r></w:p></w:tc>
    <w:tc><w:p><w:r><w:t>Директор</w:t></w:r></w:p></w:tc>
  </w:tr>
</w:tbl>
"""
    )

    parsed = extract_docx_text(raw)

    assert "Описание должности" in parsed.text
    assert "Название должности: | Директор" in parsed.text
    assert parsed.tables == [[["Название должности:", "Директор"]]]
    assert parsed.blocks[0].kind == "paragraph"
    assert any(block.kind == "table_cell" for block in parsed.blocks)


def test_build_dossier_from_text_does_not_invent_missing_fields():
    parsed = extract_docx_text(
        _docx_bytes(
            _p("Описание должности")
            + _p("Директор департамента")
            + _p("Общая информация")
            + _p("Название Компании : | АО Тест")
            + _p("Название должности : | Директор департамента")
            + _p("Подчиняется : | Генеральному директору")
            + _p("Цель существования должности")
            + _p("Руководит контуром бурения.")
            + _p("Основные области ответственности")
            + _p("1. Контроль выполнения программы.")
        )
    )

    result = build_dossier_from_text(parsed.text, source_filename="sample.docx")

    assert result.position.review_status == "draft_imported"
    assert result.position.name == "Директор департамента"
    assert result.position.dzo == "АО Тест"
    assert result.position.scope.annual_opex is None
    assert result.position.kpis == []
    assert "kpis" in result.missing_fields
    assert "scope" in result.missing_fields


def test_ai_draft_output_tolerates_null_lists_and_wrong_scalar_lists():
    out = DossierDraftOutput.model_validate(
        {
            "name": "Директор",
            "subordinates": 11,
            "project_portfolio": [],
            "assets": [],
            "decides_alone": None,
            "requires_approval": None,
            "recommends": None,
            "limits": None,
            "stakeholders": None,
            "anchor_roles": None,
            "problem_cases": None,
            "documents": None,
            "notes": "Некоторые поля не найдены в документе.",
        }
    )

    assert out.subordinates == []
    assert out.project_portfolio is None
    assert out.assets is None
    assert out.decides_alone == []
    assert out.notes == ["Некоторые поля не найдены в документе."]
