"""Тесты HTTP-слоя через FastAPI TestClient (in-memory store + фейковый агент)."""

from io import BytesIO
from zipfile import ZipFile

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from jeval.api.main import create_app  # noqa: E402
from jeval.orchestrator import JobEvaluator  # noqa: E402
from jeval.store import InMemoryStore  # noqa: E402


@pytest.fixture
def client(fake_agent):
    app = create_app(store=InMemoryStore(), evaluator=JobEvaluator(agent=fake_agent))
    return TestClient(app)


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_reference_calculator(client):
    response = client.post(
        "/api/reference/calculate",
        json={
            "know_how": {"specialization": "E", "management": "II", "communication": "2"},
            "problem_solving": {"area": "E", "complexity": 3},
            "accountability": {"freedom": "E", "magnitude": "3", "impact": "C"},
        },
    )
    assert response.status_code == 200
    score = response.json()
    assert score["know_how"]["points"] == 264
    assert score["problem_solving"]["points"] == 87
    assert score["accountability"]["points"] == 152
    assert score["total_points"] == 503
    assert score["grade"] == 17
    assert score["profile_long"] == "A4"


def test_level_rules_reference_keys_match_levels_reference(client):
    """UX P0.3: калибровочные правила должны быть доступны для тех же
    подфакторов, что и сами описания уровней — иначе фронт не сможет
    сопоставить правило с нужным факторным блоком."""
    levels = client.get("/api/reference/levels")
    rules = client.get("/api/reference/level-rules")
    assert levels.status_code == 200
    assert rules.status_code == 200
    assert set(levels.json().keys()) == set(rules.json().keys())
    assert all(isinstance(v, list) for v in rules.json().values())
    assert rules.json()["managerial_know_how"]  # непустой список правил


def test_create_list_get_position(client, full_dossier):
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    created = client.post("/api/positions", json=body).json()
    assert created["id"]
    assert any(p["id"] == created["id"] for p in client.get("/api/positions").json())
    assert client.get(f"/api/positions/{created['id']}").json()["name"] == full_dossier.name


def test_gate_and_evaluation_flow(client, full_dossier):
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]

    gate = client.post(f"/api/positions/{pid}/gate").json()
    assert gate["status"] in {"ready", "needs_clarification"}

    ev = client.post("/api/evaluations", json={"position_id": pid}).json()
    assert ev["score"]["grade"] >= 0
    assert client.get(f"/api/evaluations/{ev['id']}").json()["id"] == ev["id"]


def test_evaluation_unknown_position_404(client):
    assert client.post("/api/evaluations", json={"position_id": "nope"}).status_code == 404


def test_upload_document_appends_to_dossier(client, full_dossier, tmp_path, monkeypatch):
    from jeval import config

    monkeypatch.setattr(config.get_settings(), "jeval_upload_dir", str(tmp_path))
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]

    resp = client.post(
        f"/api/positions/{pid}/documents",
        files={"file": ("ДИ.pdf", b"%PDF-1.4 test", "application/pdf")},
    )
    assert resp.status_code == 200
    assert "ДИ.pdf" in resp.json()["documents"]
    assert (tmp_path / pid / "ДИ.pdf").read_bytes() == b"%PDF-1.4 test"


def test_import_docx_creates_draft_position(client, tmp_path, monkeypatch):
    from jeval import config

    monkeypatch.setattr(config.get_settings(), "jeval_upload_dir", str(tmp_path))
    data = _minimal_docx(
        "Описание должности",
        "Общая информация",
        "Название Компании : | АО Тест",
        "Название должности : | Директор департамента",
        "Подчиняется : | Генеральному директору",
        "Цель существования должности",
        "Руководит контуром бурения.",
    )

    resp = client.post(
        "/api/import/document?use_ai=false",
        files={
            "file": (
                "sample.docx",
                data,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert resp.status_code == 201
    body = resp.json()
    position = body["position"]
    assert position["id"]
    assert position["review_status"] == "draft_imported"
    assert position["name"] == "Директор департамента"
    assert "sample.docx" in position["documents"]
    assert "responsibilities" in body["missing_fields"]
    assert position["import_metadata"]["source_filename"] == "sample.docx"
    assert position["import_metadata"]["source_size_bytes"] == len(data)
    assert position["import_metadata"]["source_sha256"]
    assert position["import_metadata"]["field_sources"]["name"]
    assert client.get(f"/api/positions/{position['id']}").json()["id"] == position["id"]
    assert (tmp_path / position["id"] / "sample.docx").exists()


def test_list_evaluations_filtered_by_position(client, full_dossier):
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]

    assert client.get("/api/evaluations").json() == []
    ev = client.post("/api/evaluations", json={"position_id": pid}).json()

    all_evs = client.get("/api/evaluations").json()
    assert [e["id"] for e in all_evs] == [ev["id"]]
    assert client.get(f"/api/evaluations?position_id={pid}").json()[0]["id"] == ev["id"]
    assert client.get("/api/evaluations?position_id=other").json() == []


def test_public_form_creates_one_position_and_notification(client, full_dossier):
    created = client.post(
        "/api/public-forms",
        json={"title": "Описание новой роли", "recipient": "Иван", "expires_in_days": 3},
    )
    assert created.status_code == 201
    form = created.json()

    public = client.get(f"/api/public/forms/{form['token']}")
    assert public.status_code == 200
    assert public.json()["title"] == "Описание новой роли"

    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    submitted = client.post(f"/api/public/forms/{form['token']}", json=body)
    assert submitted.status_code == 201
    result = submitted.json()
    assert result["status"] == "submitted"
    assert result["position_id"]
    assert result["is_read"] is False
    assert client.get(f"/api/positions/{result['position_id']}").status_code == 200
    assert client.post(f"/api/public/forms/{form['token']}", json=body).status_code == 409

    read = client.post(f"/api/public-forms/{form['id']}/read")
    assert read.json()["is_read"] is True


def _minimal_docx(*paragraphs: str) -> bytes:
    body = "".join(f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>" for p in paragraphs)
    data = BytesIO()
    with ZipFile(data, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{body}</w:body>
</w:document>""",
        )
    return data.getvalue()
