"""Одноразовые публичные формы сбора JE-досье (без авторизации по токену)."""

from __future__ import annotations

import secrets
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from ...domain.enums import DossierReviewStatus
from ...domain.models import JobDossier, PublicFormCreate, PublicFormInfo, PublicJobForm
from ...store import Store
from ..deps import WorkspaceContext, get_store, limit_public_form, now, workspace_context, write_workspace_context

router = APIRouter(prefix="/api/public-forms", tags=["public-forms"])
public_router = APIRouter(prefix="/api/public/forms", tags=["public-forms"])


@router.post("", response_model=PublicJobForm, status_code=201)
def create_public_form(
    payload: PublicFormCreate,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> PublicJobForm:
    moment = now()
    form = PublicJobForm(
        id=str(uuid.uuid4()), token=secrets.token_urlsafe(24),
        company_id=ctx.company_id, created_by_user_id=ctx.user_id,
        title=payload.title.strip(),
        recipient=payload.recipient.strip() if payload.recipient else None,
        created_at=moment, expires_at=moment + timedelta(days=payload.expires_in_days),
    )
    result = store.save_public_form(form, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "public_form.create", "public_form", form.id)
    return result


@router.get("", response_model=list[PublicJobForm])
def list_public_forms(
    ctx: WorkspaceContext = Depends(workspace_context),
    store: Store = Depends(get_store),
) -> list[PublicJobForm]:
    moment = now()
    forms = store.list_public_forms(ctx.company_id)
    for form in forms:
        if form.status == "active" and form.expires_at <= moment:
            form.status = "expired"
            store.save_public_form(form, ctx.company_id)
    return sorted(forms, key=lambda item: item.created_at, reverse=True)


@router.post("/{form_id}/read", response_model=PublicJobForm)
def read_public_form(
    form_id: str,
    ctx: WorkspaceContext = Depends(write_workspace_context),
    store: Store = Depends(get_store),
) -> PublicJobForm:
    form = store.get_public_form(form_id, ctx.company_id)
    if not form:
        raise HTTPException(404, "Форма не найдена")
    form.is_read = True
    return store.save_public_form(form, ctx.company_id)


@public_router.get("/{token}", response_model=PublicFormInfo)
def get_public_form(
    token: str,
    store: Store = Depends(get_store),
    _rate: None = Depends(limit_public_form),
) -> PublicFormInfo:
    form = _active_public_form(token, store)
    return PublicFormInfo(title=form.title, recipient=form.recipient, status=form.status, expires_at=form.expires_at)


@public_router.post("/{token}", response_model=PublicJobForm, status_code=201)
def submit_public_form(
    token: str,
    dossier: JobDossier,
    store: Store = Depends(get_store),
    _rate: None = Depends(limit_public_form),
) -> PublicJobForm:
    form = _active_public_form(token, store)
    moment = now()
    dossier.id = str(uuid.uuid4())
    dossier.company_id = form.company_id
    dossier.review_status = DossierReviewStatus.MANUAL_DRAFT
    dossier.import_metadata = None
    dossier.created_at = moment
    dossier.updated_at = moment
    store.save_position(dossier, form.company_id)
    form.status = "submitted"
    form.position_id = dossier.id
    form.submitted_at = moment
    form.is_read = False
    store.record_audit(form.company_id, None, "public_form.submit", "public_form", form.id, {"position_id": dossier.id})
    return store.save_public_form(form, form.company_id)


def _active_public_form(token: str, store: Store) -> PublicJobForm:
    form = store.get_public_form_by_token(token)
    if not form:
        raise HTTPException(404, "Ссылка на форму не найдена")
    if form.status == "active" and form.expires_at <= now():
        form.status = "expired"
        store.save_public_form(form, form.company_id)
    if form.status == "expired":
        raise HTTPException(410, "Срок действия ссылки истёк")
    if form.status == "submitted":
        raise HTTPException(409, "Форма уже заполнена")
    return form
