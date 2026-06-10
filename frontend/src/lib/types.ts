// Типы API, синхронные с jeval/domain/models.py, + view-модели для экранов.

export type Confidence = "high" | "medium" | "low";
export type EvaluationStatus = "ready" | "needs_clarification" | "cannot_evaluate";
export type QCStatus = "pass" | "warn" | "fail";
export type Profile = "A" | "P" | "L";

// ── JE-досье (вход) ───────────────────────────────────────────────────────────

export interface ApprovalItem {
  item: string;
  approver: string;
}

export interface Authorities {
  decides_alone: string[];
  requires_approval: ApprovalItem[];
  recommends: string[];
}

export interface Scope {
  annual_opex?: number | null;
  annual_capex?: number | null;
  annual_revenue?: number | null;
  function_budget?: number | null;
  project_portfolio?: number | null;
  headcount?: number | null;
  assets?: string | null;
  source?: string | null;
}

export interface Reporting {
  manager?: string | null;
  subordinates: string[];
  matrix_links: string[];
}

/** Структурированный кейс Problem Solving (минимальный пакет доказательств). */
export interface ProblemCase {
  summary: string;
  given?: string | null;
  unknown?: string | null;
  alternatives?: string | null;
  tradeoff?: string | null;
  verification?: string | null;
  is_typical?: boolean;
}

export interface JobDossier {
  id?: string | null;
  name: string;
  dzo?: string | null;
  department?: string | null;
  function?: string | null;
  snapshot_date?: string | null;
  purpose?: string | null;
  key_results: string[];
  responsibilities: string[];
  kpis: string[];
  reporting: Reporting;
  authorities: Authorities;
  scope: Scope;
  limits: string[];
  stakeholders: string[];
  organizational_context?: string | null;
  anchor_roles: string[];
  problem_cases: string[];
  problem_cases_structured: ProblemCase[];
  documents: string[];
  confirmed_by?: string | null;
  created_at?: string;
  updated_at?: string;
}

// ── Gate 0 ────────────────────────────────────────────────────────────────────

export interface GateCheck {
  block: string;
  status: QCStatus;
  note?: string | null;
}

export interface GateResult {
  status: EvaluationStatus;
  checks: GateCheck[];
  missing_fields: string[];
  warnings: string[];
}

// ── Выбор уровней (выход агента) и расчёт (выход движка) ─────────────────────

interface FactorEvidence {
  evidence: string[];
  doubts: string[];
  confidence: Confidence;
}

export interface KnowHowSelection extends FactorEvidence {
  specialization: string;
  management: string;
  communication: string;
  plus_minus: number;
}

export interface ProblemSolvingSelection extends FactorEvidence {
  area: string;
  complexity: number;
}

export interface AccountabilitySelection extends FactorEvidence {
  freedom: string;
  magnitude: string;
  impact: string;
  plus_minus: number;
}

export interface FactorSelections {
  know_how: KnowHowSelection;
  problem_solving: ProblemSolvingSelection;
  accountability: AccountabilitySelection;
}

export interface ScoreResult {
  know_how: { selection: KnowHowSelection; points: number };
  problem_solving: { selection: ProblemSolvingSelection; percentage: number; points: number };
  accountability: { selection: AccountabilitySelection; points: number };
  total_points: number;
  profile: Profile;
  profile_steps: number;
  /** Континуум P4…P1, L, A1…A4; «*» — вне допустимых пределов. */
  profile_long: string;
  grade: number;
}

export interface QCFlag {
  code: string;
  severity: "low" | "medium" | "high";
  status: QCStatus;
  message: string;
  recommendation: string;
}

export interface Evaluation {
  id?: string | null;
  position_id?: string | null;
  status: EvaluationStatus;
  gate: GateResult;
  selections?: FactorSelections | null;
  score?: ScoreResult | null;
  qc_flags: QCFlag[];
  confidence: Confidence;
  role_summary: string;
  reasoning: string;
  clarifying_questions: string[];
  recommendation: string;
  created_at: string;
}

// ── View-модели ───────────────────────────────────────────────────────────────

/** Статус должности на дашборде: нет оценки или статус последней оценки. */
export type PositionStatus = "not_evaluated" | EvaluationStatus;

export interface PositionRow {
  id: string;
  name: string;
  dzo: string;
  function: string;
  status: PositionStatus;
  grade: number | null;
  confidence: Confidence | null;
  updatedAt: string;
}

export type FactorGroup = "know_how" | "problem_solving" | "accountability";

export const FACTOR_GROUP_LABEL: Record<FactorGroup, string> = {
  know_how: "Знания и умения · Know-How",
  problem_solving: "Решение вопросов · Problem Solving",
  accountability: "Ответственность · Accountability",
};

export const STATUS_LABEL: Record<PositionStatus, string> = {
  not_evaluated: "Не оценена",
  ready: "Готово к комитету",
  needs_clarification: "Требуются уточнения",
  cannot_evaluate: "Невозможно оценить",
};

export const CONFIDENCE_LABEL: Record<Confidence, string> = {
  high: "Высокая",
  medium: "Средняя",
  low: "Низкая",
};

export const PROFILE_LABEL: Record<Profile, string> = {
  A: "A — ответственность выше",
  P: "P — решение вопросов выше",
  L: "L — сбалансированный",
};
