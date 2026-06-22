import { useState } from "react";
import { Card } from "../components/ui";
import { cn } from "../lib/cn";

type Tab = "knowhow" | "ps" | "accountability" | "profile";

const TABS: { id: Tab; label: string }[] = [
  { id: "knowhow", label: "Знания и Умения" },
  { id: "ps", label: "Решение Вопросов" },
  { id: "accountability", label: "Ответственность" },
  { id: "profile", label: "Краткий профиль" },
];

export default function GuidePage() {
  const [tab, setTab] = useState<Tab>("knowhow");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-[32px]">Методология Hay Group</h1>
        <p className="mt-2 text-sm text-muted">
          Hay Group Guide Chart-Profile Method℠ — система оценки должностей по трём факторам
        </p>
      </div>

      <Card>
        <h2 className="mb-1 text-lg font-medium">Граничный модификатор (+/−)</h2>
        <p className="text-sm leading-6 text-muted">
          У каждой ячейки подстановочной таблицы на самом деле есть три числа: базовое
          значение и два соседних шага геометрического ряда Hay (шаг ≈15%) — «−» (шаг вниз)
          и «+» (шаг вверх). Модификатор общий для всех трёх факторов (Know-How, Problem
          Solving, Accountability) — это не способ выразить неуверенность в оценке, а
          фиксация того, что роль находится на границе между двумя соседними уровнями.
        </p>
        <div className="mt-4 grid gap-3 text-sm md:grid-cols-2">
          <div className="rounded-lg border border-[rgb(var(--row-divider))] p-3">
            <div className="font-medium">Когда ставить «+»</div>
            <p className="mt-1 text-muted">
              Роль явно превосходит базовый уровень, но не дотягивает до следующего уровня
              целиком — то есть находится выше базы, но ниже соседней ячейки сверху.
            </p>
          </div>
          <div className="rounded-lg border border-[rgb(var(--row-divider))] p-3">
            <div className="font-medium">Когда ставить «−»</div>
            <p className="mt-1 text-muted">
              Базовый уровень формально достигнут, но только по его нижней границе — роль
              на грани с соседней ячейкой снизу.
            </p>
          </div>
        </div>
        <p className="mt-4 text-xs leading-5 text-muted">
          Система требует для каждого модификатора соседнюю ячейку (<code>adjacent_level</code>)
          и текстовое объяснение границы (<code>modifier_reason</code>): без них QC-проверка
          «модификатор не имеет обоснования» помечает фактор как WARN — модификатор без
          указанной соседней ячейки и причины считается необоснованным.
        </p>
      </Card>

      {/* Tabs */}
      <div className="flex gap-6 overflow-x-auto border-b border-[#ded9d2] dark:border-white/10">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={cn(
              "shrink-0 border-b-2 px-1 pb-3 pt-1 text-sm transition-colors",
              tab === t.id
                ? "border-[#252527] font-medium text-[#252527] dark:border-white dark:text-white"
                : "border-transparent text-muted hover:text-fg",
            )}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "knowhow" && <KnowHowTab />}
      {tab === "ps" && <ProblemSolvingTab />}
      {tab === "accountability" && <AccountabilityTab />}
      {tab === "profile" && <ProfileTab />}
    </div>
  );
}

// ── Know-How ──────────────────────────────────────────────────────────────────

