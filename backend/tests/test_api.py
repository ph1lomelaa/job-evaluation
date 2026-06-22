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
    body = response.json()
    score = body["score"]
    assert score["know_how"]["points"] == 264
    assert score["problem_solving"]["points"] == 87
    assert score["accountability"]["points"] == 152
    assert score["total_points"] == 503
    assert score["grade"] == 17
    assert score["profile_long"] == "A4"
    # P2.6: калькулятор без досье всё равно гоняет QC-правила, не зависящие
    # от досье (тут — несостыковка специализации и сложности тоже могла бы
    # быть, но видна именно отсутствующая зависимость от dossier: PASS, не
    # пропущенная проверка).
    codes = {f["code"] for f in body["qc_flags"]}
    assert "accountability_non_quantitative_policy" in codes
    assert "person_not_role" not in codes  # правило, которому нужен dossier — не запускается вовсе


def test_reference_calculator_flags_low_kh_high_mgmt_without_dossier(client):
    response = client.post(
        "/api/reference/calculate",
        json={
            "know_how": {"specialization": "B", "management": "IV", "communication": "2"},
            "problem_solving": {"area": "E", "complexity": 3},
            "accountability": {"freedom": "E", "magnitude": "N", "non_quantitative_impact": "IV"},
        },
    )
    assert response.status_code == 200
    flags = {f["code"]: f for f in response.json()["qc_flags"]}
    assert flags["low_kh_high_mgmt"]["status"] == "warn"
    assert flags["low_kh_high_mgmt"]["factor_groups"] == ["know_how"]


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


def test_finalize_evaluation_unsets_other_versions(client, full_dossier):
    """UX Шаг 4b (вариант A): сверка параллельных независимых оценок одной
    должности — финальная версия одна, остальные снимаются с флага."""
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]

    ev1 = client.post("/api/evaluations", json={"position_id": pid}).json()
    ev2 = client.post("/api/evaluations", json={"position_id": pid}).json()
    assert ev1["id"] != ev2["id"]
    assert ev1["is_final"] is False and ev2["is_final"] is False

    finalized1 = client.post(f"/api/evaluations/{ev1['id']}/finalize")
    assert finalized1.status_code == 200
    assert finalized1.json()["is_final"] is True

    versions = client.get(f"/api/evaluations?position_id={pid}").json()
    by_id = {v["id"]: v for v in versions}
    assert by_id[ev1["id"]]["is_final"] is True
    assert by_id[ev2["id"]]["is_final"] is False

    # Переключение финальности — старая финальная версия теряет флаг.
    finalized2 = client.post(f"/api/evaluations/{ev2['id']}/finalize")
    assert finalized2.status_code == 200
    versions_after = {v["id"]: v for v in client.get(f"/api/evaluations?position_id={pid}").json()}
    assert versions_after[ev1["id"]]["is_final"] is False
    assert versions_after[ev2["id"]]["is_final"] is True


def test_finalize_unknown_evaluation_404(client):
    assert client.post("/api/evaluations/does-not-exist/finalize").status_code == 404


