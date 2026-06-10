import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, ErrorBanner, Field, Input, Stepper, Textarea } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import type { JobDossier, ProblemCase, QCStatus } from "../lib/types";

const STEPS = [
  "Идентификация",
  "Цель и результаты",
  "Полномочия",
  "Масштаб",
  "Якоря и кейсы",
  "Контекст",
  "Документы",
];

const DRAFT_KEY = "jeval.job-form.draft.v1";

const GATE_STEP: Partial<Record<string, number>> = {
  "Цель должности": 1,
  "Ключевые результаты": 1,
  "Описание функций": 1,
  "KPI / показатели блока": 1,
  "Полномочия (сам/согласует/рекомендует)": 2,
  "Масштаб воздействия": 3,
  "Стейкхолдеры": 3,
  "Якорные должности": 4,
  "Типовые кейсы (Problem Solving)": 4,
  "Оргконтекст": 5,
  "Дата среза": 0,
  "Лимиты (бюджет, закупки, stop-work)": 2,
  "Подтверждение руководителя / HR": 6,
};

interface FormState {
  name: string;
  dzo: string;
  department: string;
  function: string;
  snapshotDate: string;
  purpose: string;
  keyResults: string;
  responsibilities: string;
  kpis: string;
  decidesAlone: string;
  requiresApproval: string;
  recommends: string;
  limits: string;
  opex: string;
  capex: string;
  headcount: string;
  scopeSource: string;
  stakeholders: string;
  anchors: string;
  problemCases: string;
  context: string;
  manager: string;
  subordinates: string;
  documents: string;
  confirmedBy: string;
}

const EMPTY: FormState = {
  name: "", dzo: "", department: "", function: "",
  snapshotDate: new Date().toISOString().slice(0, 10),
  purpose: "", keyResults: "", responsibilities: "", kpis: "",
  decidesAlone: "", requiresApproval: "", recommends: "", limits: "",
  opex: "", capex: "", headcount: "", scopeSource: "",
  stakeholders: "", anchors: "", problemCases: "",
  context: "", manager: "", subordinates: "", documents: "", confirmedBy: "",
};

interface DraftSnapshot {
  step: number;
  form: FormState;
  savedAt: string;
}

const lines = (v: string) => v.split("\n").map((s) => s.trim()).filter(Boolean);
const num = (v: string) => {
  const n = Number(v.replace(/[\s_]/g, ""));
  return v.trim() && Number.isFinite(n) ? n : null;
};

function hasFormContent(form: FormState): boolean {
  return Object.entries(form).some(([key, value]) => key !== "snapshotDate" && value.trim().length > 0);
}

function clampStep(step: number): number {
  if (!Number.isFinite(step)) return 0;
  return Math.min(Math.max(Math.trunc(step), 0), STEPS.length - 1);
}

function normalizeForm(raw: unknown): FormState {
  const source = raw && typeof raw === "object" ? (raw as Partial<Record<keyof FormState, unknown>>) : {};
  const form = { ...EMPTY };
  for (const key of Object.keys(EMPTY) as (keyof FormState)[]) {
    form[key] = typeof source[key] === "string" ? source[key] : "";
  }
  return form;
}

function readDraft(): DraftSnapshot | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(DRAFT_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<DraftSnapshot> & { form?: unknown };
    const form = normalizeForm(parsed.form);
    if (!hasFormContent(form)) return null;
    return {
      step: clampStep(typeof parsed.step === "number" ? parsed.step : 0),
      form,
      savedAt: typeof parsed.savedAt === "string" ? parsed.savedAt : new Date().toISOString(),
    };
  } catch {
    return null;
  }
}

function writeDraft(snapshot: DraftSnapshot) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(DRAFT_KEY, JSON.stringify(snapshot));
  } catch {
    // localStorage может быть недоступен в некоторых режимах браузера.
  }
}

function clearDraft() {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(DRAFT_KEY);
  } catch {
    // ignore
  }
}

