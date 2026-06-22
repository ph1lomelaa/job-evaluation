"""Multi-tenant хранилище платформы.

Реляционные колонки отвечают за tenant-изоляцию и выборки, JSON сохраняет полный
версионируемый документ Hay без хрупкой таблицы на каждое вложенное поле.
"""

from __future__ import annotations

import json
import threading
import uuid
from collections.abc import Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Protocol

from sqlalchemy import create_engine, event, inspect, text

from .domain.identity import (
    CompanyInvite,
    CompanyInviteSummary,
    Company,
    CompanyMembership,
    CompanySummary,
    SessionRecord,
    UserRecord,
)
from .domain.models import Evaluation, JobDossier, PublicJobForm


class Store(Protocol):
    def save_position(self, dossier: JobDossier, company_id: Optional[str] = None) -> JobDossier: ...
    def get_position(self, position_id: str, company_id: Optional[str] = None) -> Optional[JobDossier]: ...
    def list_positions(self, company_id: Optional[str] = None) -> list[JobDossier]: ...
    def save_evaluation(self, evaluation: Evaluation, company_id: Optional[str] = None) -> Evaluation: ...
    def get_evaluation(self, evaluation_id: str, company_id: Optional[str] = None) -> Optional[Evaluation]: ...
    def list_evaluations(self, position_id: Optional[str] = None, company_id: Optional[str] = None) -> list[Evaluation]: ...
    def save_public_form(self, form: PublicJobForm, company_id: Optional[str] = None) -> PublicJobForm: ...
    def get_public_form(self, form_id: str, company_id: Optional[str] = None) -> Optional[PublicJobForm]: ...
    def get_public_form_by_token(self, token: str) -> Optional[PublicJobForm]: ...
    def list_public_forms(self, company_id: Optional[str] = None) -> list[PublicJobForm]: ...
    def create_user(self, user: UserRecord) -> UserRecord: ...
    def get_user(self, user_id: str) -> Optional[UserRecord]: ...
    def get_user_by_email(self, email: str) -> Optional[UserRecord]: ...
    def get_user_by_google_sub(self, google_sub: str) -> Optional[UserRecord]: ...
    def update_user_identity(self, user_id: str, auth_provider: str, google_sub: Optional[str]) -> None: ...
    def update_user_login(self, user_id: str, when: datetime) -> None: ...
    def save_session(self, session: SessionRecord) -> None: ...
    def get_user_by_session(self, token_hash: str, now: datetime) -> Optional[UserRecord]: ...
    def delete_session(self, token_hash: str) -> None: ...
    def create_company(self, company: Company, membership: CompanyMembership) -> CompanySummary: ...
    def list_companies_for_user(self, user_id: str) -> list[CompanySummary]: ...
    def get_membership(self, user_id: str, company_id: str) -> Optional[CompanyMembership]: ...
    def upsert_membership(self, membership: CompanyMembership) -> CompanyMembership: ...
    def list_company_invites(self, company_id: str) -> list[CompanyInviteSummary]: ...
    def list_company_invites_by_email(self, email: str) -> list[CompanyInviteSummary]: ...
    def get_company_invite(self, invite_id: str, company_id: str) -> Optional[CompanyInvite]: ...
    def get_company_invite_by_email(self, company_id: str, email: str) -> Optional[CompanyInvite]: ...
    def upsert_company_invite(self, invite: CompanyInvite) -> CompanyInvite: ...
    def delete_company_invite(self, invite_id: str, company_id: str) -> None: ...
    def record_audit(self, company_id: Optional[str], user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str], metadata: Optional[dict] = None) -> None: ...


class _ResultProxy:
    def __init__(self, result):
        self._result = result.mappings()

    def fetchone(self):
        return self._result.fetchone()

    def fetchall(self):
        return self._result.fetchall()


class _ConnectionProxy:
    """Тонкая обёртка вокруг одного SQLAlchemy ``Connection``: ?-плейсхолдеры
    и `sqlite3.Row`-подобный доступ к результату. Соединение ей не принадлежит —
    его жизненным циклом управляет вызывающий код (см. ``SqliteStore._connection``)."""

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql: str, params=None):
        statement, values = _translate_sql(sql, params)
        return _ResultProxy(self._conn.execute(text(statement), values))

    def executescript(self, script: str):
        for statement in (part.strip() for part in script.split(";")):
            if statement:
                self.execute(statement)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()


