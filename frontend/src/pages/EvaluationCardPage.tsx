import { AnimatePresence, motion } from "framer-motion";
import { useMemo, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, NoticeBanner, Skeleton, StatusDot } from "../components/ui";
import { QcItem, QcSection } from "../components/QcFlags";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { useFactorLevelReference, useFactorLevelRules } from "../lib/factorLevels";
import {
  EMPTY_FACTOR_LEVELS,
  EMPTY_FACTOR_RULES,
  extractionMethodLabel,
  factorCodes,
  groupEvidence,
  importFieldLabel,
  scopeSummary,
  subfactorRows,
  type SubfactorRow,
} from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import {
  CONFIDENCE_LABEL,
  FACTOR_GROUP_LABEL,
  PROFILE_LABEL,
  type Confidence,
  type Evaluation,
  type FactorGroup,
  type JobDossier,
  type QCFlag,
  type ScoreResult,
} from "../lib/types";

const STATUS_EXPLANATION: Record<
  Evaluation["status"],
  { summary: string; nextStep: string }
> = {
  ready: {
    summary:
      "Баллы рассчитаны, а блокирующих проблем по данным нет. Карточку можно выносить на Оценочный комитет.",
    nextStep: "Следующий шаг: комитет и калибровка с якорями, если они есть.",
  },
  needs_clarification: {
    summary:
      "Баллы уже есть, но есть уточнения или QC-флаги. Карточка предварительная и требует подтверждения спорных мест.",
    nextStep: "Следующий шаг: уточнить спорные факты и при необходимости доработать досье.",
  },
  cannot_evaluate: {
    summary:
      "Критических данных недостаточно. Уровни факторов, баллы и грейд не присваиваются, пока досье не будет доработано.",
    nextStep: "Следующий шаг: вернуть JE-досье на доработку.",
  },
};

const FACTOR_HINTS: Record<FactorGroup, string> = {
  know_how: "Что нужно знать и уметь, чтобы роль выполнялась на стандартном уровне.",
  problem_solving: "Сколько самостоятельного мышления и нестандартности требует работа.",
  accountability: "За какой результат роль отвечает и насколько свободно действует.",
};

