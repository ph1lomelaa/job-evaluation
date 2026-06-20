"""Модели пользователей, компаний, memberships и API авторизации."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


def _now() -> datetime:
    return datetime.now(timezone.utc)


MemberRole = Literal["owner", "admin", "evaluator", "viewer"]
AccessRole = Literal["admin", "viewer"]
AuthProvider = Literal["local", "google"]


class UserRecord(BaseModel):
    """Внутренняя модель. `password_hash` никогда не возвращается из API."""

    id: str
    email: str
    display_name: str
    password_hash: str
    auth_provider: AuthProvider = "local"
    google_sub: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    last_login_at: Optional[datetime] = None


class UserPublic(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: datetime

    @classmethod
    def from_record(cls, user: UserRecord) -> "UserPublic":
        return cls(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            created_at=user.created_at,
        )


class Company(BaseModel):
    id: str
    name: str
    slug: str
    created_by_user_id: str
    onboarding_purpose: Optional[str] = None
    onboarding_role: Optional[str] = None
    organization_size: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


class CompanyMembership(BaseModel):
    company_id: str
    user_id: str
    role: MemberRole = "viewer"
    status: Literal["active", "invited", "disabled"] = "active"
    created_at: datetime = Field(default_factory=_now)


class CompanyInvite(BaseModel):
    id: str
    company_id: str
    email: str
    role: AccessRole = "viewer"
    status: Literal["invited", "active", "disabled"] = "invited"
    created_by_user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    accepted_at: Optional[datetime] = None


class CompanyInviteCreateRequest(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    role: AccessRole = "viewer"

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().casefold()
        local, separator, domain = value.partition("@")
        if not separator or not local or "." not in domain or domain.startswith("."):
            raise ValueError("Некорректный email")
        return value


class CompanyInviteUpdateRequest(BaseModel):
    role: AccessRole
    status: Literal["invited", "active", "disabled"]


class CompanyInviteSummary(BaseModel):
    id: str
    company_id: str
    email: str
    role: AccessRole
    status: Literal["invited", "active", "disabled"]
    created_at: datetime
    updated_at: datetime
    accepted_at: Optional[datetime] = None
    created_by_user_id: Optional[str] = None


class CompanySummary(BaseModel):
    id: str
    name: str
    slug: str
    role: MemberRole
    created_at: datetime


class SessionRecord(BaseModel):
    token_hash: str
    user_id: str
    created_at: datetime = Field(default_factory=_now)
    expires_at: datetime
    last_used_at: datetime = Field(default_factory=_now)


class RegisterRequest(BaseModel):
    display_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("display_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if len(value) < 2:
            raise ValueError("Укажите имя")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().casefold()
        local, separator, domain = value.partition("@")
        if not separator or not local or "." not in domain or domain.startswith("."):
            raise ValueError("Некорректный email")
        return value


class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class CompanyCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    purpose: Optional[str] = Field(default=None, max_length=80)
    user_role: Optional[str] = Field(default=None, max_length=80)
    organization_size: Optional[str] = Field(default=None, max_length=80)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if len(value) < 2:
            raise ValueError("Укажите название компании")
        return value


class AuthResponse(BaseModel):
    access_token: str
    token_type: Literal["cookie"] = "cookie"
    user: UserPublic
    companies: list[CompanySummary] = Field(default_factory=list)
    csrf_token: str


class MeResponse(BaseModel):
    user: UserPublic
    companies: list[CompanySummary] = Field(default_factory=list)
    csrf_token: str