function formatSavedAt(ts: string | null): string {
  if (!ts) return "";
  try {
    return new Intl.DateTimeFormat("ru-RU", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(ts));
  } catch {
    return ts;
  }
}

/** Кейс PS: «суть | что задано | что неизвестно | альтернативы | tradeoff | проверка».
 * Строка без «|» остаётся простым кейсом (problem_cases). */
function parseCases(v: string): { plain: string[]; structured: ProblemCase[] } {
  const plain: string[] = [];
  const structured: ProblemCase[] = [];
  for (const line of lines(v)) {
    const parts = line.split("|").map((s) => s.trim());
    if (parts.length < 2) {
      plain.push(line);
      continue;
    }
    const [summary, given, unknown, alternatives, tradeoff, verification] = parts;
    structured.push({
      summary,
      given: given || null,
      unknown: unknown || null,
      alternatives: alternatives || null,
      tradeoff: tradeoff || null,
      verification: verification || null,
    });
  }
  return { plain, structured };
}

/** Собрать JE-досье в формате бэкенда (jeval/domain/models.py). */
function toDossier(f: FormState): JobDossier {
  const cases = parseCases(f.problemCases);
  return {
    name: f.name.trim(),
    dzo: f.dzo.trim() || null,
    department: f.department.trim() || null,
    function: f.function.trim() || null,
    snapshot_date: f.snapshotDate || null,
    purpose: f.purpose.trim() || null,
    key_results: lines(f.keyResults),
    responsibilities: lines(f.responsibilities),
    kpis: lines(f.kpis),
    reporting: {
      manager: f.manager.trim() || null,
      subordinates: lines(f.subordinates),
      matrix_links: [],
    },
    authorities: {
      decides_alone: lines(f.decidesAlone),
      // строка «что — кто утверждает» (разделители: —, ->, |)
      requires_approval: lines(f.requiresApproval).map((l) => {
        const [item, approver] = l.split(/\s*(?:—|->|\|)\s*/);
        return { item: (item ?? l).trim(), approver: (approver ?? "").trim() || "не указано" };
      }),
      recommends: lines(f.recommends),
    },
    scope: {
      annual_opex: num(f.opex),
      annual_capex: num(f.capex),
      headcount: num(f.headcount),
      source: f.scopeSource.trim() || null,
    },
    limits: lines(f.limits),
    stakeholders: lines(f.stakeholders),
    organizational_context: f.context.trim() || null,
    anchor_roles: lines(f.anchors),
    problem_cases: cases.plain,
    problem_cases_structured: cases.structured,
    documents: lines(f.documents),
    confirmed_by: f.confirmedBy.trim() || null,
  };
}

// Живой Gate 0: зеркало критических/рекомендуемых блоков jeval/gate.py.
function gate(f: FormState): { block: string; status: QCStatus; note?: string }[] {
  const filled = (v: string) => v.trim().length > 0;
  const n = (v: string) => lines(v).length;
  const cases = parseCases(f.problemCases);
  const caseCount = cases.plain.length + cases.structured.length;
  const critical = (ok: boolean): QCStatus => (ok ? "pass" : "fail");
  const recommended = (ok: boolean): QCStatus => (ok ? "pass" : "warn");
  return [
    { block: "Цель должности", status: critical(filled(f.purpose)) },
    {
      block: "Ключевые результаты",
      status: critical(n(f.keyResults) > 0),
      note: n(f.keyResults) > 0 && n(f.keyResults) < 5 ? "Желательно 5–10" : undefined,
    },
    { block: "Описание функций", status: critical(n(f.responsibilities) > 0) },
    { block: "Оргконтекст", status: critical(filled(f.context)) },
    {
      block: "Полномочия (сам/согласует/рекомендует)",
      status: critical(filled(f.decidesAlone) || filled(f.requiresApproval) || filled(f.recommends)),
    },
    {
      block: "Масштаб воздействия",
      status: critical(num(f.opex) != null || num(f.capex) != null || num(f.headcount) != null),
    },
    { block: "KPI / показатели блока", status: critical(n(f.kpis) > 0) },
    { block: "Стейкхолдеры", status: recommended(n(f.stakeholders) > 0) },
    { block: "Якорные должности", status: recommended(n(f.anchors) > 0) },
    {
      block: "Типовые кейсы (Problem Solving)",
      status: recommended(caseCount >= 3),
      note: caseCount < 3 ? "Нужно минимум 3 кейса, можно смешивать обычные и структурированные" : undefined,
    },
    { block: "Дата среза", status: recommended(filled(f.snapshotDate)) },
    { block: "Лимиты (бюджет, закупки, stop-work)", status: recommended(n(f.limits) > 0) },
    { block: "Подтверждение руководителя / HR", status: recommended(filled(f.confirmedBy)) },
  ];
}

