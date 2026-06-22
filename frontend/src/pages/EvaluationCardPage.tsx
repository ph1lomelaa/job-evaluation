import { AnimatePresence, motion } from "framer-motion";
import { useMemo, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, Skeleton, StatusDot } from "../components/ui";
import { QcItem, QcSection } from "../components/QcFlags";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { useFactorLevelReference, useFactorLevelRules } from "../lib/factorLevels";
import {
  EMPTY_FACTOR_LEVELS,
  EMPTY_FACTOR_RULES,
  factorCodes,
  groupEvidence,
  scopeSummary,
  subfactorRows,
  type SubfactorRow,
} from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import {
  CONFIDENCE_LABEL,
  FACTOR_GROUP_LABEL,
  PROFILE_LABEL,
  STATUS_LABEL,
  type Confidence,
  type Evaluation,
  type FactorGroup,
  type JobDossier,
  type QCFlag,
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
  const navigate = useNavigate();
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

  const evaluation = versions.find((v) => v.id === versionId) ?? versions[0];

  const needsDraftReview = Boolean(
    data?.[0]?.review_status === "draft_imported" &&
    data[0].import_metadata?.missing_fields.length,
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
                {evaluation.qc_flags.some((f) => f.status === "warn") && (
                  <a href="#qc-flags" title="Перейти к QC-проверкам">
                    <StatusDot color="amber">
                      ⚠ {evaluation.qc_flags.filter((f) => f.status === "warn").length} замечаний QC
                    </StatusDot>
                  </a>
                )}
                <StatusDot color={CONF_DOT[evaluation.confidence]}>
                  Уверенность: {CONFIDENCE_LABEL[evaluation.confidence].toLowerCase()}
                </StatusDot>
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
            <div className="flex items-center gap-2 print:hidden">
              <Button disabled={evaluating} onClick={runEvaluation}>
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
                  PDF
                </Button>
              )}
            </div>
          </div>
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
                Уровни факторов выбраны офлайн-заглушкой (FakeAgent), а не реальным агентом —
                это демонстрационный расчёт. Переоцените должность с настоящим агентом
                (ANTHROPIC_API_KEY/GROQ_API_KEY/OPENAI_API_KEY) перед выносом на комитет.
              </p>
            </div>
          </div>
        </Card>
      )}

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
              <div className="text-muted">Метод: {position.import_metadata.extraction_method}</div>
              {position.import_metadata.missing_fields.length > 0 && (
                <div>
                  <div className="text-xs uppercase tracking-wide text-muted">Не найдено в документе</div>
                  <div className="mt-1 text-sm">
                    {position.import_metadata.missing_fields.join(", ")}
                  </div>
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

      <DossierPreview position={position} onChanged={reload} />

      {evaluation && (
        <Card className="border-accent/20 p-5">
          <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
            <div>
              <div className="text-xs uppercase tracking-wide text-muted">Что означает статус</div>
              <p className="mt-2 text-sm leading-relaxed text-[rgb(var(--fg)/0.78)]">
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




      {evaluation?.score && <ScoreView evaluation={evaluation} score={evaluation.score} />}

      {evaluation && (
        <>
          {evaluation.role_summary && (
            <Card>
              <div className="mb-3 text-sm font-semibold">Резюме должности</div>
              <p className="text-[15px] leading-7">{evaluation.role_summary}</p>
            </Card>
          )}

<div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <Card>
              <div className="mb-3 text-sm font-semibold">Обоснование по факторам</div>
              <p className="whitespace-pre-line text-[15px] leading-7">
                {evaluation.reasoning || "—"}
              </p>
            </Card>
            <Card>
              <div className="mb-3 text-sm font-semibold">Вопросы на уточнение</div>
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
                ? `Метод: ${position.import_metadata.extraction_method}`
                : null,
              ...Object.entries(position.import_metadata.field_sources ?? {}).map(
                ([field, values]) => `${field}: ${values.join(" | ")}`,
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

function ScoreView({ evaluation, score }: { evaluation: Evaluation; score: ScoreResult }) {
  const { data: levels } = useFactorLevelReference();
  const { data: levelRules } = useFactorLevelRules();
  const groups: FactorGroup[] = ["know_how", "problem_solving", "accountability"];
  const codes = factorCodes(score);
  const rows = subfactorRows(score, levels ?? EMPTY_FACTOR_LEVELS, levelRules ?? EMPTY_FACTOR_RULES);
  const evidence = groupEvidence(score);
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
      <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
        <Summary
          label="Итоговый балл"
          value={String(score.total_points)}
          note="Сумма трех факторов"
        />
        <Summary
          label="Грейд"
          value={String(score.grade)}
          big
          note={`${score.grade_lower}–${score.grade_upper} · ${score.grade_zone} зона`}
        />
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
            plusMinus={evidence[g].plusMinus}
            modifierReason={evidence[g].modifierReason}
            adjacentLevel={evidence[g].adjacentLevel}
            qcFlags={qcByGroup[g]}
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
        {score.methodology_basis && (
          <p className="mt-4 border-t border-[rgb(var(--row-divider))] pt-3 text-xs leading-relaxed text-muted">
            {score.methodology_basis}
          </p>
        )}
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
  plusMinus,
  modifierReason,
  adjacentLevel,
  qcFlags,
}: {
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
}) {
  const failCount = qcFlags.filter((f) => f.status === "fail").length;
  const warnCount = qcFlags.filter((f) => f.status === "warn").length;
  // Если по фактору есть блокирующее замечание, разворачиваем блок сразу —
  // иначе рецензент может одобрить карточку, не заметив FAIL под счётчиком.
  const [open, setOpen] = useState(() => failCount > 0);
  const hasModifier = plusMinus !== 0;
  return (
    <div className="border-t border-[rgb(var(--row-divider))] first:border-t-0">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-start gap-4 px-5 py-4 text-left transition-colors hover:bg-black/[0.025] dark:hover:bg-white/[0.035]"
      >
        <span className="flex-1 pr-3">
          <span className="block text-xs font-semibold uppercase tracking-wide text-[rgb(var(--fg)/0.82)]">{label}</span>
          <span className="mt-1 block text-xs text-muted">{hint}</span>
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
      {rows.map((r) => (
        <div
          key={r.name}
          className="grid grid-cols-[minmax(0,1fr)_auto] gap-5 border-t border-[rgb(var(--row-divider))] px-5 py-4"
        >
          <div className="min-w-0">
            <div className="text-sm font-semibold text-fg">{r.name}</div>
            <p className="mt-1 max-w-4xl text-sm leading-6 text-[rgb(var(--fg)/0.78)]">
              {r.description}
            </p>
            <p className="mt-2 max-w-4xl text-xs leading-5 text-muted">
              <span className="font-semibold text-[rgb(var(--fg)/0.72)]">Проверочный вопрос: </span>
              {r.expertCheck}
            </p>
            {r.rules.length > 0 && (
              <details className="mt-2 max-w-4xl text-xs leading-5 text-muted">
                <summary className="cursor-pointer font-semibold text-[rgb(var(--fg)/0.72)]">
                  На что обратить внимание
                </summary>
                <ul className="mt-1.5 list-disc space-y-1 pl-4">
                  {r.rules.map((rule) => (
                    <li key={rule}>{rule}</li>
                  ))}
                </ul>
              </details>
            )}
          </div>
          <span className="num mt-0.5 min-w-10 text-center text-xl font-bold leading-none text-accent">
            {r.level}
          </span>
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
            <div className="space-y-3 bg-[#faf9f6] px-9 pb-5 pt-4 text-sm leading-6 text-[rgb(var(--fg)/0.82)] dark:bg-white/[0.025]">
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
              <>
                <div className="pt-1 text-xs font-semibold uppercase tracking-wide text-fg">
                  {hasModifier
                    ? `Почему именно ${plusMinus > 0 ? "+" : "−"} (граничный модификатор)`
                    : "Модификатор"}
                </div>
                {!hasModifier ? (
                  <p className="text-[rgb(var(--fg)/0.78)]">
                    Модификатор не применён — выбран базовый уровень ячейки.
                  </p>
                ) : modifierReason || adjacentLevel ? (
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
              {qcFlags.length > 0 && (
                <>
                  <div className="pt-1 text-xs font-semibold uppercase tracking-wide text-fg">
                    QC-замечания по этому фактору
                  </div>
                  <ul className="space-y-3">
                    {qcFlags.map((flag) => (
                      <QcItem key={flag.code} flag={flag} />
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