function KnowHowTab() {
  return (
    <div className="space-y-6">
      <Card>
        <h2 className="mb-1 text-lg font-medium">Знания и Умения (Know-How)</h2>
        <p className="text-sm text-muted leading-relaxed">
          Совокупность всех соответствующих знаний, навыков и опыта, необходимых для выполнения
          должностных обязанностей на стандартном уровне. Измеряется по трём измерениям.
        </p>
      </Card>

      <div className="grid gap-4 md:grid-cols-3">
        <DimCard
          index="I"
          title="Специальные / практические знания"
          subtitle="Глубина и ширина специализации"
          color="blue"
          levels={[
            { code: "A", label: "Элементарные базовые", desc: "Базовые умения: считать, читать, понимать простые инструкции" },
            { code: "B", label: "Общие практические", desc: "Стандартные рабочие правила, процессы, оборудование" },
            { code: "C", label: "Продвинутые практические", desc: "Широкие знания методов, техник, материалов, обучение на рабочем месте" },
            { code: "D", label: "Базовые профессиональные", desc: "Знание теоретических основ и практики в конкретной области" },
            { code: "E", label: "Зрелые профессиональные", desc: "Широкое профессиональное образование и практические знания" },
            { code: "F", label: "Профессиональные", desc: "Высокий уровень знаний в профессиональной области" },
            { code: "G", label: "Всесторонние", desc: "Разностороннее знание миниатюр/дисциплин" },
            { code: "H", label: "Уникальные", desc: "Уникальные, авторитетные знания в мировом масштабе" },
          ]}
        />
        <DimCard
          index="II"
          title="Знания и умения планировать, организовывать и интегрировать"
          subtitle="Управленческие знания"
          color="green"
          levels={[
            { code: "T", label: "Нет управления", desc: "Управленческие знания и умения не требуются" },
            { code: "I", label: "Ориентирование", desc: "Выполнение задач с помощью других лиц" },
            { code: "II", label: "Оперативное", desc: "Планирование, контроль, организация деятельности группы" },
            { code: "III", label: "Тактическое", desc: "Интеграция разнородных функций в рамках подразделения" },
            { code: "IV", label: "Стратегическое", desc: "Управление ключевыми функциями организации" },
          ]}
        />
        <DimCard
          index="III"
          title="Навыки общения и воздействия"
          subtitle="Коммуникативные навыки"
          color="yellow"
          levels={[
            { code: "1", label: "Базовые", desc: "Передача и получение информации" },
            { code: "2", label: "Важные", desc: "Влияние, убеждение или взаимодействие с другими людьми" },
            { code: "3", label: "Критические", desc: "Убеждение и мотивация людей, достижение результатов через общение" },
          ]}
        />
      </div>

      <Card>
        <h3 className="mb-4 text-sm font-medium text-muted uppercase tracking-wide">Таблица баллов Know-How (фрагмент)</h3>
        <div className="overflow-x-auto">
          <KnowHowTable />
        </div>
        <p className="mt-3 text-xs text-muted">
          Шаг между соседними значениями ~15%. Код формируется как: специализация + управление + коммуникации (например E/II/2).
        </p>
      </Card>
    </div>
  );
}

// ── Problem Solving ───────────────────────────────────────────────────────────