def test_patch_evaluation_factor_recomputes_score_and_qc(client, full_dossier):
    """UX Шаг 6: точечная правка одного подфактора — без повторного вызова
    агента, без потери обоснования по остальным факторам."""
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]
    ev = client.post("/api/evaluations", json={"position_id": pid}).json()
    assert ev["selections"]["know_how"]["specialization"] == "E"
    assert ev["selections"]["know_how"]["management"] == "III"

    patched = client.patch(
        f"/api/evaluations/{ev['id']}",
        json={
            "factor_group": "know_how",
            "field": "specialization",
            "value": "B",
            "reason": "Рецензент: специализация общепрактическая, не профессиональная.",
        },
    )
    assert patched.status_code == 200
    data = patched.json()

    # Золотой оракул: независимый вызов того же движка с теми же входами —
    # тест проверяет интеграцию PATCH, а не таблицы Hay (они уже покрыты
    # отдельными golden-тестами в test_scoring.py).
    from jeval.domain.enums import Communication, ManagerialKnowHow, SpecializedKnowHow
    from jeval.domain.models import FactorSelections, KnowHowSelection
    from jeval.scoring import compute_score

    expected_selections = FactorSelections.model_validate(ev["selections"])
    expected_selections.know_how = KnowHowSelection(
        specialization=SpecializedKnowHow.B,
        management=ManagerialKnowHow.III,
        communication=Communication.TWO,
    )
    expected_score = compute_score(expected_selections)
    assert data["score"]["know_how"]["points"] == expected_score.know_how.points
    assert data["score"]["total_points"] == expected_score.total_points

    # Понижение специализации при сохранении management III/IV — несостыковка.
    flags = {f["code"]: f for f in data["qc_flags"]}
    assert flags["low_kh_high_mgmt"]["status"] == "warn"
    assert data["status"] == "ready"  # WARN не блокирует готовность

    kh_evidence = data["selections"]["know_how"]["evidence"]
    assert any("Скорректировано экспертом" in e for e in kh_evidence)
    assert "Управляет ТОиР" in kh_evidence  # исходное evidence агента не затёрто
    # Обоснование других факторов не тронуто точечной правкой.
    assert data["selections"]["problem_solving"]["evidence"] == ev["selections"]["problem_solving"]["evidence"]

    refetched = client.get(f"/api/evaluations/{ev['id']}").json()
    assert refetched["selections"]["know_how"]["specialization"] == "B"
    assert refetched["score"]["total_points"] == data["score"]["total_points"]


def test_patch_evaluation_rejects_field_outside_factor_group(client, full_dossier):
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]
    ev = client.post("/api/evaluations", json={"position_id": pid}).json()

    response = client.patch(
        f"/api/evaluations/{ev['id']}",
        json={"factor_group": "know_how", "field": "freedom", "value": "E", "reason": "тест"},
    )
    assert response.status_code == 400


def test_patch_evaluation_unknown_id_404(client):
    response = client.patch(
        "/api/evaluations/does-not-exist",
        json={"factor_group": "know_how", "field": "specialization", "value": "B", "reason": "тест"},
    )
    assert response.status_code == 404


def test_patch_evaluation_without_selections_400(client, full_dossier):
    """Gate 0 не пройден -> selections=None -> нечего точечно править."""
    incomplete = full_dossier.model_copy(update={"purpose": None, "key_results": []})
    body = incomplete.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = client.post("/api/positions", json=body).json()["id"]
    ev = client.post("/api/evaluations", json={"position_id": pid}).json()
    assert ev["status"] == "cannot_evaluate"

    response = client.patch(
        f"/api/evaluations/{ev['id']}",
        json={"factor_group": "know_how", "field": "specialization", "value": "B", "reason": "тест"},
    )
    assert response.status_code == 400


def test_evaluation_response_includes_author_name(full_dossier, fake_agent):
    """UX Шаг 4a: created_by_name резолвится из created_by_user_id на выходе
    API (list/get/create), не хранится отдельно — см. _with_author_name."""
    from jeval.api.main import create_app
    from jeval.orchestrator import JobEvaluator
    from jeval.store import InMemoryStore

    store = InMemoryStore()
    auth_client = TestClient(create_app(store=store, auth_required=True, evaluator=JobEvaluator(agent=fake_agent)))
    reg = auth_client.post(
        "/api/auth/register",
        json={"display_name": "Айжан Эксперт", "email": "expert@example.com", "password": "strong-pass-123"},
    ).json()
    csrf = auth_client.cookies.get("jeval_csrf")
    company = auth_client.post(
        "/api/companies", headers={"X-CSRF-Token": csrf}, json={"name": "Тестовая компания"},
    ).json()
    headers = {"X-Company-ID": company["id"], "X-CSRF-Token": csrf}

    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    pid = auth_client.post("/api/positions", headers=headers, json=body).json()["id"]

    created = auth_client.post("/api/evaluations", headers=headers, json={"position_id": pid}).json()
    assert created["created_by_user_id"] == reg["user"]["id"]
    assert created["created_by_name"] == "Айжан Эксперт"

    fetched = auth_client.get(f"/api/evaluations/{created['id']}", headers=headers).json()
    assert fetched["created_by_name"] == "Айжан Эксперт"

    listed = auth_client.get("/api/evaluations", headers=headers).json()
    assert listed[0]["created_by_name"] == "Айжан Эксперт"


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


