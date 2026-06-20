import { useEffect, useMemo, useState, type ReactNode } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { cn } from "../lib/cn";
import { useTheme } from "../lib/theme";
import type { MemberRole, PublicJobForm } from "../lib/types";

type IconName = "sheet" | "grades" | "calculator" | "positions" | "new" | "form" | "guide" | "admin" | "bell" | "menu";

function Icon({ name, className = "h-5 w-5" }: { name: IconName; className?: string }) {
  const paths: Record<IconName, ReactNode> = {
    sheet: <><path d="M4 4h16v16H4z"/><path d="M4 9h16M9 4v16M14 9v11"/></>,
    grades: <><path d="M5 19V9M12 19V5M19 19v-7"/><path d="M3 19h18"/></>,
    calculator: <><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8v3H8zM8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/></>,
    positions: <><path d="M5 7h14v12H5z"/><path d="M9 7V5h6v2M5 12h14M10 12v2h4v-2"/></>,
    new: <><path d="M12 5v14M5 12h14"/><circle cx="12" cy="12" r="9"/></>,
    form: <><path d="M6 3h9l3 3v15H6z"/><path d="M15 3v4h4M9 12h6M9 16h6"/></>,
    guide: <><path d="M4 5.5A3.5 3.5 0 0 1 7.5 2H12v18H7.5A3.5 3.5 0 0 0 4 23z"/><path d="M20 5.5A3.5 3.5 0 0 0 16.5 2H12v18h4.5A3.5 3.5 0 0 1 20 23z"/></>,
    admin: <><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 10h8M8 14h5M8 18h3"/></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></>,
    menu: <><path d="M4 7h16M4 12h16M4 17h16"/></>,
  };
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>{paths[name]}</svg>;
}

const NAV: Array<{ to: string; label: string; short: string; icon: IconName }> = [
  { to: "/assessment-sheet", label: "Ведомость оценки должностей", short: "Ведомость оценки", icon: "sheet" },
  { to: "/grades", label: "Таблица грейдов", short: "Таблица грейдов", icon: "grades" },
  { to: "/calculator", label: "Калькулятор Hay Group", short: "Калькулятор", icon: "calculator" },
  { to: "/", label: "Должности", short: "Должности", icon: "positions" },
  { to: "/new", label: "Новая должность с нуля", short: "Новая должность", icon: "new" },
  { to: "/forms", label: "Создать форму", short: "Создать форму", icon: "form" },
  { to: "/guide", label: "Методология", short: "Методология", icon: "guide" },
  { to: "/admin", label: "Админ", short: "Админ", icon: "admin" },
];

const ROLE_LABEL: Record<MemberRole, string> = {
  owner: "Владелец",
  admin: "Администратор",
  evaluator: "Эксперт",
  viewer: "Наблюдатель",
};

function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return <button onClick={toggle} className="rounded-xl p-2.5 text-muted hover:bg-[rgb(var(--field-bg))] hover:text-fg" title="Переключить тему" aria-label="Переключить тему">{theme === "dark" ? "☀" : "☾"}</button>;
}

