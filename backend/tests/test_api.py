"""Тесты HTTP-слоя через FastAPI TestClient (in-memory store + фейковый агент)."""

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