export default function EvaluationCardPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const [evaluating, setEvaluating] = useState(false);
  const location = useLocation();
  const [routeError, setRouteError] = useState<string | null>(
    () => (location.state as { evaluationError?: string } | null)?.evaluationError ?? null,
  );
  const [routeNotice] = useState<string | null>(
    () => (location.state as { importNotice?: string } | null)?.importNotice ?? null,
  );
  const [evalError, setEvalError] = useState<string | null>(null);
  const [versionId, setVersionId] = useState<string | null>(null);
  const [exportingPdf, setExportingPdf] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

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

  const evaluation = versions.find((v) => v.id === versionId) ?? versions[0];

  const importedRoleCoreCount = data?.[0]
    ? Number(Boolean(data[0].purpose?.trim()))
      + Number(data[0].key_results.length > 0)
      + Number(data[0].responsibilities.length > 0)
    : 0;
  const needsDraftReview = Boolean(
    data?.[0]?.review_status === "draft_imported" && importedRoleCoreCount < 2,
  );

  async function runEvaluation() {
    if (needsDraftReview) {
      navigate(`/positions/${id}/edit`);
      return;
    }
    setEvaluating(true);
    setEvalError(null);
    setRouteError(null);
    try {
      await api.evaluate(id);
      setVersionId(null);
      reload();
    } catch (e) {
      setEvalError(e instanceof Error ? e.message : String(e));
    } finally {
      setEvaluating(false);
    }
  }

  async function exportPdf() {
    if (!evaluation?.id) return;
    setExportingPdf(true);
    setExportError(null);
    try {
      await api.exportEvaluationPdf(evaluation.id);
    } catch (e) {
      setExportError(e instanceof Error ? e.message : String(e));
    } finally {
      setExportingPdf(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        {(routeError || evalError) && <ErrorBanner message={routeError ?? evalError ?? ""} />}
        {routeNotice && <NoticeBanner message={routeNotice} />}
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
      {routeNotice && <NoticeBanner message={routeNotice} />}

      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-[32px]">{position.name}</h1>
          <div className="mt-1 text-sm text-muted">
            {[position.dzo, position.department, position.function].filter(Boolean).join(" · ") || "—"}
            {position.snapshot_date && ` · дата среза ${position.snapshot_date}`}
          </div>
          {scope.length > 0 && <div className="num mt-1 text-sm text-muted">{scope.join(" · ")}</div>}
          <div className="mt-3 flex flex-wrap items-center gap-3 text-sm text-muted">
            {evaluation ? (
              <>
                {evaluation.is_final && <StatusDot color="green">✓ Финальная версия</StatusDot>}
                {versions.length > 1 ? (
                  <select
                    className="field max-w-[260px] !py-1.5 text-xs"
                    value={evaluation.id ?? ""}
                    onChange={(e) => setVersionId(e.target.value)}
                  >
                    {versions.map((v, i) => (
                      <option key={v.id} value={v.id ?? ""}>
                        Версия {versions.length - i} · {v.created_at.slice(0, 16).replace("T", " ")}
                        {v.created_by_name ? ` · ${v.created_by_name}` : ""}
                      </option>
                    ))}
                  </select>
                ) : (
                  <span className="num text-xs text-muted">
                    оценка от {evaluation.created_at.slice(0, 10)}
                    {evaluation.created_by_name ? ` · ${evaluation.created_by_name}` : ""}
                  </span>
                )}
              </>
            ) : (
              <StatusDot color="gray">Предварительная оценка ещё не проводилась</StatusDot>
            )}
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-2 print:hidden">
              <Button variant="secondary" disabled={evaluating} onClick={runEvaluation}>
                {needsDraftReview
                  ? "Дополнить досье"
                  : evaluating
                    ? "Оценивается…"
                    : evaluation
                      ? "Переоценить"
                      : "Запустить оценку"}
              </Button>
              {evaluation?.score && (
                <Link to={`/compare?id=${id}`}>
                  <Button variant="ghost">Сравнить</Button>
                </Link>
              )}
              {versions.length > 1 && (
                <Link to={`/positions/${id}/reconcile`}>
                  <Button variant="ghost">Сверить версии</Button>
                </Link>
              )}
              {evaluation && (
                <Button
                  variant="secondary"
                  disabled={evaluation.is_test_data}
                  title={evaluation.is_test_data ? "Тестовые данные нельзя выгружать для комитета" : undefined}
                  onClick={() => window.print()}
                >
                  Печать
                </Button>
              )}
              {evaluation && (
                <Button variant="secondary" disabled={exportingPdf} onClick={exportPdf}>
                  {exportingPdf ? "Готовим PDF…" : "Экспорт в PDF"}
                </Button>
              )}
          </div>
          {exportError && <p className="mt-2 text-xs text-accent print:hidden">{exportError}</p>}
        </div>
      </div>

      {evaluation?.is_test_data && (
        <Card className="border-2 border-accent bg-accent/10 p-5 print:hidden">
          <div className="flex items-center gap-3">
            <span className="text-2xl">⚠</span>
            <div>
              <div className="text-sm font-bold uppercase tracking-wide text-accent">
                Тестовые данные — не для Оценочного комитета
              </div>
              <p className="mt-1 text-sm text-[rgb(var(--fg)/0.78)]">
                Уровни факторов выбраны офлайн-заглушкой, а не реальным AI-агентом — это
                демонстрационный расчёт. Обратитесь к администратору системы, чтобы подключить
                реальный агент, и переоцените должность перед выносом на комитет.
              </p>
            </div>
          </div>
        </Card>
      )}

      {evaluation && <EvaluationStatusHero evaluation={evaluation} />}

      {position.review_status === "draft_imported" && position.import_metadata && (
        <Card className="border-warn/30 p-5">
          <div className="grid gap-4 lg:grid-cols-[1fr_0.8fr]">
            <div>
              <div className="text-sm font-medium">Черновик импортирован из документа</div>
              <p className="mt-2 text-sm text-muted">
                Проверьте заполненные поля перед Gate 0 и оценкой. Данные, которых не было в
                документе, не заполнялись автоматически.
              </p>
              {position.import_metadata.notes.length > 0 && (
                <ul className="mt-3 list-disc space-y-1 pl-5 text-xs text-muted">
                  {position.import_metadata.notes.map((note) => (
                    <li key={note}>{note}</li>
                  ))}
                </ul>
              )}
            </div>
            <div className="space-y-2 text-sm">
              <div className="text-muted">Источник: {position.import_metadata.source_filename ?? "—"}</div>
              <div className="text-muted">{extractionMethodLabel(position.import_metadata.extraction_method)}</div>
              {position.import_metadata.missing_fields.length > 0 && (
                <div>
                  <div className="text-xs font-medium text-muted">Можно дополнить, если данные доступны:</div>
                  <ul className="mt-2 grid gap-x-5 gap-y-1 text-sm sm:grid-cols-2">
                    {position.import_metadata.missing_fields.map((field) => (
                      <li key={field} className="flex gap-2"><span className="text-warn">•</span>{importFieldLabel(field)}</li>
                    ))}
                  </ul>
                </div>
              )}
              <Link to={`/positions/${id}/edit`}>
                <Button variant="secondary" className="mt-2">
                  Проверить и дополнить
                </Button>
              </Link>
            </div>
          </div>
        </Card>
      )}

      {evaluation && (
        <ClarificationPanel positionId={id} evaluation={evaluation} />
      )}




      {evaluation?.score && <ScoreView evaluation={evaluation} score={evaluation.score} onChanged={reload} />}

      <DossierPreview position={position} onChanged={reload} />

      {evaluation && (
        <>
          {evaluation.role_summary && (
            <Card>
              <div className="mb-3 text-sm font-semibold">Резюме должности</div>
              <p className="text-[15px] leading-7">{evaluation.role_summary}</p>
            </Card>
          )}

          <Card>
            <div className="mb-3 text-sm font-semibold">Обоснование по факторам</div>
            <p className="whitespace-pre-line text-[15px] leading-7">
              {evaluation.reasoning || "—"}
            </p>
          </Card>

          <Card className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="text-sm font-semibold">Рекомендация для Оценочного комитета</div>
              <div className="mt-2 max-w-4xl text-[15px] font-medium leading-7">{evaluation.recommendation || "—"}</div>
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

const GATE_EDIT_STEP: Record<string, number> = {
  "Цель должности": 1,
  "Ключевые результаты": 1,
  "Описание функций": 1,
  "KPI / показатели блока": 1,
  "Полномочия (сам/согласует/рекомендует)": 2,
  "Лимиты (бюджет, закупки, штат, stop-work)": 2,
  "Масштаб воздействия": 3,
  "Стейкхолдеры": 3,
  "Якорные должности": 4,
  "Типовые кейсы (Problem Solving)": 4,
  "Оргконтекст": 5,
  "Дата среза": 0,
  "Подтверждение руководителя / HR": 6,
};

function EvaluationStatusHero({ evaluation }: { evaluation: Evaluation }) {
  return (
    <Card className={cn(
      "border-2 p-6",
      evaluation.status === "ready" ? "border-ok/35 bg-ok/[0.045]" :
        evaluation.status === "needs_clarification" ? "border-warn/45 bg-warn/[0.065]" :
          "border-accent/40 bg-accent/[0.055]",
    )}>
      <div className="grid gap-5 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-muted">Решение для HR / C&amp;B</div>
          <div className={cn(
            "mt-2 text-2xl font-bold",
            evaluation.status === "ready" ? "text-ok" : evaluation.status === "needs_clarification" ? "text-warn" : "text-accent",
          )}>
            {evaluation.status === "ready" ? "Готово к комитету" : evaluation.status === "needs_clarification" ? "Требуются уточнения" : "Оценка невозможна"}
          </div>
          <p className="mt-2 max-w-3xl text-[15px] leading-7 text-[rgb(var(--fg)/0.86)]">
            {STATUS_EXPLANATION[evaluation.status].summary}
          </p>
        </div>
        <div className="rounded-xl border border-current/10 bg-white/65 p-4 dark:bg-black/15">
          <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
            <span className="font-semibold text-accent">✗ {evaluation.qc_flags.filter((flag) => flag.status === "fail").length} блокирующих</span>
            <span className="font-semibold text-warn">⚠ {evaluation.qc_flags.filter((flag) => flag.status === "warn").length} уточнений</span>
          </div>
          <p className="mt-3 text-sm leading-6 text-[rgb(var(--fg)/0.78)]">{STATUS_EXPLANATION[evaluation.status].nextStep}</p>
        </div>
      </div>
    </Card>
  );
}

function ClarificationPanel({ positionId, evaluation }: { positionId: string; evaluation: Evaluation }) {
  const unresolved = evaluation.gate.checks.filter((check) => check.status !== "pass");
  if (unresolved.length === 0 && evaluation.clarifying_questions.length === 0) return null;

  const blocking = unresolved.filter((check) => check.status === "fail");
  const recommended = unresolved.filter((check) => check.status === "warn");

  return (
    <Card className="border-warn/35 p-0 overflow-hidden">
      <div className="border-b border-[rgb(var(--row-divider))] bg-warn/[0.06] px-5 py-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <div className="text-sm font-semibold">Что уточнить для надёжной оценки</div>
            <p className="mt-1 text-xs leading-5 text-[rgb(var(--fg)/0.72)]">
              Предварительный расчёт уже доступен. Дополняйте только те блоки, которые могут изменить уровни или уверенность.
            </p>
          </div>
          <span className="num text-xs font-semibold text-warn">
            {unresolved.length} {unresolved.length === 1 ? "пункт" : "пунктов"}
          </span>
        </div>
      </div>

      <div className="divide-y divide-[rgb(var(--row-divider))]">
        {[...blocking, ...recommended].map((check) => {
          const step = GATE_EDIT_STEP[check.block] ?? 0;
          return (
            <div key={check.block} className="flex flex-wrap items-center justify-between gap-3 px-5 py-3.5">
              <div className="flex min-w-0 items-start gap-3">
                <span className={cn("num mt-0.5 text-xs font-bold", check.status === "fail" ? "text-accent" : "text-warn")}>
                  {check.status === "fail" ? "✗" : "⚠"}
                </span>
                <div>
                  <div className="text-sm font-medium">{check.block}</div>
                  <div className="mt-0.5 text-xs text-muted">
                    {check.status === "fail" ? "Расчёт использует предположение — требуется подтверждение" : "Желательно для повышения уверенности"}
                  </div>
                </div>
              </div>
              <Link
                to={`/positions/${positionId}/edit?step=${step}`}
                className="shrink-0 rounded-lg border border-[rgb(var(--field-border))] px-3 py-2 text-xs font-medium transition-colors hover:border-accent hover:text-accent"
              >
                Дополнить
              </Link>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

function DossierPreview({ position, onChanged }: { position: JobDossier; onChanged: () => void }) {
  const [inferring, setInferring] = useState(false);
  const [inferError, setInferError] = useState<string | null>(null);

  async function applyDefaultAuthorities() {
    setInferring(true);
    setInferError(null);
    try {
      await api.inferAuthorities(position.id ?? "");
      onChanged();
    } catch (e) {
      setInferError(e instanceof Error ? e.message : String(e));
    } finally {
      setInferring(false);
    }
  }

  const authoritiesEmpty =
    position.authorities.decides_alone.length === 0 &&
    position.authorities.requires_approval.length === 0 &&
    position.authorities.recommends.length === 0;
  const canInferAuthorities = authoritiesEmpty && Boolean(position.reporting.manager);

  const sections = [
    { title: "Цель должности", items: position.purpose ? [position.purpose] : [] },
    { title: "Ключевые результаты", items: position.key_results },
    { title: "Обязанности", items: position.responsibilities },
    { title: "KPI / показатели", items: position.kpis },
    {
      title: "Полномочия",
      items: [
        ...position.authorities.decides_alone.map((v) => `Решает самостоятельно: ${v}`),
        ...position.authorities.requires_approval.map((v) => `Согласует: ${v.item} — ${v.approver}`),
        ...position.authorities.recommends.map((v) => `Рекомендует: ${v}`),
        ...position.limits.map((v) => `Лимит: ${v}`),
      ],
    },
    {
      title: "Контекст и документы",
      items: [
        position.organizational_context,
        position.reporting.manager ? `Руководитель: ${position.reporting.manager}` : null,
        position.scope.headcount != null ? `Численность: ${position.scope.headcount}` : null,
        ...position.documents.map((d) => `Документ: ${d}`),
      ].filter(Boolean) as string[],
    },
    ...(position.import_metadata
      ? [
          {
            title: "Источники и provenance",
            items: [
              position.import_metadata.source_filename ? `Файл: ${position.import_metadata.source_filename}` : null,
              position.import_metadata.source_type ? `Тип: ${position.import_metadata.source_type}` : null,
              position.import_metadata.source_mime_type ? `MIME: ${position.import_metadata.source_mime_type}` : null,
              position.import_metadata.source_size_bytes != null
                ? `Размер: ${position.import_metadata.source_size_bytes} bytes`
                : null,
              position.import_metadata.source_sha256 ? `SHA-256: ${position.import_metadata.source_sha256}` : null,
              position.import_metadata.extraction_method
                ? extractionMethodLabel(position.import_metadata.extraction_method)
                : null,
              ...Object.entries(position.import_metadata.field_sources ?? {}).map(
                ([field, values]) => `${importFieldLabel(field)}: ${values.join(" | ")}`,
              ),
            ].filter(Boolean) as string[],
          },
        ]
      : []),
  ];

  return (
    <Card>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="text-sm font-medium">Распознанное досье</div>
          <div className="mt-1 text-xs text-muted">Проверьте эти данные перед запуском оценки.</div>
        </div>
        <Link to={`/positions/${position.id}/edit`} className="print:hidden">
          <Button variant="secondary">Редактировать</Button>
        </Link>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {sections.map((section) => (
          <div key={section.title} className="rounded-lg border border-[rgb(var(--row-divider))] p-4">
            <div className="mb-2 text-xs uppercase tracking-wide text-muted">{section.title}</div>
            {section.items.length > 0 ? (
              <ul className="max-h-[260px] list-disc space-y-1 overflow-auto pl-5 text-sm">
                {section.items.map((item, idx) => (
                  <li key={`${section.title}-${idx}`}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted">Не заполнено</p>
            )}
            {section.title === "Полномочия" && canInferAuthorities && (
              <div className="mt-3 border-t border-[rgb(var(--row-divider))] pt-3">
                <Button variant="secondary" disabled={inferring} onClick={applyDefaultAuthorities}>
                  {inferring ? "Заполняем…" : "Заполнить шаблоном по умолчанию"}
                </Button>
                <p className="mt-2 text-xs text-muted">
                  Документ не описывает полномочия явно. Шаблон — предположение по
                  организационной иерархии (решает в своей зоне, согласует с
                  руководителем), помечается явно и заваливает QC до подтверждения
                  человеком. Надёжнее — заполнить настоящими фактами через
                  «Редактировать».
                </p>
                {inferError && <p className="mt-2 text-xs text-accent">{inferError}</p>}
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}


// ── Полная карточка с расчётом ────────────────────────────────────────────────

function groupClarifyingQuestions(questions: string[]): Record<FactorGroup | "general", string[]> {
  const result: Record<FactorGroup | "general", string[]> = {
    know_how: [], problem_solving: [], accountability: [], general: [],
  };
  for (const question of questions) {
    const text = question.toLowerCase();
    if (/полномоч|соглас|бюджет|capex|opex|масштаб|штат|подчин|ответствен|решает/.test(text)) {
      result.accountability.push(question);
    } else if (/кейс|сложн|неопредел|альтернатив|компромисс|нестандарт|trade.?off/.test(text)) {
      result.problem_solving.push(question);
    } else if (/знан|эксперт|коммуникац|переговор|домен|квалификац|функци/.test(text)) {
      result.know_how.push(question);
    } else {
      result.general.push(question);
    }
  }
  return result;
}

function ScoreView({ evaluation, score, onChanged }: { evaluation: Evaluation; score: ScoreResult; onChanged: () => void }) {
  const { data: levels } = useFactorLevelReference();
  const { data: levelRules } = useFactorLevelRules();
  const { data: scoreRange } = useFetch(
    () => evaluation.id ? api.getEvaluationRange(evaluation.id) : Promise.resolve(null),
    [evaluation.id, score.total_points],
  );
  const groups: FactorGroup[] = ["know_how", "problem_solving", "accountability"];
  const codes = factorCodes(score);
  const rows = subfactorRows(score, levels ?? EMPTY_FACTOR_LEVELS, levelRules ?? EMPTY_FACTOR_RULES);
  const evidence = groupEvidence(score);
  const clarificationQuestions = groupClarifyingQuestions(evaluation.clarifying_questions);
  const points: Record<FactorGroup, number> = {
    know_how: score.know_how.points,
    problem_solving: score.problem_solving.points,
    accountability: score.accountability.points,
  };
  // QC P1.4: показать предупреждение прямо на том факторном блоке, которого
  // оно касается (по QCFlag.factor_groups), а не только в общей карточке QC.
  const qcByGroup: Record<FactorGroup, QCFlag[]> = {
    know_how: evaluation.qc_flags.filter((f) => f.factor_groups.includes("know_how") && f.status !== "pass"),
    problem_solving: evaluation.qc_flags.filter((f) => f.factor_groups.includes("problem_solving") && f.status !== "pass"),
    accountability: evaluation.qc_flags.filter((f) => f.factor_groups.includes("accountability") && f.status !== "pass"),
  };

  return (
    <>
      {/* Summary */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Summary
          label="Грейд"
          value={String(score.grade)}
          big
          note={`${score.grade_lower}–${score.grade_upper} · ${score.grade_zone} зона`}
        />
        <Summary
          label="Итоговый балл"
          value={String(score.total_points)}
          note="Сумма трёх факторов"
        />
        <SummaryProfile
          profile={score.profile}
          steps={score.profile_steps}
          long={score.profile_long}
          note="Форма роли: A / P / L"
        />
        <ConfidenceSummary
          confidence={evaluation.confidence}
          failCount={evaluation.qc_flags.filter((flag) => flag.status === "fail").length}
          warnCount={evaluation.qc_flags.filter((flag) => flag.status === "warn").length}
        />
      </div>

      {scoreRange && (scoreRange.min_grade !== scoreRange.max_grade || scoreRange.min_points !== scoreRange.max_points) && (
        <Card className="border-warn/35 bg-warn/[0.045] p-5">
          <div className="grid gap-4 md:grid-cols-[1fr_auto] md:items-center">
            <div>
              <div className="text-xs font-semibold uppercase tracking-wide text-warn">Чувствительность предварительной оценки</div>
              <p className="mt-2 text-sm leading-6 text-[rgb(var(--fg)/0.82)]">
                При сдвиге только неподтверждённых подфакторов на один соседний уровень результат находится в диапазоне
                <span className="num font-semibold"> {scoreRange.min_points}–{scoreRange.max_points} баллов</span> и
                <span className="num font-semibold"> {scoreRange.min_grade}–{scoreRange.max_grade} грейд</span>.
              </p>
              <p className="mt-1 text-xs text-muted">
                Проверено сценариев: {scoreRange.scenarios_checked}. Это диапазон чувствительности, а не автоматически выбранный грейд.
              </p>
            </div>
            <div className="rounded-xl border border-warn/30 bg-white/70 px-5 py-3 text-center dark:bg-black/15">
              <div className="text-xs text-muted">Основной результат</div>
              <div className="num mt-1 text-2xl font-bold text-accent">{score.grade}</div>
              <div className="num text-xs text-muted">{score.total_points} баллов</div>
            </div>
          </div>
        </Card>
      )}

      {/* Factor table */}
      <Card className="p-0">
        {groups.map((g) => (
          <FactorGroupBlock
            key={g}
            group={g}
            label={FACTOR_GROUP_LABEL[g]}
            hint={FACTOR_HINTS[g]}
            code={codes[g]}
            points={points[g]}
            rows={rows[g]}
            evidence={evidence[g].evidence}
            doubts={evidence[g].doubts}
            confidence={evidence[g].confidence}
            plusMinus={evidence[g].plusMinus}
            modifierReason={evidence[g].modifierReason}
            adjacentLevel={evidence[g].adjacentLevel}
            qcFlags={qcByGroup[g]}
            questions={clarificationQuestions[g]}
            evaluationId={evaluation.id ?? null}
            editFields={factorEditFields(score)[g]}
            editOptions={factorEditOptions(score, levels ?? EMPTY_FACTOR_LEVELS)[g]}
            onChanged={onChanged}
          />
        ))}
      </Card>

      {clarificationQuestions.general.length > 0 && (
        <Card className="border-warn/25 p-5">
          <div className="text-sm font-semibold">Общие вопросы для уточнения</div>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-[15px] leading-6">
            {clarificationQuestions.general.map((question) => <li key={question}>{question}</li>)}
          </ul>
        </Card>
      )}

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
          <span className="font-semibold">Итого {score.total_points}</span>
          <Op>→</Op>
          <span>Грейд {score.grade}</span>
          <span className="text-muted">
            · Профиль {score.profile_long || score.profile} ({score.profile_steps}{" "}
            {stepsWord(score.profile_steps)})
          </span>
        </div>
      </Card>

      <Card>
        <div className="mb-3 text-sm font-medium">Подробное объяснение расчёта</div>
        <ol className="list-decimal space-y-2 pl-5 text-sm leading-relaxed">
          {(score.calculation_explanation ?? []).map((line, index) => (
            <li key={index}>{line}</li>
          ))}
        </ol>
      </Card>

      {/* QC flags */}
      <Card id="qc-flags">
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
            <QcSection title="Блокирующие" color="red" positionId={evaluation.position_id} reviewMode items={evaluation.qc_flags.filter((q) => q.status === "fail")} />
            <QcSection
              title="Требуют уточнения"
              color="amber"
              positionId={evaluation.position_id}
              reviewMode
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

function factWord(n: number): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "факт";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "факта";
  return "фактов";
}

function doubtWord(n: number): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "сомнение";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "сомнения";
  return "сомнений";
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
  const cappedSteps = Math.min(steps, 4);
  const markerPosition = profile === "L"
    ? 50
    : profile === "A"
      ? 50 - (cappedSteps / 4) * 50
      : 50 + (cappedSteps / 4) * 50;
  const outsideRange = long.endsWith("*");

  return (
    <Card className="p-5">
      <div className="text-sm text-muted">Профиль</div>
      <div className="mt-2">
        <div className="flex items-baseline justify-between gap-3">
          <span className={cn("num text-3xl font-semibold", outsideRange && "text-warn")}>{long || profile}</span>
          <span className="text-xs text-muted">{PROFILE_LABEL[profile]}</span>
        </div>

        <div className="mt-5 px-1" aria-label={`Положение профиля: ${long || profile}`}>
          <div className="relative h-3 rounded-full bg-[rgb(var(--row-divider))]">
            <span className="absolute left-1/2 top-[-3px] h-[18px] w-px bg-[rgb(var(--fg)/0.35)]" />
            {[0, 25, 75, 100].map((position) => (
              <span
                key={position}
                className="absolute top-0 h-3 w-px bg-[rgb(var(--fg)/0.18)]"
                style={{ left: `${position}%` }}
              />
            ))}
            <span
              className={cn(
                "absolute top-1/2 h-5 w-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-[3px] border-white bg-accent shadow-[0_1px_5px_rgb(0_0_0/0.28)] dark:border-[#171717]",
                outsideRange && "bg-warn ring-4 ring-warn/20",
              )}
              style={{ left: `${markerPosition}%` }}
            />
          </div>
          <div className="num mt-2 flex justify-between text-[11px] font-medium text-muted">
            <span>A4</span>
            <span>L</span>
            <span>P4</span>
          </div>
        </div>

        {outsideRange && (
          <div className="mt-3 text-xs font-medium text-warn">
            Разрыв {steps} {stepsWord(steps)}, допустимо ≤4
          </div>
        )}
      </div>
      {note && <div className="mt-2 text-xs text-muted">{note}</div>}
    </Card>
  );
}

function ConfidenceSummary({
  confidence,
  failCount,
  warnCount,
}: {
  confidence: Confidence;
  failCount: number;
  warnCount: number;
}) {
  const tone = confidence === "high" ? "text-ok" : confidence === "medium" ? "text-warn" : "text-accent";
  const reason = failCount > 0
    ? `${failCount} блокирующих замечаний требуют подтверждения`
    : warnCount > 0
      ? `${warnCount} замечаний требуют проверки`
      : "Критических замечаний по данным нет";
  return (
    <Card className="p-5">
      <div className="text-sm text-muted">Надёжность данных</div>
      <div className={cn("mt-2 text-2xl font-bold", tone)}>{CONFIDENCE_LABEL[confidence]}</div>
      <div className="mt-2 text-sm leading-5 text-muted">{reason}</div>
    </Card>
  );
}

function factorEditFields(score: ScoreResult): Record<FactorGroup, Array<string | null>> {
  return {
    know_how: ["specialization", "management", "communication"],
    problem_solving: ["area", "complexity"],
    accountability: [
      "freedom",
      null, // В KMG DIGITAL ветка N фиксирована корпоративным правилом.
      score.accountability.selection.non_quantitative_impact ? "non_quantitative_impact" : "impact",
    ],
  };
}

function levelOptions(record: Record<string, string>): Array<{ value: string; label: string }> {
  return Object.entries(record).map(([value, label]) => ({ value, label }));
}

function factorEditOptions(
  score: ScoreResult,
  levels: typeof EMPTY_FACTOR_LEVELS,
): Record<FactorGroup, Array<Array<{ value: string; label: string }>>> {
  const accountabilityImpact = score.accountability.selection.non_quantitative_impact
    ? levels.non_quantitative_impact
    : levels.impact_type;
  return {
    know_how: [
      levelOptions(levels.specialized_know_how),
      levelOptions(levels.managerial_know_how),
      levelOptions(levels.communication),
    ],
    problem_solving: [
      levelOptions(levels.problem_area),
      levelOptions(levels.problem_complexity),
    ],
    accountability: [
      levelOptions(levels.freedom_to_act),
      [],
      levelOptions(accountabilityImpact),
    ],
  };
}

function AttentionDetails({ initiallyOpen, rules }: { initiallyOpen: boolean; rules: string[] }) {
  const [open, setOpen] = useState(initiallyOpen);
  return (
    <details
      open={open}
      onToggle={(event) => setOpen(event.currentTarget.open)}
      className="mt-2 max-w-4xl text-sm leading-6 text-muted"
    >
      <summary className="cursor-pointer font-semibold text-[rgb(var(--fg)/0.72)]">
        На что обратить внимание
      </summary>
      <ul className="mt-1.5 list-disc space-y-1 pl-4">
        {rules.map((rule) => <li key={rule}>{rule}</li>)}
      </ul>
    </details>
  );
}

function FactorGroupBlock({
  group,
  label,
  hint,
  code,
  points,
  rows,
  evidence,
  doubts,
  confidence,
  plusMinus,
  modifierReason,
  adjacentLevel,
  qcFlags,
  questions,
  evaluationId,
  editFields,
  editOptions,
  onChanged,
}: {
  group: FactorGroup;
  label: string;
  hint: string;
  code: string;
  points: number;
  rows: SubfactorRow[];
  evidence: string[];
  doubts: string[];
  confidence: Confidence;
  plusMinus: number;
  modifierReason: string | null;
  adjacentLevel: string | null;
  qcFlags: QCFlag[];
  questions: string[];
  evaluationId: string | null;
  editFields: Array<string | null>;
  editOptions: Array<Array<{ value: string; label: string }>>;
  onChanged: () => void;
}) {
  const failCount = qcFlags.filter((f) => f.status === "fail").length;
  const warnCount = qcFlags.filter((f) => f.status === "warn").length;
  const hasQcIssue = failCount > 0 || warnCount > 0;
  // Проблемный фактор раскрываем при первом рендере для FAIL и WARN.
  // После этого пользователь по-прежнему может свернуть его вручную.
  const [open, setOpen] = useState(() => hasQcIssue);
  const [editingRow, setEditingRow] = useState<number | null>(null);
  const [nextLevel, setNextLevel] = useState("");
  const [editReason, setEditReason] = useState("");
  const [savingLevel, setSavingLevel] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);
  const hasModifier = plusMinus !== 0;

  function beginEdit(index: number, currentLevel: string) {
    setEditingRow(index);
    setNextLevel(currentLevel);
    setEditReason("");
    setEditError(null);
  }

  async function saveLevel(index: number) {
    const field = editFields[index];
    if (!evaluationId || !field || !editReason.trim()) return;
    setSavingLevel(true);
    setEditError(null);
    try {
      await api.patchEvaluationFactor(evaluationId, {
        factor_group: group,
        field,
        value: field === "complexity" ? Number(nextLevel) : nextLevel,
        reason: editReason.trim(),
      });
      setEditingRow(null);
      onChanged();
    } catch (reason) {
      setEditError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setSavingLevel(false);
    }
  }
  return (
    <div className="border-t border-[rgb(var(--row-divider))] first:border-t-0">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-start gap-4 px-5 py-4 text-left transition-colors hover:bg-black/[0.025] dark:hover:bg-white/[0.035]"
      >
        <span className="flex-1 pr-3">
          <span className="block text-sm font-semibold uppercase tracking-wide text-[rgb(var(--fg)/0.88)]">{label}</span>
          <span className="mt-1 block text-sm leading-5 text-muted">{hint}</span>
        </span>
        {(failCount > 0 || warnCount > 0) && (
          <span className="mt-0.5 flex items-center gap-1.5 text-xs" title="QC-замечания по этому фактору — см. ниже">
            {failCount > 0 && <span className="num font-semibold text-accent">✗ {failCount}</span>}
            {warnCount > 0 && <span className="num font-semibold text-warn">⚠ {warnCount}</span>}
          </span>
        )}
        <span className="num text-sm text-muted">{code}</span>
        <span
          onClick={(e) => e.stopPropagation()}
          title={rows.map((r) => `${r.name}: ${r.level} — ${r.description}`).join("\n\n")}
          className="grid h-4 w-4 shrink-0 cursor-help place-items-center rounded-full border border-[rgb(var(--row-divider))] text-[10px] text-muted"
        >
          ?
        </span>
        <span className="num w-16 text-right text-sm font-semibold">{points}</span>
        <span className="w-24 text-right text-sm text-muted">
          <span className="block">{CONFIDENCE_LABEL[confidence]}</span>
          <span className="block text-[11px]">
            {evidence.length} {factWord(evidence.length)} · {doubts.length} {doubtWord(doubts.length)}
          </span>
        </span>
        {/* Шеврон сворачивания — не "+/−": этот же символ выше в коде факторов
            означает методологический модификатор границы, нельзя путать. */}
        <span className={cn("mt-1 w-4 text-center text-muted transition-transform", open && "rotate-180")}>▾</span>
      </button>
      {rows.map((r, rowIndex) => (
        <div
          key={r.name}
          className="grid grid-cols-[minmax(0,1fr)_auto] gap-5 border-t border-[rgb(var(--row-divider))] px-5 py-4"
        >
          <div className="min-w-0">
            <div className="text-[15px] font-semibold text-fg">{r.name}</div>
            <p className="mt-1 max-w-4xl text-[15px] leading-7 text-[rgb(var(--fg)/0.84)]">
              {r.description}
            </p>
            <p className="mt-2 max-w-4xl text-sm leading-6 text-muted">
              <span className="font-semibold text-[rgb(var(--fg)/0.72)]">Проверочный вопрос: </span>
              {r.expertCheck}
            </p>
            {r.rules.length > 0 && (
              <AttentionDetails initiallyOpen={hasQcIssue} rules={r.rules} />
            )}
          </div>
          <div className="mt-0.5 min-w-16 text-right">
            {editFields[rowIndex] && evaluationId ? (
              <button
                type="button"
                title="Изменить уровень и сразу пересчитать оценку"
                onClick={() => beginEdit(rowIndex, r.level)}
                className="num text-xl font-bold leading-none text-accent underline decoration-accent/25 underline-offset-4 transition hover:decoration-accent"
              >
                {r.level}
              </button>
            ) : (
              <span className="num text-xl font-bold leading-none text-accent">{r.level}</span>
            )}
          </div>
          {editingRow === rowIndex && (
            <div className="col-span-2 rounded-xl border border-accent/25 bg-accent/[0.035] p-4">
              <div className="grid gap-3 md:grid-cols-[minmax(180px,0.55fr)_minmax(260px,1fr)_auto] md:items-end">
                <label className="block">
                  <span className="mb-1.5 block text-xs font-medium text-muted">Новый уровень</span>
                  <select className="field" value={nextLevel} onChange={(event) => setNextLevel(event.target.value)}>
                    {editOptions[rowIndex].map((option) => (
                      <option key={option.value} value={option.value}>{option.value} — {option.label}</option>
                    ))}
                  </select>
                </label>
                <label className="block">
                  <span className="mb-1.5 block text-xs font-medium text-muted">Основание изменения</span>
                  <input
                    className="field"
                    value={editReason}
                    onChange={(event) => setEditReason(event.target.value)}
                    placeholder="Какой факт подтверждает новый уровень?"
                  />
                </label>
                <div className="flex gap-2">
                  <Button disabled={savingLevel || !editReason.trim() || nextLevel === r.level} onClick={() => void saveLevel(rowIndex)}>
                    {savingLevel ? "Сохраняем…" : "Применить"}
                  </Button>
                  <Button variant="ghost" onClick={() => setEditingRow(null)}>Отмена</Button>
                </div>
              </div>
              {editError && <p className="mt-2 text-xs text-accent">{editError}</p>}
              <p className="mt-2 text-xs text-muted">Баллы, грейд, профиль и QC пересчитаются автоматически. Основание сохранится в аудите оценки.</p>
            </div>
          )}
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
            <div className="space-y-4 bg-[#faf9f6] px-7 pb-6 pt-5 text-[15px] leading-7 text-[rgb(var(--fg)/0.86)] dark:bg-white/[0.025] sm:px-9">
              <div className="text-xs font-semibold uppercase tracking-wide text-fg">Доказательства выбора уровня</div>
              <ul className="list-disc space-y-1.5 pl-5">
                {evidence.length > 0 ? evidence.map((e) => <li key={e}>{e}</li>) : <li>—</li>}
              </ul>
              {doubts.length > 0 && (
                <>
                  <div className="pt-1 text-xs font-semibold uppercase tracking-wide text-fg">Что нужно подтвердить</div>
                  <ul className="list-disc space-y-1.5 pl-5">
                    {doubts.map((d) => (
                      <li key={d}>{d}</li>
                    ))}
                  </ul>
                </>
              )}
              {questions.length > 0 && (
                <div className="rounded-xl border border-warn/30 bg-warn/[0.055] p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-warn">Вопросы HR по этому фактору</div>
                  <ul className="mt-2 list-disc space-y-1.5 pl-5">
                    {questions.map((question) => <li key={question}>{question}</li>)}
                  </ul>
                </div>
              )}
              {hasModifier && (
                <>
                  <div className="pt-1 text-xs font-semibold uppercase tracking-wide text-fg">
                    {`Почему именно ${plusMinus > 0 ? "+" : "−"} (граничный модификатор)`}
                  </div>
                  {modifierReason || adjacentLevel ? (
                    <p className="text-[rgb(var(--fg)/0.82)]">
                      {adjacentLevel && (
                        <>
                          Сравнивали с соседней ячейкой <span className="num font-semibold">{adjacentLevel}</span>.{" "}
                        </>
                      )}
                      {modifierReason || "Причина границы не указана текстом."}
                    </p>
                  ) : (
                    <p className="text-warn">
                      Модификатор применён, но эксперт/агент не указал ни соседний уровень, ни причину
                      границы — это считается необоснованным (см. QC «Модификатор не имеет обоснования»).
                    </p>
                  )}
                </>
              )}
              {qcFlags.length > 0 && (
                <>
                  <div className="pt-1 text-xs font-semibold uppercase tracking-wide text-fg">
                    QC-замечания по этому фактору
                  </div>
                  <ul className="space-y-2">
                    {qcFlags.map((flag, flagIndex) => (
                      <li key={flag.code}>
                        <a
                          href={`#qc-${flag.code}`}
                          className={cn(
                            "flex items-center justify-between gap-3 rounded-lg border px-4 py-3 text-sm font-medium transition-colors hover:border-accent",
                            flag.status === "fail" ? "border-accent/30 bg-accent/[0.045] text-accent" : "border-warn/30 bg-warn/[0.045] text-warn",
                          )}
                        >
                          <span>
                            {flag.status === "fail" ? "✗ Блокирующее замечание" : "⚠ Замечание"}
                            {qcFlags.length > 1 ? ` ${flagIndex + 1}` : ""}
                          </span>
                          <span className="shrink-0 text-xs">См. QC ниже ↓</span>
                        </a>
                      </li>
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
