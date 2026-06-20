"""Должности (JE-досье): CRUD, Gate 0, загрузка документов, импорт из .docx."""

from __future__ import annotations

import hashlib
import logging
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from ...config import get_settings
from ...domain.enums import DossierReviewStatus
from ...domain.models import DossierImportResult, GateResult, JobDossier
from ...gate import evaluate_gate
from ...importer import build_dossier_from_text, extract_docx_text
from ...importer.agent import DossierExtractionAgent
from ...store import Store
from ..deps import WorkspaceContext, get_store, now, workspace_context, write_workspace_context

router = APIRouter(prefix="/api/positions", tags=["positions"])
logger = logging.getLogger(__name__)

# Произвольные вложения к досье (ДИ, оргструктура, RACI, DoA…): ограничиваем
# тип и размер — раньше эндпоинт принимал любой файл без проверки.
_ALLOWED_DOCUMENT_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg"}
_MAX_DOCUMENT_BYTES = 20 * 1024 * 1024


@router.post("", response_model=JobDossier, status_code=201)
def create_position(
    dossier: JobDossier,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> JobDossier:
    dossier.id = dossier.id or str(uuid.uuid4())
    dossier.company_id = ctx.company_id
    dossier.created_by_user_id = ctx.user_id
    dossier.updated_at = now()
    result = store.save_position(dossier, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "position.create", "position", dossier.id)
    return result


@router.get("", response_model=list[JobDossier])
def list_positions(
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> list[JobDossier]:
    return store.list_positions(ctx.company_id)


@router.get("/{position_id}", response_model=JobDossier)
def get_position(
    position_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> JobDossier:
    pos = store.get_position(position_id, ctx.company_id)
    if not pos:
        raise HTTPException(404, "Должность не найдена")
    return pos


@router.put("/{position_id}", response_model=JobDossier)
def update_position(
    position_id: str,
    dossier: JobDossier,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> JobDossier:
    existing = store.get_position(position_id, ctx.company_id)
    if not existing:
        raise HTTPException(404, "Должность не найдена")
    dossier.id = position_id
    dossier.company_id = ctx.company_id
    dossier.created_by_user_id = existing.created_by_user_id or ctx.user_id
    dossier.created_at = existing.created_at
    dossier.updated_at = now()
    if existing.review_status == DossierReviewStatus.DRAFT_IMPORTED:
        dossier.review_status = DossierReviewStatus.REVIEWED
        dossier.import_metadata = existing.import_metadata
    result = store.save_position(dossier, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "position.update", "position", position_id)
    return result


@router.post("/{position_id}/gate", response_model=GateResult)
def gate_check(
    position_id: str,
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> GateResult:
    pos = store.get_position(position_id, ctx.company_id)
    if not pos:
        raise HTTPException(404, "Должность не найдена")
    return evaluate_gate(pos)


@router.post("/{position_id}/documents", response_model=JobDossier)
async def upload_document(
    position_id: str,
    file: UploadFile,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> JobDossier:
    pos = store.get_position(position_id, ctx.company_id)
    if not pos:
        raise HTTPException(404, "Должность не найдена")
    safe_name = Path(file.filename or "файл").name
    if Path(safe_name).suffix.lower() not in _ALLOWED_DOCUMENT_SUFFIXES:
        raise HTTPException(422, "Недопустимый тип файла. Разрешены: PDF, DOC(X), XLS(X), PNG, JPG.")
    data = await file.read()
    if len(data) > _MAX_DOCUMENT_BYTES:
        raise HTTPException(413, "Файл слишком большой (максимум 20 МБ).")
    target_dir = _upload_directory(get_settings().jeval_upload_dir, ctx.company_id, position_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / safe_name).write_bytes(data)
    if safe_name not in pos.documents:
        pos.documents.append(safe_name)
    pos.updated_at = now()
    store.record_audit(ctx.company_id, ctx.user_id, "position.document_upload", "position", position_id, {"filename": safe_name})
    return store.save_position(pos, ctx.company_id)


# Отдельный роутер: путь /api/import/... не входит в префикс /api/positions,
# но логика тесно связана с созданием досье, поэтому живёт в этом же модуле.
import_router = APIRouter(prefix="/api/import", tags=["import"])


@import_router.post("/document", response_model=DossierImportResult, status_code=201)
async def import_document(
    file: UploadFile,
    use_ai: Optional[bool] = None,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> DossierImportResult:
    settings = get_settings()
    safe_name = Path(file.filename or "document.docx").name
    if not safe_name.lower().endswith(".docx"):
        raise HTTPException(422, "Поддерживается только .docx")
    data = await file.read()
    if len(data) > _MAX_DOCUMENT_BYTES:
        raise HTTPException(413, "Файл слишком большой (максимум 20 МБ).")
    digest = _sha256_hex(data)
    try:
        parsed = extract_docx_text(data)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    should_use_ai = settings.jeval_import_use_ai if use_ai is None else use_ai
    if should_use_ai:
        try:
            result = DossierExtractionAgent().extract(
                parsed.text,
                source_filename=safe_name,
                source_mime_type=file.content_type,
                source_size_bytes=len(data),
                source_sha256=digest,
                source_blocks=parsed.blocks,
            )
        except Exception as exc:
            # Не отдаём текст исключения клиенту — там могут быть детали ответа
            # LLM-провайдера или внутреннего состояния. Подробности — в лог.
            logger.exception("AI-импорт документа не удался")
            raise HTTPException(503, "ИИ-импорт временно недоступен. Попробуйте позже или без ИИ.") from exc
    else:
        result = build_dossier_from_text(
            parsed.text,
            source_filename=safe_name,
            source_mime_type=file.content_type,
            source_size_bytes=len(data),
            source_sha256=digest,
            source_blocks=parsed.blocks,
        )
    result.position.id = result.position.id or str(uuid.uuid4())
    result.position.company_id = ctx.company_id
    result.position.created_by_user_id = ctx.user_id
    moment = now()
    result.position.created_at = moment
    result.position.updated_at = moment
    target_dir = _upload_directory(settings.jeval_upload_dir, ctx.company_id, result.position.id or "")
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / safe_name).write_bytes(data)
    result.position = store.save_position(result.position, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "position.import", "position", result.position.id, {"filename": safe_name})
    return result


def _upload_directory(root: str, company_id: Optional[str], position_id: str) -> Path:
    base = Path(root)
    return base / company_id / position_id if company_id else base / position_id


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()