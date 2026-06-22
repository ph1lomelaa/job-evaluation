import { useState, type FormEvent } from "react";
import { useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, Field, Input, Skeleton, Textarea } from "../components/ui";
import { api } from "../lib/api";
import { useFetch } from "../lib/useFetch";
import type { JobDossier } from "../lib/types";

const lines = (value: string) => value.split("\n").map((item) => item.trim()).filter(Boolean);
const number = (value: string) => value.trim() && Number.isFinite(Number(value.replace(/\s/g, ""))) ? Number(value.replace(/\s/g, "")) : null;

export default function PublicFormPage() {
  const { token = "" } = useParams();
  const { data: info, error: loadError, loading } = useFetch(() => api.getPublicForm(token), [token]);
  const [f, setF] = useState({ name: "", dzo: "", department: "", function: "", purpose: "", results: "", responsibilities: "", kpis: "", manager: "", subordinates: "", decisions: "", approvals: "", limits: "", opex: "", capex: "", headcount: "", source: "", stakeholders: "", context: "", cases: "", confirmed: "" });
  const [busy, setBusy] = useState(false); const [error, setError] = useState<string | null>(null); const [done, setDone] = useState(false);
  const set = (key: keyof typeof f) => (event: { target: { value: string } }) => setF((value) => ({ ...value, [key]: event.target.value }));

  async function submit(event: FormEvent) {
    event.preventDefault(); setBusy(true); setError(null);
    const dossier: JobDossier = {
      name: f.name.trim(), dzo: f.dzo.trim() || null, department: f.department.trim() || null, function: f.function.trim() || null,
      snapshot_date: new Date().toISOString().slice(0, 10), purpose: f.purpose.trim() || null, key_results: lines(f.results), responsibilities: lines(f.responsibilities), kpis: lines(f.kpis),
      reporting: { manager: f.manager.trim() || null, subordinates: lines(f.subordinates), matrix_links: [] },
      authorities: { decides_alone: lines(f.decisions), requires_approval: lines(f.approvals).map((line) => { const [item, approver] = line.split(/\s*(?:—|->|\|)\s*/); return { item, approver: approver || "не указано" }; }), recommends: [] },
      scope: { annual_opex: number(f.opex), annual_capex: number(f.capex), headcount: number(f.headcount), source: f.source.trim() || null }, limits: lines(f.limits), stakeholders: lines(f.stakeholders), organizational_context: f.context.trim() || null,
      anchor_roles: [], problem_cases: lines(f.cases), problem_cases_structured: [], documents: [], confirmed_by: f.confirmed.trim() || null,
    };
    try { await api.submitPublicForm(token, dossier); setDone(true); window.scrollTo({ top: 0, behavior: "smooth" }); }
    catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    finally { setBusy(false); }
  }

  if (loading) return <div className="min-h-screen bg-bg p-6"><Skeleton className="mx-auto h-96 max-w-3xl" /></div>;
  if (loadError) return <div className="grid min-h-screen place-items-center bg-bg p-6"><div className="w-full max-w-lg"><ErrorBanner message={loadError} /></div></div>;
  if (done) return <div className="grid min-h-screen place-items-center bg-bg p-6"><Card className="max-w-lg p-10 text-center"><div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-emerald-100 text-xl text-emerald-700">✓</div><h1 className="mt-5 text-2xl">Форма отправлена</h1><p className="mt-3 text-muted">Описание должности передано эксперту. Повторно использовать эту ссылку нельзя.</p></Card></div>;

  return <div className="min-h-screen bg-bg"><header className="border-b border-[rgb(var(--row-divider))] bg-white px-6 py-5 dark:bg-[rgb(var(--glass-bg))]"><div className="mx-auto flex max-w-4xl items-center gap-3"><div><div className="font-semibold">Hay Eval</div><div className="text-xs text-muted">Описание должности</div></div></div></header><main className="mx-auto max-w-4xl px-5 py-9"><div className="mb-8"><div className="text-sm font-medium text-accent">Форма для оценки должности</div><h1 className="mt-2">{info?.title}</h1><p className="mt-3 text-sm text-muted">Заполняйте сведения о должности, а не о конкретном сотруднике. Указывайте фактические полномочия, масштаб и типовые задачи.</p>{info?.recipient && <p className="mt-2 text-sm">Получатель: <span className="font-medium">{info.recipient}</span></p>}</div>{error && <div className="mb-6"><ErrorBanner message={error} /></div>}
    <form onSubmit={submit} className="space-y-6">
      <Card className="grid gap-5 p-6 md:grid-cols-2"><h2 className="md:col-span-2 text-lg">1. Общая информация</h2><Field label="Название должности *"><Input required value={f.name} onChange={set("name")} /></Field><Field label="Организация"><Input value={f.dzo} onChange={set("dzo")} /></Field><Field label="Подразделение"><Input value={f.department} onChange={set("department")} /></Field><Field label="Функция"><Input value={f.function} onChange={set("function")} /></Field><div className="md:col-span-2"><Field label="Цель должности *" hint="1–2 предложения: зачем существует роль"><Textarea required value={f.purpose} onChange={set("purpose")} /></Field></div></Card>
      <Card className="grid gap-5 p-6"><h2 className="text-lg">2. Результаты и задачи</h2><Field label="Ключевые результаты *" hint="по одному в строке"><Textarea required value={f.results} onChange={set("results")} /></Field><Field label="Обязанности *" hint="по одной в строке"><Textarea required value={f.responsibilities} onChange={set("responsibilities")} /></Field><Field label="KPI / показатели" hint="по одному в строке"><Textarea value={f.kpis} onChange={set("kpis")} /></Field><Field label="Типовые нестандартные задачи" hint="минимум 3 реальных примера, по одному в строке"><Textarea value={f.cases} onChange={set("cases")} /></Field></Card>
      <Card className="grid gap-5 p-6 md:grid-cols-2"><h2 className="md:col-span-2 text-lg">3. Полномочия и структура</h2><Field label="Непосредственный руководитель"><Input value={f.manager} onChange={set("manager")} /></Field><Field label="Подчинённые" hint="по одному в строке"><Textarea value={f.subordinates} onChange={set("subordinates")} /></Field><Field label="Решает самостоятельно" hint="по одному решению в строке"><Textarea value={f.decisions} onChange={set("decisions")} /></Field><Field label="Требует согласования" hint="формат: решение — кто утверждает"><Textarea value={f.approvals} onChange={set("approvals")} /></Field><div className="md:col-span-2"><Field label="Лимиты полномочий"><Textarea value={f.limits} onChange={set("limits")} /></Field></div></Card>
      <Card className="grid gap-5 p-6 md:grid-cols-3"><h2 className="md:col-span-3 text-lg">4. Масштаб ответственности</h2><Field label="Годовой OPEX, ₸"><Input inputMode="numeric" value={f.opex} onChange={set("opex")} /></Field><Field label="Годовой CAPEX, ₸"><Input inputMode="numeric" value={f.capex} onChange={set("capex")} /></Field><Field label="Численность"><Input inputMode="numeric" value={f.headcount} onChange={set("headcount")} /></Field><div className="md:col-span-3"><Field label="Источник цифр"><Input value={f.source} onChange={set("source")} /></Field></div></Card>
      <Card className="grid gap-5 p-6"><h2 className="text-lg">5. Контекст и подтверждение</h2><Field label="Ключевые стейкхолдеры" hint="по одному в строке"><Textarea value={f.stakeholders} onChange={set("stakeholders")} /></Field><Field label="Организационный контекст"><Textarea value={f.context} onChange={set("context")} /></Field><Field label="Кто подтвердил информацию *"><Input required value={f.confirmed} onChange={set("confirmed")} placeholder="ФИО, должность" /></Field></Card>
      <div className="flex justify-end"><Button type="submit" disabled={busy} className="min-w-[180px]">{busy ? "Отправка…" : "Отправить эксперту"}</Button></div>
    </form></main></div>;
}
