// Преобразование API-моделей (jeval/domain) в view-модели экранов.

import type {
  Confidence,
  Evaluation,
  FactorGroup,
  FactorLevelReference,
  FactorLevelRules,
  JobDossier,
  PositionRow,
  ScoreResult,
} from "./types";

// Заглушки до первого фетча справочника уровней/правил (GET /api/reference/levels,
// /api/reference/level-rules) — используются и карточкой оценки, и сверкой версий.
export const EMPTY_FACTOR_LEVELS: FactorLevelReference = {
  specialized_know_how: {},
  managerial_know_how: {},
  communication: {},
  problem_area: {},
  problem_complexity: {},
  freedom_to_act: {},
  magnitude: {},
  impact_type: {},
  non_quantitative_impact: {},
};

export const EMPTY_FACTOR_RULES: FactorLevelRules = {
  specialized_know_how: [],
  managerial_know_how: [],
  communication: [],
  problem_area: [],
  problem_complexity: [],
  freedom_to_act: [],
  magnitude: [],
  impact_type: [],
  non_quantitative_impact: [],
};

/** Последняя оценка для каждой должности (по created_at). */
export function latestByPosition(evaluations: Evaluation[]): Map<string, Evaluation> {
  const map = new Map<string, Evaluation>();
  for (const ev of evaluations) {
    if (!ev.position_id) continue;
    const prev = map.get(ev.position_id);
    if (!prev || ev.created_at > prev.created_at) map.set(ev.position_id, ev);
  }
  return map;
}

export function toPositionRow(dossier: JobDossier, latest?: Evaluation): PositionRow {
  return {
    id: dossier.id ?? "",
    name: dossier.name,
    dzo: dossier.dzo ?? "—",
    function: dossier.function ?? "—",
    status: latest?.status ?? (dossier.review_status === "draft_imported" ? "draft_imported" : "not_evaluated"),
    grade: latest?.score?.grade ?? null,
    confidence: latest ? latest.confidence : null,
    updatedAt: (dossier.updated_at ?? "").slice(0, 10),
  };
}

// ── Коды факторов (формат из инструкции, разделы 5–7) ─────────────────────────

function pm(plusMinus: number): string {
  return plusMinus > 0 ? "+" : plusMinus < 0 ? "−" : "";
}

/** Know-How: «E / III / 2», Problem Solving: «E / 4 / 43%», Accountability: «E / N / IV». */
export function factorCodes(score: ScoreResult): Record<FactorGroup, string> {
  const kh = score.know_how.selection;
  const ps = score.problem_solving.selection;
  const acc = score.accountability.selection;
  return {
    know_how: `${kh.specialization} / ${kh.management} / ${kh.communication}${pm(kh.plus_minus)}`,
    problem_solving: `${ps.area} / ${ps.complexity}${pm(ps.plus_minus ?? 0)} / ${score.problem_solving.percentage}%`,
    accountability: `${acc.freedom} / ${acc.magnitude} / ${acc.non_quantitative_impact ?? acc.impact ?? "—"}${pm(acc.plus_minus)}`,
  };
}

export interface SubfactorRow {
  name: string;
  level: string;
  description: string;
  expertCheck: string;
  rules: string[];
}

const NO_RULES: string[] = [];

function detail(
  name: string,
  level: string,
  levels: Record<string, string>,
  expertCheck: string,
  rules: string[] = NO_RULES,
): SubfactorRow {
  return {
    name,
    level,
    description: levels[level] ?? "Описание уровня отсутствует.",
    expertCheck,
    rules,
  };
}

/** Строки подфакторов для факторной таблицы (уровни — по группам).
 * Тексты уровней приходят с backend (`GET /api/reference/levels`) — тот же
 * справочник, что и в системном промпте агента, без отдельной копии на фронте.
 * `rules` (`GET /api/reference/level-rules`) — те же калибровочные анти-
 * паттерны, что видит агент в промпте, теперь видимые и эксперту-рецензенту. */
