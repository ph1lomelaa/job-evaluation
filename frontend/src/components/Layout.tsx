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
      className="rounded-lg px-3 py-2 text-xl text-muted transition-colors hover:text-fg"
    >
      {theme === "dark" ? "☀️" : "🌙"}
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
