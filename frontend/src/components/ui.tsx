import { motion } from "framer-motion";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  TextareaHTMLAttributes,
} from "react";
import { cn } from "../lib/cn";

// ── Button ──────────────────────────────────────────────────────────────────
type ButtonVariant = "primary" | "secondary" | "danger" | "ghost";

const BUTTON_VARIANTS: Record<ButtonVariant, string> = {
  primary: "bg-accent text-white hover:opacity-90",
  secondary: "border border-[rgb(var(--field-border))] text-fg hover:border-[rgb(var(--glass-border-hover))]",
  danger: "bg-[#252527] text-white hover:bg-[#151516] dark:bg-white dark:text-[#252527] dark:hover:bg-[#ececec]",
  ghost: "text-muted hover:text-fg",
};

export function Button({
  variant = "primary",
  className,
  children,
  ...rest
}: { variant?: ButtonVariant } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-lg px-4 py-3 text-sm font-medium transition-colors",
        "min-h-[40px] disabled:cursor-not-allowed disabled:opacity-50",
        BUTTON_VARIANTS[variant],
        className,
      )}
      {...rest}
    >
      {children}
    </button>
  );
}

// ── Field (label + input/textarea) ────────────────────────────────────────────
export function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm text-muted">{label}</span>
      {children}
      {hint && <span className="mt-1 block text-xs text-muted">{hint}</span>}
    </label>
  );
}

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input className="field" {...props} />;
}

export function Textarea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea className="field min-h-[96px] resize-y" {...props} />;
}

// ── Card / Glass ──────────────────────────────────────────────────────────────
export function Card({
  className,
  children,
  hover,
  onClick,
  ...rest
}: {
  className?: string;
  children: ReactNode;
  hover?: boolean;
  onClick?: () => void;
} & HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      onClick={onClick}
      className={cn("glass p-6", hover && "glass-hover cursor-pointer", className)}
      {...rest}
    >
      {children}
    </div>
  );
}

// ── StatusDot (точка + текст, без фоновых бейджей) ────────────────────────────
type DotColor = "gray" | "red" | "green" | "blue" | "amber";
const DOT: Record<DotColor, string> = {
  gray: "bg-muted",
  red: "bg-accent",
  green: "bg-ok",
  blue: "bg-[#3b82f6]",
  amber: "bg-warn",
};

export function StatusDot({ color, children }: { color: DotColor; children: ReactNode }) {
  return (
    <span className="inline-flex items-center gap-2 text-sm">
      <span className={cn("h-2 w-2 rounded-full", DOT[color])} />
      {children}
    </span>
  );
}

// ── ErrorBanner ───────────────────────────────────────────────────────────────
export function ErrorBanner({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="glass flex flex-wrap items-center justify-between gap-3 border-accent/40 p-4 text-sm">
      <span className="text-err">⚠ {message}</span>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          Повторить
        </Button>
      )}
    </div>
  );
}

// ── Skeleton ──────────────────────────────────────────────────────────────────
export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("glass animate-pulse rounded-lg", className)} />;
}

// ── Stepper (горизонтальный, только номера) ───────────────────────────────────
export function Stepper({
  steps,
  current,
  onSelect,
}: {
  steps: string[];
  current: number;
  onSelect: (i: number) => void;
}) {
  return (
    <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
      {steps.map((label, i) => {
        const done = i < current;
        const active = i === current;
        return (
          <button
            key={label}
            onClick={() => onSelect(i)}
            className="group flex items-center gap-2 text-sm transition-colors"
          >
            <span
              className={cn(
                "num text-xs",
                done ? "text-ok" : active ? "text-accent" : "text-muted",
              )}
            >
              {done ? "✓" : String(i + 1).padStart(2, "0")}
            </span>
            <span
              className={cn(
                "border-b pb-0.5 transition-colors",
                active
                  ? "border-accent text-fg"
                  : "border-transparent text-muted group-hover:text-fg",
              )}
            >
              {label}
            </span>
          </button>
        );
      })}
    </div>
  );
}

// ── Modal ──────────────────────────────────────────────────────────────────────
export function Modal({
  open,
  onClose,
  children,
}: {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}) {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: "rgb(var(--overlay))" }}
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.15 }}
        className="glass w-full max-w-[600px] p-8"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </motion.div>
    </div>
  );
}