const GATE_ICON: Record<QCStatus, { ch: string; cls: string }> = {
  pass: { ch: "✓", cls: "text-ok" },
  warn: { ch: "⚠", cls: "text-warn" },
  fail: { ch: "✗", cls: "text-accent" },
};

function GateIssue({
  check,
  actionLabel,
  stepLabel,
  onOpen,
  muted,
}: {
  check: { block: string; status: QCStatus; note?: string };
  actionLabel: string;
  stepLabel: string;
  onOpen: () => void;
  muted?: boolean;
}) {
  return (
    <div className={cn("rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-3", muted && "opacity-90")}>
      <div className="flex items-start gap-3">
        <span className={cn("num w-4 shrink-0", GATE_ICON[check.status].cls)}>{GATE_ICON[check.status].ch}</span>
        <div className="min-w-0 flex-1">
          <div className="text-sm">{check.block}</div>
          <div className="mt-0.5 text-xs text-muted">
            {check.note ? <span>{check.note}</span> : <span>Проверьте этот блок досье.</span>}
            <span className="ml-1">· {stepLabel}</span>
          </div>
        </div>
        <Button
          variant="ghost"
          className="px-2 py-1 text-[11px] min-h-0"
          onClick={onOpen}
          type="button"
        >
          {actionLabel}
        </Button>
      </div>
    </div>
  );
}

