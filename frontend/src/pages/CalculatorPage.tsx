import { useState, type ReactNode } from "react";
import { Button, Card, ErrorBanner, Input, StatusDot } from "../components/ui";
import { QcSection } from "../components/QcFlags";
import { api } from "../lib/api";
import { useFactorLevelReference } from "../lib/factorLevels";
import type { CalculateResponse, Confidence, FactorSelections, QCFlag, ScoreResult } from "../lib/types";

const LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"];
const MANAGEMENT = ["T", "I", "II", "III", "IV"];
const NUMBERS_3 = ["1", "2", "3"];
const COMPLEXITY = ["1", "2", "3", "4", "5"];
const NON_QUANTITATIVE_IMPACT = ["I", "II", "III", "IV", "V", "VI"];
const MAGNITUDES = ["N", "1", "2", "3", "4"];
const IMPACT_TYPES = ["R", "C", "S", "P"];

interface CalculatorForm {
  businessArea: string;
  department: string;
  jobTitle: string;
  remarks: string;
  specialization: string;
  management: string;
  communication: string;
  area: string;
  complexity: string;
  freedom: string;
  magnitude: string;
  impact: string;
}

const INITIAL: CalculatorForm = {
  businessArea: "",
  department: "",
  jobTitle: "",
  remarks: "",
  specialization: "E",
  management: "II",
  communication: "2",
  area: "E",
  complexity: "3",
  freedom: "E",
  magnitude: "N",
  impact: "IV",
};

const withBoundaries = (codes: string[]) =>
  codes.flatMap((code) => [`${code}-`, code, `${code}+`]);

const baseCode = (code: string) => code.replace(/[+-]$/, "");
const boundary = (code: string) => code.endsWith("+") ? 1 : code.endsWith("-") ? -1 : 0;
const aggregateBoundary = (...codes: string[]) =>
  Math.max(-1, Math.min(1, codes.reduce((sum, code) => sum + boundary(code), 0)));

/** "E" → "E — Зрелые профессиональные…"; без справочника (ещё не загрузился) — голый код. */
function decodeWith(levels?: Record<string, string>) {
  return (code: string) => (levels?.[code] ? `${code} — ${levels[code]}` : code);
}

export default function CalculatorPage() {
  const [form, setForm] = useState<CalculatorForm>(INITIAL);
  const [result, setResult] = useState<CalculateResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { data: levels } = useFactorLevelReference();

  function set<K extends keyof CalculatorForm>(key: K, value: CalculatorForm[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function calculate() {
    setBusy(true);
    setError(null);
    try {
      setResult(await api.calculateScore(toSelections(form)));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1>Калькулятор Hay Group</h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">
          Расчёт по функциям COMP, IC, PTSIC и FINALITE из исходного файла «Калькулятор Hay Group.xlsm».
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      <Card className="p-5">
        <div className="mb-4">
          <h2 className="text-lg">Данные должности</h2>
          <p className="mt-1 text-xs text-muted">
            Поля соответствуют информационным колонкам листа Worksheet и не изменяют расчёт баллов.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-[0.8fr_1fr_1.4fr_1.2fr]">
          <TextField label="Area · Направление" value={form.businessArea} onChange={(value) => set("businessArea", value)} />
          <TextField label="Department · Подразделение" value={form.department} onChange={(value) => set("department", value)} />
          <TextField label="Job title · Название должности" value={form.jobTitle} onChange={(value) => set("jobTitle", value)} placeholder="Введите название должности" />
          <TextField label="Remarks · Примечание" value={form.remarks} onChange={(value) => set("remarks", value)} />
        </div>
      </Card>

      <div className="grid gap-5 xl:grid-cols-3">
        <FactorCard title="Знания и умения · Know-How">
          <Select label="Специальные знания" value={form.specialization} options={withBoundaries(LETTERS)} optionLabel={decodeBoundaryWith(levels?.specialized_know_how)} onChange={(v) => set("specialization", v)} />
          <Select label="Планирование и интеграция" value={form.management} options={withBoundaries(MANAGEMENT)} optionLabel={decodeBoundaryWith(levels?.managerial_know_how)} onChange={(v) => set("management", v)} />
          <Select label="Коммуникации" value={form.communication} options={NUMBERS_3} optionLabel={decodeWith(levels?.communication)} onChange={(v) => set("communication", v)} />
        </FactorCard>

        <FactorCard title="Решение вопросов · Problem Solving">
          <Select label="Область решаемых вопросов" value={form.area} options={withBoundaries(LETTERS)} optionLabel={decodeBoundaryWith(levels?.problem_area)} onChange={(v) => set("area", v)} />
          <Select label="Сложность" value={form.complexity} options={withBoundaries(COMPLEXITY)} optionLabel={decodeBoundaryWith(levels?.problem_complexity)} onChange={(v) => set("complexity", v)} />
        </FactorCard>

        <FactorCard title="Ответственность · Accountability">
          <Select label="Свобода действий" value={form.freedom} options={withBoundaries(LETTERS)} optionLabel={decodeBoundaryWith(levels?.freedom_to_act)} onChange={(v) => set("freedom", v)} />
          <Select
            label="Величина воздействия"
            value={form.magnitude}
            options={withBoundaries(MAGNITUDES)}
            onChange={(value) => {
              set("magnitude", value);
              set("impact", baseCode(value) === "N" ? "IV" : "C");
            }}
          />
          {baseCode(form.magnitude) === "N" ? (
            <Select label="Неколичественный уровень воздействия" value={form.impact} options={withBoundaries(NON_QUANTITATIVE_IMPACT)} optionLabel={decodeBoundaryWith(levels?.non_quantitative_impact)} onChange={(v) => set("impact", v)} />
          ) : (
            <Select label="Тип влияния" value={form.impact} options={withBoundaries(IMPACT_TYPES)} onChange={(v) => set("impact", v)} />
          )}
        </FactorCard>
      </div>

      <div className="flex flex-wrap items-center gap-4">
        <Button className="rounded-full bg-[#252527] px-7 text-white hover:bg-[#151516]" disabled={busy} onClick={calculate}>
          {busy ? "Рассчитываем…" : "Рассчитать"}
        </Button>
        <p className="max-w-3xl text-xs leading-5 text-muted">
          Суффиксы −/+ соответствуют граничным значениям из Excel. Если несколько
          суффиксов заданы в одном факторе, XLSM объединяет их в один шаг от − до +.
          Для KMG DIGITAL рабочей является ветка N / I–VI; выбор 1–4 / R–P будет
          рассчитан как в XLSM, но отмечен корпоративным QC.
        </p>
      </div>

      {result && <Result score={result.score} qcFlags={result.qc_flags} />}
    </div>
  );
}

function FactorCard({ title, children }: { title: string; children: ReactNode }) {
  return (
    <Card className="space-y-4 bg-white p-5 dark:bg-white/5">
      <h2 className="text-lg">{title}</h2>
      {children}
    </Card>
  );
}

function Select({ label, value, options, onChange, optionLabel }: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
  optionLabel?: (value: string) => string;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium text-muted">{label}</span>
      <select className="field" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => <option key={option} value={option}>{optionLabel?.(option) ?? option}</option>)}
      </select>
    </label>
  );
}