export function subfactorRows(
  score: ScoreResult,
  levels: FactorLevelReference,
  rules: FactorLevelRules,
): Record<FactorGroup, SubfactorRow[]> {
  const kh = score.know_how.selection;
  const ps = score.problem_solving.selection;
  const acc = score.accountability.selection;
  return {
    know_how: [
      detail("Специальные / практические знания", kh.specialization, levels.specialized_know_how,
        "Какая глубина и широта знаний действительно необходима для стандартного выполнения роли, независимо от диплома и стажа работника?",
        rules.specialized_know_how),
      detail("Планирование, организация и интеграция", kh.management, levels.managerial_know_how,
        "Сколько разных процессов или функций роль должна интегрировать и какие компромиссы между ними принимает?",
        rules.managerial_know_how),
      detail("Коммуникации и воздействие", kh.communication, levels.communication,
        "Роль только передаёт информацию, рационально убеждает или должна менять позицию людей при реальном сопротивлении?",
        rules.communication),
    ],
    problem_solving: [
      detail("Область решаемых вопросов / свобода мышления", ps.area, levels.problem_area,
        "Насколько правила, процедуры, политики и помощь заранее определяют, что и как должна решать роль?",
        rules.problem_area),
      detail("Сложность решаемых вопросов", String(ps.complexity), levels.problem_complexity,
        "Насколько решения повторяются и какие типовые кейсы подтверждают необходимость адаптации, синтеза или новых концепций?",
        rules.problem_complexity),
    ],
    accountability: [
      detail("Свобода действий", acc.freedom, levels.freedom_to_act,
        "Какие решения роль принимает сама, что согласует, как контролируется результат и через какой период видны последствия?",
        rules.freedom_to_act),
      detail("Ветка величины", acc.magnitude, levels.magnitude,
        "В KMG DIGITAL используется N: доход, выручка и денежные диапазоны не участвуют в оценке.",
        rules.magnitude),
      detail("Неколичественный уровень воздействия", acc.non_quantitative_impact ?? acc.impact ?? "—",
        acc.non_quantitative_impact ? levels.non_quantitative_impact : levels.impact_type,
        "Каков реальный организационный охват роли: отдельная услуга, подразделение, несколько функций, критичная система, команды или политика всей организации?",
        acc.non_quantitative_impact ? rules.non_quantitative_impact : rules.impact_type),
    ],
  };
}

export interface GroupEvidence {
  evidence: string[];
  doubts: string[];
  confidence: Confidence;
  plusMinus: number;
  modifierReason: string | null;
  adjacentLevel: string | null;
}

export function groupEvidence(score: ScoreResult): Record<FactorGroup, GroupEvidence> {
  return {
    know_how: pick(score.know_how.selection),
    problem_solving: pick(score.problem_solving.selection),
    accountability: pick(score.accountability.selection),
  };
}

function pick(s: {
  evidence: string[];
  doubts: string[];
  confidence: Confidence;
  plus_minus: number;
  modifier_reason?: string | null;
  adjacent_level?: string | null;
}): GroupEvidence {
  return {
    evidence: s.evidence,
    doubts: s.doubts,
    confidence: s.confidence,
    plusMinus: s.plus_minus,
    modifierReason: s.modifier_reason ?? null,
    adjacentLevel: s.adjacent_level ?? null,
  };
}

// ── Форматирование ────────────────────────────────────────────────────────────

const nf = new Intl.NumberFormat("ru-RU");

export function formatMoney(v?: number | null): string | null {
  if (v == null) return null;
  if (v >= 1e9) return `${nf.format(Math.round((v / 1e9) * 10) / 10)} млрд ₸`;
  if (v >= 1e6) return `${nf.format(Math.round((v / 1e6) * 10) / 10)} млн ₸`;
  return `${nf.format(v)} ₸`;
}

/** Краткая строка масштаба для шапки карточки. */
export function scopeSummary(d: JobDossier): string[] {
  const parts: string[] = [];
  const opex = formatMoney(d.scope.annual_opex);
  const capex = formatMoney(d.scope.annual_capex);
  const revenue = formatMoney(d.scope.annual_revenue);
  if (opex) parts.push(`OPEX ${opex}/год`);
  if (capex) parts.push(`CAPEX ${capex}/год`);
  if (revenue) parts.push(`выручка ${revenue}/год`);
  if (d.scope.headcount != null) parts.push(`${nf.format(d.scope.headcount)} чел.`);
  if (d.scope.assets) parts.push(d.scope.assets);
  return parts;
}
