import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, ErrorBanner, Input, StatusDot } from "../components/ui";
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
  { value: "draft_imported", label: STATUS_LABEL.draft_imported, color: "blue" },
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
  draft_imported: "blue",
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
  const [importBusy, setImportBusy] = useState(false);
  const [importError, setImportError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const importInput = useRef<HTMLInputElement>(null);

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

  async function importDocument(file: File | null) {
    if (!file) return;
    setImportBusy(true);
    setImportError(null);
    try {
      const result = await api.importDocument(file, true);
      const id = result.position.id;
      reload();
      if (id) navigate(`/positions/${id}`);
    } catch (e) {
      setImportError(e instanceof Error ? e.message : String(e));
    } finally {
      setImportBusy(false);
      if (importInput.current) importInput.current.value = "";
    }
  }

  const departments = useMemo(
    () => [...new Set(allRows.flatMap((r) => [r.dzo, r.function]).filter((d) => d !== "—"))].sort(),
    [allRows],
  );

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
    <div className="space-y-8">
      <div className="border-t border-[#dfdbd5] pt-8 dark:border-white/10">
        <div>
          <h1 className="text-[28px] font-semibold tracking-[-0.5px]">Должности</h1>
          <p className="mt-2 max-w-3xl text-sm text-muted">
            Загрузите описание должности для автоматического черновика или откройте существующую карточку.
          </p>
        </div>
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
      {importError && <ErrorBanner message={importError} />}

      <Card
        className={cn("dashboard-upload overflow-hidden p-0 transition-colors", dragActive && "border-accent bg-[#faf7fd] dark:bg-purple-950/20")}
        onDragEnter={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={(e) => { if (!e.currentTarget.contains(e.relatedTarget as Node)) setDragActive(false); }}
        onDrop={(e) => { e.preventDefault(); setDragActive(false); void importDocument(e.dataTransfer.files?.[0] ?? null); }}
      >
        <div className="flex min-h-[300px] flex-col items-center justify-center px-6 py-12 text-center">
          <div className="grid h-14 w-14 place-items-center rounded-full border border-[#ddd8d1] bg-white text-[#363330] dark:border-white/15 dark:bg-white/5 dark:text-white">
            <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M12 16V4m0 0L7 9m5-5 5 5"/><path d="M5 14v5h14v-5"/></svg>
          </div>
          <div className="mt-4 text-base font-semibold">Перетащите описание должности сюда</div>
          <div className="mt-5 flex flex-wrap justify-center gap-3">
            <input
              ref={importInput}
              type="file"
              accept=".docx"
              className="hidden"
              onChange={(e) => importDocument(e.target.files?.[0] ?? null)}
            />
            <Button
              className="rounded-full bg-[#252527] px-6 text-white hover:bg-[#151516] dark:bg-white dark:text-[#252527] dark:hover:bg-[#ececec]"
              disabled={importBusy}
              onClick={() => importInput.current?.click()}
            >
              {importBusy ? "Создаём черновик…" : "Выбрать файл на компьютере"}
            </Button>
          </div>
        </div>
      </Card>

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
                  ? "border-[#252527] bg-[#252527] text-white dark:border-white dark:bg-white dark:text-[#252527]"
                  : "border-[#ddd8d1] bg-white text-muted hover:border-[#aaa49c] hover:text-fg dark:border-white/10 dark:bg-white/5",
              )}
            >
              <span className="inline-block h-1.5 w-1.5 rounded-full" style={{
                background: isActive ? "currentColor" : "rgb(var(--muted))"
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
      <Card className="overflow-hidden rounded-[20px] border-[#e0dcd6] bg-white p-0 shadow-none dark:border-white/10 dark:bg-white/5">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[#f8f6f2] text-left text-muted dark:bg-white/5">
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
                  className="cursor-pointer border-t border-[rgb(var(--row-divider))] transition-colors hover:bg-[#faf8f4] dark:hover:bg-white/5"
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
