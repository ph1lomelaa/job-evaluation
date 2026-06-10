import { AnimatePresence, motion } from "framer-motion";
import { useMemo, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { factorCodes, groupEvidence, scopeSummary, subfactorRows } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import {
  CONFIDENCE_LABEL,
  FACTOR_GROUP_LABEL,
  PROFILE_LABEL,
  STATUS_LABEL,
  type Confidence,
  type Evaluation,
  type FactorGroup,
  type GateResult,
  type QCStatus,
  type ScoreResult,
} from "../lib/types";

const CONF_DOT: Record<Confidence, Parameters<typeof StatusDot>[0]["color"]> = {
  high: "green",
  medium: "amber",
  low: "red",
};
const STATUS_DOT: Record<Evaluation["status"], Parameters<typeof StatusDot>[0]["color"]> = {
  ready: "green",
  needs_clarification: "amber",
  cannot_evaluate: "red",
};
const FLAG: Record<QCStatus, { ch: string; cls: string; label: string }> = {
  pass: { ch: "✓", cls: "text-ok", label: "PASS" },
  warn: { ch: "⚠", cls: "text-warn", label: "WARN" },
  fail: { ch: "✗", cls: "text-accent", label: "FAIL" },
};

const STATUS_EXPLANATION: Record<
  Evaluation["status"],
  { summary: string; nextStep: string; tone: Parameters<typeof StatusDot>[0]["color"] }
> = {
  ready: {
    summary:
      "Баллы рассчитаны, а блокирующих проблем по данным нет. Карточку можно выносить на Оценочный комитет.",
    nextStep: "Следующий шаг: комитет и калибровка с якорями, если они есть.",
    tone: "green",
  },
  needs_clarification: {
    summary:
      "Баллы уже есть, но есть уточнения или QC-флаги. Карточка предварительная и требует подтверждения спорных мест.",
    nextStep: "Следующий шаг: уточнить спорные факты и при необходимости доработать досье.",
    tone: "amber",
  },
  cannot_evaluate: {
    summary:
      "Критических данных недостаточно. Уровни факторов, баллы и грейд не присваиваются, пока досье не будет доработано.",
    nextStep: "Следующий шаг: вернуть JE-досье на доработку.",
    tone: "red",
  },
};

const FACTOR_HINTS: Record<FactorGroup, string> = {
  know_how: "Что нужно знать и уметь, чтобы роль выполнялась на стандартном уровне.",
  problem_solving: "Сколько самостоятельного мышления и нестандартности требует работа.",
  accountability: "За какой результат роль отвечает и насколько свободно действует.",
};

export default function EvaluationCardPage() {
  const { id = "" } = useParams();
  const [evaluating, setEvaluating] = useState(false);
  const location = useLocation();
  const [routeError, setRouteError] = useState<string | null>(
    () => (location.state as { evaluationError?: string } | null)?.evaluationError ?? null,
  );
  const [evalError, setEvalError] = useState<string | null>(null);
  const [versionId, setVersionId] = useState<string | null>(null);

  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.getPosition(id), api.listEvaluations(id)]),
    [id],
  );

  const [position, versions] = useMemo(() => {
    if (!data) return [undefined, [] as Evaluation[]] as const;
    const [pos, evs] = data;
    const sorted = [...evs].sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    return [pos, sorted] as const;
  }, [data]);

  // Выбранная версия (по умолчанию — последняя).
  const evaluation = versions.find((v) => v.id === versionId) ?? versions[0];
  const selectedVersionIndex = evaluation ? versions.findIndex((v) => v.id === evaluation.id) : -1;
  const previousVersion = selectedVersionIndex >= 0 ? versions[selectedVersionIndex + 1] : undefined;
  const currentScore = evaluation?.score ?? null;
  const previousScore = previousVersion?.score ?? null;

  async function runEvaluation() {
    setEvaluating(true);
    setEvalError(null);
    setRouteError(null);
    try {
      await api.evaluate(id);
      setVersionId(null); // показать новую (последнюю) версию
      reload();
    } catch (e) {
      setEvalError(e instanceof Error ? e.message : String(e));
    } finally {
      setEvaluating(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        {(routeError || evalError) && <ErrorBanner message={routeError ?? evalError ?? ""} />}
        <Skeleton className="h-24" />
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          {Array.from({ length: 4 }, (_, i) => (
            <Skeleton key={i} className="h-[100px]" />
          ))}
        </div>
        <Skeleton className="h-64" />
      </div>
    );
  }
  if (error || !position) {
    return <ErrorBanner message={error ?? "Должность не найдена"} onRetry={reload} />;
  }

  const scope = scopeSummary(position);

  return (
    <div className="space-y-6">
      {(routeError || evalError) && <ErrorBanner message={routeError ?? evalError ?? ""} />}

      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-[32px]">{position.name}</h1>
          <div className="mt-1 text-sm text-muted">
            {[position.dzo, position.department, position.function].filter(Boolean).join(" · ") || "—"}
            {position.snapshot_date && ` · дата среза ${position.snapshot_date}`}
          </div>
          {scope.length > 0 && <div className="num mt-1 text-sm text-muted">{scope.join(" · ")}</div>}
          <div className="mt-3 flex flex-wrap items-center gap-4">
            {evaluation ? (
              <>
                <StatusDot color={STATUS_DOT[evaluation.status]}>
                  {STATUS_LABEL[evaluation.status]}
                </StatusDot>
                <StatusDot color={CONF_DOT[evaluation.confidence]}>
                  Уверенность: {CONFIDENCE_LABEL[evaluation.confidence].toLowerCase()}
                </StatusDot>
                {versions.length > 1 ? (
                  <select
                    className="field max-w-[260px] !py-1.5 text-xs"
                    value={evaluation.id ?? ""}
                    onChange={(e) => setVersionId(e.target.value)}
                  >
                    {versions.map((v, i) => (
                      <option key={v.id} value={v.id ?? ""}>
                        Версия {versions.length - i} · {v.created_at.slice(0, 16).replace("T", " ")}
                      </option>
                    ))}
                  </select>
                ) : (
                  <span className="num text-xs text-muted">
                    оценка от {evaluation.created_at.slice(0, 10)}
                  </span>
                )}
              </>
            ) : (
              <StatusDot color="gray">Предварительная оценка ещё не проводилась</StatusDot>
            )}
          </div>
        </div>
        <div className="flex items-center gap-3 print:hidden">
          {evaluation?.score && (
            <Link to={`/compare?id=${id}`}>
              <Button variant="ghost">Сравнить с якорями</Button>
            </Link>
          )}
          {evaluation && (
            <Button variant="secondary" onClick={() => window.print()}>
              Печать / PDF
            </Button>
          )}
          <Button disabled={evaluating} onClick={runEvaluation}>
            {evaluating ? "Оценивается…" : evaluation ? "Переоценить" : "Запустить оценку"}
          </Button>
        </div>
      </div>

      {evaluation && (
        <Card className="border-accent/20 p-5">
          <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <div className="text-xs uppercase tracking-wide text-muted">Что означает статус</div>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {STATUS_EXPLANATION[evaluation.status].summary}
              </p>
            </div>
            <div className="space-y-2">
              <StatusDot color={STATUS_EXPLANATION[evaluation.status].tone}>
                {evaluation.status === "ready"
                  ? "Готово к комитету"
                  : evaluation.status === "needs_clarification"
                    ? "Требуются уточнения"
                    : "Оценка невозможна"}
              </StatusDot>
              <p className="text-xs text-muted">{STATUS_EXPLANATION[evaluation.status].nextStep}</p>
            </div>
          </div>
        </Card>
      )}

      {versions.length > 1 && (
        <Card>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-sm text-muted">История версий</div>
              <div className="mt-1 text-xs text-muted">
                Новые версии сверху. Нажмите на версию, чтобы посмотреть её расчёт и QC.
              </div>
            </div>
            {currentScore && previousScore && (
              <div className="text-right text-xs text-muted">
                <div>
                  Изменение к предыдущей: {signed(scoreDelta(currentScore.total_points, previousScore.total_points))} баллов
                </div>
                <div>
                  Грейд: {signed(scoreDelta(currentScore.grade, previousScore.grade))}
                </div>
              </div>
            )}
          </div>
          <div className="mt-4 grid gap-2 md:grid-cols-2">
            {versions.map((v, index) => {
              const selected = v.id === evaluation?.id;
              const score = v.score;
              return (
                <button
                  key={v.id ?? index}
                  type="button"
                  onClick={() => setVersionId(v.id ?? null)}
                  className={cn(
                    "rounded-xl border px-4 py-3 text-left transition-colors",
                    selected
                      ? "border-accent bg-[rgb(255_61_0_/_0.05)]"
                      : "border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] hover:border-[rgb(var(--glass-border-hover))]",
                  )}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium">
                        Версия {versions.length - index}
                        {selected && <span className="ml-2 text-xs text-accent">выбрана</span>}
                      </div>
                      <div className="mt-1 text-xs text-muted">
                        {v.created_at.slice(0, 16).replace("T", " ")}
                      </div>
                    </div>
                    <StatusDot color={STATUS_DOT[v.status]}>{STATUS_LABEL[v.status]}</StatusDot>
                  </div>
                  <div className="mt-3 flex flex-wrap items-center gap-3 text-sm">
                    <span className="num">Грейд {score?.grade ?? "—"}</span>
                    {score && <span className="text-muted">Баллы {score.total_points}</span>}
                    <StatusDot color={CONF_DOT[v.confidence]}>Уверенность: {CONFIDENCE_LABEL[v.confidence].toLowerCase()}</StatusDot>
                  </div>
                </button>
              );
            })}
          </div>
        </Card>
      )}

      {!evaluation && <GatePreview positionId={id} />}

      {evaluation && evaluation.status === "cannot_evaluate" && (
        <CannotEvaluate evaluation={evaluation} />
      )}

      {evaluation?.score && <ScoreView evaluation={evaluation} score={evaluation.score} />}

      {evaluation && (
        <>
          {evaluation.role_summary && (
            <Card>
              <div className="mb-3 text-sm text-muted">Резюме должности</div>
              <p className="text-sm leading-relaxed">{evaluation.role_summary}</p>
            </Card>
          )}

          {evaluation.status !== "cannot_evaluate" && (
            <GateChecks gate={evaluation.gate} title="Проверка входных данных (Gate 0)" collapsible />
          )}

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <Card>
              <div className="mb-3 text-sm text-muted">Обоснование</div>
              <p className="whitespace-pre-line text-sm leading-relaxed">
                {evaluation.reasoning || "—"}
              </p>
            </Card>
            <Card>
              <div className="mb-3 text-sm text-muted">Вопросы на уточнение</div>
              {evaluation.clarifying_questions.length > 0 ? (
                <ol className="list-decimal space-y-2 pl-5 text-sm">
                  {evaluation.clarifying_questions.map((q) => (
                    <li key={q}>{q}</li>
                  ))}
                </ol>
              ) : (
                <p className="text-sm text-muted">Нет — данных достаточно.</p>
              )}
            </Card>
          </div>

          <Card className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="text-sm text-muted">Рекомендация для Оценочного комитета</div>
              <div className="mt-1 text-lg">{evaluation.recommendation || "—"}</div>
            </div>
            <p className="max-w-[360px] text-xs text-muted">
              Оценка предварительная: итоговый грейд утверждает Оценочный комитет.
            </p>
          </Card>
        </>
      )}
    </div>
  );
}

