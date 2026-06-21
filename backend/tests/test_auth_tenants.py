"""Авторизация и строгая изоляция данных компаний."""

import sqlite3

from fastapi.testclient import TestClient

from jeval.api.main import create_app
from jeval.api.routers import auth as auth_router
from jeval.config import get_settings
from jeval.domain.identity import CompanyInvite
from jeval.store import InMemoryStore, SqliteStore


def _register(client: TestClient, email: str = "expert@example.com") -> dict:
    response = client.post(
        "/api/auth/register",
        json={"display_name": "Айжан Эксперт", "email": email, "password": "strong-pass-123"},
    )
    assert response.status_code == 201
    return response.json()


def _auth(company_id: str | None = None, csrf: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if company_id:
        headers["X-Company-ID"] = company_id
    if csrf:
        headers["X-CSRF-Token"] = csrf
    return headers


def _company(client: TestClient, name: str) -> dict:
    response = client.post(
        "/api/companies",
        headers=_auth(csrf=client.cookies.get("jeval_csrf")),
        json={
            "name": name,
            "purpose": "job-evaluation",
            "user_role": "hr-cb",
            "organization_size": "251-1000",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_registration_session_company_and_logout():
    store = InMemoryStore()
    client = TestClient(create_app(store=store, auth_required=True))

    auth = _register(client)
    token = auth["access_token"]
    assert auth["companies"] == []
    assert "password" not in auth["user"]
    assert token not in store._sessions  # в store находится только SHA-256 хеш

    assert client.get("/api/auth/me").status_code == 200
    assert client.get("/api/auth/me").status_code == 200
    company = _company(client, "Тестовая компания")
    assert company["role"] == "owner"
    assert client.get("/api/companies").json()[0]["id"] == company["id"]

    assert client.post("/api/auth/logout", headers=_auth(csrf=client.cookies.get("jeval_csrf"))).status_code == 200
    assert client.get("/api/auth/me").status_code == 401

    signed_in = client.post(
        "/api/auth/login",
        json={"email": "EXPERT@example.com", "password": "strong-pass-123"},
    )
    assert signed_in.status_code == 200
    assert signed_in.json()["companies"][0]["id"] == company["id"]


def test_duplicate_email_is_case_insensitive():
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    _register(client, "Expert@Example.com")
    duplicate = client.post(
        "/api/auth/register",
        json={"display_name": "Другой эксперт", "email": "expert@example.COM", "password": "strong-pass-123"},
    )
    assert duplicate.status_code == 409


def test_one_user_switches_companies_with_strict_position_isolation(full_dossier):
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    auth = _register(client)
    first = _company(client, "Первая компания")
    second = _company(client, "Вторая компания")
    assert client.post(
        f"/api/companies/{second['id']}/activate", headers=_auth(csrf=client.cookies.get("jeval_csrf"))
    ).status_code == 200

    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    created = client.post(
        "/api/positions", headers=_auth(first["id"], client.cookies.get("jeval_csrf")), json=body
    )
    assert created.status_code == 201
    position_id = created.json()["id"]

    assert len(client.get("/api/positions", headers=_auth(first["id"])).json()) == 1
    assert client.get("/api/positions", headers=_auth(second["id"])).json() == []
    assert client.get(
        f"/api/positions/{position_id}", headers=_auth(second["id"])
    ).status_code == 404


def test_user_cannot_select_another_users_company():
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    owner = _register(client, "owner@example.com")
    company = _company(client, "Закрытая компания")
    outsider = _register(client, "outsider@example.com")

    response = client.get(
        "/api/positions",
        headers=_auth(company["id"]),
    )
    assert response.status_code == 403


def test_viewer_can_read_but_cannot_change_company_data(full_dossier):
    store = InMemoryStore()
    client = TestClient(create_app(store=store, auth_required=True))
    auth = _register(client, "viewer@example.com")
    company = _company(client, "Компания наблюдателя")
    store._memberships[(auth["user"]["id"], company["id"])].role = "viewer"

    headers = _auth(company["id"])
    assert client.get("/api/positions", headers=headers).status_code == 200
    body = full_dossier.model_dump(mode="json", exclude_none=True)
    body.pop("id", None)
    assert client.post("/api/positions", headers=_auth(company["id"], client.cookies.get("jeval_csrf")), json=body).status_code == 403


def test_private_endpoint_requires_company_context():
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    auth = _register(client)
    assert client.get("/api/positions").status_code == 400
    fresh = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    assert fresh.get("/api/positions").status_code == 401


def test_csrf_required_for_state_changing_requests():
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    _register(client)
    missing = client.post(
        "/api/companies",
        json={
            "name": "Нет CSRF",
            "purpose": "job-evaluation",
            "user_role": "hr-cb",
            "organization_size": "251-1000",
        },
    )
    assert missing.status_code == 403

    ok = client.post(
        "/api/companies",
        headers=_auth(csrf=client.cookies.get("jeval_csrf")),
        json={
            "name": "Есть CSRF",
            "purpose": "job-evaluation",
            "user_role": "hr-cb",
            "organization_size": "251-1000",
        },
    )
    assert ok.status_code == 201


def test_admin_can_manage_company_access_allowlist():
    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    _register(client, "owner@example.com")
    company = _company(client, "Админ компания")

    created = client.post(
        "/api/admin/access",
        headers=_auth(company["id"], client.cookies.get("jeval_csrf")),
        json={"email": "viewer@gmail.com", "role": "viewer"},
    )
    assert created.status_code == 201
    invite_id = created.json()["id"]

    listed = client.get("/api/admin/access", headers=_auth(company["id"]))
    assert listed.status_code == 200
    assert listed.json()[0]["email"] == "viewer@gmail.com"

    updated = client.put(
        f"/api/admin/access/{invite_id}",
        headers=_auth(company["id"], client.cookies.get("jeval_csrf")),
        json={"role": "admin", "status": "active"},
    )
    assert updated.status_code == 200
    assert updated.json()["role"] == "admin"
    assert updated.json()["status"] == "active"

    deleted = client.delete(
        f"/api/admin/access/{invite_id}",
        headers=_auth(company["id"], client.cookies.get("jeval_csrf")),
    )
    assert deleted.status_code == 200
    assert client.get("/api/admin/access", headers=_auth(company["id"])).json() == []


def test_viewer_cannot_manage_company_access():
    store = InMemoryStore()
    client = TestClient(create_app(store=store, auth_required=True))
    auth = _register(client, "viewer-admin@example.com")
    company = _company(client, "Компания для проверки доступа")
    store._memberships[(auth["user"]["id"], company["id"])].role = "viewer"

    response = client.post(
        "/api/admin/access",
        headers=_auth(company["id"], client.cookies.get("jeval_csrf")),
        json={"email": "blocked@gmail.com", "role": "viewer"},
    )
    assert response.status_code == 403


def test_google_callback_accepts_allowlisted_email(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "jeval_google_enabled", True, raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_id", "client-id", raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_secret", "client-secret", raising=False)
    monkeypatch.setattr(settings, "jeval_frontend_url", "http://frontend.local", raising=False)

    store = InMemoryStore()
    client = TestClient(create_app(store=store, auth_required=True))
    _register(client, "owner@example.com")
    company = _company(client, "Google allowlist")
    store.upsert_company_invite(
        CompanyInvite(
            id="invite-1",
            company_id=company["id"],
            email="google.user@gmail.com",
            role="viewer",
            status="invited",
        )
    )

    monkeypatch.setattr(
        auth_router,
        "_fetch_google_profile",
        lambda **kwargs: {"email": "google.user@gmail.com", "sub": "google-sub-1", "name": "Google User"},
    )

    start = client.get("/api/auth/google/start", follow_redirects=False)
    assert start.status_code == 302
    state = client.cookies.get("jeval_google_state")
    assert state

    callback = client.get(f"/api/auth/google/callback?code=code-1&state={state}", follow_redirects=False)
    assert callback.status_code == 302
    assert callback.headers["location"] == "http://frontend.local/"

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["user"]["email"] == "google.user@gmail.com"
    assert me.json()["companies"][0]["id"] == company["id"]


def test_google_callback_denies_non_allowlisted_email(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "jeval_google_enabled", True, raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_id", "client-id", raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_secret", "client-secret", raising=False)
    monkeypatch.setattr(settings, "jeval_frontend_url", "http://frontend.local", raising=False)
    # Явно фиксируем гейт включённым независимо от локального .env разработчика
    # (JEVAL_DISABLE_ACCESS_GATE может быть true на машине, где это запускается).
    monkeypatch.setattr(settings, "jeval_disable_access_gate", False, raising=False)

    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    monkeypatch.setattr(
        auth_router,
        "_fetch_google_profile",
        lambda **kwargs: {"email": "blocked@gmail.com", "sub": "google-sub-2", "name": "Blocked User"},
    )

    client.get("/api/auth/google/start", follow_redirects=False)
    state = client.cookies.get("jeval_google_state")
    assert state

    callback = client.get(f"/api/auth/google/callback?code=code-2&state={state}", follow_redirects=False)
    assert callback.status_code == 302
    assert "auth_error=access_denied" in callback.headers["location"]


def test_access_gate_disabled_by_default():
    """Проверяем дефолт ПОЛЯ в Settings, а не текущий get_settings() — последний
    читает локальный .env разработчика, где JEVAL_DISABLE_ACCESS_GATE временно
    может быть true (см. .env.example: пометка "ВРЕМЕННО для разработки")."""
    from jeval.config import Settings

    assert Settings.model_fields["jeval_disable_access_gate"].default is False


def test_disable_access_gate_lets_new_google_user_in_without_invite(monkeypatch):
    """ВРЕМЕННО для разработки: JEVAL_DISABLE_ACCESS_GATE=1 пропускает allowlist —
    новый Google-пользователь без приглашения и без существующей компании всё
    равно логинится (как при обычной email/password-регистрации)."""
    settings = get_settings()
    monkeypatch.setattr(settings, "jeval_google_enabled", True, raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_id", "client-id", raising=False)
    monkeypatch.setattr(settings, "jeval_google_client_secret", "client-secret", raising=False)
    monkeypatch.setattr(settings, "jeval_frontend_url", "http://frontend.local", raising=False)
    monkeypatch.setattr(settings, "jeval_disable_access_gate", True, raising=False)

    client = TestClient(create_app(store=InMemoryStore(), auth_required=True))
    monkeypatch.setattr(
        auth_router,
        "_fetch_google_profile",
        lambda **kwargs: {"email": "no-invite@gmail.com", "sub": "google-sub-3", "name": "No Invite"},
    )

    client.get("/api/auth/google/start", follow_redirects=False)
    state = client.cookies.get("jeval_google_state")
    assert state

    callback = client.get(f"/api/auth/google/callback?code=code-3&state={state}", follow_redirects=False)
    assert callback.status_code == 302
    assert callback.headers["location"] == "http://frontend.local/"

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["user"]["email"] == "no-invite@gmail.com"
    assert me.json()["companies"] == []  # как при обычной регистрации — без приглашения


def test_old_sqlite_documents_are_migrated_to_first_company(tmp_path, full_dossier):
    path = tmp_path / "legacy.db"
    dossier = full_dossier.model_copy(deep=True)
    dossier.id = "legacy-position"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE positions (id TEXT PRIMARY KEY, doc TEXT NOT NULL)")
        connection.execute(
            "INSERT INTO positions (id, doc) VALUES (?, ?)",
            (dossier.id, dossier.model_dump_json()),
        )

    client = TestClient(create_app(store=SqliteStore(str(path)), auth_required=True))
    auth = _register(client, "migration@example.com")
    company = _company(client, "Компания после миграции")

    positions = client.get(
        "/api/positions", headers=_auth(company["id"])
    ).json()
    assert [position["id"] for position in positions] == ["legacy-position"]
    assert positions[0]["company_id"] == company["id"]


def test_clean_sqlite_schema_has_tenant_foreign_keys(tmp_path):
    path = tmp_path / "clean.db"
    SqliteStore(str(path))
    with sqlite3.connect(path) as connection:
        position_targets = {
            row[2] for row in connection.execute("PRAGMA foreign_key_list(positions)")
        }
        evaluation_targets = {
            row[2] for row in connection.execute("PRAGMA foreign_key_list(evaluations)")
        }
    assert {"companies", "users"} <= position_targets
    assert {"companies", "positions", "users"} <= evaluation_targets
