import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Card, ErrorBanner, Field, Skeleton } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { latestByPosition } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import { PROFILE_LABEL, type Profile, type ScoreResult } from "../lib/types";

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
  };
}

export default function ComparisonPage() {
  const [params] = useSearchParams();
  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.listPositions(), api.listEvaluations()]),
    [],
  );

  // Все должности с рассчитанной оценкой.
  const evaluated = useMemo<RoleCol[]>(() => {
    if (!data) return [];
    const [positions, evaluations] = data;
    const latest = latestByPosition(evaluations);
    return positions.flatMap((p) => {
      const score = p.id ? latest.get(p.id)?.score : null;
      return p.id && score ? [toCol(p.id, p.name, score)] : [];
    });
  }, [data]);

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
    () => (current ? shownAnchors.map((anchor) => buildComparison(current, anchor)) : []),
    [current, shownAnchors],
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

function buildComparison(current: RoleCol, anchor: RoleCol) {
  const gradeGap = current.grade - anchor.grade;
  const totalGap = current.total - anchor.total;
  const profileText =
    current.profile === anchor.profile
      ? "Профиль совпадает"
      : `Профили различаются (${current.profile} против ${anchor.profile})`;
  const factorGaps = [
    { label: "Know-How", delta: current.knowHow - anchor.knowHow, threshold: 25 },
    { label: "Problem Solving", delta: current.problemSolving - anchor.problemSolving, threshold: 15 },
    { label: "Accountability", delta: current.accountability - anchor.accountability, threshold: 25 },
  ];
  const notable = factorGaps.filter((item) => Math.abs(item.delta) >= item.threshold);
  const primaryDifference =
    notable.length > 0
      ? notable
          .sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta))
          .map((item) => `${item.label} ${signed(item.delta)}`)
          .join(" · ")
      : "Существенных расхождений по факторам нет";
  const factorNotes =
    notable.length > 0
      ? notable.map((item) => `${item.label} ${signed(item.delta)}`)
      : ["Баллы по факторам близки"];

  return {
    anchor,
    gradeGap,
    totalGap,
    profileText,
    primaryDifference,
    factorNotes,
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

function MiniHint({ label, text }: { label: string; text: string }) {
  return (
    <div className="rounded-lg border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-3">
      <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-1 text-sm">{text}</div>
    </div>
  );
}

function Line({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <dt className="shrink-0 text-muted">{label}</dt>
      <dd className="text-right">{value}</dd>
    </div>
  );
}

function RoleCard({ role, current }: { role: RoleCol; current?: boolean }) {
  return (
    <Card className={cn(current && "border-accent")}>
      {current && <div className="mb-2 text-xs uppercase tracking-wide text-accent">Текущая</div>}
      <div className="min-h-[44px] text-sm font-medium">{role.name}</div>

      <div className="mt-4 flex items-baseline gap-3">
        <span className="num text-5xl">{role.grade}</span>
        <span className="text-sm text-muted">грейд</span>
      </div>

      <div className="mt-3 flex items-center gap-3">
        <span className="num">{role.profileLong}</span>
        <span className="text-xs text-muted">{PROFILE_LABEL[role.profile]}</span>
      </div>

      <div className="num mt-2 text-sm text-muted">Итого {role.total}</div>

      <dl className="mt-4 space-y-2 border-t border-[rgb(var(--row-divider))] pt-4 text-sm">
        <Row label="Know-How" value={role.knowHow} max={role.total} />
        <Row label="Problem Solving" value={role.problemSolving} max={role.total} />
        <Row label="Accountability" value={role.accountability} max={role.total} />
      </dl>
    </Card>
  );
}

function Row({ label, value, max }: { label: string; value: number; max: number }) {
  return (
    <div>
      <div className="flex justify-between">
        <dt className="text-muted">{label}</dt>
        <dd className="num">{value}</dd>
      </div>
      <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-[rgb(var(--field-bg))]">
        <div className="h-full bg-accent/70" style={{ width: `${Math.round((value / max) * 100)}%` }} />
      </div>
    </div>
  );
}