export function MainLayout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, companies, activeCompany, selectCompany, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [forms, setForms] = useState<PublicJobForm[]>([]);
  const current = useMemo(
    () => NAV.find((item) => item.to === "/" ? pathname === "/" : pathname.startsWith(item.to)),
    [pathname],
  );
  const isAdmin = activeCompany?.role === "owner" || activeCompany?.role === "admin";

  useEffect(() => {
    setMobileOpen(false);
    setProfileOpen(false);
  }, [pathname]);
  useEffect(() => {
    let active = true;
    const load = () => api.listPublicForms().then((value) => active && setForms(value)).catch(() => undefined);
    load();
    const timer = window.setInterval(load, 30000);
    return () => { active = false; window.clearInterval(timer); };
  }, [pathname]);

  const unread = forms.filter((form) => form.status === "submitted" && !form.is_read);
  const initials = initialsFor(user?.display_name || "Пользователь");

  async function openSubmission(form: PublicJobForm) {
    try { await api.markPublicFormRead(form.id); } catch { /* карточка всё равно доступна */ }
    setNotificationsOpen(false);
    if (form.position_id) navigate(`/positions/${form.position_id}`);
  }

  function switchCompany(company: NonNullable<typeof activeCompany>) {
    selectCompany(company);
    setProfileOpen(false);
    setMobileOpen(false);
    navigate("/");
  }

  return (
    <div className="min-h-screen bg-[#f9f8f5] dark:bg-bg">
      {mobileOpen && <button className="fixed inset-0 z-40 bg-black/30 lg:hidden" onClick={() => setMobileOpen(false)} aria-label="Закрыть меню" />}
      <aside className={cn("fixed inset-y-0 left-0 z-50 flex w-[300px] flex-col border-r border-[#e5e1db] bg-[#fbfaf8] transition-transform dark:border-white/10 dark:bg-[rgb(var(--glass-bg))] lg:translate-x-0", mobileOpen ? "translate-x-0" : "-translate-x-full")}>
        <div className="flex h-[94px] items-center gap-3.5 border-b border-[#e5e1db] px-6 dark:border-white/10">
          <div className="grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[#7c4dba]/45 text-[#7c4dba]" aria-hidden="true">
            <span className="flex items-end gap-[3px]">
              <span className="h-2 w-[3px] rounded-full bg-current opacity-45" />
              <span className="h-4 w-[3px] rounded-full bg-current" />
              <span className="h-3 w-[3px] rounded-full bg-current opacity-70" />
            </span>
          </div>
          <div className="min-w-0">
            <div className="truncate font-semibold leading-tight">Оценка должностей</div>
            <div className="mt-0.5 truncate text-xs text-muted">{activeCompany?.name}</div>
          </div>
        </div>
        <nav className="flex-1 space-y-2 overflow-y-auto px-4 py-5">
          {NAV.filter((item) => item.to !== "/admin" || isAdmin).map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === "/"} className={({ isActive }) => cn("flex min-h-[48px] items-center gap-3.5 rounded-[15px] px-4 text-sm transition-colors", isActive ? "bg-[#252527] font-medium text-white dark:bg-white dark:text-[#252527]" : "text-[#69655f] hover:bg-white hover:text-[#252527] dark:text-muted dark:hover:bg-white/5 dark:hover:text-white")}>
              <Icon name={item.icon} className="h-5 w-5 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="relative border-t border-[#e5e1db] p-4 dark:border-white/10">
          {profileOpen && (
            <ProfileMenu
              userName={user?.display_name || "Пользователь"}
              email={user?.email || ""}
              companies={companies}
              activeCompanyId={activeCompany?.id}
              onSelect={switchCompany}
              onAdd={() => { setProfileOpen(false); navigate("/onboarding"); }}
              onLogout={() => void logout()}
            />
          )}
          <button
            type="button"
            onClick={() => setProfileOpen((value) => !value)}
            className={cn("flex w-full items-center gap-3 rounded-[15px] px-2.5 py-2.5 text-left transition hover:bg-white dark:hover:bg-white/5", profileOpen && "bg-white dark:bg-white/5")}
          >
            <div className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-[#ece9e3] text-xs font-semibold text-[#55514c] dark:bg-white/10 dark:text-white">{initials}</div>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium">{user?.display_name}</div>
              <div className="truncate text-xs text-muted">{activeCompany?.name}</div>
            </div>
            <span className="text-xs text-muted">•••</span>
          </button>
        </div>
      </aside>

      <div className="app-canvas min-h-screen lg:pl-[300px]">
        <header className="sticky top-0 z-30 flex h-[68px] items-center bg-[#f9f8f5]/90 px-5 backdrop-blur-xl dark:bg-[rgb(var(--bg)/0.9)] md:px-8 lg:h-[48px] lg:px-[clamp(48px,5vw,88px)]">
          <button className="mr-3 rounded-xl p-2 text-muted lg:hidden" onClick={() => setMobileOpen(true)} aria-label="Открыть меню"><Icon name="menu" /></button>
          <div className="min-w-0 flex-1 lg:hidden">
            <div className="truncate text-lg font-semibold">{current?.short ?? "Оценка должности"}</div>
            <div className="truncate text-xs text-muted">{activeCompany?.name}</div>
          </div>
          <div className="relative ml-auto flex items-center gap-1">
            <ThemeToggle />
            <button onClick={() => setNotificationsOpen((value) => !value)} className="relative rounded-xl p-2.5 text-muted hover:bg-[rgb(var(--field-bg))] hover:text-fg" aria-label="Уведомления"><Icon name="bell" />{unread.length > 0 && <span className="absolute right-1 top-1 grid h-4 min-w-4 place-items-center rounded-full bg-accent px-1 text-[9px] font-semibold text-white">{unread.length}</span>}</button>
            {notificationsOpen && (
              <div className="absolute right-0 top-12 w-[340px] overflow-hidden rounded-2xl border border-[rgb(var(--glass-border))] bg-white shadow-xl dark:bg-[rgb(var(--glass-bg))]">
                <div className="border-b border-[rgb(var(--row-divider))] px-4 py-3 font-medium">Новые формы</div>
                {unread.length === 0 ? <div className="px-4 py-6 text-sm text-muted">Новых заполненных форм нет.</div> : unread.map((form) => <button key={form.id} onClick={() => openSubmission(form)} className="block w-full border-b border-[rgb(var(--row-divider))] px-4 py-3 text-left hover:bg-[rgb(var(--field-bg))]"><div className="text-sm font-medium">{form.title}</div><div className="mt-1 text-xs text-muted">Форма заполнена · открыть карточку</div></button>)}
              </div>
            )}
          </div>
        </header>
        <main className="mx-auto max-w-[1760px] px-5 pb-14 pt-4 md:px-8 md:pt-5 lg:px-[clamp(48px,5vw,88px)] lg:pt-0">{children}</main>
      </div>
    </div>
  );
}

function ProfileMenu({
  userName,
  email,
  companies,
  activeCompanyId,
  onSelect,
  onAdd,
  onLogout,
}: {
  userName: string;
  email: string;
  companies: ReturnType<typeof useAuth>["companies"];
  activeCompanyId?: string;
  onSelect: (company: ReturnType<typeof useAuth>["companies"][number]) => void;
  onAdd: () => void;
  onLogout: () => void;
}) {
  return (
    <div className="absolute bottom-[82px] left-4 right-4 overflow-hidden rounded-2xl border border-black/10 bg-white shadow-[0_18px_50px_rgba(34,25,17,0.16)] dark:border-white/10 dark:bg-[#181818]">
      <div className="border-b border-[rgb(var(--row-divider))] px-4 py-4">
        <div className="truncate text-sm font-medium">{userName}</div>
        <div className="mt-0.5 truncate text-xs text-muted">{email}</div>
      </div>
      <div className="max-h-[260px] overflow-y-auto p-2">
        <div className="px-2 pb-2 pt-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-muted">Компании</div>
        {companies.map((company) => (
          <button key={company.id} type="button" onClick={() => onSelect(company)} className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left hover:bg-[#f7f4f1] dark:hover:bg-white/5">
            <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-[#eee4f7] text-xs font-semibold text-accent">{initialsFor(company.name)}</div>
            <div className="min-w-0 flex-1">
              <div className="truncate text-sm font-medium">{company.name}</div>
              <div className="text-[11px] text-muted">{ROLE_LABEL[company.role]}</div>
            </div>
            {company.id === activeCompanyId && <span className="text-sm text-accent">✓</span>}
          </button>
        ))}
        <button type="button" onClick={onAdd} className="mt-1 flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm font-medium text-accent hover:bg-[#f7f4f1] dark:hover:bg-white/5">
          <span className="grid h-8 w-8 place-items-center rounded-lg border border-dashed border-accent/50 text-lg">+</span>
          Добавить компанию
        </button>
      </div>
      <div className="border-t border-[rgb(var(--row-divider))] p-2">
        <button type="button" onClick={onLogout} className="w-full rounded-xl px-3 py-2.5 text-left text-sm text-muted hover:bg-[#f7f4f1] hover:text-fg dark:hover:bg-white/5">Выйти из аккаунта</button>
      </div>
    </div>
  );
}

function initialsFor(value: string): string {
  return value.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]?.toLocaleUpperCase()).join("") || "H";
}
