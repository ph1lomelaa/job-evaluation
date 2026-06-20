import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, ErrorBanner, Input, Skeleton } from "../components/ui";
import { api } from "../lib/api";
import { latestByPosition } from "../lib/mapping";
import { useFetch } from "../lib/useFetch";

const COLORS = {
  blue: { label: "Нижняя", cls: "bg-blue-100 text-blue-700" },
  green: { label: "Средняя", cls: "bg-emerald-100 text-emerald-700" },
  orange: { label: "Верхняя", cls: "bg-orange-100 text-orange-700" },
} as const;

const CELL = "border-b border-r border-[#d8d3cc] px-5 py-3.5 dark:border-white/15";

export default function GradeTablePage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const { data, error, loading, reload } = useFetch(
    () => Promise.all([api.listPositions(), api.listEvaluations(), api.listGradeBands()]),
    [],
  );

  const rows = useMemo(() => {
    if (!data) return [];
    const latest = latestByPosition(data[1]);
    return data[0]
      .map((position) => ({ position, score: position.id ? latest.get(position.id)?.score : undefined }))
      .filter(({ position }) => !query || position.name.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => (b.score?.grade ?? -1) - (a.score?.grade ?? -1));
  }, [data, query]);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1>Таблица грейдов</h1>
          <p className="mt-2 text-sm text-muted">Баллы, диапазон грейда и положение каждой должности.</p>
        </div>
        <div className="w-full md:w-[320px]">
          <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Найти должность" />
        </div>
      </div>

      {error && <ErrorBanner message={error} onRetry={reload} />}

      {loading ? (
        <Skeleton className="h-72" />
      ) : (
        <Card className="overflow-hidden rounded-[18px] p-0">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[1080px] border-collapse text-sm">
              <thead className="sticky top-0 z-10 bg-[#f5f3ef] text-left text-xs text-fg dark:bg-[#242424]">
                <tr>
                  {["Должность", "Организация / функция", "Баллы", "Грейд", "Диапазон", "Положение", "Зона"].map((heading) => (
                    <th key={heading} className={`${CELL} font-semibold last:border-r-0`}>{heading}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map(({ position, score }) => {
                  const color = score ? COLORS[score.grade_color] : null;
                  return (
                    <tr
                      key={position.id}
                      onDoubleClick={() => position.id && navigate(`/positions/${position.id}`)}
                      title="Двойной клик — открыть карточку"
                      className="cursor-pointer bg-white transition-colors hover:bg-[#f8f6f2] dark:bg-[rgb(var(--glass-bg))] dark:hover:bg-white/5"
                    >
                      <td className={`${CELL} font-medium`}>{position.name}</td>
                      <td className={`${CELL} text-muted`}>{position.dzo || position.function || "—"}</td>
                      <td className={`${CELL} num text-center text-base font-semibold`}>{score?.total_points ?? "—"}</td>
                      <td className={`${CELL} num text-center text-base font-semibold`}>{score?.grade ?? "—"}</td>
                      <td className={`${CELL} num text-center`}>{score ? `${score.grade_lower}–${score.grade_upper}` : "—"}</td>
                      <td className={`${CELL} text-center`}>{score?.grade_zone ?? "—"}</td>
                      <td className="border-b border-[#d8d3cc] px-5 py-3.5 text-center dark:border-white/15">
                        {color ? <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${color.cls}`}>{color.label}</span> : "—"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {rows.length === 0 && <div className="py-12 text-center text-muted">Оценённых должностей пока нет.</div>}
        </Card>
      )}

      {data && (
        <Card className="overflow-hidden rounded-[18px] p-0">
          <div className="border-b border-[#bdb7af] px-5 py-4 dark:border-white/20">
            <h3 className="text-base">Эталонная матрица Jobgrades</h3>
            <p className="mt-1 text-xs text-muted">Точные границы из листа Jobgrades калькулятора Hay Group.</p>
          </div>
          <div className="max-h-[420px] overflow-auto">
            <table className="w-full border-collapse text-sm">
              <thead className="sticky top-0 z-10 bg-[#f5f3ef] text-left text-xs text-fg dark:bg-[#242424]">
                <tr>
                  {["Грейд", "Нижняя граница", "Середина", "Верхняя граница"].map((heading) => (
                    <th key={heading} className={`${CELL} font-semibold last:border-r-0`}>{heading}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data[2].map((band) => (
                  <tr key={band.grade} className="bg-white hover:bg-[#f8f6f2] dark:bg-[rgb(var(--glass-bg))] dark:hover:bg-white/5">
                    <td className={`${CELL} num font-semibold`}>{band.grade}</td>
                    <td className={`${CELL} num`}>{band.lower}</td>
                    <td className={`${CELL} num`}>{band.mid}</td>
                    <td className="border-b border-[#d8d3cc] px-5 py-3.5 font-mono dark:border-white/15">{band.upper}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
