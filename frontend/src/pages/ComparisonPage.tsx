import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Card, ErrorBanner, Field, Skeleton } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { groupEvidence, latestByPosition } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import { PROFILE_LABEL, type Evaluation, type FactorGroup, type Profile, type ScoreResult } from "../lib/types";

interface RoleCol {
  id: string;
  name: string;
  grade: number;
  profile: Profile;
  profileLong: string;
  total: number;
  knowHow: number;
  problemSolving: number;
  accountability: number;
  tableVersion: string;
}

function toCol(id: string, name: string, s: ScoreResult): RoleCol {
  return {
    id,
    name,
    grade: s.grade,
    profile: s.profile,
    profileLong: s.profile_long || s.profile,
    total: s.total_points,
    knowHow: s.know_how.points,
    problemSolving: s.problem_solving.points,
    accountability: s.accountability.points,
    tableVersion: s.table_version,
  };
}

export default function ComparisonPage() {
  const [params] = useSearchParams();
  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.listPositions(), api.listEvaluations()]),
    [],
  );

  // Последняя оценка на должность — переиспользуется и для карточек с баллами,
  // и для блока "Обоснование" (evidence/doubts по факторной группе), чтобы не
  // ходить за полной Evaluation отдельным запросом.
  const latestEvalByPosition = useMemo<Map<string, Evaluation>>(
    () => (data ? latestByPosition(data[1]) : new Map()),
    [data],
  );

  // Все должности с рассчитанной оценкой.
  const evaluated = useMemo<RoleCol[]>(() => {
    if (!data) return [];
    const [positions] = data;
    return positions.flatMap((p) => {
      const score = p.id ? latestEvalByPosition.get(p.id)?.score : null;
      return p.id && score ? [toCol(p.id, p.name, score)] : [];
    });
  }, [data, latestEvalByPosition]);

  const [currentId, setCurrentId] = useState(params.get("id") ?? "");
  const [anchorIds, setAnchorIds] = useState<[string, string]>(["", ""]);

  const current =
    evaluated.find((r) => r.id === currentId) ?? (currentId === "" ? evaluated[0] : undefined);
  const anchors = anchorIds
    .map((id) => evaluated.find((r) => r.id === id))
    .filter((r): r is RoleCol => r != null && r.id !== current?.id);
  const defaultAnchors = useMemo(() => {
    const pool = evaluated.filter((r) => r.id !== current?.id);
    if (!current) return pool.slice(0, 2);
    return pool
      .sort((a, b) => Math.abs(a.grade - current.grade) - Math.abs(b.grade - current.grade))
      .slice(0, 2);
  }, [current, evaluated]);
  const shownAnchors = anchors.length > 0 ? anchors : defaultAnchors;
  const comparisons = useMemo(
    () =>
      current
        ? shownAnchors.map((anchor) => buildComparison(current, anchor, latestEvalByPosition))
        : [],
    [current, shownAnchors, latestEvalByPosition],
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-[32px]">Сравнение с якорями</h1>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          {Array.from({ length: 3 }, (_, i) => (
            <Skeleton key={i} className="h-72" />
          ))}
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-[32px]">Сравнение с якорями</h1>
        <ErrorBanner message={error} onRetry={reload} />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-[32px] text-center">Сравнение</h1>

      {evaluated.length === 0 ? (
        <Card className="p-10 text-center text-muted">
          Нет оценённых должностей. Создайте должность и запустите предварительную оценку.
        </Card>
      ) : (
        <>
          {/* Выбор ролей */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <Field label="Текущая должность">
              <select
                className="field"
                value={current?.id ?? ""}
                onChange={(e) => setCurrentId(e.target.value)}
              >
                {evaluated.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            </Field>
            {[0, 1].map((i) => (
              <Field key={i} label={`Якорь ${i + 1}`} hint="Авто = ближайшие по грейду">
                <select
                  className="field"
                  value={anchorIds[i]}
                  onChange={(e) =>
                    setAnchorIds((prev) => {
                      const next: [string, string] = [...prev];
                      next[i] = e.target.value;
                      return next;
                    })
                  }
                >
                  <option value="">Авто</option>
                  {evaluated
                    .filter((r) => r.id !== current?.id)
                    .map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.name}
                      </option>
                    ))}
                </select>
              </Field>
            ))}
          </div>


          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            {current && <RoleCard role={current} current />}
            {shownAnchors.map((r) => (
              <RoleCard key={r.id} role={r} />
            ))}
          </div>

          {current && shownAnchors.length > 0 && comparisons.length > 0 && (
            <Card>
              <div className="mb-4 text-sm font-medium">Анализ различий</div>
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                {comparisons.map((item) => (
                  <div
                    key={item.anchor.id}
                    className="rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-4"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="text-xs uppercase tracking-wide text-muted">Якорь</div>
                        <div className="mt-1 text-sm font-medium">{item.anchor.name}</div>
                      </div>
                      <div className={cn("text-right", gradeTone(item.gradeGap))}>
                        <div className="num text-3xl">{gradeGapText(item.gradeGap)}</div>
                        <div className="text-xs text-muted">грейда</div>
                      </div>
                    </div>

                    <dl className="mt-4 space-y-3 text-sm">
                      <Line label="Итоговые баллы" value={formatGap(item.totalGap, current.total, item.anchor.total)} />
                      <Line label="Профиль" value={item.profileText} />
                      <Line label="Главное отличие" value={item.primaryDifference} />
                      <Line label="Факторы" value={item.factorNotes.join(" · ")} />
                    </dl>

                    {item.versionMismatch && (
                      <div className="mt-3 rounded-lg bg-warn/10 px-3 py-2 text-xs text-warn">
                        Оценки посчитаны по разным версиям методологии ({current.tableVersion} и{" "}
                        {item.anchor.tableVersion}) — сравнение может быть некорректным.
                      </div>
                    )}

                    {(item.currentEvidence || item.anchorEvidence) && (
                      <div className="mt-4 border-t border-[rgb(var(--row-divider))] pt-3">
                        <div className="text-xs uppercase tracking-wide text-muted">
                          Обоснование · {item.biggestFactor.label}
                        </div>
                        <div className="mt-2 grid grid-cols-2 gap-3 text-xs">
                          <EvidenceColumn title="Текущая" data={item.currentEvidence} />
                          <EvidenceColumn title="Якорь" data={item.anchorEvidence} />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}

          {current && shownAnchors.length === 0 && (
            <Card className="text-sm text-muted">
              Для сравнения нужна хотя бы ещё одна оценённая должность.
            </Card>
          )}
        </>
      )}
    </div>
  );
}

// Зеркалит backend/jeval/scoring/grades.py:steps_15pct (тот же геометрический
// шаг 15% ряда Hay) и порог "разрыв" из backend/jeval/hierarchy.py
// (anchor_grade_gap: distance >= 3) — чтобы один и тот же сценарий давал
// одинаковый вердикт "существенно/не существенно" и на фронте, и в QC.
// Раньше здесь были независимые абсолютные пороги по баллам факторов
// (25/15/25), которые расходились с backend даже при равном total: например,
// компенсирующие сдвиги +30 Know-How / −30 Accountability не меняют total и
// не флагуются backend'ом (distance = 0), но фронт показывал "существенное
// расхождение" из-за превышения порога по одному фактору.
const ANCHOR_GAP_STEPS_THRESHOLD = 3;

function steps15pct(a: number, b: number): number {
  if (a <= 0 || b <= 0) return 0;
  const hi = Math.max(a, b);
  const lo = Math.min(a, b);
  return Math.round(Math.log(hi / lo) / Math.log(1.15));
}

/** evidence/doubts конкретной факторной группы у последней оценки должности —
 * для блока "Обоснование", не для самого расчёта расхождения. */
function evidenceFor(
  positionId: string,
  key: FactorGroup,
  evalByPosition: Map<string, Evaluation>,
): { evidence: string[]; doubts: string[] } | null {
  const score = evalByPosition.get(positionId)?.score;
  return score ? groupEvidence(score)[key] : null;
}

function buildComparison(
  current: RoleCol,
  anchor: RoleCol,
  evalByPosition: Map<string, Evaluation>,
) {
  const gradeGap = current.grade - anchor.grade;
  const totalGap = current.total - anchor.total;
  const versionMismatch =
    !!current.tableVersion && !!anchor.tableVersion && current.tableVersion !== anchor.tableVersion;
  const profileText =
    current.profile === anchor.profile
      ? "Профиль совпадает"
      : `Профили различаются (${current.profile} против ${anchor.profile})`;

  const totalSteps = steps15pct(current.total, anchor.total);
  const isSignificant = totalSteps >= ANCHOR_GAP_STEPS_THRESHOLD;

  const factorGaps: { key: FactorGroup; label: string; delta: number }[] = [
    { key: "know_how", label: "Know-How", delta: current.knowHow - anchor.knowHow },
    { key: "problem_solving", label: "Problem Solving", delta: current.problemSolving - anchor.problemSolving },
    { key: "accountability", label: "Accountability", delta: current.accountability - anchor.accountability },
  ];
  const biggestFactor = [...factorGaps].sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta))[0];

  const primaryDifference = isSignificant
    ? `Существенное расхождение: ${totalSteps} шагов по 15% по сумме баллов`
      + (biggestFactor.delta !== 0 ? ` — главным образом за счёт ${biggestFactor.label} (${signed(biggestFactor.delta)})` : "")
    : `Существенных расхождений нет (${totalSteps} шагов по 15%, порог — ${ANCHOR_GAP_STEPS_THRESHOLD})`;
  const factorNotes = factorGaps.map((item) => `${item.label} ${signed(item.delta)}`);

  return {
    anchor,
    gradeGap,
    totalGap,
    profileText,
    primaryDifference,
    factorNotes,
    versionMismatch,
    biggestFactor,
    currentEvidence: evidenceFor(current.id, biggestFactor.key, evalByPosition),
    anchorEvidence: evidenceFor(anchor.id, biggestFactor.key, evalByPosition),
  };
}

function formatGap(delta: number, current: number, anchor: number): string {
  return `${current} vs ${anchor} (${signed(delta)})`;
}

function signed(value: number): string {
  return value > 0 ? `+${value}` : String(value);
}

function gradeGapText(delta: number): string {
  if (delta === 0) return "0";
  return delta > 0 ? `+${delta}` : String(delta);
}

function gradeTone(delta: number): string {
  if (delta === 0) return "text-muted";
  return delta > 0 ? "text-ok" : "text-accent";
}

function Line({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <dt className="shrink-0 text-muted">{label}</dt>
      <dd className="text-right">{value}</dd>
    </div>
  );
}

function EvidenceColumn({
  title,
  data,
}: {
  title: string;
  data: { evidence: string[]; doubts: string[] } | null;
}) {
  return (
    <div>
      <div className="font-medium text-muted">{title}</div>
      {data && data.evidence.length > 0 ? (
        <ul className="mt-1 list-disc space-y-1 pl-4">
          {data.evidence.map((e) => (
            <li key={e}>{e}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-1 text-muted">—</p>
      )}
      {data && data.doubts.length > 0 && (
        <ul className="mt-1 list-disc space-y-1 pl-4 text-warn">
          {data.doubts.map((d) => (
            <li key={d}>{d}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

function RoleCard({ role, current }: { role: RoleCol; current?: boolean }) {
  return (
    <Card className={cn(current ? "border-accent/40" : "border-[rgb(var(--glass-border))]")}>
      <div className="mb-3 flex items-center justify-between">
        {current
          ? <span className="text-xs font-medium uppercase tracking-wide text-accent">Текущая</span>
          : <span className="text-xs text-muted uppercase tracking-wide">Якорь</span>
        }
      </div>
      <div className="min-h-[44px] text-sm font-medium">{role.name}</div>

      <div className="mt-4 flex items-baseline gap-3">
        <span className="num text-5xl">{role.grade}</span>
        <span className="text-sm text-muted">грейд</span>
      </div>

      <div className="mt-3 flex items-center gap-3">
        <span className="num text-sm">{role.profileLong}</span>
        <span className="text-xs text-muted">{PROFILE_LABEL[role.profile]}</span>
      </div>

      <div className="num mt-1 text-sm text-muted">Итого {role.total}</div>

      <dl className="mt-4 space-y-3 border-t border-[rgb(var(--row-divider))] pt-4 text-sm">
        <Row label="Know-How" value={role.knowHow} max={role.total} current={current} />
        <Row label="Problem Solving" value={role.problemSolving} max={role.total} current={current} />
        <Row label="Accountability" value={role.accountability} max={role.total} current={current} />
      </dl>
    </Card>
  );
}

function Row({ label, value, max, current }: { label: string; value: number; max: number; current?: boolean }) {
  return (
    <div>
      <div className="flex justify-between">
        <dt className="text-muted">{label}</dt>
        <dd className="num">{value}</dd>
      </div>
      <div className="mt-1 h-1 overflow-hidden rounded-full bg-[rgb(var(--field-bg))]">
        <div
          className={cn("h-full rounded-full", current ? "bg-accent/60" : "bg-[rgb(var(--muted)/0.4)]")}
          style={{ width: `${Math.round((value / max) * 100)}%` }}
        />
      </div>
    </div>
  );
}
