"""Регистрация, вход, сессия, Google OAuth."""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
import uuid
from datetime import timedelta
from typing import Optional
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse

from ...config import get_settings
from ...domain.identity import (
    AuthResponse,
    CompanyMembership,
    LoginRequest,
    MeResponse,
    RegisterRequest,
    SessionRecord,
    UserPublic,
    UserRecord,
)
from ...security import (
    hash_password,
    hash_session_token,
    new_session_token,
    normalize_email,
    verify_password,
)
from ...store import Store
from ..deps import (
    CSRF_COOKIE_NAME,
    SESSION_COOKIE_NAME,
    current_user,
    get_store,
    limit_login,
    limit_register,
    now,
    require_csrf,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

GOOGLE_STATE_COOKIE_NAME = "jeval_google_state"
GOOGLE_VERIFIER_COOKIE_NAME = "jeval_google_verifier"

GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_TOKENINFO_ENDPOINT = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"


def issue_auth(user: UserRecord, store: Store, response: Response) -> AuthResponse:
    settings = get_settings()
    moment = now()
    token = new_session_token()
    csrf_token = new_session_token()
    store.save_session(
        SessionRecord(
            token_hash=hash_session_token(token),
            user_id=user.id,
            created_at=moment,
            expires_at=moment + timedelta(days=settings.jeval_session_days),
            last_used_at=moment,
        )
    )
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.jeval_env == "production",
        max_age=settings.jeval_session_days * 24 * 60 * 60,
        path="/",
    )
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=csrf_token,
        httponly=False,
        samesite="lax",
        secure=settings.jeval_env == "production",
        max_age=settings.jeval_session_days * 24 * 60 * 60,
        path="/",
    )
    return AuthResponse(
        access_token=token,
        user=UserPublic.from_record(user),
        companies=store.list_companies_for_user(user.id),
        csrf_token=csrf_token,
    )


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    payload: RegisterRequest,
    response: Response,
    store: Store = Depends(get_store),
    _rate: None = Depends(limit_register),
) -> AuthResponse:
    email = normalize_email(payload.email)
    if store.get_user_by_email(email):
        raise HTTPException(409, "Аккаунт с таким email уже существует")
    user = UserRecord(
        id=str(uuid.uuid4()),
        email=email,
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
    )
    try:
        store.create_user(user)
    except ValueError as exc:
        raise HTTPException(409, "Аккаунт с таким email уже существует") from exc
    store.record_audit(None, user.id, "auth.register", "user", user.id)
    return issue_auth(user, store, response)