function ProblemSolvingTab() {
  return (
    <div className="space-y-6">
      <Card>
        <h2 className="mb-1 text-lg font-medium">Решение Вопросов (Problem Solving)</h2>
        <p className="text-sm text-muted leading-relaxed">
          Уровень сложности проблем, которые необходимо решать. Это уровень знаний и умений, применяемых
          для анализа, рассуждений, оценки, создания решений, формирования выводов и заключений.
          Измеряется как процент от баллов Know-How.
        </p>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <DimCard
          index="1"
          title="Область решаемых вопросов — Свобода мышления"
          subtitle="Среда, в которой происходит мышление"
          color="blue"
          levels={[
            { code: "A", label: "Строго «по шаблону»", desc: "Мышление в пределах стандартных инструкций, очень чётко определённых правил" },
            { code: "B", label: "«По шаблону»", desc: "Мышление в пределах стандартных практик и процедур, постоянный контроль" },
            { code: "C", label: "Процедурная (полушаблонная)", desc: "Действует в рамках стандартных практик и процедуры, контроль конечных результатов" },
            { code: "D", label: "Нормативная", desc: "Действует в рамках конкретных политик и регламентов, оценка руководителя" },
            { code: "E", label: "Ясно определённая", desc: "Мышление в пределах принципов и задач, определённых руководством" },
            { code: "F", label: "Широко определённая", desc: "Мышление в пределах широких политик и целей организации" },
            { code: "G", label: "В целом определённая", desc: "Мышление в пределах общих стратегических целей компании" },
            { code: "H", label: "Абстрактно определённая", desc: "Мышление в пределах философии бизнеса, законов природы" },
          ]}
        />
        <DimCard
          index="2"
          title="Сложность решаемых вопросов"
          subtitle="Характер мышления и сложность задач"
          color="green"
          levels={[
            { code: "1", label: "Повторяющиеся", desc: "Решение вопросов путём простого выбора из ограниченного числа заученных ответов" },
            { code: "2", label: "Подобные (шаблонные)", desc: "Решение применяется с помощью сравнения альтернатив" },
            { code: "3", label: "Изменяющиеся", desc: "Разнообразные ситуации, применение суждений и приобретённых знаний" },
            { code: "4", label: "Нестандартные", desc: "Аналитическое, интерпретирующее, оценочное мышление, разработка новых решений" },
            { code: "5", label: "Неизученные", desc: "Исследование неизвестных ситуаций, разработка концепций и подходов" },
          ]}
        />
      </div>

      <Card>
        <h3 className="mb-4 text-sm font-medium text-muted uppercase tracking-wide">Как читать таблицу</h3>
        <div className="grid gap-4 md:grid-cols-2 text-sm">
          <div>
            <div className="font-medium mb-1">Формат кода</div>
            <p className="text-muted">Буква (область) + цифра (сложность), например <span className="num font-medium text-fg">E/3</span> означает "Ясно определённая / Изменяющиеся".</p>
          </div>
          <div>
            <div className="font-medium mb-1">Результат в процентах</div>
            <p className="text-muted">Баллы Problem Solving = баллы Know-How × процент из таблицы. Процент зависит от комбинации области и сложности.</p>
          </div>
        </div>
        <div className="mt-4 overflow-x-auto">
          <PSTable />
        </div>
      </Card>
    </div>
  );
}

// ── Accountability ────────────────────────────────────────────────────────────

function AccountabilityTab() {
  return (
    <div className="space-y-6">
      <Card>
        <h2 className="mb-1 text-lg font-medium">Ответственность (Accountability)</h2>
        <p className="text-sm text-muted leading-relaxed">
          Степень ответственности за действия и их последствия. По корпоративному правилу
          KMG DIGITAL доход и денежная величина не учитываются: применяется ветка N,
          состоящая из свободы действий A–H и неколичественного уровня воздействия I–VI.
        </p>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <DimCard
          index="I"
          title="Свобода действий (полномочия)"
          subtitle="Степень самостоятельности"
          color="blue"
          levels={[
            { code: "A", label: "Строго контролируемая", desc: "Следует детальным инструкциям, работает под постоянным строгим контролем" },
            { code: "B", label: "Контролируемая", desc: "Следует детальным инструкциям и работает под постоянным контролем" },
            { code: "C", label: "Нормированная", desc: "Действует в рамках стандартных практик и процедур" },
            { code: "D", label: "Регулируемая в целом", desc: "Действует в рамках конкретных политик и процедур, контроль результатов" },
            { code: "E", label: "Управляемая", desc: "Действует под общим руководством функциональных политик и целей" },
            { code: "F", label: "Управляемая в общих чертах", desc: "Направление деятельности в рамках широких политик компании" },
            { code: "G", label: "Направляющая", desc: "Определение целей компании в рамках общих стратегических политик" },
            { code: "H", label: "Стратегически ориентируемая", desc: "В силу размера и сложности организации, определяет общее направление" },
          ]}
        />
        <DimCard
          index="II"
          title="Неколичественный уровень воздействия"
          subtitle="Организационный охват и характер вклада"
          color="green"
          levels={[
            { code: "I", label: "Вспомогательное", desc: "Разовые услуги или отдельные операции для других ролей" },
            { code: "II", label: "Поддерживающее", desc: "Информационная или административная поддержка внутри подразделения" },
            { code: "III", label: "Операционное", desc: "Услуги нескольким подразделениям или поддержка ключевого процесса" },
            { code: "IV", label: "Аналитическое", desc: "Специализированная аналитика, диагностика, консультации или критичные сложные системы" },
            { code: "V", label: "Направляющее", desc: "Ежедневное руководство направлениями, командами или проектами; системные решения" },
            { code: "VI", label: "Воздействующее", desc: "Несколько связанных команд, стратегические программы или политика всей организации" },
          ]}
        />
      </div>

      <Card>
        <h3 className="mb-2 text-sm font-medium text-muted uppercase tracking-wide">Как читать код</h3>
        <p className="text-sm leading-6">
          Пример <span className="num font-semibold">E / N / IV</span>: свобода действий E,
          неколичественная ветка N, аналитический уровень воздействия IV. Коды 1–4 и
          R/C/S/P в новых оценках не применяются.
        </p>
      </Card>
    </div>
  );
}

