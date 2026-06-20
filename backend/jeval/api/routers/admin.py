"""Управление доступом компании (инвайты): только owner/admin."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException

from ...domain.identity import (
    CompanyInvite,
    CompanyInviteCreateRequest,
    CompanyInviteSummary,
    CompanyInviteUpdateRequest,
)
from ...store import Store
from ..deps import (
    WorkspaceContext,
    admin_workspace_context,
    admin_write_workspace_context,
    get_store,
    now,
)

router = APIRouter(prefix="/api/admin/access", tags=["admin"])


@router.get("", response_model=list[CompanyInviteSummary])
def list_company_access(
    ctx: WorkspaceContext = Depends(admin_workspace_context),
    store: Store = Depends(get_store),
) -> list[CompanyInviteSummary]:
    if not ctx.company_id:
        return []
    return store.list_company_invites(ctx.company_id)


@router.post("", response_model=CompanyInviteSummary, status_code=201)
def create_company_access(
    payload: CompanyInviteCreateRequest,
    ctx: WorkspaceContext = Depends(admin_write_workspace_context),
    store: Store = Depends(get_store),
) -> CompanyInviteSummary:
    if not ctx.company_id:
        raise HTTPException(400, "Не выбрана компания")
    moment = now()
    existing = store.get_company_invite_by_email(ctx.company_id, payload.email)
    invite = CompanyInvite(
        id=existing.id if existing else str(uuid.uuid4()),
        company_id=ctx.company_id,
        email=payload.email,
        role=payload.role,
        status="invited",
        created_by_user_id=ctx.user_id,
        created_at=existing.created_at if existing else moment,
        updated_at=moment,
        accepted_at=existing.accepted_at if existing else None,
    )
    store.upsert_company_invite(invite)
    store.record_audit(
        ctx.company_id, ctx.user_id, "admin.access.upsert", "company_invite", invite.id,
        {"email": invite.email, "role": invite.role},
    )
    return CompanyInviteSummary.model_validate(invite.model_dump())


@router.put("/{invite_id}", response_model=CompanyInviteSummary)
def update_company_access(
    invite_id: str,
    payload: CompanyInviteUpdateRequest,
    ctx: WorkspaceContext = Depends(admin_write_workspace_context),
    store: Store = Depends(get_store),
) -> CompanyInviteSummary:
    if not ctx.company_id:
        raise HTTPException(400, "Не выбрана компания")
    existing = store.get_company_invite(invite_id, ctx.company_id)
    if not existing:
        raise HTTPException(404, "Запись доступа не найдена")
    updated = existing.model_copy(update={"role": payload.role, "status": payload.status, "updated_at": now()})
    store.upsert_company_invite(updated)
    store.record_audit(
        ctx.company_id, ctx.user_id, "admin.access.update", "company_invite", invite_id,
        {"email": updated.email, "role": updated.role, "status": updated.status},
    )
    return CompanyInviteSummary.model_validate(updated.model_dump())


@router.delete("/{invite_id}")
def delete_company_access(
    invite_id: str,
    ctx: WorkspaceContext = Depends(admin_write_workspace_context),
    store: Store = Depends(get_store),
) -> dict[str, bool]:
    if not ctx.company_id:
        raise HTTPException(400, "Не выбрана компания")
    existing = store.get_company_invite(invite_id, ctx.company_id)
    if not existing:
        raise HTTPException(404, "Запись доступа не найдена")
    store.delete_company_invite(invite_id, ctx.company_id)
    store.record_audit(ctx.company_id, ctx.user_id, "admin.access.delete", "company_invite", invite_id, {"email": existing.email})
    return {"ok": True}
