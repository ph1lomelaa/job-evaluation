import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, ErrorBanner, Input, Skeleton, StatusDot } from "../components/ui";
import { api } from "../lib/api";
import { latestByPosition } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";
import { STATUS_LABEL, type EvaluationStatus } from "../lib/types";

const STATUS_COLOR: Record<EvaluationStatus, "green" | "amber" | "red"> = {
  ready: "green",
  needs_clarification: "amber",
  cannot_evaluate: "red",
};

const modifier = (value: number) => value > 0 ? "+" : value < 0 ? "−" : "0";

export default function AssessmentSheetPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const { data, error, loading, reload } = useFetch(() => Promise.all([api.listPositions(), api.listEvaluations()]), []);
  const rows = useMemo(() => {
    if (!data) return [];
    const evaluations = latestByPosition(data[1]);
    return data[0].map((position) => ({ position, evaluation: position.id ? evaluations.get(position.id) : undefined }))
      .filter(({ position }) => !query || position.name.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => a.position.name.localeCompare(b.position.name, "ru"));
  }, [data, query]);

  return <div className="space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><h1>Ведомость оценки должностей</h1><p className="mt-2 max-w-3xl text-sm text-muted">Единый реестр факторных оценок. Модификаторы «+» и «−» показаны отдельно от базовых уровней и уже учтены в баллах.</p></div>
      <div className="w-full md:w-[320px]"><Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Найти должность" /></div>
    </div>
    {error && <ErrorBanner message={error} onRetry={reload} />}
    {loading ? <Skeleton className="h-80" /> : <Card className="overflow-hidden rounded-[18px] p-0">
      <div className="overflow-x-auto">
      <table className="w-full min-w-[1480px] border-collapse text-sm">
        <thead className="sticky top-0 z-20 text-xs">
          <tr className="text-center">
            <th rowSpan={2} className="sticky left-0 z-30 min-w-[270px] border-b border-r border-[#d8d3cc] bg-[#f5f3ef] px-5 py-3 text-left font-semibold text-fg dark:border-white/15 dark:bg-[#242424]">Должность</th>
            <th colSpan={3} className="border-b border-r border-[#d8d3cc] bg-[#f2eee7] px-4 py-2.5 font-semibold text-fg dark:border-white/15 dark:bg-white/10">Знания и умения · Know-How</th>
            <th colSpan={4} className="border-b border-r border-[#d8d3cc] bg-[#eef1ed] px-4 py-2.5 font-semibold text-fg dark:border-white/15 dark:bg-white/[0.07]">Решение вопросов · Problem Solving</th>
            <th colSpan={3} className="border-b border-r border-[#d8d3cc] bg-[#f1edf3] px-4 py-2.5 font-semibold text-fg dark:border-white/15 dark:bg-white/10">Ответственность · Accountability</th>
            <th rowSpan={2} className="border-b border-r border-[#d8d3cc] bg-[#f5f3ef] px-4 py-3 font-semibold text-fg dark:border-white/15 dark:bg-[#242424]">Итого</th>
            <th rowSpan={2} className="border-b border-r border-[#d8d3cc] bg-[#f5f3ef] px-4 py-3 font-semibold text-fg dark:border-white/15 dark:bg-[#242424]">Профиль</th>
            <th rowSpan={2} className="border-b border-r border-[#d8d3cc] bg-[#f5f3ef] px-4 py-3 font-semibold text-fg dark:border-white/15 dark:bg-[#242424]">Грейд</th>
            <th rowSpan={2} className="min-w-[180px] border-b border-[#d8d3cc] bg-[#f5f3ef] px-4 py-3 text-left font-semibold text-fg dark:border-white/15 dark:bg-[#242424]">Статус</th>
          </tr>
          <tr className="bg-[#faf9f6] text-center text-muted dark:bg-[#202020]">
            {["Код", "+/−", "Баллы", "Код", "+/−", "% KH", "Баллы", "Код", "+/−", "Баллы"].map((label, index) => (
              <th key={`${label}-${index}`} className="border-b border-r border-[#d8d3cc] px-3 py-2 font-medium dark:border-white/15">{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>{rows.map(({ position, evaluation }) => {
          const s = evaluation?.selections; const score = evaluation?.score;
          const cell = "border-b border-r border-[#dedad4] px-3 py-3 text-center dark:border-white/10";
          return <tr key={position.id} onDoubleClick={() => position.id && navigate(`/positions/${position.id}`)} title="Двойной клик — открыть карточку" className="group cursor-pointer bg-white transition-colors hover:bg-[#f8f6f2] dark:bg-[rgb(var(--glass-bg))] dark:hover:bg-white/5">
            <td className="sticky left-0 z-10 border-b border-r border-[#dedad4] bg-white px-5 py-3 font-medium shadow-[4px_0_8px_rgba(38,32,25,0.035)] group-hover:bg-[#f8f6f2] dark:border-white/10 dark:bg-[rgb(var(--glass-bg))] dark:group-hover:bg-[#252525]">{position.name}<div className="mt-1 text-xs font-normal text-muted">{position.dzo || position.department || "—"}</div></td>
            <td className={`${cell} num`}>{s ? `${s.know_how.specialization}/${s.know_how.management}/${s.know_how.communication}` : "—"}</td><td className={`${cell} num`}>{s ? modifier(s.know_how.plus_minus) : "—"}</td><td className={`${cell} num font-semibold`}>{score?.know_how.points ?? "—"}</td>
            <td className={`${cell} num`}>{s ? `${s.problem_solving.area}/${s.problem_solving.complexity}` : "—"}</td><td className={`${cell} num`}>{s ? modifier(s.problem_solving.plus_minus) : "—"}</td><td className={`${cell} num`}>{score ? `${score.problem_solving.percentage}%` : "—"}</td><td className={`${cell} num font-semibold`}>{score?.problem_solving.points ?? "—"}</td>
            <td className={`${cell} num`}>{s ? `${s.accountability.freedom}/${s.accountability.magnitude}/${s.accountability.non_quantitative_impact ?? s.accountability.impact ?? "—"}` : "—"}</td><td className={`${cell} num`}>{s ? modifier(s.accountability.plus_minus) : "—"}</td><td className={`${cell} num font-semibold`}>{score?.accountability.points ?? "—"}</td>
            <td className={`${cell} num text-base font-semibold`}>{score?.total_points ?? "—"}</td><td className={`${cell} num font-medium`}>{score?.profile_long || "—"}</td><td className={`${cell} num font-semibold`}>{score?.grade ?? "—"}</td>
            <td className="border-b border-[#dedad4] px-4 py-3 dark:border-white/10">{evaluation ? <StatusDot color={STATUS_COLOR[evaluation.status]}>{STATUS_LABEL[evaluation.status]}</StatusDot> : <StatusDot color="gray">Не оценена</StatusDot>}</td>
          </tr>;
        })}</tbody>
      </table>
      </div>
      {rows.length === 0 && <div className="py-14 text-center text-muted">Должности не найдены.</div>}
    </Card>}
  </div>;
}