export default function JobFormPage() {
  const navigate = useNavigate();
  const [draftSnapshot] = useState<DraftSnapshot | null>(() => readDraft());
  const [step, setStep] = useState(() => draftSnapshot?.step ?? 0);
  const [f, setF] = useState<FormState>(() => draftSnapshot?.form ?? EMPTY);
  const [files, setFiles] = useState<File[]>([]);
  const fileInput = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState<"save" | "evaluate" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [draftSavedAt, setDraftSavedAt] = useState<string | null>(draftSnapshot?.savedAt ?? null);
  const [draftRestored, setDraftRestored] = useState(() => draftSnapshot !== null);
  const set = (k: keyof FormState) => (e: { target: { value: string } }) =>
    setF((s) => ({ ...s, [k]: e.target.value }));
  const addFiles = (list: FileList | null) => {
    if (list) setFiles((fs) => [...fs, ...Array.from(list)]);
  };

  const checks = useMemo(() => gate(f), [f]);
  const hasFail = checks.some((c) => c.status === "fail");
  const hasWarn = checks.some((c) => c.status === "warn");
  const criticalChecks = checks.filter((c) => c.status === "fail");
  const warningChecks = checks.filter((c) => c.status === "warn");
  const noName = !f.name.trim();
  const verdict = hasFail
    ? { text: "Оценка невозможна без данных", cls: "text-accent" }
    : hasWarn
      ? { text: "Требуются уточнения", cls: "text-warn" }
      : { text: "Готово к оценке", cls: "text-ok" };

  useEffect(() => {
    const timer = window.setTimeout(() => {
      if (!hasFormContent(f)) {
        clearDraft();
        setDraftSavedAt(null);
        return;
      }
      const snapshot: DraftSnapshot = { step, form: f, savedAt: new Date().toISOString() };
      writeDraft(snapshot);
      setDraftSavedAt(snapshot.savedAt);
    }, 350);
    return () => window.clearTimeout(timer);
  }, [f, step]);

  function discardDraft() {
    setF(EMPTY);
    setStep(0);
    setFiles([]);
    clearDraft();
    setDraftSavedAt(null);
    setDraftRestored(false);
  }

  async function save(): Promise<string | null> {
    setError(null);
    try {
      const created = await api.createPosition(toDossier(f));
      const id = created.id ?? null;
      if (id) {
        for (const file of files) {
          await api.uploadDocument(id, file);
        }
      }
      return id;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      return null;
    }
  }

  async function onSave() {
    setBusy("save");
    const id = await save();
    setBusy(null);
    if (id) {
      discardDraft();
      navigate(`/positions/${id}`);
    }
  }

  async function onEvaluate() {
    setBusy("evaluate");
    const id = await save();
    if (!id) {
      setBusy(null);
      return;
    }
    try {
      await api.evaluate(id);
      discardDraft();
      setBusy(null);
      navigate(`/positions/${id}`);
    } catch (e) {
      // должность уже сохранена — показываем ошибку оценки на её карточке
      const message = e instanceof Error ? e.message : String(e);
      setBusy(null);
      navigate(`/positions/${id}`, { state: { evaluationError: message } });
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-[32px]">Новая должность</h1>
      <Stepper steps={STEPS} current={step} onSelect={setStep} />
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] px-4 py-3 text-xs text-muted">
        <span>
          {draftSavedAt
            ? `Черновик сохранён локально ${formatSavedAt(draftSavedAt)}`
            : "Автосохранение включено: черновик появится после первого заполнения."}
        </span>
        {draftSavedAt && (
          <Button
            variant="ghost"
            className="px-3 py-1.5 text-xs min-h-0"
            onClick={discardDraft}
            type="button"
          >
            Очистить черновик
          </Button>
        )}
      </div>
      {draftRestored && (
        <p className="text-xs text-muted">Черновик восстановлен из локального хранилища браузера.</p>
      )}
      <p className="max-w-[920px] text-sm text-muted">
        Сначала заполните цель, результаты, полномочия, масштаб и KPI. Именно эти блоки решают,
        можно ли вообще переходить к оценке.
      </p>

      {error && <ErrorBanner message={error} />}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px]">
        {/* Левая панель: поля шага */}
        <Card className="space-y-5">
          {step === 0 && (
            <>
              <Field label="Наименование должности">
                <Input value={f.name} onChange={set("name")} placeholder="Начальник управления ТОиР актива" />
              </Field>
              <Field label="ДЗО / организация">
                <Input value={f.dzo} onChange={set("dzo")} placeholder="ДЗО Добыча" />
              </Field>
              <Field label="Подразделение">
                <Input value={f.department} onChange={set("department")} placeholder="Управление ТОиР" />
              </Field>
              <Field label="Функция">
                <Input value={f.function} onChange={set("function")} placeholder="ТОиР / Производство" />
              </Field>
              <Field label="Дата среза" hint="оценивается роль «как есть» на эту дату">
                <Input type="date" value={f.snapshotDate} onChange={set("snapshotDate")} />
              </Field>
            </>
          )}
          {step === 1 && (
            <>
              <Field label="Цель должности" hint="1–2 предложения: зачем существует роль">
                <Textarea value={f.purpose} onChange={set("purpose")} />
              </Field>
              <Field label="Ключевые результаты" hint="по одному в строке, 5–10 результатов (не процессов)">
                <Textarea value={f.keyResults} onChange={set("keyResults")} />
              </Field>
              <Field label="Описание функций / обязанности" hint="по одной в строке">
                <Textarea value={f.responsibilities} onChange={set("responsibilities")} />
              </Field>
              <Field label="KPI / показатели" hint="по одному в строке; если индивидуальных нет — KPI блока">
                <Textarea value={f.kpis} onChange={set("kpis")} />
              </Field>
            </>
          )}
          {step === 2 && (
            <>
              <Field label="Решает самостоятельно" hint="по одному в строке">
                <Textarea value={f.decidesAlone} onChange={set("decidesAlone")} />
              </Field>
              <Field
                label="Требует согласования"
                hint="формат: «что — кто утверждает», напр. «CAPEX свыше лимита — Комитет»"
              >
                <Textarea value={f.requiresApproval} onChange={set("requiresApproval")} />
              </Field>
              <Field label="Только рекомендует" hint="по одному в строке">
                <Textarea value={f.recommends} onChange={set("recommends")} />
              </Field>
              <Field
                label="Лимиты"
                hint="бюджет, закупки, договоры, штат, stop-work, технические решения — по одному в строке"
              >
                <Textarea value={f.limits} onChange={set("limits")} />
              </Field>
            </>
          )}
          {step === 3 && (
            <>
              <Field label="Годовой OPEX, ₸" hint="в зоне ответственности роли, не всей компании">
                <Input value={f.opex} onChange={set("opex")} placeholder="4000000000" inputMode="numeric" />
              </Field>
              <Field label="Годовой CAPEX, ₸">
                <Input value={f.capex} onChange={set("capex")} placeholder="1500000000" inputMode="numeric" />
              </Field>
              <Field label="Численность в зоне роли">
                <Input value={f.headcount} onChange={set("headcount")} placeholder="120" inputMode="numeric" />
              </Field>
              <Field label="Источник цифр" hint="бюджет, бизнес-план, управленческая отчётность">
                <Input value={f.scopeSource} onChange={set("scopeSource")} placeholder="Бюджет 2026" />
              </Field>
              <Field label="Стейкхолдеры" hint="по одному в строке, включая внешних">
                <Textarea value={f.stakeholders} onChange={set("stakeholders")} />
              </Field>
            </>
          )}
          {step === 4 && (
            <>
              <Field label="Якорные должности" hint="2–3 сопоставимые утверждённые роли, по одной в строке">
                <Textarea value={f.anchors} onChange={set("anchors")} />
              </Field>
              <Field
                label="Типовые нестандартные кейсы"
                hint={
                  "минимум 3, по одному в строке. Структурированный формат через «|»: " +
                  "суть | что задано | что неизвестно | альтернативы | tradeoff | проверка"
                }
              >
                <Textarea value={f.problemCases} onChange={set("problemCases")} />
              </Field>
            </>
          )}
          {step === 5 && (
            <>
              <Field label="Организационный контекст" hint="операторская модель, governance, лимиты, DoA">
                <Textarea value={f.context} onChange={set("context")} />
              </Field>
              <Field label="Непосредственный руководитель">
                <Input value={f.manager} onChange={set("manager")} placeholder="Директор по производству" />
              </Field>
              <Field label="Подчинённые" hint="должности/группы, по одной в строке">
                <Textarea value={f.subordinates} onChange={set("subordinates")} />
              </Field>
            </>
          )}
          {step === 6 && (
            <>
              <Field
                label="Файлы досье"
                hint="ДИ, оргструктура, положение, RACI, DoA — загрузятся при сохранении; файлы не входят в локальный черновик"
              >
                <div
                  onClick={() => fileInput.current?.click()}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    addFiles(e.dataTransfer.files);
                  }}
                  className="cursor-pointer rounded-lg border border-dashed border-[rgb(var(--field-border))] p-8 text-center text-sm text-muted transition-colors hover:border-accent"
                >
                  Перетащите файлы или нажмите для выбора
                  <input
                    ref={fileInput}
                    type="file"
                    multiple
                    className="hidden"
                    onChange={(e) => addFiles(e.target.files)}
                  />
                </div>
              </Field>
              {files.length > 0 && (
                <ul className="space-y-1 text-sm">
                  {files.map((file, i) => (
                    <li key={`${file.name}-${i}`} className="flex items-center justify-between gap-3">
                      <span>{file.name}</span>
                      <button
                        className="text-muted transition-colors hover:text-accent"
                        onClick={() => setFiles((fs) => fs.filter((_, j) => j !== i))}
                      >
                        убрать
                      </button>
                    </li>
                  ))}
                </ul>
              )}
              <Field
                label="Дополнительно — перечень документов без файлов"
                hint="по одному в строке"
              >
                <Textarea value={f.documents} onChange={set("documents")} />
              </Field>
              <Field label="Досье подтвердил (руководитель / HR)" hint="ФИО и должность подтверждающего">
                <Input
                  value={f.confirmedBy}
                  onChange={set("confirmedBy")}
                  placeholder="Иванов И.И., HR-директор ДЗО"
                />
              </Field>
            </>
          )}

          <div className="flex justify-between pt-2">
            <Button variant="secondary" disabled={step === 0} onClick={() => setStep((s) => s - 1)}>
              Назад
            </Button>
            {step < STEPS.length - 1 ? (
              <Button onClick={() => setStep((s) => s + 1)}>Далее</Button>
            ) : (
              <Button disabled={noName || busy !== null} onClick={onSave}>
                {busy === "save" ? "Сохранение…" : "Сохранить досье"}
              </Button>
            )}
          </div>
        </Card>

        {/* Правая sticky-панель: Gate 0 */}
        <div>
          <Card className="sticky top-24 space-y-4">
            <div className="text-sm font-medium">Готовность к оценке (Gate 0)</div>
            <p className="text-xs text-muted">
              Если отсутствуют цель, полномочия, масштаб или контекст, уровни и грейд не
              присваиваются.
            </p>
            {criticalChecks.length > 0 ? (
              <div className="space-y-2">
                <div className="text-xs uppercase tracking-wide text-accent">Блокеры</div>
                <div className="space-y-2">
                  {criticalChecks.map((c) => {
                    const stepIndex = GATE_STEP[c.block] ?? 0;
                    return (
                      <GateIssue
                        key={c.block}
                        check={c}
                        actionLabel={`Шаг ${stepIndex + 1}`}
                        stepLabel={STEPS[stepIndex]}
                        onOpen={() => setStep(stepIndex)}
                      />
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="rounded-xl border border-ok/20 bg-ok/5 px-3 py-2 text-xs text-muted">
                Критических блокеров нет.
              </div>
            )}

            {warningChecks.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs uppercase tracking-wide text-muted">Что стоит уточнить</div>
                <div className="space-y-2">
                  {warningChecks.map((c) => {
                    const stepIndex = GATE_STEP[c.block] ?? 0;
                    return (
                      <GateIssue
                        key={c.block}
                        check={c}
                        actionLabel={`Шаг ${stepIndex + 1}`}
                        stepLabel={STEPS[stepIndex]}
                        onOpen={() => setStep(stepIndex)}
                        muted
                      />
                    );
                  })}
                </div>
              </div>
            )}
            <div className={cn("border-t border-[rgb(var(--row-divider))] pt-3 text-sm font-medium", verdict.cls)}>
              {verdict.text}
            </div>
            <p className="text-xs text-muted">Правило: «нет понимания — нет оценки».</p>
            <Button
              className="w-full"
              disabled={hasFail || noName || busy !== null}
              onClick={onEvaluate}
            >
              {busy === "evaluate" ? "Оценивается…" : "Запустить предварительную оценку"}
            </Button>
            {noName && <p className="text-xs text-muted">Укажите наименование должности.</p>}
          </Card>
        </div>
      </div>
    </div>
  );
}
