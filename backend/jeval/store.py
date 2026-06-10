"""Простое хранилище должностей и оценок.

Две реализации одного протокола:
  * InMemoryStore — для тестов;
  * SqliteStore   — JSON-документы в SQLite (stdlib sqlite3, без ORM-боилерплейта).
"""

from __future__ import annotations

import json
import sqlite3
import threading
from typing import Optional, Protocol

from .domain.models import Evaluation, JobDossier


class Store(Protocol):
    def save_position(self, dossier: JobDossier) -> JobDossier: ...
    def get_position(self, position_id: str) -> Optional[JobDossier]: ...
    def list_positions(self) -> list[JobDossier]: ...
    def save_evaluation(self, evaluation: Evaluation) -> Evaluation: ...
    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]: ...
    def list_evaluations(self, position_id: Optional[str] = None) -> list[Evaluation]: ...


class InMemoryStore:
    def __init__(self) -> None:
        self._positions: dict[str, JobDossier] = {}
        self._evaluations: dict[str, Evaluation] = {}

    def save_position(self, dossier: JobDossier) -> JobDossier:
        self._positions[dossier.id or ""] = dossier
        return dossier

    def get_position(self, position_id: str) -> Optional[JobDossier]:
        return self._positions.get(position_id)

    def list_positions(self) -> list[JobDossier]:
        return list(self._positions.values())

    def save_evaluation(self, evaluation: Evaluation) -> Evaluation:
        self._evaluations[evaluation.id or ""] = evaluation
        return evaluation

    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        return self._evaluations.get(evaluation_id)

    def list_evaluations(self, position_id: Optional[str] = None) -> list[Evaluation]:
        evs = list(self._evaluations.values())
        if position_id is not None:
            evs = [e for e in evs if e.position_id == position_id]
        return evs


class SqliteStore:
    """JSON-документы в SQLite. Подходит для одного инстанса сервиса."""

    def __init__(self, path: str) -> None:
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS positions (id TEXT PRIMARY KEY, doc TEXT NOT NULL)"
        )
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS evaluations (id TEXT PRIMARY KEY, doc TEXT NOT NULL)"
        )
        self._conn.commit()

    def save_position(self, dossier: JobDossier) -> JobDossier:
        self._upsert("positions", dossier.id or "", dossier.model_dump_json())
        return dossier

    def get_position(self, position_id: str) -> Optional[JobDossier]:
        row = self._fetch("positions", position_id)
        return JobDossier.model_validate_json(row) if row else None

    def list_positions(self) -> list[JobDossier]:
        with self._lock:
            rows = self._conn.execute("SELECT doc FROM positions").fetchall()
        return [JobDossier.model_validate_json(r[0]) for r in rows]

    def save_evaluation(self, evaluation: Evaluation) -> Evaluation:
        self._upsert("evaluations", evaluation.id or "", evaluation.model_dump_json())
        return evaluation

    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        row = self._fetch("evaluations", evaluation_id)
        return Evaluation.model_validate_json(row) if row else None

    def list_evaluations(self, position_id: Optional[str] = None) -> list[Evaluation]:
        with self._lock:
            rows = self._conn.execute("SELECT doc FROM evaluations").fetchall()
        evs = [Evaluation.model_validate_json(r[0]) for r in rows]
        if position_id is not None:
            evs = [e for e in evs if e.position_id == position_id]
        return evs

    def _upsert(self, table: str, key: str, doc: str) -> None:
        with self._lock:
            self._conn.execute(
                f"INSERT INTO {table} (id, doc) VALUES (?, ?) "
                f"ON CONFLICT(id) DO UPDATE SET doc = excluded.doc",
                (key, doc),
            )
            self._conn.commit()

    def _fetch(self, table: str, key: str) -> Optional[str]:
        with self._lock:
            row = self._conn.execute(
                f"SELECT doc FROM {table} WHERE id = ?", (key,)
            ).fetchone()
        return row[0] if row else None


def build_store(db_url: str) -> Store:
    """Фабрика по JEVAL_DB_URL. sqlite:///path → SqliteStore; иначе InMemoryStore."""
    if db_url.startswith("sqlite"):
        # sqlite:///./jeval.db  или  sqlite:////abs/path.db
        path = db_url.split("sqlite:///", 1)[-1].lstrip("/") or "jeval.db"
        if db_url.startswith("sqlite:////"):
            path = "/" + path
        return SqliteStore(path)
    return InMemoryStore()


# ── JSON utility (на случай ручной сериализации) ──────────────────────────────


def dumps(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)