def _translate_sql(sql: str, params=None) -> tuple[str, dict]:
    if params is None:
        params = ()
    if isinstance(params, Mapping):
        return sql, dict(params)
    if not isinstance(params, (list, tuple)):
        params = (params,)
    values: dict[str, object] = {}
    pieces: list[str] = []
    index = 0
    for char in sql:
        if char == "?":
            index += 1
            key = f"p{index}"
            pieces.append(f":{key}")
            values[key] = params[index - 1]
        else:
            pieces.append(char)
    return "".join(pieces), values


class InMemoryStore:
    def __init__(self) -> None:
        self._positions: dict[str, JobDossier] = {}
        self._evaluations: dict[str, Evaluation] = {}
        self._public_forms: dict[str, PublicJobForm] = {}
        self._users: dict[str, UserRecord] = {}
        self._sessions: dict[str, SessionRecord] = {}
        self._companies: dict[str, Company] = {}
        self._memberships: dict[tuple[str, str], CompanyMembership] = {}
        self._company_invites: dict[str, CompanyInvite] = {}
        self._audit: list[dict] = []

    def save_position(self, dossier: JobDossier, company_id: Optional[str] = None) -> JobDossier:
        dossier.company_id = company_id or dossier.company_id
        self._positions[dossier.id or ""] = dossier
        return dossier

    def get_position(self, position_id: str, company_id: Optional[str] = None) -> Optional[JobDossier]:
        value = self._positions.get(position_id)
        return value if value and (company_id is None or value.company_id == company_id) else None

    def list_positions(self, company_id: Optional[str] = None) -> list[JobDossier]:
        return [p for p in self._positions.values() if company_id is None or p.company_id == company_id]

    def save_evaluation(self, evaluation: Evaluation, company_id: Optional[str] = None) -> Evaluation:
        evaluation.company_id = company_id or evaluation.company_id
        self._evaluations[evaluation.id or ""] = evaluation
        return evaluation

    def get_evaluation(self, evaluation_id: str, company_id: Optional[str] = None) -> Optional[Evaluation]:
        value = self._evaluations.get(evaluation_id)
        return value if value and (company_id is None or value.company_id == company_id) else None

    def list_evaluations(self, position_id: Optional[str] = None, company_id: Optional[str] = None) -> list[Evaluation]:
        return [
            e for e in self._evaluations.values()
            if (position_id is None or e.position_id == position_id)
            and (company_id is None or e.company_id == company_id)
        ]

    def save_public_form(self, form: PublicJobForm, company_id: Optional[str] = None) -> PublicJobForm:
        form.company_id = company_id or form.company_id
        self._public_forms[form.id] = form
        return form

    def get_public_form(self, form_id: str, company_id: Optional[str] = None) -> Optional[PublicJobForm]:
        value = self._public_forms.get(form_id)
        return value if value and (company_id is None or value.company_id == company_id) else None

    def get_public_form_by_token(self, token: str) -> Optional[PublicJobForm]:
        return next((form for form in self._public_forms.values() if form.token == token), None)

    def list_public_forms(self, company_id: Optional[str] = None) -> list[PublicJobForm]:
        return [f for f in self._public_forms.values() if company_id is None or f.company_id == company_id]

    def create_user(self, user: UserRecord) -> UserRecord:
        if self.get_user_by_email(user.email):
            raise ValueError("email_exists")
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[UserRecord]:
        return self._users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        return next((user for user in self._users.values() if user.email == email), None)

    def get_user_by_google_sub(self, google_sub: str) -> Optional[UserRecord]:
        return next((user for user in self._users.values() if user.google_sub == google_sub), None)

    def update_user_identity(self, user_id: str, auth_provider: str, google_sub: Optional[str]) -> None:
        user = self._users.get(user_id)
        if user:
            user.auth_provider = auth_provider
            user.google_sub = google_sub

    def update_user_login(self, user_id: str, when: datetime) -> None:
        user = self._users.get(user_id)
        if user:
            user.last_login_at = when

    def save_session(self, session: SessionRecord) -> None:
        self._sessions[session.token_hash] = session

    def get_user_by_session(self, token_hash: str, now: datetime) -> Optional[UserRecord]:
        session = self._sessions.get(token_hash)
        if not session or session.expires_at <= now:
            self._sessions.pop(token_hash, None)
            return None
        session.last_used_at = now
        return self.get_user(session.user_id)

    def delete_session(self, token_hash: str) -> None:
        self._sessions.pop(token_hash, None)

    def create_company(self, company: Company, membership: CompanyMembership) -> CompanySummary:
        first_company = not self._companies
        self._companies[company.id] = company
        self._memberships[(membership.user_id, membership.company_id)] = membership
        if first_company:
            for dossier in self._positions.values():
                dossier.company_id = dossier.company_id or company.id
            for evaluation in self._evaluations.values():
                evaluation.company_id = evaluation.company_id or company.id
            for form in self._public_forms.values():
                form.company_id = form.company_id or company.id
        return _company_summary(company, membership)

    def list_companies_for_user(self, user_id: str) -> list[CompanySummary]:
        values = []
        for (member_user_id, company_id), membership in self._memberships.items():
            if member_user_id == user_id and membership.status == "active":
                values.append(_company_summary(self._companies[company_id], membership))
        return sorted(values, key=lambda item: item.created_at)

    def get_membership(self, user_id: str, company_id: str) -> Optional[CompanyMembership]:
        membership = self._memberships.get((user_id, company_id))
        return membership if membership and membership.status == "active" else None

    def upsert_membership(self, membership: CompanyMembership) -> CompanyMembership:
        self._memberships[(membership.user_id, membership.company_id)] = membership
        return membership

    def list_company_invites(self, company_id: str) -> list[CompanyInviteSummary]:
        return [
            CompanyInviteSummary.model_validate(invite.model_dump())
            for invite in self._company_invites.values()
            if invite.company_id == company_id
        ]

    def list_company_invites_by_email(self, email: str) -> list[CompanyInviteSummary]:
        return [
            CompanyInviteSummary.model_validate(invite.model_dump())
            for invite in self._company_invites.values()
            if invite.email == email and invite.status != "disabled"
        ]

    def get_company_invite(self, invite_id: str, company_id: str) -> Optional[CompanyInvite]:
        invite = self._company_invites.get(invite_id)
        return invite if invite and invite.company_id == company_id else None

    def get_company_invite_by_email(self, company_id: str, email: str) -> Optional[CompanyInvite]:
        return next(
            (invite for invite in self._company_invites.values() if invite.company_id == company_id and invite.email == email),
            None,
        )

    def upsert_company_invite(self, invite: CompanyInvite) -> CompanyInvite:
        self._company_invites[invite.id] = invite
        return invite

    def delete_company_invite(self, invite_id: str, company_id: str) -> None:
        invite = self._company_invites.get(invite_id)
        if invite and invite.company_id == company_id:
            self._company_invites.pop(invite_id, None)

    def record_audit(self, company_id: Optional[str], user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str], metadata: Optional[dict] = None) -> None:
        self._audit.append({"company_id": company_id, "user_id": user_id, "action": action, "entity_type": entity_type, "entity_id": entity_id, "metadata": metadata or {}})