def test_import_docx_fill_default_authorities_is_opt_in(client, tmp_path, monkeypatch):
    from jeval import config

    monkeypatch.setattr(config.get_settings(), "jeval_upload_dir", str(tmp_path))
    data = _minimal_docx(
        "Описание должности",
        "Общая информация",
        "Название должности : | Начальник цеха",
        "Подчиняется : | Директор завода",
        "Цель существования должности",
        "Руководит цехом.",
    )

    # Без флага — полномочия не трогаются, остаются пустыми.
    without_flag = client.post(
        "/api/import/document?use_ai=false",
        files={"file": ("a.docx", data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    ).json()
    assert without_flag["position"]["authorities"]["decides_alone"] == []

    # С флагом — шаблон по умолчанию, явно помеченный как предположение.
    with_flag = client.post(
        "/api/import/document?use_ai=false&fill_default_authorities=true",
        files={"file": ("b.docx", data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    ).json()
    decides_alone = with_flag["position"]["authorities"]["decides_alone"]
    assert decides_alone and "ПРЕДПОЛОЖЕНИЕ" in decides_alone[0]
    assert with_flag["position"]["authorities"]["requires_approval"][0]["approver"] == "Директор завода"
    assert any("ПРЕДПОЛОЖЕНИЕ" in note for note in with_flag["notes"])
    assert any("ПРЕДПОЛОЖЕНИЕ" in note for note in with_flag["position"]["import_metadata"]["notes"])


def test_infer_authorities_endpoint_fills_template(client, tmp_path, monkeypatch):
    """UX: то же, что fill_default_authorities при импорте, но для досье,
    которое уже сохранено без полномочий (импортировано без флага или
    дозаполнено вручную позже) — кнопка на карточке оценки."""
    from jeval import config

    monkeypatch.setattr(config.get_settings(), "jeval_upload_dir", str(tmp_path))
    data = _minimal_docx(
        "Описание должности",
        "Общая информация",
        "Название должности : | Начальник цеха",
        "Подчиняется : | Директор завода",
        "Цель существования должности",
        "Руководит цехом.",
    )
    imported = client.post(
        "/api/import/document?use_ai=false",
        files={"file": ("a.docx", data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    ).json()
    pid = imported["position"]["id"]
    assert imported["position"]["authorities"]["decides_alone"] == []

    response = client.post(f"/api/positions/{pid}/infer-authorities")
    assert response.status_code == 200
    body = response.json()
    assert "ПРЕДПОЛОЖЕНИЕ" in body["authorities"]["decides_alone"][0]
    assert body["authorities"]["requires_approval"][0]["approver"] == "Директор завода"
    assert any("ПРЕДПОЛОЖЕНИЕ" in note for note in body["import_metadata"]["notes"])

    refetched = client.get(f"/api/positions/{pid}").json()
    assert refetched["authorities"]["decides_alone"] == body["authorities"]["decides_alone"]


def test_infer_authorities_endpoint_rejects_when_no_manager(client, full_dossier):
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    body["reporting"]["manager"] = None
    body["authorities"] = {"decides_alone": [], "requires_approval": [], "recommends": []}
    pid = client.post("/api/positions", json=body).json()["id"]

    response = client.post(f"/api/positions/{pid}/infer-authorities")
    assert response.status_code == 400


def test_infer_authorities_endpoint_unknown_position_404(client):
    assert client.post("/api/positions/does-not-exist/infer-authorities").status_code == 404


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
