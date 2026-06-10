import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, ErrorBanner, Input, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { latestByPosition, toPositionRow } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import {
  CONFIDENCE_LABEL,
  STATUS_LABEL,
  type Confidence,
  type PositionRow,
  type PositionStatus,
} from "../lib/types";

const FILTERS_KEY = "jeval.dashboard.filters.v1";
const DRAFT_KEY = "jeval.job-form.draft.v1";

interface DashboardFilters {
  query: string;
  dept: string;
  status: string;
}

interface DraftMeta {
  step: number;
  savedAt: string;
  filledFields: number;
}

const STATUS_FILTERS: Array<{
  value: PositionStatus | "";
  label: string;
  color: Parameters<typeof StatusDot>[0]["color"];
}> = [
  { value: "", label: "Все", color: "gray" },
  { value: "not_evaluated", label: STATUS_LABEL.not_evaluated, color: "gray" },
  { value: "ready", label: STATUS_LABEL.ready, color: "green" },
  { value: "needs_clarification", label: STATUS_LABEL.needs_clarification, color: "amber" },
  { value: "cannot_evaluate", label: STATUS_LABEL.cannot_evaluate, color: "red" },
];

function readJson<T>(key: string): T | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

function writeJson(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // ignore
  }
}

function removeKey(key: string) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(key);
  } catch {
    // ignore
  }
}

function readSavedFilters(): DashboardFilters {
  const parsed = readJson<Partial<DashboardFilters>>(FILTERS_KEY);
  return {
    query: typeof parsed?.query === "string" ? parsed.query : "",
    dept: typeof parsed?.dept === "string" ? parsed.dept : "",
    status: typeof parsed?.status === "string" ? parsed.status : "",
  };
}

function persistFilters(filters: DashboardFilters) {
  if (!filters.query && !filters.dept && !filters.status) {
    removeKey(FILTERS_KEY);
    return;
  }
  writeJson(FILTERS_KEY, filters);
}

function readDraftMeta(): DraftMeta | null {
  const parsed = readJson<{ step?: unknown; savedAt?: unknown; form?: unknown }>(DRAFT_KEY);
  const form = parsed?.form;
  if (!form || typeof form !== "object") return null;
  const filledFields = Object.entries(form).filter(
    ([key, value]) =>
      key !== "snapshotDate" && typeof value === "string" && value.trim().length > 0,
  ).length;
  if (filledFields === 0) return null;
  const step = typeof parsed?.step === "number" ? Math.min(Math.max(Math.trunc(parsed.step), 0), 6) : 0;
  return {
    step,
    savedAt: typeof parsed?.savedAt === "string" ? parsed.savedAt : new Date().toISOString(),
    filledFields,
  };
}

function formatSavedAt(ts: string): string {
  try {
    return new Intl.DateTimeFormat("ru-RU", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(ts));
  } catch {
    return ts;
  }
}

const STATUS_DOT: Record<PositionStatus, Parameters<typeof StatusDot>[0]["color"]> = {
  not_evaluated: "gray",
  ready: "green",
  needs_clarification: "amber",
  cannot_evaluate: "red",
};

const CONF_DOT: Record<Confidence, Parameters<typeof StatusDot>[0]["color"]> = {
  high: "green",
  medium: "amber",
  low: "red",
};

