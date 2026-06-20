import { useState } from "react";
import { Button, Card, ErrorBanner, Field, Input, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { useFetch } from "../lib/useFetch";
import type { AccessRole, CompanyInviteSummary } from "../lib/types";

const STATUS_COLOR: Record<CompanyInviteSummary["status"], Parameters<typeof StatusDot>[0]["color"]> = {
  invited: "amber",
  active: "green",
  disabled: "gray",
};

export default function AdminAccessPage() {
  const { data, error, loading, reload } = useFetch(() => api.listCompanyAccess(), []);
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<AccessRole>("viewer");
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function addAccess() {
    const normalized = email.trim().toLowerCase();
    if (!normalized) return;
    setBusy(true);
    setActionError(null);
    try {
      await api.createCompanyAccess({ email: normalized, role });
      setEmail("");
      setRole("viewer");
      reload();
    } catch (reason) {
      setActionError(reason instanceof Error ? reason.message : String(reason));
    } finally {
      setBusy(false);
    }
  }

  async function updateAccess(item: CompanyInviteSummary, nextRole: AccessRole, nextStatus: CompanyInviteSummary["status"]) {
    setActionError(null);
    try {
      await api.updateCompanyAccess(item.id, { role: nextRole, status: nextStatus });
      reload();
    } catch (reason) {
      setActionError(reason instanceof Error ? reason.message : String(reason));
    }
  }

  async function deleteAccess(item: CompanyInviteSummary) {
    setActionError(null);
    try {
      await api.deleteCompanyAccess(item.id);
      reload();
    } catch (reason) {
      setActionError(reason instanceof Error ? reason.message : String(reason));
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1>Админ-доступ</h1>
        <p className="mt-2 max-w-3xl text-sm text-muted">
          Добавляйте Gmail в allowlist. После подключения Google OAuth эти адреса смогут входить в
          систему.
        </p>
      </div>

      {(error || actionError) && <ErrorBanner message={error || actionError || "Ошибка"} onRetry={error ? reload : undefined} />}

      <Card className="grid gap-5 p-6 md:grid-cols-[1fr_220px_auto] md:items-end">
        <Field label="Gmail пользователя">
          <Input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="name@gmail.com"
          />
        </Field>
        <Field label="Роль">
          <select className="field" value={role} onChange={(event) => setRole(event.target.value as AccessRole)}>
            <option value="viewer">Viewer</option>
            <option value="admin">Admin</option>
          </select>
        </Field>
        <Button disabled={busy || !email.trim()} onClick={addAccess}>
          {busy ? "Сохранение…" : "Добавить"}
        </Button>
      </Card>

      {loading ? (
        <Skeleton className="h-80" />
      ) : (
        <Card className="overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="min-w-[900px] w-full text-sm">
              <thead className="bg-slate-50 text-left text-xs text-muted dark:bg-white/5">
                <tr>
                  {["Email", "Роль", "Статус", "Создано", "Действия"].map((heading) => (
                    <th key={heading} className="px-5 py-4 font-medium">
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data?.map((item) => (
                  <tr key={item.id} className="border-t border-[rgb(var(--row-divider))]">
                    <td className="px-5 py-4 font-medium">{item.email}</td>
                    <td className="px-5 py-4">
                      <select
                        className="field !py-2 text-sm"
                        value={item.role}
                        onChange={(event) => void updateAccess(item, event.target.value as AccessRole, item.status)}
                      >
                        <option value="viewer">Viewer</option>
                        <option value="admin">Admin</option>
                      </select>
                    </td>
                    <td className="px-5 py-4">
                      <StatusDot color={STATUS_COLOR[item.status]}>
                        {item.status}
                      </StatusDot>
                    </td>
                    <td className="px-5 py-4 text-muted">{item.created_at.slice(0, 10)}</td>
                    <td className="px-5 py-4">
                      <div className="flex flex-wrap gap-2">
                        <Button
                          variant="secondary"
                          className="min-h-0 px-3 py-2 text-xs"
                          onClick={() =>
                            void updateAccess(
                              item,
                              item.role,
                              item.status === "invited" ? "active" : "invited",
                            )
                          }
                        >
                          {item.status === "invited" ? "Активировать" : "В приглашения"}
                        </Button>
                        <Button
                          variant="secondary"
                          className="min-h-0 px-3 py-2 text-xs"
                          onClick={() => void deleteAccess(item)}
                        >
                          Удалить
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {data?.length === 0 && <div className="py-12 text-center text-muted">Пока нет добавленных Gmail.</div>}
        </Card>
      )}

      <Card className="p-5">
        <div className="text-sm font-medium">Как это будет работать</div>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-muted">
          <li>Сначала пользователь входит через Google.</li>
          <li>Сервер сравнивает его email с allowlist.</li>
          <li>Если email есть, ему открывается назначенная роль.</li>
          <li>Если email нет, доступ не выдаётся.</li>
        </ul>
      </Card>
    </div>
  );
}
