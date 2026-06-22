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
  positionId,
  reviewMode = false,
}: {
  title: string;
  color: Parameters<typeof StatusDot>[0]["color"];
  items: QCFlag[];
  positionId?: string | null;
  reviewMode?: boolean;
}) {
  if (items.length === 0) return null;
  const isBlockingReview = reviewMode && items.some((item) => item.status === "fail");
  return (
    <div className={cn(
      "rounded-xl bg-[rgb(var(--field-bg))] p-4",
      isBlockingReview ? "border-2 border-accent/55 bg-accent/[0.035]" : "border border-[rgb(var(--row-divider))]",
    )}>
      {isBlockingReview ? (
        <div className="-mx-4 -mt-4 mb-4 rounded-t-[10px] bg-accent px-4 py-3 text-white">
          <div className="text-sm font-bold uppercase tracking-wide">
            ✗ Блокирует вынос на комитет · {items.length}
          </div>
        </div>
      ) : (
        <div className="mb-3 flex items-center justify-between gap-3">
          <StatusDot color={color}>{title} ({items.length})</StatusDot>
        </div>
      )}
      <ul className="space-y-2.5">
        {items.map((q) => (
          <QcItem key={q.code} flag={q} positionId={positionId} reviewMode={reviewMode} />
        ))}
      </ul>
    </div>
  );
}

export function QcItem({
  flag,
  positionId,
  reviewMode = false,
}: {
  flag: QCFlag;
  positionId?: string | null;
  reviewMode?: boolean;
}) {
  const needsAction =
    flag.status !== "pass" && flag.recommendation && flag.recommendation !== "—";
  const isBlockingReview = reviewMode && flag.status === "fail";

  return (
    <li
      id={`qc-${flag.code}`}
      className={cn(
        "grid gap-3 rounded-lg px-4 py-4 sm:grid-cols-[86px_minmax(0,1fr)]",
        isBlockingReview ? "border-2 border-accent/55 bg-accent/[0.085]" : cn("border-l-[3px]", ITEM_TONE[flag.status]),
      )}
    >
      <span
        className={cn(
          "num h-fit w-fit rounded-md px-2 py-1 text-xs font-semibold shadow-sm",
          isBlockingReview ? "bg-accent px-3 py-1.5 text-sm font-bold text-white" : cn("bg-white/70 dark:bg-black/20", FLAG[flag.status].cls),
        )}
      >
        {FLAG[flag.status].ch} {FLAG[flag.status].label}
      </span>
      <div className="min-w-0 text-[15px] leading-6">
        <div className="text-[11px] font-semibold uppercase tracking-wide text-[rgb(var(--fg)/0.58)]">
          {flag.status === "pass" ? "Результат проверки" : "Почему отмечено"}
        </div>
        <div className="mt-0.5 font-medium text-fg">{flag.message}</div>
        {needsAction && (
          <div className="mt-3 border-t border-current/10 pt-2.5">
            <div className={cn("text-[11px] font-semibold uppercase tracking-wide", FLAG[flag.status].cls)}>
              Что нужно сделать
            </div>
            <div className="mt-1 text-sm leading-6 text-[rgb(var(--fg)/0.86)]">
              {flag.recommendation}
            </div>
            {positionId && flag.code === "authorities_assumed" && (
              <a
                href={`/positions/${positionId}/edit?step=2`}
                className="mt-3 inline-flex rounded-lg border border-accent/30 px-3 py-2 text-sm font-semibold text-accent transition-colors hover:bg-accent/5"
              >
                Перейти к полномочиям →
              </a>
            )}
          </div>
        )}
      </div>
    </li>
  );
}
