// Типы API, синхронные с jeval/domain/models.py, + view-модели для экранов.

export type Confidence = "high" | "medium" | "low";
export type EvaluationStatus = "ready" | "needs_clarification" | "cannot_evaluate";
export type QCStatus = "pass" | "warn" | "fail";
export type Profile = "A" | "P" | "L";
export type DossierReviewStatus = "draft_imported" | "manual_draft" | "reviewed";

// ── Аккаунт и рабочие пространства ──────────────────────────────────────────

export type MemberRole = "owner" | "admin" | "evaluator" | "viewer";
export type AccessRole = "viewer" | "admin";

export interface User {
  id: string;
  email: string;
  display_name: string;
  created_at: string;
}

export interface Company {
  id: string;
  name: string;
  slug: string;
  role: MemberRole;
  created_at: string;
}

export interface CompanyInviteSummary {
  id: string;
  company_id: string;
  email: string;
  role: AccessRole;
  status: "invited" | "active" | "disabled";
  created_at: string;
  updated_at: string;
  accepted_at?: string | null;
  created_by_user_id?: string | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: "cookie";
  user: User;
  companies: Company[];
  csrf_token: string;
}

export interface MeResponse {
  user: User;
  companies: Company[];
  csrf_token: string;
}

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
  company_id?: string | null;
  created_by_user_id?: string | null;
  review_status?: DossierReviewStatus;
  import_metadata?: ImportMetadata | null;
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

export interface ImportMetadata {
  source_filename?: string | null;
  source_type: string;
  source_mime_type?: string | null;
  source_size_bytes?: number | null;
  source_sha256?: string | null;
  extraction_method: string;
  confidence: Confidence;
  notes: string[];
  missing_fields: string[];
  field_sources: Record<string, string[]>;
  raw_text_preview?: string | null;
}

export interface DossierImportResult {
  position: JobDossier;
  raw_text: string;
  extracted_fields: string[];
  missing_fields: string[];
  notes: string[];
}

export interface GradeBand {
  grade: number;
  lower: number;
  mid: number;
  upper: number;
}

// Описания уровней подфакторов с backend (jeval/reference/levels.py) — единый
// источник текста для UI и системного промпта агента, без локальной копии.
export interface FactorLevelReference {
  specialized_know_how: Record<string, string>;
  managerial_know_how: Record<string, string>;
  communication: Record<string, string>;
  problem_area: Record<string, string>;
  problem_complexity: Record<string, string>;
  freedom_to_act: Record<string, string>;
  magnitude: Record<string, string>;
  impact_type: Record<string, string>;
  non_quantitative_impact: Record<string, string>;
}

// Калибровочные анти-паттерны по подфактору (jeval/reference/levels.py,
// *_RULES) — те же ключи, что и FactorLevelReference. Раньше шли только в
// промпт агента, теперь доступны и эксперту-рецензенту в UI.
export type FactorLevelRules = Record<keyof FactorLevelReference, string[]>;

export interface PublicJobForm {
  id: string;
  token: string;
  company_id?: string | null;
  created_by_user_id?: string | null;
  title: string;
  recipient?: string | null;
  status: "active" | "submitted" | "expired";
  is_read: boolean;
  position_id?: string | null;
  created_at: string;
  expires_at: string;
  submitted_at?: string | null;
}

export interface PublicFormInfo {
  title: string;
  recipient?: string | null;
  status: "active" | "submitted" | "expired";
  expires_at: string;
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
  modifier_reason?: string | null;
  adjacent_level?: string | null;
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
  plus_minus: number;
}

export interface AccountabilitySelection extends FactorEvidence {
  freedom: string;
  magnitude: string;
  impact?: string | null;
  non_quantitative_impact?: string | null;
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
  grade_lower: number;
  grade_mid: number;
  grade_upper: number;
  grade_zone: string;
  grade_color: "blue" | "green" | "orange";
  calculation_explanation: string[];
  methodology_basis: string;
  table_version: string;
}

export interface QCFlag {
  code: string;
  severity: "low" | "medium" | "high";
  status: QCStatus;
  message: string;
  recommendation: string;
  factor_groups: string[];
}

export interface Evaluation {
  id?: string | null;
  position_id?: string | null;
  company_id?: string | null;
  created_by_user_id?: string | null;
  status: EvaluationStatus;
  gate: GateResult;
  selections?: FactorSelections | null;
  score?: ScoreResult | null;
  qc_flags: QCFlag[];
  confidence: Confidence;
  is_test_data: boolean;
  role_summary: string;
  reasoning: string;
  clarifying_questions: string[];
  recommendation: string;
  table_version: string;
  created_at: string;
}

// ── View-модели ───────────────────────────────────────────────────────────────

/** Статус должности на дашборде: нет оценки или статус последней оценки. */
export type PositionStatus = "draft_imported" | "not_evaluated" | EvaluationStatus;

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
  draft_imported: "Черновик из документа",
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
