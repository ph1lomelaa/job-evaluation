import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, ErrorBanner, Field, Input, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { useFetch } from "../lib/useFetch";
import type { PublicJobForm } from "../lib/types";

const STATUS = {
  active: { label: "Ожидает заполнения", color: "blue" as const },
  submitted: { label: "Заполнена", color: "green" as const },
  expired: { label: "Срок истёк", color: "gray" as const },
};

const date = (value: string) => new Intl.DateTimeFormat("ru-RU", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));

export default function FormLinksPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("Описание должности для оценки");
  const [recipient, setRecipient] = useState("");
  const [days, setDays] = useState("7");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const { data: forms, error: loadError, loading, reload } = useFetch(() => api.listPublicForms(), []);

  const link = (form: PublicJobForm) => `${window.location.origin}/fill/${form.token}`;

  async function create() {
    if (!title.trim()) return;
    setBusy(true); setError(null);
    try {
      const form = await api.createPublicForm({ title: title.trim(), recipient: recipient.trim() || undefined, expires_in_days: Number(days) || 7 });
      await navigator.clipboard.writeText(link(form));
      setCopied(form.id); setRecipient(""); reload();
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    finally { setBusy(false); }
  }

  async function copy(form: PublicJobForm) {
    try { await navigator.clipboard.writeText(link(form)); setCopied(form.id); window.setTimeout(() => setCopied(null), 2000); }
    catch { setError("Не удалось скопировать ссылку. Скопируйте её вручную."); }
  }

  async function openResult(form: PublicJobForm) {
    try { await api.markPublicFormRead(form.id); } catch { /* переход остаётся доступен */ }
    if (form.position_id) navigate(`/positions/${form.position_id}`);
  }

  return <div className="space-y-8">
    <div><h1>Создать форму</h1><p className="mt-2 max-w-3xl text-sm text-muted">Создайте ограниченную ссылку на стандартный шаблон описания должности. Ссылка одноразовая: после отправки появится уведомление и черновик для проверки.</p></div>
    {(error || loadError) && <ErrorBanner message={error || loadError || "Ошибка"} onRetry={loadError ? reload : undefined} />}
    <Card className="p-6 md:p-8"><div className="grid gap-5 lg:grid-cols-[1fr_1fr_180px_auto] lg:items-end">
      <Field label="Название формы"><Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Описание должности" /></Field>
      <Field label="Кому отправляется (необязательно)"><Input value={recipient} onChange={(e) => setRecipient(e.target.value)} placeholder="ФИО или подразделение" /></Field>
      <Field label="Срок действия"><select className="field" value={days} onChange={(e) => setDays(e.target.value)}><option value="1">1 день</option><option value="3">3 дня</option><option value="7">7 дней</option><option value="14">14 дней</option><option value="30">30 дней</option></select></Field>
      <Button disabled={busy || !title.trim()} onClick={create} className="lg:mb-0">{busy ? "Создание…" : "Создать и скопировать"}</Button>
    </div></Card>

    <div><h2 className="text-xl">Отправленные формы</h2><p className="mt-1 text-sm text-muted">Статусы обновляются автоматически; новые ответы также отображаются в колокольчике.</p></div>
    {loading ? <Skeleton className="h-64" /> : <Card className="overflow-hidden p-0"><div className="overflow-x-auto"><table className="min-w-[900px] w-full text-sm"><thead className="bg-slate-50 text-left text-xs text-muted dark:bg-white/5"><tr>{["Форма", "Получатель", "Статус", "Создана", "Истекает", "Действие"].map((h) => <th key={h} className="px-5 py-4 font-medium">{h}</th>)}</tr></thead><tbody>{forms?.map((form) => <tr key={form.id} className="border-t border-[rgb(var(--row-divider))]"><td className="px-5 py-4"><div className="font-medium">{form.title}</div>{form.status === "submitted" && !form.is_read && <div className="mt-1 text-xs font-medium text-accent">Новый ответ</div>}</td><td className="px-5 py-4 text-muted">{form.recipient || "—"}</td><td className="px-5 py-4"><StatusDot color={STATUS[form.status].color}>{STATUS[form.status].label}</StatusDot></td><td className="px-5 py-4 text-muted">{date(form.created_at)}</td><td className="px-5 py-4 text-muted">{date(form.expires_at)}</td><td className="px-5 py-4">{form.status === "active" ? <Button variant="secondary" className="min-h-0 px-3 py-2 text-xs" onClick={() => copy(form)}>{copied === form.id ? "Скопировано" : "Копировать ссылку"}</Button> : form.position_id ? <Button variant="secondary" className="min-h-0 px-3 py-2 text-xs" onClick={() => openResult(form)}>Открыть карточку</Button> : "—"}</td></tr>)}</tbody></table></div>{forms?.length === 0 && <div className="py-12 text-center text-muted">Вы ещё не создавали формы.</div>}</Card>}
  </div>;
}
