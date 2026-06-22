import { useState, type ReactNode } from "react";
import { Button, Card, ErrorBanner, StatusDot } from "../components/ui";
import { QcSection } from "../components/QcFlags";
import { api } from "../lib/api";
import { useFactorLevelReference } from "../lib/factorLevels";
import type { CalculateResponse, Confidence, FactorSelections, QCFlag, ScoreResult } from "../lib/types";

const LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"];
const MANAGEMENT = ["T", "I", "II", "III", "IV"];
const NUMBERS_3 = ["1", "2", "3"];
const COMPLEXITY = ["1", "2", "3", "4", "5"];
const NON_QUANTITATIVE_IMPACT = ["I", "II", "III", "IV", "V", "VI"];
const MODIFIERS = ["-1", "0", "1"];

interface CalculatorForm {
  specialization: string;
  management: string;
  communication: string;
  khModifier: string;
  area: string;
  complexity: string;
  psModifier: string;
  freedom: string;
  nonQuantitativeImpact: string;
  accModifier: string;
}

const INITIAL: CalculatorForm = {
  specialization: "E",
  management: "II",
  communication: "2",
  khModifier: "0",
  area: "E",
  complexity: "3",
  psModifier: "0",
  freedom: "E",
  nonQuantitativeImpact: "IV",
  accModifier: "0",
};

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

      <div className="grid gap-5 xl:grid-cols-3">
        <FactorCard title="Знания и умения · Know-How">
          <Select label="Специальные знания" value={form.specialization} options={LETTERS} optionLabel={decodeWith(levels?.specialized_know_how)} onChange={(v) => set("specialization", v)} />
          <Select label="Планирование и интеграция" value={form.management} options={MANAGEMENT} optionLabel={decodeWith(levels?.managerial_know_how)} onChange={(v) => set("management", v)} />
          <Select label="Коммуникации" value={form.communication} options={NUMBERS_3} optionLabel={decodeWith(levels?.communication)} onChange={(v) => set("communication", v)} />
          <Select label="Модификатор таблицы" value={form.khModifier} options={MODIFIERS} optionLabel={modifierLabel} onChange={(v) => set("khModifier", v)} />
        </FactorCard>

        <FactorCard title="Решение вопросов · Problem Solving">
          <Select label="Область решаемых вопросов" value={form.area} options={LETTERS} optionLabel={decodeWith(levels?.problem_area)} onChange={(v) => set("area", v)} />
          <Select label="Сложность" value={form.complexity} options={COMPLEXITY} optionLabel={decodeWith(levels?.problem_complexity)} onChange={(v) => set("complexity", v)} />
          <Select label="Модификатор таблицы" value={form.psModifier} options={MODIFIERS} optionLabel={modifierLabel} onChange={(v) => set("psModifier", v)} />
        </FactorCard>

        <FactorCard title="Ответственность · Accountability">
          <Select label="Свобода действий" value={form.freedom} options={LETTERS} optionLabel={decodeWith(levels?.freedom_to_act)} onChange={(v) => set("freedom", v)} />
          <div className="rounded-xl border border-[rgb(var(--border))] bg-[rgb(var(--surface-subtle))] px-3 py-2 text-sm">
            Величина воздействия: <span className="font-semibold">N · неколичественная</span>
          </div>
          <Select label="Уровень воздействия" value={form.nonQuantitativeImpact} options={NON_QUANTITATIVE_IMPACT} optionLabel={decodeWith(levels?.non_quantitative_impact)} onChange={(v) => set("nonQuantitativeImpact", v)} />
          <Select label="Модификатор таблицы" value={form.accModifier} options={MODIFIERS} optionLabel={modifierLabel} onChange={(v) => set("accModifier", v)} />
        </FactorCard>
      </div>

      <div className="flex flex-wrap items-center gap-4">
        <Button className="rounded-full bg-[#252527] px-7 text-white hover:bg-[#151516]" disabled={busy} onClick={calculate}>
          {busy ? "Рассчитываем…" : "Рассчитать"}
        </Button>
        <p className="max-w-3xl text-xs leading-5 text-muted">
          Корпоративное правило: доход и денежная величина не учитываются. Расчёт Accountability всегда использует ветку N и уровень I–VI.
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

function Result({ score, qcFlags }: { score: ScoreResult; qcFlags: QCFlag[] }) {
  const fails = qcFlags.filter((f) => f.status === "fail");
  const warns = qcFlags.filter((f) => f.status === "warn");
  const passes = qcFlags.filter((f) => f.status === "pass");
  return (
    <div className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <Metric label="Know-How" value={score.know_how.points} />
        <Metric label={`Problem Solving · ${score.problem_solving.percentage}%`} value={score.problem_solving.points} />
        <Metric label="Accountability" value={score.accountability.points} />
        <Metric label="Итоговый балл" value={score.total_points} />
        <Metric label="Грейд / профиль" value={`${score.grade} · ${score.profile_long}`} />
      </div>
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
  return <Card className="bg-white p-5 dark:bg-white/5"><div className="text-xs text-muted">{label}</div><div className="num mt-2 text-3xl font-semibold">{value}</div></Card>;
}

function modifierLabel(value: string): string {
  return value === "1" ? "+" : value === "-1" ? "−" : "Без модификатора";
}

function toSelections(form: CalculatorForm): FactorSelections {
  const evidence = { evidence: [], doubts: [], confidence: "medium" as Confidence };
  return {
    know_how: {
      ...evidence,
      specialization: form.specialization,
      management: form.management,
      communication: form.communication,
      plus_minus: Number(form.khModifier),
    },
    problem_solving: {
      ...evidence,
      area: form.area,
      complexity: Number(form.complexity),
      plus_minus: Number(form.psModifier),
    },
    accountability: {
      ...evidence,
      freedom: form.freedom,
      magnitude: "N",
      impact: null,
      non_quantitative_impact: form.nonQuantitativeImpact,
      plus_minus: Number(form.accModifier),
    },
  };
}