// ── Gate 0 до первой оценки ────────────────────────────────────────────────────

function GatePreview({ positionId }: { positionId: string }) {
  const { data, error, loading, reload } = useFetch(() => api.gateCheck(positionId), [positionId]);
  if (loading) return <Skeleton className="h-48" />;
  if (error || !data) return <ErrorBanner message={error ?? "Проверка недоступна"} onRetry={reload} />;
  return <GateChecks gate={data} title="Входные данные" />;
}

function GateChecks({
  gate,
  title,
  collapsible,
}: {
  gate: GateResult;
  title: string;
  collapsible?: boolean;
}) {
  const [open, setOpen] = useState(!collapsible);
  const warns = gate.checks.filter((c) => c.status !== "pass").length;
  return (
    <Card>
      <button
        className={cn("flex w-full items-center justify-between text-left", !collapsible && "pointer-events-none")}
        onClick={() => collapsible && setOpen((o) => !o)}
      >
        <span className="text-sm text-muted">
          {title}
          {warns > 0 && <span className="ml-2 text-warn">⚠ {warns}</span>}
        </span>
        {collapsible && <span className="num text-muted">{open ? "−" : "+"}</span>}
      </button>
      {open && (
        <ul className="mt-4 grid grid-cols-1 gap-2 text-sm md:grid-cols-2">
          {gate.checks.map((c) => (
            <li key={c.block} className="flex items-start gap-2">
              <span className={cn("num w-4", FLAG[c.status].cls)}>{FLAG[c.status].ch}</span>
              <span>
                {c.block}
                {c.note && <span className="block text-xs text-muted">{c.note}</span>}
              </span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

function CannotEvaluate({ evaluation }: { evaluation: Evaluation }) {
  return (
    <>
      <Card className="border-accent/40">
        <div className="text-lg font-medium">Требуется дополнить данные</div>
        <ul className="mt-4 space-y-2 text-sm">
          {evaluation.gate.missing_fields.map((m) => (
            <li key={m} className="flex items-start gap-2">
              <span className="text-accent mt-0.5">✗</span>
              <span>{m}</span>
            </li>
          ))}
        </ul>
      </Card>
      <GateChecks gate={evaluation.gate} title="Проверка данных" />
    </>
  );
}

// ── Полная карточка с расчётом ────────────────────────────────────────────────

function ScoreView({ evaluation, score }: { evaluation: Evaluation; score: ScoreResult }) {
  const groups: FactorGroup[] = ["know_how", "problem_solving", "accountability"];
  const codes = factorCodes(score);
  const rows = subfactorRows(score);
  const evidence = groupEvidence(score);
  const points: Record<FactorGroup, number> = {
    know_how: score.know_how.points,
    problem_solving: score.problem_solving.points,
    accountability: score.accountability.points,
  };

  return (
    <>
      {/* Summary */}
      <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
        <Summary
          label="Итоговый балл"
          value={String(score.total_points)}
          note="Сумма трех факторов"
        />
        <Summary label="Грейд" value={String(score.grade)} big note="По матрице грейдов" />
        <SummaryProfile
          profile={score.profile}
          steps={score.profile_steps}
          long={score.profile_long}
          note="Форма роли: A / P / L"
        />
        <SummaryBar
          label="Уверенность"
          pct={evaluation.confidence === "high" ? 85 : evaluation.confidence === "medium" ? 60 : 35}
          note="Насколько надежны данные"
        />
      </div>

      {/* Factor table */}
      <Card className="p-0">
        {groups.map((g) => (
          <FactorGroupBlock
            key={g}
            label={FACTOR_GROUP_LABEL[g]}
            hint={FACTOR_HINTS[g]}
            code={codes[g]}
            points={points[g]}
            rows={rows[g]}
            evidence={evidence[g].evidence}
            doubts={evidence[g].doubts}
            confidence={evidence[g].confidence}
          />
        ))}
      </Card>

      {/* Formula */}
      <Card>
        <div className="mb-3 text-sm text-muted">Итоговая формула</div>
        <div className="num flex flex-wrap items-center gap-x-3 gap-y-2 text-lg">
          <span>Know-How {score.know_how.points}</span>
          <Op>+</Op>
          <span>Problem Solving {score.problem_solving.points}</span>
          <span className="text-muted">({score.problem_solving.percentage}%)</span>
          <Op>+</Op>
          <span>Accountability {score.accountability.points}</span>
          <Op>=</Op>
          <span className="text-accent">Итого {score.total_points}</span>
          <Op>→</Op>
          <span>Грейд {score.grade}</span>
          <span className="text-muted">
            · Профиль {score.profile_long || score.profile} ({score.profile_steps}{" "}
            {stepsWord(score.profile_steps)})
          </span>
        </div>
      </Card>

      {/* QC flags */}
      <Card>
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div className="text-sm font-medium">QC-проверки</div>
          <div className="flex flex-wrap gap-2 text-xs">
            <StatusDot color="red">FAIL: {evaluation.qc_flags.filter((q) => q.status === "fail").length}</StatusDot>
            <StatusDot color="amber">WARN: {evaluation.qc_flags.filter((q) => q.status === "warn").length}</StatusDot>
            <StatusDot color="green">PASS: {evaluation.qc_flags.filter((q) => q.status === "pass").length}</StatusDot>
          </div>
        </div>
        {evaluation.qc_flags.length === 0 ? (
          <p className="text-sm text-muted">Проверки не выполнялись.</p>
        ) : (
          <div className="space-y-4">
            <QcSection title="Блокирующие" color="red" items={evaluation.qc_flags.filter((q) => q.status === "fail")} />
            <QcSection
              title="Требуют уточнения"
              color="amber"
              items={evaluation.qc_flags.filter((q) => q.status === "warn")}
            />
            <details className="rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] px-4 py-3">
              <summary className="cursor-pointer list-none text-sm text-muted">
                Подтверждено ({evaluation.qc_flags.filter((q) => q.status === "pass").length})
              </summary>
              <div className="mt-3 space-y-3">
                {evaluation.qc_flags
                  .filter((q) => q.status === "pass")
                  .map((q) => (
                    <QcItem key={q.code} flag={q} />
                  ))}
              </div>
            </details>
          </div>
        )}
      </Card>
    </>
  );
}

function stepsWord(n: number): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "шаг";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "шага";
  return "шагов";
}

function scoreDelta(current: number, previous: number): number {
  return current - previous;
}

function signed(value: number): string {
  return value > 0 ? `+${value}` : String(value);
}

function Op({ children }: { children: string }) {
  return <span className="text-muted">{children}</span>;
}

function Summary({
  label,
  value,
  big,
  note,
}: {
  label: string;
  value: string;
  big?: boolean;
  note?: string;
}) {
  return (
    <Card className="p-5">
      <div className="text-sm text-muted">{label}</div>
      <div className={cn("num mt-2", big ? "text-5xl" : "text-3xl")}>{value}</div>
      {note && <div className="mt-2 text-xs text-muted">{note}</div>}
    </Card>
  );
}

function SummaryProfile({
  profile,
  steps,
  long,
  note,
}: {
  profile: ScoreResult["profile"];
  steps: number;
  long: string;
  note?: string;
}) {
  return (
    <Card className="p-5">
      <div className="text-sm text-muted">Профиль</div>
      <div className="mt-2 flex items-center gap-3">
        <span className={cn("num text-3xl", long.endsWith("*") && "text-warn")}>{long || profile}</span>
        <div className="flex-1">
          <div className="h-2 overflow-hidden rounded-full bg-[rgb(var(--field-bg))]">
            <div className="h-full bg-accent" style={{ width: `${Math.min(steps * 25, 100)}%` }} />
          </div>
          <div className="mt-1 text-xs text-muted">
            {PROFILE_LABEL[profile]}
            {long.endsWith("*") && " · вне пределов P4…A4"}
          </div>
        </div>
      </div>
      {note && <div className="mt-2 text-xs text-muted">{note}</div>}
    </Card>
  );
}

function SummaryBar({ label, pct, note }: { label: string; pct: number; note?: string }) {
  return (
    <Card className="p-5">
      <div className="text-sm text-muted">{label}</div>
      <div className="num mt-2 text-3xl">{pct}%</div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-[rgb(var(--field-bg))]">
        <div className="h-full bg-ok" style={{ width: `${pct}%` }} />
      </div>
      {note && <div className="mt-2 text-xs text-muted">{note}</div>}
    </Card>
  );
}

function FactorGroupBlock({
  label,
  hint,
  code,
  points,
  rows,
  evidence,
  doubts,
  confidence,
}: {
  label: string;
  hint: string;
  code: string;
  points: number;
  rows: { name: string; level: string }[];
  evidence: string[];
  doubts: string[];
  confidence: Confidence;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-t border-[rgb(var(--row-divider))] first:border-t-0">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-start gap-4 px-5 py-3 text-left transition-colors hover:bg-[rgb(255_61_0_/_0.05)]"
      >
        <span className="flex-1 pr-3">
          <span className="block text-xs uppercase tracking-wide text-muted">{label}</span>
          <span className="mt-1 block text-xs text-muted">{hint}</span>
        </span>
        <span className="num text-sm text-muted">{code}</span>
        <span className="num w-16 text-right text-sm">{points}</span>
        <span className="w-24 text-right text-sm text-muted">
          <span className="block">{CONFIDENCE_LABEL[confidence]}</span>
          <span className="block text-[11px]">
            {evidence.length} фактов · {doubts.length} сомнений
          </span>
        </span>
        <span className="num w-4 text-center text-muted">{open ? "−" : "+"}</span>
      </button>
      {rows.map((r) => (
        <div
          key={r.name}
          className="flex items-center gap-4 border-t border-[rgb(var(--row-divider))] px-5 py-2.5 text-sm"
        >
          <span className="flex-1">{r.name}</span>
          <span className="num w-16 text-muted">{r.level}</span>
          <span className="w-16" />
          <span className="w-24" />
          <span className="w-4" />
        </div>
      ))}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.18 }}
            className="overflow-hidden"
          >
            <div className="space-y-2 px-9 pb-4 pt-1 text-sm text-muted">
              <div className="text-xs uppercase tracking-wide">Доказательства</div>
              <ul className="list-disc space-y-1 pl-5">
                {evidence.length > 0 ? evidence.map((e) => <li key={e}>{e}</li>) : <li>—</li>}
              </ul>
              {doubts.length > 0 && (
                <>
                  <div className="pt-1 text-xs uppercase tracking-wide">Сомнения</div>
                  <ul className="list-disc space-y-1 pl-5">
                    {doubts.map((d) => (
                      <li key={d}>{d}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function QcSection({
  title,
  color,
  items,
}: {
  title: string;
  color: Parameters<typeof StatusDot>[0]["color"];
  items: Evaluation["qc_flags"];
}) {
  if (items.length === 0) return null;
  return (
    <div className="rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <StatusDot color={color}>{title} ({items.length})</StatusDot>
      </div>
      <ul className="space-y-3">
        {items.map((q) => (
          <QcItem key={q.code} flag={q} />
        ))}
      </ul>
    </div>
  );
}

function QcItem({ flag }: { flag: Evaluation["qc_flags"][number] }) {
  return (
    <li className="flex gap-3 border-t border-[rgb(var(--row-divider))] pt-3 first:border-t-0 first:pt-0">
      <span className={cn("num w-12 shrink-0 text-sm", FLAG[flag.status].cls)}>
        {FLAG[flag.status].ch} {FLAG[flag.status].label}
      </span>
      <div className="text-sm">
        <div>{flag.message}</div>
        {flag.recommendation && flag.recommendation !== "—" && (
          <div className="mt-0.5 text-xs text-muted">{flag.recommendation}</div>
        )}
      </div>
    </li>
  );
}
