// Рендер QC-флагов (PASS/WARN/FAIL) — общий для карточки оценки и калькулятора,
// чтобы оба места показывали QC одинаково и не расходились в разметке.
import { cn } from "../lib/cn";
import type { QCFlag, QCStatus } from "../lib/types";
import { StatusDot } from "./ui";

const FLAG: Record<QCStatus, { ch: string; cls: string; label: string }> = {
  pass: { ch: "✓", cls: "text-ok", label: "PASS" },
  warn: { ch: "⚠", cls: "text-warn", label: "WARN" },
  fail: { ch: "✗", cls: "text-accent", label: "FAIL" },
};

const ITEM_TONE: Record<QCStatus, string> = {
  pass: "border-ok/25 bg-ok/[0.045]",
  warn: "border-warn/40 bg-warn/[0.07]",
  fail: "border-accent/35 bg-accent/[0.055]",
};

export function QcSection({
  title,
  color,
  items,
}: {
  title: string;
  color: Parameters<typeof StatusDot>[0]["color"];
  items: QCFlag[];
}) {
  if (items.length === 0) return null;
  return (
    <div className="rounded-xl border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <StatusDot color={color}>{title} ({items.length})</StatusDot>
      </div>
      <ul className="space-y-2.5">
        {items.map((q) => (
          <QcItem key={q.code} flag={q} />
        ))}
      </ul>
    </div>
  );
}

export function QcItem({ flag }: { flag: QCFlag }) {
  const needsAction =
    flag.status !== "pass" && flag.recommendation && flag.recommendation !== "—";

  return (
    <li
      className={cn(
        "grid gap-3 rounded-lg border-l-[3px] px-4 py-3 sm:grid-cols-[76px_minmax(0,1fr)]",
        ITEM_TONE[flag.status],
      )}
    >
      <span
        className={cn(
          "num h-fit w-fit rounded-md bg-white/70 px-2 py-1 text-xs font-semibold shadow-sm dark:bg-black/20",
          FLAG[flag.status].cls,
        )}
      >
        {FLAG[flag.status].ch} {FLAG[flag.status].label}
      </span>
      <div className="min-w-0 text-sm leading-6">
        <div className="text-[11px] font-semibold uppercase tracking-wide text-[rgb(var(--fg)/0.58)]">
          {flag.status === "pass" ? "Результат проверки" : "Почему отмечено"}
        </div>
        <div className="mt-0.5 font-medium text-fg">{flag.message}</div>
        {needsAction && (
          <div className="mt-3 border-t border-current/10 pt-2.5">
            <div className={cn("text-[11px] font-semibold uppercase tracking-wide", FLAG[flag.status].cls)}>
              Что нужно сделать
            </div>
            <div className="mt-0.5 text-[13px] leading-5 text-[rgb(var(--fg)/0.82)]">
              {flag.recommendation}
            </div>
          </div>
        )}
      </div>
    </li>
  );
}