class SqliteStore:
    """Хранилище на SQLAlchemy (SQLite/Postgres).

    Соединение берётся из пула SQLAlchemy на каждый вызов, а не держится одно
    на весь процесс: один общий ``Connection`` нельзя безопасно использовать
    из нескольких потоков одновременно. Глобальный лок нужен только для SQLite
    (один писатель на файл базы) — для Postgres конкурентность отдаёт пулу и
    самой БД, ничего не сериализуя на уровне приложения.
    """

    def __init__(self, path: str) -> None:
        if "://" not in path:
            raw_path = Path(path)
            if raw_path.is_absolute():
                path = f"sqlite:///{raw_path}"
            else:
                path = f"sqlite:///{raw_path.as_posix()}"
        self._is_sqlite = path.startswith("sqlite")
        connect_args = {"check_same_thread": False} if self._is_sqlite else {}
        self._engine = create_engine(path, future=True, pool_pre_ping=True, connect_args=connect_args)
        self._lock = threading.RLock() if self._is_sqlite else None
        if self._is_sqlite:
            # PRAGMA — настройка на уровне соединения, а не файла БД, поэтому
            # её нужно применять к каждому новому DBAPI-соединению из пула,
            # а не один раз при старте (раньше соединение было одно на весь
            # процесс, и разового вызова в __init__ было достаточно).
            @event.listens_for(self._engine, "connect")
            def _set_sqlite_pragma(dbapi_connection, _record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        self._migrate()

    @contextmanager
    def _connection(self):
        """Соединение из пула на время одного вызова/блока операций."""
        if self._lock is not None:
            with self._lock, self._engine.connect() as raw_conn:
                yield _ConnectionProxy(raw_conn)
        else:
            with self._engine.connect() as raw_conn:
                yield _ConnectionProxy(raw_conn)

    def _migrate(self) -> None:
        with self._connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    display_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    auth_provider TEXT NOT NULL DEFAULT 'local',
                    google_sub TEXT,
                    created_at TEXT NOT NULL,
                    last_login_at TEXT
                );
                CREATE TABLE IF NOT EXISTS companies (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL UNIQUE,
                    created_by_user_id TEXT NOT NULL REFERENCES users(id),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS company_memberships (
                    company_id TEXT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK(role IN ('owner','admin','evaluator','viewer')),
                    status TEXT NOT NULL CHECK(status IN ('active','invited','disabled')),
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (company_id, user_id)
                );
                CREATE TABLE IF NOT EXISTS company_invites (
                    id TEXT PRIMARY KEY,
                    company_id TEXT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin','viewer')),
                    status TEXT NOT NULL CHECK(status IN ('invited','active','disabled')),
                    created_by_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    accepted_at TEXT
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    last_used_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS positions (
                    id TEXT PRIMARY KEY,
                    company_id TEXT REFERENCES companies(id) ON DELETE CASCADE,
                    created_by_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                    name TEXT,
                    department TEXT,
                    function_name TEXT,
                    review_status TEXT,
                    updated_at TEXT,
                    doc TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS evaluations (
                    id TEXT PRIMARY KEY,
                    company_id TEXT REFERENCES companies(id) ON DELETE CASCADE,
                    position_id TEXT REFERENCES positions(id) ON DELETE CASCADE,
                    created_by_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                    status TEXT,
                    grade INTEGER,
                    total_points INTEGER,
                    created_at TEXT,
                    doc TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS public_forms (
                    id TEXT PRIMARY KEY,
                    company_id TEXT REFERENCES companies(id) ON DELETE CASCADE,
                    created_by_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                    token TEXT,
                    status TEXT,
                    position_id TEXT REFERENCES positions(id) ON DELETE SET NULL,
                    created_at TEXT,
                    expires_at TEXT,
                    doc TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS audit_events (
                    id TEXT PRIMARY KEY,
                    company_id TEXT REFERENCES companies(id) ON DELETE SET NULL,
                    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                    action TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                """
            )
            # Commit перед inspect(): inspect() открывает СВОЁ соединение из пула
            # движка, а не использует `conn` — на Postgres (READ COMMITTED) только
            # что созданные таблицы из ещё не закоммиченной транзакции `conn` в нём
            # не видны (NoSuchTableError). На SQLite это маскировалось тем, что DDL
            # там обычно коммитится сразу же на уровне драйвера.
            conn.commit()
            for table, columns in {
                "positions": {
                    "company_id": "TEXT",
                    "created_by_user_id": "TEXT",
                    "name": "TEXT",
                    "department": "TEXT",
                    "function_name": "TEXT",
                    "review_status": "TEXT",
                    "updated_at": "TEXT",
                },
                "users": {
                    "auth_provider": "TEXT",
                    "google_sub": "TEXT",
                },
                "evaluations": {
                    "company_id": "TEXT",
                    "position_id": "TEXT",
                    "created_by_user_id": "TEXT",
                    "status": "TEXT",
                    "grade": "INTEGER",
                    "total_points": "INTEGER",
                    "created_at": "TEXT",
                },
                "public_forms": {
                    "company_id": "TEXT",
                    "created_by_user_id": "TEXT",
                    "token": "TEXT",
                    "status": "TEXT",
                    "position_id": "TEXT",
                    "created_at": "TEXT",
                    "expires_at": "TEXT",
                },
            }.items():
                existing = {column["name"] for column in inspect(self._engine).get_columns(table)}
                for column, kind in columns.items():
                    if column not in existing:
                        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {kind}")
            conn.executescript(
                """
                CREATE INDEX IF NOT EXISTS idx_memberships_user_status ON company_memberships(user_id, status);
                CREATE UNIQUE INDEX IF NOT EXISTS idx_company_invites_company_email ON company_invites(company_id, email);
                CREATE INDEX IF NOT EXISTS idx_company_invites_company_status ON company_invites(company_id, status, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_sessions_user_expiry ON sessions(user_id, expires_at);
                CREATE INDEX IF NOT EXISTS idx_positions_company_updated ON positions(company_id, updated_at DESC);
                CREATE INDEX IF NOT EXISTS idx_positions_company_status ON positions(company_id, review_status);
                CREATE INDEX IF NOT EXISTS idx_evaluations_company_position ON evaluations(company_id, position_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_evaluations_company_status ON evaluations(company_id, status);
                CREATE UNIQUE INDEX IF NOT EXISTS idx_public_forms_token ON public_forms(token) WHERE token IS NOT NULL;
                CREATE INDEX IF NOT EXISTS idx_public_forms_company_status ON public_forms(company_id, status, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_audit_company_created ON audit_events(company_id, created_at DESC);
                """
            )
            self._backfill_document_columns(conn)
            self._backfill_user_columns(conn)
            conn.commit()

    def _backfill_user_columns(self, conn) -> None:
        rows = conn.execute("SELECT id, auth_provider FROM users").fetchall()
        for row in rows:
            if not row["auth_provider"]:
                conn.execute("UPDATE users SET auth_provider = 'local' WHERE id = ?", (row["id"],))

    def _backfill_document_columns(self, conn) -> None:
        mappings = {
            "positions": ("company_id", "created_by_user_id", "name", "department", "function_name", "review_status", "updated_at"),
            "evaluations": ("company_id", "position_id", "created_by_user_id", "status", "grade", "total_points", "created_at"),
            "public_forms": ("company_id", "created_by_user_id", "token", "status", "position_id", "created_at", "expires_at"),
        }
        for table, columns in mappings.items():
            rows = conn.execute(f"SELECT id, doc FROM {table}").fetchall()
            for row in rows:
                try:
                    doc = json.loads(row["doc"])
                except (TypeError, json.JSONDecodeError):
                    continue
                values = []
                for column in columns:
                    if column == "function_name":
                        values.append(doc.get("function"))
                    elif column == "grade":
                        values.append((doc.get("score") or {}).get("grade"))
                    elif column == "total_points":
                        values.append((doc.get("score") or {}).get("total_points"))
                    else:
                        values.append(doc.get(column))
                assignments = ", ".join(f"{column} = COALESCE({column}, ?)" for column in columns)
                conn.execute(f"UPDATE {table} SET {assignments} WHERE id = ?", (*values, row["id"]))

    def save_position(self, dossier: JobDossier, company_id: Optional[str] = None) -> JobDossier:
        dossier.company_id = company_id or dossier.company_id
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO positions
                   (id, company_id, created_by_user_id, name, department, function_name, review_status, updated_at, doc)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET company_id=excluded.company_id,
                     created_by_user_id=excluded.created_by_user_id, name=excluded.name,
                     department=excluded.department, function_name=excluded.function_name,
                     review_status=excluded.review_status, updated_at=excluded.updated_at, doc=excluded.doc""",
                (dossier.id or "", dossier.company_id, dossier.created_by_user_id, dossier.name,
                 dossier.department, dossier.function, dossier.review_status.value,
                 dossier.updated_at.isoformat(), dossier.model_dump_json()),
            )
            conn.commit()
        return dossier

    def get_position(self, position_id: str, company_id: Optional[str] = None) -> Optional[JobDossier]:
        row = self._fetch_doc("positions", position_id, company_id)
        return JobDossier.model_validate_json(row) if row else None

    def list_positions(self, company_id: Optional[str] = None) -> list[JobDossier]:
        return [JobDossier.model_validate_json(doc) for doc in self._list_docs("positions", company_id)]

    def save_evaluation(self, evaluation: Evaluation, company_id: Optional[str] = None) -> Evaluation:
        evaluation.company_id = company_id or evaluation.company_id
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO evaluations
                   (id, company_id, position_id, created_by_user_id, status, grade, total_points, created_at, doc)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET company_id=excluded.company_id,
                     position_id=excluded.position_id, created_by_user_id=excluded.created_by_user_id,
                     status=excluded.status, grade=excluded.grade, total_points=excluded.total_points,
                     created_at=excluded.created_at, doc=excluded.doc""",
                (evaluation.id or "", evaluation.company_id, evaluation.position_id,
                 evaluation.created_by_user_id, evaluation.status.value,
                 evaluation.score.grade if evaluation.score else None,
                 evaluation.score.total_points if evaluation.score else None,
                 evaluation.created_at.isoformat(), evaluation.model_dump_json()),
            )
            conn.commit()
        return evaluation

    def get_evaluation(self, evaluation_id: str, company_id: Optional[str] = None) -> Optional[Evaluation]:
        row = self._fetch_doc("evaluations", evaluation_id, company_id)
        return Evaluation.model_validate_json(row) if row else None

    def list_evaluations(self, position_id: Optional[str] = None, company_id: Optional[str] = None) -> list[Evaluation]:
        clauses, params = [], []
        if position_id is not None:
            clauses.append("position_id = ?")
            params.append(position_id)
        if company_id is not None:
            clauses.append("company_id = ?")
            params.append(company_id)
        query = "SELECT doc FROM evaluations" + (" WHERE " + " AND ".join(clauses) if clauses else "")
        with self._connection() as conn:
            rows = conn.execute(query, params).fetchall()
        return [Evaluation.model_validate_json(row["doc"]) for row in rows]

    def save_public_form(self, form: PublicJobForm, company_id: Optional[str] = None) -> PublicJobForm:
        form.company_id = company_id or form.company_id
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO public_forms
                   (id, company_id, created_by_user_id, token, status, position_id, created_at, expires_at, doc)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET company_id=excluded.company_id,
                     created_by_user_id=excluded.created_by_user_id, token=excluded.token,
                     status=excluded.status, position_id=excluded.position_id,
                     created_at=excluded.created_at, expires_at=excluded.expires_at, doc=excluded.doc""",
                (form.id, form.company_id, form.created_by_user_id, form.token, form.status,
                 form.position_id, form.created_at.isoformat(), form.expires_at.isoformat(),
                 form.model_dump_json()),
            )
            conn.commit()
        return form

    def get_public_form(self, form_id: str, company_id: Optional[str] = None) -> Optional[PublicJobForm]:
        row = self._fetch_doc("public_forms", form_id, company_id)
        return PublicJobForm.model_validate_json(row) if row else None

    def get_public_form_by_token(self, token: str) -> Optional[PublicJobForm]:
        with self._connection() as conn:
            row = conn.execute("SELECT doc FROM public_forms WHERE token = ?", (token,)).fetchone()
        return PublicJobForm.model_validate_json(row["doc"]) if row else None

    def list_public_forms(self, company_id: Optional[str] = None) -> list[PublicJobForm]:
        return [PublicJobForm.model_validate_json(doc) for doc in self._list_docs("public_forms", company_id)]

    def create_user(self, user: UserRecord) -> UserRecord:
        try:
            with self._connection() as conn:
                conn.execute(
                    "INSERT INTO users (id,email,display_name,password_hash,auth_provider,google_sub,created_at,last_login_at) VALUES (?,?,?,?,?,?,?,?)",
                    (user.id, user.email, user.display_name, user.password_hash,
                     user.auth_provider, user.google_sub, user.created_at.isoformat(), _iso(user.last_login_at)),
                )
                conn.commit()
        except Exception as exc:
            raise ValueError("email_exists") from exc
        return user

    def get_user(self, user_id: str) -> Optional[UserRecord]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return _user_from_row(row) if row else None

    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return _user_from_row(row) if row else None

    def get_user_by_google_sub(self, google_sub: str) -> Optional[UserRecord]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE google_sub = ?", (google_sub,)).fetchone()
        return _user_from_row(row) if row else None

    def update_user_identity(self, user_id: str, auth_provider: str, google_sub: Optional[str]) -> None:
        with self._connection() as conn:
            conn.execute(
                "UPDATE users SET auth_provider = ?, google_sub = ? WHERE id = ?",
                (auth_provider, google_sub, user_id),
            )
            conn.commit()

    def update_user_login(self, user_id: str, when: datetime) -> None:
        with self._connection() as conn:
            conn.execute("UPDATE users SET last_login_at = ? WHERE id = ?", (when.isoformat(), user_id))
            conn.commit()

    def save_session(self, session: SessionRecord) -> None:
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO sessions (token_hash,user_id,created_at,expires_at,last_used_at)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(token_hash) DO UPDATE SET user_id=excluded.user_id,
                     created_at=excluded.created_at, expires_at=excluded.expires_at,
                     last_used_at=excluded.last_used_at""",
                (session.token_hash, session.user_id, session.created_at.isoformat(),
                 session.expires_at.isoformat(), session.last_used_at.isoformat()),
            )
            conn.commit()

    def get_user_by_session(self, token_hash: str, now: datetime) -> Optional[UserRecord]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT user_id, expires_at FROM sessions WHERE token_hash = ?", (token_hash,)
            ).fetchone()
            if not row:
                return None
            if _dt(row["expires_at"]) <= now:
                conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
                conn.commit()
                return None
            conn.execute("UPDATE sessions SET last_used_at = ? WHERE token_hash = ?", (now.isoformat(), token_hash))
            conn.commit()
        return self.get_user(row["user_id"])

    def delete_session(self, token_hash: str) -> None:
        with self._connection() as conn:
            conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
            conn.commit()

    def create_company(self, company: Company, membership: CompanyMembership) -> CompanySummary:
        with self._connection() as conn:
            first_company = conn.execute("SELECT COUNT(*) AS count FROM companies").fetchone()["count"] == 0
            try:
                conn.execute(
                    """INSERT INTO companies
                       (id,name,slug,created_by_user_id,created_at,updated_at)
                       VALUES (?,?,?,?,?,?)""",
                    (company.id, company.name, company.slug, company.created_by_user_id,
                     company.created_at.isoformat(), company.updated_at.isoformat()),
                )
                conn.execute(
                    "INSERT INTO company_memberships (company_id,user_id,role,status,created_at) VALUES (?,?,?,?,?)",
                    (membership.company_id, membership.user_id, membership.role,
                     membership.status, membership.created_at.isoformat()),
                )
                if first_company:
                    for table in ("positions", "evaluations", "public_forms"):
                        rows = conn.execute(f"SELECT id, doc FROM {table} WHERE company_id IS NULL").fetchall()
                        for row in rows:
                            try:
                                doc = json.loads(row["doc"])
                            except (TypeError, json.JSONDecodeError):
                                doc = {}
                            doc["company_id"] = company.id
                            conn.execute(
                                f"UPDATE {table} SET company_id = ?, doc = ? WHERE id = ?",
                                (company.id, json.dumps(doc, ensure_ascii=False), row["id"]),
                            )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
        return _company_summary(company, membership)

    def list_companies_for_user(self, user_id: str) -> list[CompanySummary]:
        with self._connection() as conn:
            rows = conn.execute(
                """SELECT c.*, m.role FROM companies c
                   JOIN company_memberships m ON m.company_id = c.id
                   WHERE m.user_id = ? AND m.status = 'active' ORDER BY c.created_at""",
                (user_id,),
            ).fetchall()
        return [CompanySummary(id=row["id"], name=row["name"], slug=row["slug"], role=row["role"], created_at=_dt(row["created_at"])) for row in rows]

    def get_membership(self, user_id: str, company_id: str) -> Optional[CompanyMembership]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM company_memberships WHERE user_id = ? AND company_id = ? AND status = 'active'",
                (user_id, company_id),
            ).fetchone()
        return CompanyMembership(company_id=row["company_id"], user_id=row["user_id"], role=row["role"], status=row["status"], created_at=_dt(row["created_at"])) if row else None

    def upsert_membership(self, membership: CompanyMembership) -> CompanyMembership:
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO company_memberships (company_id,user_id,role,status,created_at)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(company_id, user_id) DO UPDATE SET role=excluded.role, status=excluded.status, created_at=excluded.created_at""",
                (membership.company_id, membership.user_id, membership.role, membership.status, membership.created_at.isoformat()),
            )
            conn.commit()
        return membership

    def list_company_invites(self, company_id: str) -> list[CompanyInviteSummary]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT * FROM company_invites WHERE company_id = ? ORDER BY created_at DESC",
                (company_id,),
            ).fetchall()
        return [
            CompanyInviteSummary(
                id=row["id"],
                company_id=row["company_id"],
                email=row["email"],
                role=row["role"],
                status=row["status"],
                created_at=_dt(row["created_at"]),
                updated_at=_dt(row["updated_at"]),
                accepted_at=_dt(row["accepted_at"]) if row["accepted_at"] else None,
                created_by_user_id=row["created_by_user_id"],
            )
            for row in rows
        ]

    def list_company_invites_by_email(self, email: str) -> list[CompanyInviteSummary]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT * FROM company_invites WHERE email = ? AND status != 'disabled' ORDER BY created_at DESC",
                (email,),
            ).fetchall()
        return [
            CompanyInviteSummary(
                id=row["id"],
                company_id=row["company_id"],
                email=row["email"],
                role=row["role"],
                status=row["status"],
                created_at=_dt(row["created_at"]),
                updated_at=_dt(row["updated_at"]),
                accepted_at=_dt(row["accepted_at"]) if row["accepted_at"] else None,
                created_by_user_id=row["created_by_user_id"],
            )
            for row in rows
        ]

    def get_company_invite(self, invite_id: str, company_id: str) -> Optional[CompanyInvite]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM company_invites WHERE id = ? AND company_id = ?",
                (invite_id, company_id),
            ).fetchone()
        return _invite_from_row(row) if row else None

    def get_company_invite_by_email(self, company_id: str, email: str) -> Optional[CompanyInvite]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM company_invites WHERE company_id = ? AND email = ?",
                (company_id, email),
            ).fetchone()
        return _invite_from_row(row) if row else None

    def upsert_company_invite(self, invite: CompanyInvite) -> CompanyInvite:
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO company_invites
                   (id, company_id, email, role, status, created_by_user_id, created_at, updated_at, accepted_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET company_id=excluded.company_id, email=excluded.email,
                     role=excluded.role, status=excluded.status, created_by_user_id=excluded.created_by_user_id,
                     created_at=excluded.created_at, updated_at=excluded.updated_at, accepted_at=excluded.accepted_at""",
                (
                    invite.id,
                    invite.company_id,
                    invite.email,
                    invite.role,
                    invite.status,
                    invite.created_by_user_id,
                    invite.created_at.isoformat(),
                    invite.updated_at.isoformat(),
                    _iso(invite.accepted_at),
                ),
            )
            conn.commit()
        return invite

    def delete_company_invite(self, invite_id: str, company_id: str) -> None:
        with self._connection() as conn:
            conn.execute("DELETE FROM company_invites WHERE id = ? AND company_id = ?", (invite_id, company_id))
            conn.commit()

    def record_audit(self, company_id: Optional[str], user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str], metadata: Optional[dict] = None) -> None:
        with self._connection() as conn:
            conn.execute(
                "INSERT INTO audit_events (id, company_id,user_id,action,entity_type,entity_id,metadata_json,created_at) VALUES (?,?,?,?,?,?,?,?)",
                (str(uuid.uuid4()), company_id, user_id, action, entity_type, entity_id,
                 json.dumps(metadata or {}, ensure_ascii=False), datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()

    def _fetch_doc(self, table: str, key: str, company_id: Optional[str]) -> Optional[str]:
        query, params = f"SELECT doc FROM {table} WHERE id = ?", [key]
        if company_id is not None:
            query += " AND company_id = ?"
            params.append(company_id)
        with self._connection() as conn:
            row = conn.execute(query, params).fetchone()
        return row["doc"] if row else None

    def _list_docs(self, table: str, company_id: Optional[str]) -> list[str]:
        query, params = f"SELECT doc FROM {table}", []
        if company_id is not None:
            query += " WHERE company_id = ?"
            params.append(company_id)
        with self._connection() as conn:
            rows = conn.execute(query, params).fetchall()
        return [row["doc"] for row in rows]


def _company_summary(company: Company, membership: CompanyMembership) -> CompanySummary:
    return CompanySummary(id=company.id, name=company.name, slug=company.slug, role=membership.role, created_at=company.created_at)


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _iso(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def _user_from_row(row: Mapping[str, object]) -> UserRecord:
    return UserRecord(
        id=row["id"], email=row["email"], display_name=row["display_name"],
        password_hash=row["password_hash"], auth_provider=row["auth_provider"] or "local",
        google_sub=row["google_sub"] if "google_sub" in row.keys() else None,
        created_at=_dt(row["created_at"]),
        last_login_at=_dt(row["last_login_at"]) if row["last_login_at"] else None,
    )


def _invite_from_row(row: Mapping[str, object]) -> CompanyInvite:
    return CompanyInvite(
        id=row["id"],
        company_id=row["company_id"],
        email=row["email"],
        role=row["role"],
        status=row["status"],
        created_by_user_id=row["created_by_user_id"],
        created_at=_dt(row["created_at"]),
        updated_at=_dt(row["updated_at"]),
        accepted_at=_dt(row["accepted_at"]) if row["accepted_at"] else None,
    )


def build_store(db_url: str) -> Store:
    """Фабрика хранилища по SQLAlchemy URL."""
    return SqliteStore(db_url)


def dumps(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)
