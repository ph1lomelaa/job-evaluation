import type { ReactNode } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { cn } from "../lib/cn";
import { useTheme } from "../lib/theme";

function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return (
    <button
      onClick={toggle}
      aria-label="Переключить тему"
      className="rounded-lg px-2 py-2 text-muted transition-colors hover:text-fg flex items-center justify-center"
      title={theme === "dark" ? "Светлый режим" : "Тёмный режим"}
    >
      {theme === "dark" ? (
        // Sun icon (for switching to light)
        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
      ) : (
        // Moon icon (for switching to dark)
        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      )}
    </button>
  );
}

const NAV = [
  { to: "/", label: "Должности" },
  { to: "/new", label: "Новая должность" },
  { to: "/compare", label: "Сравнение" },
];

function Header() {
  return (
    <header className="glass sticky top-0 z-40 flex h-16 items-center justify-between rounded-none border-x-0 border-t-0 px-6">
      <div className="flex items-center gap-12">
        <nav className="flex items-center gap-1">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.to === "/"}
              className={({ isActive }) =>
                cn(
                  "rounded-lg px-3 py-2 text-sm transition-colors",
                  isActive ? "text-fg" : "text-muted hover:text-fg",
                )
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <span className="num h-8 w-8 rounded-full bg-[rgb(var(--field-bg))] text-center text-sm leading-8">
          АК
        </span>
      </div>
    </header>
  );
}

export function MainLayout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  return (
    <div className="min-h-screen">
      <Header key={pathname} />
      <main className="mx-auto max-w-[1440px] px-8 py-8">
        {children}
      </main>
    </div>
  );
}
