// Преобразование API-моделей (jeval/domain) в view-модели экранов.

import type {
  Confidence,
  Evaluation,
  FactorGroup,
  JobDossier,
  PositionRow,
  ScoreResult,
} from "./types";

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
    status: latest?.status ?? "not_evaluated",
    grade: latest?.score?.grade ?? null,
    confidence: latest ? latest.confidence : null,
    updatedAt: (dossier.updated_at ?? "").slice(0, 10),
  };
}

// ── Коды факторов (формат из инструкции, разделы 5–7) ─────────────────────────

function pm(plusMinus: number): string {
  return plusMinus > 0 ? "+" : plusMinus < 0 ? "−" : "";
}

/** Know-How: «E / III / 2», Problem Solving: «E / 4 / 43%», Accountability: «E / 3 / S». */
export function factorCodes(score: ScoreResult): Record<FactorGroup, string> {
  const kh = score.know_how.selection;
  const ps = score.problem_solving.selection;
  const acc = score.accountability.selection;
  return {
    know_how: `${kh.specialization} / ${kh.management} / ${kh.communication}${pm(kh.plus_minus)}`,
    problem_solving: `${ps.area} / ${ps.complexity} / ${score.problem_solving.percentage}%`,
    accountability: `${acc.freedom} / ${acc.magnitude} / ${acc.impact}${pm(acc.plus_minus)}`,
  };
}

export interface SubfactorRow {
  name: string;
  level: string;
}

/** Строки подфакторов для факторной таблицы (уровни — по группам). */
export function subfactorRows(score: ScoreResult): Record<FactorGroup, SubfactorRow[]> {
  const kh = score.know_how.selection;
  const ps = score.problem_solving.selection;
  const acc = score.accountability.selection;
  return {
    know_how: [
      { name: "Специальные / практические знания", level: kh.specialization },
      { name: "Управленческие знания", level: kh.management },
      { name: "Коммуникации и воздействие", level: kh.communication },
    ],
    problem_solving: [
      { name: "Область решаемых вопросов", level: ps.area },
      { name: "Сложность решаемых вопросов", level: String(ps.complexity) },
    ],
    accountability: [
      { name: "Свобода действий", level: acc.freedom },
      { name: "Величина воздействия", level: acc.magnitude },
      { name: "Тип влияния", level: acc.impact },
    ],
  };
}

export function groupEvidence(score: ScoreResult): Record<FactorGroup, { evidence: string[]; doubts: string[]; confidence: Confidence }> {
  return {
    know_how: pick(score.know_how.selection),
    problem_solving: pick(score.problem_solving.selection),
    accountability: pick(score.accountability.selection),
  };
}

function pick(s: { evidence: string[]; doubts: string[]; confidence: Confidence }) {
  return { evidence: s.evidence, doubts: s.doubts, confidence: s.confidence };
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