// ── Profile ───────────────────────────────────────────────────────────────────

function ProfileTab() {
  return (
    <div className="space-y-6">
      <Card>
        <h2 className="mb-1 text-lg font-medium">Краткий профиль должности</h2>
        <p className="text-sm text-muted leading-relaxed">
          Профиль определяет соотношение между тремя факторами. Он показывает ориентацию должности —
          на знания, на мышление или на результат. Определяется сравнением баллов Решения Вопросов (РВ)
          и Ответственности (ОТ).
        </p>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[
          {
            code: "P4",
            label: "Фундаментальные исследования",
            desc: "РВ значительно превышает ОТ. Должность ориентирована на глубокое исследование и знания.",
            color: "text-blue-400",
          },
          {
            code: "P3 / P2 / P1",
            label: "Прикладные исследования и разработка",
            desc: "РВ > ОТ. Акцент на аналитику, методологию, консультирование и экспертную поддержку.",
            color: "text-blue-300",
          },
          {
            code: "L",
            label: "Сбалансированный",
            desc: "РВ ≈ ОТ (разница ≤15%). Равновесие между мышлением и ответственностью за результат.",
            color: "text-muted",
          },
          {
            code: "A1 / A2 / A3 / A4",
            label: "Ориентация на результат",
            desc: "ОТ > РВ. Акцент на достижение конкретных показателей, управление, фронт.",
            color: "text-accent",
          },
        ].map((p) => (
          <Card key={p.code}>
            <div className={cn("num text-2xl font-medium", p.color)}>{p.code}</div>
            <div className="mt-2 text-sm font-medium">{p.label}</div>
            <p className="mt-1 text-xs text-muted leading-relaxed">{p.desc}</p>
          </Card>
        ))}
      </div>

      <Card>
        <h3 className="mb-3 text-sm font-medium text-muted uppercase tracking-wide">Логика расчёта профиля</h3>
        <div className="space-y-3 text-sm">
          <div className="flex items-start gap-3 rounded-lg border border-[rgb(var(--row-divider))] p-3">
            <span className="num mt-0.5 text-accent">1</span>
            <div>
              <div className="font-medium">Считаем три фактора</div>
              <p className="mt-0.5 text-muted">Know-How (абс.) + Problem Solving (% от KH) + Accountability (абс.) = Итого баллов</p>
            </div>
          </div>
          <div className="flex items-start gap-3 rounded-lg border border-[rgb(var(--row-divider))] p-3">
            <span className="num mt-0.5 text-accent">2</span>
            <div>
              <div className="font-medium">Определяем соотношение РВ и ОТ</div>
              <p className="mt-0.5 text-muted">Если РВ {'>'} ОТ — профиль P (исследовательский). Если ОТ {'>'} РВ — профиль A (результативный). L ставится при совпадении баллов; один 15%-шаг уже даёт P1 или A1.</p>
            </div>
          </div>
          <div className="flex items-start gap-3 rounded-lg border border-[rgb(var(--row-divider))] p-3">
            <span className="num mt-0.5 text-accent">3</span>
            <div>
              <div className="font-medium">Определяем грейд по матрице</div>
              <p className="mt-0.5 text-muted">Итоговые баллы переводятся в грейд (0–38) по листу Jobgrades предоставленного XLSM. Показываются нижняя, средняя и верхняя зоны диапазона.</p>
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <h3 className="mb-3 text-sm font-medium text-muted uppercase tracking-wide">Шкала грейдов (баллы → грейд)</h3>
        <div className="overflow-x-auto">
          <GradeTable />
        </div>
      </Card>
    </div>
  );
}

