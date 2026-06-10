// Типизированный клиент к FastAPI-бэкенду (jeval/api).
// Базовый URL — из .env (VITE_API_URL).

import type { Evaluation, GateResult, JobDossier } from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

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
      headers: { "Content-Type": "application/json" },
      ...init,
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
    res = await fetch(`${BASE}${path}`, { method: "POST", body: form });
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
  listPositions: () => request<JobDossier[]>("/api/positions"),
  getPosition: (id: string) => request<JobDossier>(`/api/positions/${id}`),
  createPosition: (body: JobDossier) =>
    request<JobDossier>("/api/positions", { method: "POST", body: JSON.stringify(body) }),
  gateCheck: (id: string) => request<GateResult>(`/api/positions/${id}/gate`, { method: "POST" }),
  uploadDocument: (positionId: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return requestForm<JobDossier>(`/api/positions/${positionId}/documents`, form);
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
};
