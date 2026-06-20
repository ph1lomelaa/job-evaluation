"""Компании: список, создание, переключение активной."""

from __future__ import annotations

import re
import unicodedata
import uuid

from fastapi import APIRouter, Depends, HTTPException

from ...domain.identity import (
    Company,
    CompanyCreateRequest,
    CompanyMembership,
    CompanySummary,
    UserRecord,
)
from ...store import Store
from ..deps import current_user, get_store, now, require_csrf

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.get("", response_model=list[CompanySummary])
def list_companies(
    user: UserRecord = Depends(current_user), store: Store = Depends(get_store)
) -> list[CompanySummary]:
    return store.list_companies_for_user(user.id)


@router.post("", response_model=CompanySummary, status_code=201)
def create_company(
    payload: CompanyCreateRequest,
    user: UserRecord = Depends(current_user),
    store: Store = Depends(get_store),
    _csrf: None = Depends(require_csrf),
) -> CompanySummary:
    moment = now()
    company_id = str(uuid.uuid4())
    company = Company(
        id=company_id,
        name=payload.name,
        slug=f"{_slug(payload.name)}-{company_id[:8]}",
        created_by_user_id=user.id,
        onboarding_purpose=payload.purpose,
        onboarding_role=payload.user_role,
        organization_size=payload.organization_size,
        created_at=moment,
        updated_at=moment,
    )
    membership = CompanyMembership(
        company_id=company_id,
        user_id=user.id,
        role="owner",
        status="active",
        created_at=moment,
    )
    summary = store.create_company(company, membership)
    store.record_audit(company_id, user.id, "company.create", "company", company_id, {"name": company.name})
    return summary


@router.post("/{company_id}/activate", response_model=CompanySummary)
def activate_company(
    company_id: str,
    user: UserRecord = Depends(current_user),
    store: Store = Depends(get_store),
    _csrf: None = Depends(require_csrf),
) -> CompanySummary:
    membership = store.get_membership(user.id, company_id)
    company = next(
        (item for item in store.list_companies_for_user(user.id) if item.id == company_id),
        None,
    )
    if not membership or not company:
        raise HTTPException(404, "Компания не найдена")
    store.record_audit(company_id, user.id, "company.activate", "company", company_id)
    return company


def _slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-")
    return slug or "company"
