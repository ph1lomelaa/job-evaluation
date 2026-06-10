"""FastAPI-приложение: должности, Gate 0 и предварительная оценка."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..agent import FakeAgent
from ..config import get_settings
from ..domain.models import Evaluation, GateResult, JobDossier
from ..gate import evaluate_gate
from ..orchestrator import JobEvaluator
from ..store import Store, build_store


class EvaluateRequest(BaseModel):
    position_id: str


def create_app(store: Optional[Store] = None, evaluator: Optional[JobEvaluator] = None) -> FastAPI:
    """Фабрика приложения. store/evaluator можно инъектировать в тестах."""
    settings = get_settings()
    app = FastAPI(title="Платформа оценки должностей (Hay Group)", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.store = store or build_store(settings.jeval_db_url)
    app.state.evaluator = evaluator  # ленивая инициализация (нужен API-ключ)

    def get_store() -> Store:
        return app.state.store

    def get_evaluator() -> JobEvaluator:
        if app.state.evaluator is None:
            if settings.jeval_fake_agent:
                app.state.evaluator = JobEvaluator(agent=FakeAgent())
            elif not settings.anthropic_api_key:
                raise HTTPException(
                    503,
                    "Агент недоступен: ANTHROPIC_API_KEY не задан. "
                    "Укажите ключ в backend/.env или включите офлайн-режим JEVAL_FAKE_AGENT=1.",
                )
            else:
                app.state.evaluator = JobEvaluator()
        return app.state.evaluator

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

    # ── Должности ─────────────────────────────────────────────────────────────

    @app.post("/api/positions", response_model=JobDossier, status_code=201)
    def create_position(dossier: JobDossier, store: Store = Depends(get_store)) -> JobDossier:
        dossier.id = dossier.id or str(uuid.uuid4())
        dossier.updated_at = datetime.now(timezone.utc)
        return store.save_position(dossier)

    @app.get("/api/positions", response_model=list[JobDossier])
    def list_positions(store: Store = Depends(get_store)) -> list[JobDossier]:
        return store.list_positions()

    @app.get("/api/positions/{position_id}", response_model=JobDossier)
    def get_position(position_id: str, store: Store = Depends(get_store)) -> JobDossier:
        pos = store.get_position(position_id)
        if not pos:
            raise HTTPException(404, "Должность не найдена")
        return pos

    @app.post("/api/positions/{position_id}/gate", response_model=GateResult)
    def gate_check(position_id: str, store: Store = Depends(get_store)) -> GateResult:
        pos = store.get_position(position_id)
        if not pos:
            raise HTTPException(404, "Должность не найдена")
        return evaluate_gate(pos)

    @app.post("/api/positions/{position_id}/documents", response_model=JobDossier)
    async def upload_document(
        position_id: str, file: UploadFile, store: Store = Depends(get_store)
    ) -> JobDossier:
        """Загрузить файл досье (ДИ, оргструктура, RACI, DoA…).

        Файл сохраняется в JEVAL_UPLOAD_DIR/{position_id}/, имя добавляется
        в documents. Содержимое пока не парсится (только перечень для Gate 0).
        """
        pos = store.get_position(position_id)
        if not pos:
            raise HTTPException(404, "Должность не найдена")
        safe_name = Path(file.filename or "файл").name
        target_dir = Path(settings.jeval_upload_dir) / position_id
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / safe_name).write_bytes(await file.read())
        if safe_name not in pos.documents:
            pos.documents.append(safe_name)
        pos.updated_at = datetime.now(timezone.utc)
        return store.save_position(pos)

    # ── Оценка ────────────────────────────────────────────────────────────────

    @app.post("/api/evaluations", response_model=Evaluation, status_code=201)
    def create_evaluation(
        req: EvaluateRequest,
        store: Store = Depends(get_store),
        evaluator: JobEvaluator = Depends(get_evaluator),
    ) -> Evaluation:
        pos = store.get_position(req.position_id)
        if not pos:
            raise HTTPException(404, "Должность не найдена")
        peers = _collect_peers(store, exclude_id=pos.id)
        try:
            evaluation = evaluator.evaluate(pos, peers=peers)
        except RuntimeError as exc:  # нет ключа / агент не вернул tool-use
            raise HTTPException(502, f"Ошибка агента: {exc}") from exc
        evaluation.id = evaluation.id or str(uuid.uuid4())
        return store.save_evaluation(evaluation)

    @app.get("/api/evaluations", response_model=list[Evaluation])
    def list_evaluations(
        position_id: Optional[str] = None, store: Store = Depends(get_store)
    ) -> list[Evaluation]:
        return store.list_evaluations(position_id)

    @app.get("/api/evaluations/{evaluation_id}", response_model=Evaluation)
    def get_evaluation(evaluation_id: str, store: Store = Depends(get_store)) -> Evaluation:
        ev = store.get_evaluation(evaluation_id)
        if not ev:
            raise HTTPException(404, "Оценка не найдена")
        return ev

    return app


def _collect_peers(
    store: Store, exclude_id: Optional[str]
) -> list[tuple[JobDossier, Evaluation]]:
    """Другие должности с их последними оценками — для проверки иерархии (9.5)."""
    peers: list[tuple[JobDossier, Evaluation]] = []
    for p in store.list_positions():
        if not p.id or p.id == exclude_id:
            continue
        evaluations = store.list_evaluations(p.id)
        if evaluations:
            latest = max(evaluations, key=lambda e: e.created_at)
            peers.append((p, latest))
    return peers


# Экземпляр по умолчанию для `uvicorn jeval.api.main:app`.
app = create_app()