// ── Shared components ─────────────────────────────────────────────────────────

const COLOR_MAP = {
  blue: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  green: "bg-green-500/10 text-green-400 border-green-500/20",
  yellow: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
};

function DimCard({
  index, title, subtitle, color, levels,
}: {
  index: string;
  title: string;
  subtitle: string;
  color: keyof typeof COLOR_MAP;
  levels: { code: string; label: string; desc: string }[];
}) {
  return (
    <Card>
      <div className={cn("mb-3 inline-flex items-center gap-2 rounded-lg border px-2 py-1 text-xs font-medium", COLOR_MAP[color])}>
        <span className="num">{index}</span>
        <span>{subtitle}</span>
      </div>
      <div className="mb-3 text-sm font-medium">{title}</div>
      <ul className="space-y-2">
        {levels.map((l) => (
          <li key={l.code} className="flex items-start gap-2 text-xs">
            <span className="num mt-0.5 w-5 shrink-0 font-medium text-fg">{l.code}</span>
            <div>
              <span className="font-medium">{l.label}</span>
              <span className="ml-1 text-muted">— {l.desc}</span>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}

function KnowHowTable() {
  const cols = ["A", "B", "C", "D", "E", "F", "G", "H"];
  const mgmt = [
    { label: "T/1", vals: [43, 57, 76, 100, 132, 175, 230, 304] },
    { label: "T/2", vals: [50, 66, 87, 115, 152, 200, 264, 350] },
    { label: "T/3", vals: [57, 76, 100, 132, 175, 230, 304, 400] },
    { label: "I/1", vals: [57, 76, 100, 132, 175, 230, 304, 400] },
    { label: "I/2", vals: [66, 87, 115, 152, 200, 264, 350, 460] },
    { label: "I/3", vals: [76, 100, 132, 175, 230, 304, 400, 528] },
    { label: "II/1", vals: [76, 100, 132, 175, 230, 304, 400, 528] },
    { label: "II/2", vals: [87, 115, 152, 200, 264, 350, 460, 608] },
    { label: "II/3", vals: [100, 132, 175, 230, 304, 400, 528, 700] },
    { label: "III/1", vals: [100, 132, 175, 230, 304, 400, 528, 700] },
    { label: "III/2", vals: [115, 152, 200, 264, 350, 460, 608, 800] },
    { label: "III/3", vals: [132, 175, 230, 304, 400, 528, 700, 920] },
    { label: "IV/1", vals: [132, 175, 230, 304, 400, 528, 700, 920] },
    { label: "IV/2", vals: [152, 200, 264, 350, 460, 608, 800, 1056] },
    { label: "IV/3", vals: [175, 230, 304, 400, 528, 700, 920, 1216] },
  ];
  return (
    <table className="num w-full text-sm">
      <thead>
        <tr className="border-b border-[rgb(var(--row-divider))]">
          <th className="pb-3 pr-4 text-left text-muted">Упр / Ком</th>
          {cols.map((c) => (
            <th key={c} className="pb-3 px-3 text-center text-base font-semibold">{c}</th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-[rgb(var(--row-divider))]">
        {mgmt.map((row) => (
          <tr key={row.label} className="hover:bg-[rgb(var(--field-bg))] transition-colors">
            <td className="py-2.5 pr-4 font-semibold text-muted">{row.label}</td>
            {row.vals.map((v, i) => (
              <td key={i} className="py-2.5 px-3 text-center text-sm">{v}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function PSTable() {
  const cols = ["A", "B", "C", "D", "E", "F", "G", "H"];
  const rows = [
    { label: "1", vals: ["10%", "12%", "14%", "16%", "19%", "22%", "25%", "29%"] },
    { label: "2", vals: ["12%", "14%", "16%", "19%", "22%", "25%", "29%", "33%"] },
    { label: "3", vals: ["14%", "16%", "19%", "22%", "25%", "29%", "33%", "38%"] },
    { label: "4", vals: ["16%", "19%", "22%", "25%", "29%", "33%", "38%", "43%"] },
    { label: "5", vals: ["19%", "22%", "25%", "29%", "33%", "38%", "43%", "50%"] },
  ];
  return (
    <table className="num w-full text-sm">
      <thead>
        <tr className="border-b border-[rgb(var(--row-divider))]">
          <th className="pb-3 pr-4 text-left text-muted">Сложность \ Область</th>
          {cols.map((c) => (
            <th key={c} className="pb-3 px-4 text-center text-base font-semibold">{c}</th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-[rgb(var(--row-divider))]">
        {rows.map((row) => (
          <tr key={row.label} className="hover:bg-[rgb(var(--field-bg))] transition-colors">
            <td className="py-3 pr-4 font-semibold text-muted">{row.label}</td>
            {row.vals.map((v, i) => (
              <td key={i} className="py-3 px-4 text-center text-sm">{v}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function GradeTable() {
  const grades = [
    [0, 0, 14, 29], [1, 30, 34, 39], [2, 40, 43, 46], [3, 47, 50, 53],
    [4, 54, 58, 62], [5, 63, 67, 72], [6, 73, 78, 84], [7, 85, 91, 97],
    [8, 98, 105, 113], [9, 114, 124, 134], [10, 135, 147, 160], [11, 161, 176, 191],
    [12, 192, 209, 227], [13, 228, 248, 268], [14, 269, 291, 313], [15, 314, 342, 370],
    [16, 371, 404, 438], [17, 439, 478, 518], [18, 519, 566, 613], [19, 614, 674, 734],
    [20, 735, 807, 879], [21, 880, 967, 1055], [22, 1056, 1158, 1260], [23, 1261, 1384, 1507],
    [24, 1508, 1654, 1800], [25, 1801, 1970, 2140], [26, 2141, 2345, 2550],
    [27, 2551, 2785, 3020], [28, 3021, 3300, 3580], [29, 3581, 3915, 4250],
    [30, 4251, 4655, 5060], [31, 5061, 5540, 6020], [32, 6021, 6590, 7160],
    [33, 7161, 7740, 8320], [34, 8321, 8980, 9640], [35, 9641, 10410, 11180],
    [36, 11181, 12080, 12980], [37, 12981, 14030, 15080], [38, 15081, 16310, 17540],
  ];
  return (
    <div className="grid grid-cols-2 gap-2 text-sm md:grid-cols-3 lg:grid-cols-4">
      {grades.map(([grade, lower, mid, upper]) => (
        <div
          key={grade}
          className="rounded-lg border border-[rgb(var(--row-divider))] bg-[rgb(var(--field-bg))] px-3 py-3"
        >
          <div className="num text-lg font-semibold">Грейд {grade}</div>
          <div className="mt-2 grid grid-cols-3 gap-1 text-center text-[11px]">
            <span className="rounded bg-blue-500/15 px-1 py-1 text-blue-400">{lower} · синий</span>
            <span className="rounded bg-green-500/15 px-1 py-1 text-green-400">{mid} · зелёный</span>
            <span className="rounded bg-orange-500/15 px-1 py-1 text-orange-400">{upper} · оранжевый</span>
          </div>
        </div>
      ))}
    </div>
  );
}
