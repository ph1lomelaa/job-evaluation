// Сверка параллельных независимых оценок одной должности (UX Шаг 4b,
// вариант A): несколько версий уже могут существовать (несколько экспертов
// независимо запускали оценку) — здесь видно расхождение по каждому
// подфактору и можно зафиксировать согласованную (финальную) версию.
import { useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Button, Card, ErrorBanner, Field, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { cn } from "../lib/cn";
import { useFactorLevelReference, useFactorLevelRules } from "../lib/factorLevels";
import { EMPTY_FACTOR_LEVELS, EMPTY_FACTOR_RULES, groupEvidence, subfactorRows } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import { FACTOR_GROUP_LABEL, type Evaluation, type FactorGroup } from "../lib/types";

const GROUPS: FactorGroup[] = ["know_how", "problem_solving", "accountability"];

export default function ReconciliationPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const [busyId, setBusyId] = useState<string | null>(null);
  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.getPosition(id), api.listEvaluations(id)]),
    [id],
  );
  const { data: levels } = useFactorLevelReference();
  const { data: rules } = useFactorLevelRules();

  const [position, versions] = useMemo(() => {
    if (!data) return [undefined, [] as Evaluation[]] as const;
    const [pos, evs] = data;
    const scored = evs
      .filter((e) => e.score)
      .sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    return [pos, scored] as const;
  }, [data]);

  const [leftId, setLeftId] = useState("");
  const [rightId, setRightId] = useState("");
  const left = versions.find((v) => v.id === leftId) ?? versions[1] ?? versions[0];
  const right = versions.find((v) => v.id === rightId) ?? versions[0];

  async function finalize(versionId: string) {
    setBusyId(versionId);
    try {
      await api.finalizeEvaluation(versionId);
      reload();
    } finally {
      setBusyId(null);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-24" />
        <Skeleton className="h-96" />
      </div>
    );
  }
  if (error || !position) {
    return <ErrorBanner message={error ?? "Должность не найдена"} onRetry={reload} />;
  }

  return (
    <div className="space-y-6">
      <div>
        <Link to={`/positions/${id}`} className="text-sm text-muted hover:text-fg">
          ← Назад к карточке оценки
        </Link>
        <h1 className="mt-2 text-[32px]">Сверка версий · {position.name}</h1>
        <p className="mt-2 max-w-3xl text-sm text-muted">
          Если несколько экспертов независимо запускали оценку этой должности — здесь видно,
          где их выводы расходятся по конкретным подфакторам, и можно зафиксировать
          согласованную версию для Оценочного комитета.
        </p>
      </div>

      {versions.length < 2 ? (
        <Card className="p-10 text-center text-muted">
          Для сверки нужно минимум 2 версии оценки с рассчитанными баллами. Сейчас доступна{" "}
          {versions.length}.
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <VersionPicker
              label="Версия A"
              versions={versions}
              value={left?.id ?? ""}
              onChange={setLeftId}
            />
            <VersionPicker
              label="Версия B"
              versions={versions}
              value={right?.id ?? ""}
              onChange={setRightId}
            />
          </div>

          {left && right && (
            <>
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <VersionSummary
                  evaluation={left}
                  busy={busyId === left.id}
                  onFinalize={() => finalize(left.id ?? "")}
                />
                <VersionSummary
                  evaluation={right}
                  busy={busyId === right.id}
                  onFinalize={() => finalize(right.id ?? "")}
                />
              </div>

              {GROUPS.map((group) => (
                <FactorDiffCard
                  key={group}
                  group={group}
                  left={left}
                  right={right}
                  levels={levels ?? EMPTY_FACTOR_LEVELS}
                  rules={rules ?? EMPTY_FACTOR_RULES}
                />
              ))}
            </>
          )}
        </>
      )}

      <div className="print:hidden">
        <Button variant="secondary" onClick={() => navigate(`/positions/${id}`)}>
          Открыть карточку оценки
        </Button>
      </div>
    </div>
  );
}

