import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, Field, Input, Skeleton, Stepper, Textarea } from "../components/ui";
import { api } from "../lib/api";
import { useFetch } from "../lib/useFetch";
import type { JobDossier, ProblemCase } from "../lib/types";

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

function formFromDossier(d: JobDossier): FormState {
  return {
    name: d.name ?? "",
    dzo: d.dzo ?? "",
    department: d.department ?? "",
    function: d.function ?? "",
    snapshotDate: d.snapshot_date ?? new Date().toISOString().slice(0, 10),
    purpose: d.purpose ?? "",
    keyResults: d.key_results.join("\n"),
    responsibilities: d.responsibilities.join("\n"),
    kpis: d.kpis.join("\n"),
    decidesAlone: d.authorities.decides_alone.join("\n"),
    requiresApproval: d.authorities.requires_approval
      .map((item) => `${item.item} — ${item.approver}`)
      .join("\n"),
    recommends: d.authorities.recommends.join("\n"),
    limits: d.limits.join("\n"),
    opex: d.scope.annual_opex == null ? "" : String(d.scope.annual_opex),
    capex: d.scope.annual_capex == null ? "" : String(d.scope.annual_capex),
    headcount: d.scope.headcount == null ? "" : String(d.scope.headcount),
    scopeSource: d.scope.source ?? "",
    stakeholders: d.stakeholders.join("\n"),
    anchors: d.anchor_roles.join("\n"),
    problemCases: [
      ...d.problem_cases,
      ...d.problem_cases_structured.map((c) =>
        [c.summary, c.given, c.unknown, c.alternatives, c.tradeoff, c.verification]
          .filter(Boolean)
          .join(" | "),
      ),
    ].join("\n"),
    context: d.organizational_context ?? "",
    manager: d.reporting.manager ?? "",
    subordinates: d.reporting.subordinates.join("\n"),
    documents: d.documents.join("\n"),
    confirmedBy: d.confirmed_by ?? "",
  };
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

export default function JobFormPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);
  const { data: existing, error: loadError, loading } = useFetch(
    () => (id ? api.getPosition(id) : Promise.resolve(null)),
    [id],
  );
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

  const noName = !f.name.trim();

  useEffect(() => {
    if (existing) {
      setF(formFromDossier(existing));
      setStep(0);
      setDraftRestored(false);
      setDraftSavedAt(null);
    }
  }, [existing]);

  useEffect(() => {
    if (isEdit) return;
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
  }, [f, step, isEdit]);

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
      const body = toDossier(f);
      const created = isEdit && id ? await api.updatePosition(id, body) : await api.createPosition(body);
      const positionId = created.id ?? null;
      if (positionId) {
        for (const file of files) {
          await api.uploadDocument(positionId, file);
        }
      }
      return positionId;
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


  return (
    <div className="space-y-6">
      <h1 className="text-[32px]">{isEdit ? "Проверка досье" : "Новая должность"}</h1>
      <Stepper steps={STEPS} current={step} onSelect={setStep} />
      {!isEdit && (
        <>
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
        </>
      )}
      {isEdit && existing?.import_metadata?.missing_fields.length ? (
        <Card className="border-warn/30 p-4 text-sm">
          <div className="font-medium">Нужно дополнить перед оценкой</div>
          <div className="mt-1 text-muted">{existing.import_metadata.missing_fields.join(", ")}</div>
        </Card>
      ) : null}
      <p className="max-w-[920px] text-sm text-muted">
        Сначала заполните цель, результаты, полномочия, масштаб и KPI. Именно эти блоки решают,
        можно ли вообще переходить к оценке.
      </p>

      {loadError && <ErrorBanner message={loadError} />}
      {error && <ErrorBanner message={error} />}
      {loading && isEdit && <Skeleton className="h-64" />}

      {(!loading || !isEdit) && <div className="grid grid-cols-1 gap-6">
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
                {busy === "save" ? "Сохранение…" : isEdit ? "Сохранить проверенное досье" : "Сохранить досье"}
              </Button>
            )}
          </div>
        </Card>

      </div>}
    </div>
  );
}
