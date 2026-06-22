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
      <ul className="space-y-3">
        {items.map((q) => (
          <QcItem key={q.code} flag={q} />
        ))}
      </ul>
    </div>
  );
}

export function QcItem({ flag }: { flag: QCFlag }) {
  return (
    <li className="flex gap-3 border-t border-[rgb(var(--row-divider))] pt-3 first:border-t-0 first:pt-0">
      <span className={cn("num w-12 shrink-0 text-sm", FLAG[flag.status].cls)}>
        {FLAG[flag.status].ch} {FLAG[flag.status].label}
      </span>
      <div className="text-sm">
        <div>{flag.message}</div>
        {flag.status !== "pass" && flag.recommendation && flag.recommendation !== "—" && (
          <div className="mt-0.5 text-xs text-muted">{flag.recommendation}</div>
        )}
      </div>
    </li>
  );
}
