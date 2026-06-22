// Типизированный клиент к FastAPI-бэкенду (jeval/api).
// Базовый URL — из .env (VITE_API_URL).

import type {
  AuthResponse,
  CalculateResponse,
  Company,
  CompanyInviteSummary,
  DossierImportResult,
  Evaluation,
  FactorLevelReference,
  FactorLevelRules,
  FactorSelections,
  GateResult,
  GradeBand,
  JobDossier,
  MeResponse,
  PublicFormInfo,
  PublicJobForm,
} from "./types";

const BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "http://127.0.0.1:8000" : window.location.origin);
export const API_BASE_URL = BASE;

export const ACTIVE_COMPANY_KEY = "jeval.auth.company.v1";
export const CSRF_TOKEN_KEY = "jeval.auth.csrf.v1";

function sessionHeaders(contentType = true): Record<string, string> {
  const headers: Record<string, string> = {};
  if (contentType) headers["Content-Type"] = "application/json";
  const companyId = window.localStorage.getItem(ACTIVE_COMPANY_KEY);
  if (companyId) headers["X-Company-ID"] = companyId;
  const csrf = window.localStorage.getItem(CSRF_TOKEN_KEY);
  if (csrf) headers["X-CSRF-Token"] = csrf;
  return headers;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      ...init,
      credentials: "include",
      headers: { ...sessionHeaders(), ...(init?.headers ?? {}) },
    });
  } catch {
    throw new ApiError(`Бэкенд недоступен (${BASE}). Запустите: uvicorn jeval.api.main:app`);
  }
  if (!res.ok) {
    // FastAPI кладёт человекочитаемое сообщение в {"detail": ...}
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      /* не JSON — оставляем статус */
    }
    throw new ApiError(detail, res.status);
  }
  return res.json() as Promise<T>;
}

async function requestForm<T>(path: string, form: FormData): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      method: "POST",
      credentials: "include",
      headers: sessionHeaders(false),
      body: form,
    });
  } catch {
    throw new ApiError(`Бэкенд недоступен (${BASE}). Запустите: uvicorn jeval.api.main:app`);
  }
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      /* не JSON */
    }
    throw new ApiError(detail, res.status);
  }
  return res.json() as Promise<T>;
}

export const api = {
  register: (body: { display_name: string; email: string; password: string }) =>
    request<AuthResponse>("/api/auth/register", { method: "POST", body: JSON.stringify(body) }),
  login: (body: { email: string; password: string }) =>
    request<AuthResponse>("/api/auth/login", { method: "POST", body: JSON.stringify(body) }),
  me: () => request<MeResponse>("/api/auth/me"),
  logout: () => request<{ ok: boolean }>("/api/auth/logout", { method: "POST" }),
  listCompanies: () => request<Company[]>("/api/companies"),
  createCompany: (body: {
    name: string;
    purpose?: string;
    user_role?: string;
    organization_size?: string;
  }) => request<Company>("/api/companies", { method: "POST", body: JSON.stringify(body) }),
  activateCompany: (id: string) =>
    request<Company>(`/api/companies/${id}/activate`, { method: "POST" }),
  listGradeBands: () => request<GradeBand[]>("/api/reference/grades"),
  getFactorLevels: () => request<FactorLevelReference>("/api/reference/levels"),
  getFactorLevelRules: () => request<FactorLevelRules>("/api/reference/level-rules"),
  calculateScore: (body: FactorSelections) =>
    request<CalculateResponse>("/api/reference/calculate", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  listPositions: () => request<JobDossier[]>("/api/positions"),
  getPosition: (id: string) => request<JobDossier>(`/api/positions/${id}`),
  createPosition: (body: JobDossier) =>
    request<JobDossier>("/api/positions", { method: "POST", body: JSON.stringify(body) }),
  updatePosition: (id: string, body: JobDossier) =>
    request<JobDossier>(`/api/positions/${id}`, { method: "PUT", body: JSON.stringify(body) }),
  gateCheck: (id: string) => request<GateResult>(`/api/positions/${id}/gate`, { method: "POST" }),
  uploadDocument: (positionId: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return requestForm<JobDossier>(`/api/positions/${positionId}/documents`, form);
  },
  importDocument: (file: File, useAi = false) => {
    const form = new FormData();
    form.append("file", file);
    return requestForm<DossierImportResult>(`/api/import/document?use_ai=${useAi ? "true" : "false"}`, form);
  },
  evaluate: (positionId: string) =>
    request<Evaluation>("/api/evaluations", {
      method: "POST",
      body: JSON.stringify({ position_id: positionId }),
    }),
  getEvaluation: (id: string) => request<Evaluation>(`/api/evaluations/${id}`),
  listEvaluations: (positionId?: string) =>
    request<Evaluation[]>(
      positionId ? `/api/evaluations?position_id=${encodeURIComponent(positionId)}` : "/api/evaluations",
    ),
  finalizeEvaluation: (id: string) =>
    request<Evaluation>(`/api/evaluations/${id}/finalize`, { method: "POST" }),
  listPublicForms: () => request<PublicJobForm[]>("/api/public-forms"),
  createPublicForm: (body: { title: string; recipient?: string; expires_in_days: number }) =>
    request<PublicJobForm>("/api/public-forms", { method: "POST", body: JSON.stringify(body) }),
  markPublicFormRead: (id: string) =>
    request<PublicJobForm>(`/api/public-forms/${id}/read`, { method: "POST" }),
  getPublicForm: (token: string) =>
    request<PublicFormInfo>(`/api/public/forms/${encodeURIComponent(token)}`),
  submitPublicForm: (token: string, body: JobDossier) =>
    request<PublicJobForm>(`/api/public/forms/${encodeURIComponent(token)}`, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  listCompanyAccess: () => request<CompanyInviteSummary[]>("/api/admin/access"),
  createCompanyAccess: (body: { email: string; role: "viewer" | "admin" }) =>
    request<CompanyInviteSummary>("/api/admin/access", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  updateCompanyAccess: (id: string, body: { role: "viewer" | "admin"; status: "invited" | "active" | "disabled" }) =>
    request<CompanyInviteSummary>(`/api/admin/access/${id}`, {
      method: "PUT",
      body: JSON.stringify(body),
    }),
  deleteCompanyAccess: (id: string) =>
    request<{ ok: boolean }>(`/api/admin/access/${id}`, { method: "DELETE" }),
};