@router.post("/login", response_model=AuthResponse)
def login(
    payload: LoginRequest,
    response: Response,
    store: Store = Depends(get_store),
    _rate: None = Depends(limit_login),
) -> AuthResponse:
    user = store.get_user_by_email(normalize_email(payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Неверный email или пароль")
    moment = now()
    store.update_user_login(user.id, moment)
    user.last_login_at = moment
    store.record_audit(None, user.id, "auth.login", "user", user.id)
    return issue_auth(user, store, response)


@router.get("/me", response_model=MeResponse)
def me(
    user: UserRecord = Depends(current_user),
    csrf_cookie: Optional[str] = Cookie(default=None, alias=CSRF_COOKIE_NAME),
    store: Store = Depends(get_store),
) -> MeResponse:
    csrf_token = csrf_cookie.strip() if csrf_cookie and csrf_cookie.strip() else ""
    return MeResponse(
        user=UserPublic.from_record(user),
        companies=store.list_companies_for_user(user.id),
        csrf_token=csrf_token,
    )


@router.post("/logout")
def logout(
    response: Response,
    session_cookie: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    user: UserRecord = Depends(current_user),
    store: Store = Depends(get_store),
    _csrf: None = Depends(require_csrf),
) -> dict[str, bool]:
    token = session_cookie.strip() if session_cookie and session_cookie.strip() else None
    if token:
        store.delete_session(hash_session_token(token))
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    response.delete_cookie(key=CSRF_COOKIE_NAME, path="/")
    store.record_audit(None, user.id, "auth.logout", "user", user.id)
    return {"ok": True}


@router.get("/google/start")
def google_start() -> Response:
    settings = get_settings()
    if not settings.jeval_google_enabled or not settings.jeval_google_client_id or not settings.jeval_google_client_secret:
        raise HTTPException(503, "Google login не настроен")
    state = secrets.token_urlsafe(24)
    verifier = secrets.token_urlsafe(64)
    redirect_uri = settings.jeval_google_redirect_uri
    params = {
        "client_id": settings.jeval_google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "code_challenge": _pkce_challenge(verifier),
        "code_challenge_method": "S256",
        "prompt": "select_account",
    }
    response = RedirectResponse(f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}", status_code=302)
    _set_oauth_cookie(response, GOOGLE_STATE_COOKIE_NAME, state, settings)
    _set_oauth_cookie(response, GOOGLE_VERIFIER_COOKIE_NAME, verifier, settings)
    return response


@router.get("/google/callback", name="google_callback")
def google_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    oauth_state: Optional[str] = Cookie(default=None, alias=GOOGLE_STATE_COOKIE_NAME),
    oauth_verifier: Optional[str] = Cookie(default=None, alias=GOOGLE_VERIFIER_COOKIE_NAME),
    store: Store = Depends(get_store),
) -> Response:
    settings = get_settings()
    frontend_root = settings.jeval_frontend_url.rstrip("/")
    if error:
        response = RedirectResponse(f"{frontend_root}/?auth_error={error}", status_code=302)
        _clear_oauth_cookies(response)
        return response
    if not code or not state or not oauth_state or not oauth_verifier or state != oauth_state:
        response = RedirectResponse(f"{frontend_root}/?auth_error=google_state", status_code=302)
        _clear_oauth_cookies(response)
        return response
    try:
        profile = _fetch_google_profile(
            code=code,
            code_verifier=oauth_verifier,
            client_id=settings.jeval_google_client_id,
            client_secret=settings.jeval_google_client_secret,
            redirect_uri=settings.jeval_google_redirect_uri,
        )
    except HTTPException as exc:
        response = RedirectResponse(f"{frontend_root}/?auth_error=google_{exc.status_code}", status_code=302)
        _clear_oauth_cookies(response)
        return response

    email = normalize_email(profile["email"])
    display_name = profile.get("name") or email.split("@", 1)[0]
    google_sub = profile["sub"]
    invite_matches = store.list_company_invites_by_email(email)
    # ВРЕМЕННО для разработки (JEVAL_DISABLE_ACCESS_GATE=1): allowlist-проверка
    # ниже (приглашение или уже состоящий в компании пользователь) пропускается
    # целиком. RBAC после входа (роли в компаниях) не затрагивается — просто
    # новый пользователь проходит дальше без приглашения, как при обычной
    # email/password-регистрации. По умолчанию флаг False — ветка не меняет
    # поведение, пока её явно не включили.
    if not settings.jeval_disable_access_gate and not invite_matches:
        existing = store.get_user_by_email(email)
        if not existing:
            response = RedirectResponse(f"{frontend_root}/?auth_error=access_denied", status_code=302)
            _clear_oauth_cookies(response)
            return response
        allowed_company_ids = [summary.id for summary in store.list_companies_for_user(existing.id)]
        if not allowed_company_ids:
            response = RedirectResponse(f"{frontend_root}/?auth_error=access_denied", status_code=302)
            _clear_oauth_cookies(response)
            return response
    user = store.get_user_by_google_sub(google_sub) or store.get_user_by_email(email)
    if user and user.google_sub and user.google_sub != google_sub:
        response = RedirectResponse(f"{frontend_root}/?auth_error=google_conflict", status_code=302)
        _clear_oauth_cookies(response)
        return response
    moment = now()
    if user is None:
        user = UserRecord(
            id=str(uuid.uuid4()),
            email=email,
            display_name=display_name,
            password_hash=secrets.token_urlsafe(32),
            auth_provider="google",
            google_sub=google_sub,
        )
        store.create_user(user)
    else:
        store.update_user_identity(user.id, "google", google_sub)
        if user.display_name != display_name and display_name:
            user.display_name = display_name
    store.update_user_login(user.id, moment)

    for invite_summary in invite_matches:
        invite = store.get_company_invite(invite_summary.id, invite_summary.company_id)
        if not invite or invite.status == "disabled":
            continue
        membership = store.get_membership(user.id, invite.company_id)
        role = "admin" if invite.role == "admin" else "viewer"
        if membership and membership.role == "owner":
            role = "owner"
        store.upsert_membership(
            CompanyMembership(
                company_id=invite.company_id,
                user_id=user.id,
                role=role,
                status="active",
                created_at=membership.created_at if membership else moment,
            )
        )
        updated_invite = invite.model_copy(update={"status": "active", "accepted_at": moment, "updated_at": moment})
        store.upsert_company_invite(updated_invite)

    response = RedirectResponse(f"{frontend_root}/", status_code=302)
    issue_auth(user, store, response)
    _clear_oauth_cookies(response)
    return response


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _set_oauth_cookie(response: Response, key: str, value: str, settings) -> None:
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        samesite="lax",
        secure=settings.jeval_env == "production",
        max_age=600,
        path="/",
    )


def _clear_oauth_cookies(response: Response) -> None:
    response.delete_cookie(key=GOOGLE_STATE_COOKIE_NAME, path="/")
    response.delete_cookie(key=GOOGLE_VERIFIER_COOKIE_NAME, path="/")


def _fetch_google_profile(
    *,
    code: str,
    code_verifier: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
) -> dict[str, str]:
    token_payload = urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")
    token_request = UrlRequest(
        GOOGLE_TOKEN_ENDPOINT,
        data=token_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(token_request, timeout=15) as response:
            token_data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - network path
        raise HTTPException(503, f"Не удалось обменять Google code: {exc}") from exc

    id_token = token_data.get("id_token")
    if not id_token:
        raise HTTPException(503, "Google не вернул id_token")

    profile_request = UrlRequest(f"{GOOGLE_TOKENINFO_ENDPOINT}?{urlencode({'id_token': id_token})}", method="GET")
    try:
        with urlopen(profile_request, timeout=15) as response:
            profile = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - network path
        raise HTTPException(503, f"Не удалось проверить Google profile: {exc}") from exc

    if profile.get("aud") != client_id:
        raise HTTPException(403, "Google token audience mismatch")
    if str(profile.get("email_verified")).lower() not in {"true", "1"}:
        raise HTTPException(403, "Google email не подтверждён")
    email = profile.get("email")
    sub = profile.get("sub")
    if not email or not sub:
        raise HTTPException(403, "Google profile неполный")
    return {"email": email, "sub": sub, "name": profile.get("name") or ""}