export default function DashboardPage() {
  const navigate = useNavigate();
  const initialFilters = useMemo(() => readSavedFilters(), []);
  const [query, setQuery] = useState(() => initialFilters.query);
  const [dept, setDept] = useState(() => initialFilters.dept);
  const [status, setStatus] = useState(() => initialFilters.status);
  const [draftMeta, setDraftMeta] = useState<DraftMeta | null>(() => readDraftMeta());

  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.listPositions(), api.listEvaluations()]),
    [],
  );

  const allRows = useMemo<PositionRow[]>(() => {
    if (!data) return [];
    const [positions, evaluations] = data;
    const latest = latestByPosition(evaluations);
    return positions
      .map((p) => toPositionRow(p, p.id ? latest.get(p.id) : undefined))
      .sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1));
  }, [data]);

  const statusCounts = useMemo(
    () =>
      Object.fromEntries(
        STATUS_FILTERS.map(({ value }) => [
          value || "all",
          value ? allRows.filter((r) => r.status === value).length : allRows.length,
        ]),
      ) as Record<string, number>,
    [allRows],
  );

  useEffect(() => {
    persistFilters({ query, dept, status });
  }, [query, dept, status]);

  function clearFilters() {
    setQuery("");
    setDept("");
    setStatus("");
    removeKey(FILTERS_KEY);
  }

  function clearDraft() {
    removeKey(DRAFT_KEY);
    setDraftMeta(null);
  }

  const departments = useMemo(
    () => [...new Set(allRows.flatMap((r) => [r.dzo, r.function]).filter((d) => d !== "—"))].sort(),
    [allRows],
  );

  const kpis = useMemo(() => {
    const graded = allRows.filter((r) => r.grade != null);
    const avg = graded.length
      ? (graded.reduce((s, r) => s + (r.grade ?? 0), 0) / graded.length).toFixed(1)
      : "—";
    return [
      { label: "Всего должностей", value: String(allRows.length) },
      { label: "Готово к комитету", value: String(allRows.filter((r) => r.status === "ready").length) },
      { label: "Средний грейд", value: avg },
      {
        label: "Требуют уточнения",
        value: String(allRows.filter((r) => r.status === "needs_clarification").length),
      },
    ];
  }, [allRows]);

  const rows = useMemo(
    () =>
      allRows.filter(
        (p) =>
          (!query || p.name.toLowerCase().includes(query.toLowerCase())) &&
          (!dept || p.dzo === dept || p.function === dept) &&
          (!status || p.status === status),
      ),
    [allRows, query, dept, status],
  );

  return (
    <div className="space-y-12">
      <div className="flex flex-wrap items-center justify-center gap-8">
        <Button onClick={() => navigate("/new")}>Новая должность</Button>
        <Button onClick={() => navigate("/compare")} variant="secondary">Сравнение</Button>
      </div>

      {draftMeta && (
        <Card className="border-accent/20 p-6">
          <div className="space-y-3">
            <div className="text-sm font-medium">Есть черновик JE-досье</div>
            <p className="text-sm text-muted">
              Шаг {draftMeta.step + 1}, заполнено {draftMeta.filledFields} полей, сохранено{" "}
              {formatSavedAt(draftMeta.savedAt)}.
            </p>
            <div className="flex flex-wrap gap-3">
              <Button onClick={() => navigate("/new")}>Продолжить черновик</Button>
              <Button variant="secondary" onClick={clearDraft}>
                Удалить черновик
              </Button>
            </div>
          </div>
        </Card>
      )}

      {error && <ErrorBanner message={error} onRetry={reload} />}

      {/* KPI */}
      <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
        {loading
          ? Array.from({ length: 4 }, (_, i) => <Skeleton key={i} className="h-[92px]" />)
          : kpis.map((k) => (
              <Card key={k.label} className="p-6 shadow-none" style={{
                background: "rgb(var(--glass-bg) / 0.4)",
                border: "1px solid rgb(var(--glass-border))",
              }}>
                <div className="text-sm text-muted">{k.label}</div>
                <div className="num mt-3 text-4xl font-600">{k.value}</div>
              </Card>
            ))}
      </div>

      {/* Status filter pills */}
      <div className="flex flex-wrap items-center gap-3">
        {STATUS_FILTERS.map((item) => {
          const isActive = status === item.value;
          const count = statusCounts[item.value || "all"] ?? 0;
          return (
            <button
              key={item.value || "all"}
              type="button"
              onClick={() => setStatus(item.value)}
              className={cn(
                "inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
                isActive
                  ? "border-accent bg-[rgb(255_61_0_/_0.1)] text-fg"
                  : "border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] text-muted hover:text-fg",
              )}
            >
              <span className="inline-block h-1.5 w-1.5 rounded-full" style={{
                background: isActive ? "rgb(255, 61, 0)" : "rgb(var(--muted))"
              }} />
              {item.label}
              <span className="num text-xs">{count}</span>
            </button>
          );
        })}
        {(query || dept || status) && (
          <Button variant="ghost" className="px-2 py-1 text-xs min-h-0 ml-auto" onClick={clearFilters}>
            ✕ Сбросить
          </Button>
        )}
      </div>

      {/* Фильтры */}
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[280px]">
          <Input
            placeholder="Поиск по названию должности"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <select className="field max-w-[220px]" value={dept} onChange={(e) => setDept(e.target.value)}>
          <option value="">Все подразделения</option>
          {departments.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>

      {/* Таблица */}
      <Card className="p-0 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-muted bg-[rgb(var(--field-bg))]">
              {["Должность", "ДЗО", "Функция", "Статус", "Грейд", "Уверенность", "Обновлено"].map(
                (h) => (
                  <th key={h} className="px-6 py-4 font-normal text-xs uppercase tracking-wide">
                    {h}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={7} className="px-6 py-12 text-center text-muted">
                  Загрузка…
                </td>
              </tr>
            )}
            {!loading &&
              rows.map((p) => (
                <tr
                  key={p.id}
                  onClick={() => navigate(`/positions/${p.id}`)}
                  className="cursor-pointer border-t border-[rgb(var(--row-divider))] transition-colors hover:bg-[rgb(255_61_0_/_0.04)]"
                >
                  <td className="px-6 py-4 font-medium">{p.name}</td>
                  <td className="px-6 py-4 text-muted text-sm">{p.dzo}</td>
                  <td className="px-6 py-4 text-muted text-sm">{p.function}</td>
                  <td className="px-6 py-4">
                    <StatusDot color={STATUS_DOT[p.status]}>{STATUS_LABEL[p.status]}</StatusDot>
                  </td>
                  <td className="px-6 py-4 font-mono text-base tabular-nums font-medium">{p.grade ?? "—"}</td>
                  <td className="px-6 py-4">
                    {p.confidence ? (
                      <StatusDot color={CONF_DOT[p.confidence]}>
                        {CONFIDENCE_LABEL[p.confidence]}
                      </StatusDot>
                    ) : (
                      <span className="text-muted text-sm">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-muted text-sm">{p.updatedAt || "—"}</td>
                </tr>
              ))}
            {!loading && !error && rows.length === 0 && (
              <tr>
                <td colSpan={7} className="px-6 py-12 text-center text-muted">
                  {allRows.length === 0
                    ? "Должностей пока нет. Создайте первую — «Новая должность»."
                    : "Ничего не найдено. Измените фильтры."}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