function VersionPicker({
  label,
  versions,
  value,
  onChange,
}: {
  label: string;
  versions: Evaluation[];
  value: string;
  onChange: (id: string) => void;
}) {
  return (
    <Field label={label}>
      <select className="field" value={value} onChange={(e) => onChange(e.target.value)}>
        {versions.map((v, i) => (
          <option key={v.id} value={v.id ?? ""}>
            Версия {versions.length - i} · {v.created_at.slice(0, 16).replace("T", " ")}
            {v.created_by_name ? ` · ${v.created_by_name}` : ""}
            {v.is_final ? " · ✓ финальная" : ""}
          </option>
        ))}
      </select>
    </Field>
  );
}

function VersionSummary({
  evaluation,
  busy,
  onFinalize,
}: {
  evaluation: Evaluation;
  busy: boolean;
  onFinalize: () => void;
}) {
  return (
    <Card className="flex flex-wrap items-center justify-between gap-3">
      <div>
        <div className="text-sm font-medium">
          {evaluation.created_by_name ?? "Автор не указан"}
        </div>
        <div className="mt-1 text-xs text-muted">
          {evaluation.created_at.slice(0, 16).replace("T", " ")} · грейд{" "}
          {evaluation.score?.grade ?? "—"} · {evaluation.score?.total_points ?? "—"} баллов
        </div>
      </div>
      {evaluation.is_final ? (
        <StatusDot color="green">✓ Финальная версия</StatusDot>
      ) : (
        <Button variant="secondary" disabled={busy} onClick={onFinalize}>
          {busy ? "Сохраняем…" : "Сделать финальной"}
        </Button>
      )}
    </Card>
  );
}

function FactorDiffCard({
  group,
  left,
  right,
  levels,
  rules,
}: {
  group: FactorGroup;
  left: Evaluation;
  right: Evaluation;
  levels: Parameters<typeof subfactorRows>[1];
  rules: Parameters<typeof subfactorRows>[2];
}) {
  if (!left.score || !right.score) return null;
  const leftRows = subfactorRows(left.score, levels, rules)[group];
  const rightRows = subfactorRows(right.score, levels, rules)[group];
  const leftEvidence = groupEvidence(left.score)[group];
  const rightEvidence = groupEvidence(right.score)[group];
  const anyDiff = leftRows.some((r, i) => r.level !== rightRows[i]?.level);

  return (
    <Card className="p-0">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[rgb(var(--row-divider))] px-5 py-4">
        <div className="text-sm font-semibold">{FACTOR_GROUP_LABEL[group]}</div>
        {anyDiff && <StatusDot color="amber">Есть расхождение</StatusDot>}
      </div>
      {leftRows.map((row, i) => {
        const rightRow = rightRows[i];
        const differs = rightRow && row.level !== rightRow.level;
        return (
          <div
            key={row.name}
            className={cn(
              "grid grid-cols-[minmax(0,1fr)_auto_auto] items-center gap-4 border-t border-[rgb(var(--row-divider))] px-5 py-3 text-sm first:border-t-0",
              differs && "bg-warn/10",
            )}
          >
            <div className="text-[rgb(var(--fg)/0.82)]">{row.name}</div>
            <span className="num min-w-10 text-center text-lg font-bold text-accent">
              {row.level}
            </span>
            <span
              className={cn(
                "num min-w-10 text-center text-lg font-bold",
                differs ? "text-warn" : "text-accent",
              )}
            >
              {rightRow?.level ?? "—"}
            </span>
          </div>
        );
      })}
      <div className="grid grid-cols-1 gap-4 border-t border-[rgb(var(--row-divider))] px-5 py-4 text-xs leading-5 md:grid-cols-2">
        <EvidenceList title="Доказательства · Версия A" evidence={leftEvidence.evidence} />
        <EvidenceList title="Доказательства · Версия B" evidence={rightEvidence.evidence} />
      </div>
    </Card>
  );
}

function EvidenceList({ title, evidence }: { title: string; evidence: string[] }) {
  return (
    <div>
      <div className="font-semibold uppercase tracking-wide text-muted">{title}</div>
      {evidence.length > 0 ? (
        <ul className="mt-1.5 list-disc space-y-1 pl-4">
          {evidence.map((e) => (
            <li key={e}>{e}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-1.5 text-muted">—</p>
      )}
    </div>
  );
}