function TextField({ label, value, onChange, placeholder }: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium text-muted">{label}</span>
      <Input value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function Result({ score, qcFlags }: { score: ScoreResult; qcFlags: QCFlag[] }) {
  const fails = qcFlags.filter((f) => f.status === "fail");
  const warns = qcFlags.filter((f) => f.status === "warn");
  const passes = qcFlags.filter((f) => f.status === "pass");
  return (
    <div className="space-y-5">
      <Card className="overflow-hidden p-0">
        <div className="grid divide-y divide-[rgb(var(--row-divider))] sm:grid-cols-2 sm:divide-x sm:divide-y-0 xl:grid-cols-6">
        <Metric label="Know-How" value={score.know_how.points} />
        <Metric label={`Problem Solving · ${score.problem_solving.percentage}%`} value={score.problem_solving.points} />
        <Metric label="Accountability" value={score.accountability.points} />
        <Metric label="Total" value={score.total_points} />
        <Metric label="Grade" value={score.grade} />
        <Metric label="Profile" value={score.profile_long} />
        </div>
      </Card>
      <Card>
        <h2 className="text-lg">Расшифровка расчёта</h2>
        <ol className="mt-4 list-decimal space-y-2 pl-5 text-sm leading-6">
          {score.calculation_explanation.map((line) => <li key={line}>{line}</li>)}
        </ol>
        <p className="mt-4 border-t border-[rgb(var(--row-divider))] pt-4 text-xs leading-5 text-muted">
          {score.methodology_basis}
        </p>
      </Card>
      {qcFlags.length > 0 && (
        <Card>
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-lg">QC-проверки этой комбинации уровней</h2>
            <div className="flex flex-wrap gap-2 text-xs">
              <StatusDot color="red">FAIL: {fails.length}</StatusDot>
              <StatusDot color="amber">WARN: {warns.length}</StatusDot>
              <StatusDot color="green">PASS: {passes.length}</StatusDot>
            </div>
          </div>
          <p className="mb-4 text-xs text-muted">
            Калькулятор работает без JE-досье — это только правила, проверяющие сами уровни
            (несостыковки, профиль вне диапазона, необоснованные модификаторы).
          </p>
          <div className="space-y-4">
            <QcSection title="Блокирующие" color="red" items={fails} />
            <QcSection title="Требуют уточнения" color="amber" items={warns} />
            <QcSection title="Подтверждено" color="green" items={passes} />
          </div>
        </Card>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return <div className="bg-white p-5 dark:bg-white/[0.025]"><div className="text-xs font-medium uppercase tracking-wide text-muted">{label}</div><div className="num mt-2 text-3xl font-bold text-accent">{value}</div></div>;
}

function decodeBoundaryWith(levels?: Record<string, string>) {
  return (code: string) => {
    const base = baseCode(code);
    return levels?.[base] ? `${code} — ${levels[base]}` : code;
  };
}

function toSelections(form: CalculatorForm): FactorSelections {
  const evidence = { evidence: [], doubts: [], confidence: "medium" as Confidence };
  return {
    know_how: {
      ...evidence,
      specialization: baseCode(form.specialization),
      management: baseCode(form.management),
      communication: form.communication,
      plus_minus: aggregateBoundary(form.specialization, form.management),
    },
    problem_solving: {
      ...evidence,
      area: baseCode(form.area),
      complexity: Number(baseCode(form.complexity)),
      plus_minus: aggregateBoundary(form.area, form.complexity),
    },
    accountability: {
      ...evidence,
      freedom: baseCode(form.freedom),
      magnitude: baseCode(form.magnitude),
      impact: baseCode(form.magnitude) === "N" ? null : baseCode(form.impact),
      non_quantitative_impact: baseCode(form.magnitude) === "N" ? baseCode(form.impact) : null,
      plus_minus: aggregateBoundary(form.freedom, form.magnitude, form.impact),
    },
  };
}
