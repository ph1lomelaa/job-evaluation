# Промпт для Figma AI (Make Designs / First Draft)

Этот файл — готовый промпт для генерации UI платформы предварительной оценки
должностей по методике Korn Ferry Hay Group. Вставь блок «MASTER PROMPT» в
Figma AI (Figma Make / «First Draft»), затем при необходимости уточняй экраны
блоками ниже.

> Продукт русскоязычный (КМГ / Самрук-Қазына). Промпт на английском — Figma AI
> лучше понимает английский, — но вся UI-копия задана на русском.

---

## MASTER PROMPT

```
Design a professional enterprise web application called "Платформа оценки должностей"
(Job Evaluation Platform) for an HR department and an Evaluation Committee of a large
oil & gas holding (KMG / Samruk-Kazyna). It is an internal analytics tool, not a public
site. The AI assistant prepares a preliminary job evaluation using the Korn Ferry Hay
Group method (3 factors: Know-How, Problem Solving, Accountability); a human committee
approves the final grade.

AUDIENCE & TONE: corporate, trustworthy, data-dense but calm. Desktop-first (1440px),
responsive down to 1024px. All UI copy in Russian.

DESIGN SYSTEM:

- Style: clean corporate SaaS, generous whitespace, subtle shadows, 8px grid.
- Primary color: deep corporate blue #16387A (Hay Group blue), accent #2D7FF9,
  success #1E9E6A, warning #E5A400, danger #D64545, neutral grays #F5F7FA / #E3E8EF /
  #5B6B82 / #1B2430.
- Typography: Inter (or system sans). Headings semibold, body regular, tabular numbers
  for points/grades.
- Components: left sidebar navigation, top bar with breadcrumb + user menu, cards,
  data tables, status chips, progress steppers, side drawers, modals, toasts.
- Status chips: Черновик (gray), Готово к оценке (blue), Оценивается (amber, animated),
  Оценено (green), На комитете (purple), Утверждено (dark green).
- Confidence badges: высокая (green), средняя (amber), низкая (red).


SCREENS TO GENERATE (multi-screen flow):
1. Дашборд — table of positions: name, ДЗО, function, status chip, grade, confidence,
   updated date; filters (ДЗО, статус, грейд), search, "+ Новая должность" button; KPI
   cards on top (всего должностей, ожидают комитета, средний грейд, низкая уверенность).
2. Создание/редактирование должности (JE-досье) — long multi-section form in a stepper:
   Идентификация, Цель и результаты, Полномочия, Масштаб, Стейкхолдеры, Контекст,
   Якорные роли, Документы. Right rail shows live "Gate 0" completeness checklist
   (PASS / PARTIAL / FAIL per block).
3. Карточка оценки (главный экран результата) — see detailed prompt below.
4. Сравнение с якорными должностями (калибровка) — side-by-side columns of 2–3 roles
   with factor codes, points, grade, profile; highlight differences.

Generate screens 1–3 in full, with realistic Russian sample data.
```

---

## Экран 3 — «Карточка оценки» (детальный промпт)

```
Design the "Карточка оценки должности" screen — the core output. Layout:

HEADER: position title, ДЗО / подразделение, дата среза, large status chip and a
confidence badge. Right side: actions "На Оценочный комитет", "Вернуть на доработку",
"Скачать PDF".

SUMMARY STRIP (cards): Итоговый балл (large tabular number), Грейд (big pill, e.g. "14"),
Профиль (A / P / L with a small bar), Уверенность.

SECTION "Факторная оценка" — a table with rows grouped by factor:
  Знания и умения (Know-How): Специальные знания, Управленческие знания, Коммуникации
  Решение вопросов (Problem Solving): Область, Сложность
  Ответственность (Accountability): Свобода действий, Величина воздействия, Тип влияния
Columns: Подфактор | Уровень (chip, e.g. "E", "III", "2") | Баллы | Уверенность |
Доказательства (2–3 bullet facts) | Флаги. Expandable rows reveal full evidence text.

SECTION "Итоговая формула": visual equation
  Know-How [E/III/2] = 264   +   Problem Solving [E/4 · 43%] = 115   +
  Accountability [E/3/S] = 175   =   Итого 554   →   Грейд 14   ·   Профиль A (2 шага).

SECTION "QC-флаги": list with PASS/WARN/FAIL icons, e.g.
  "P без KPI и ресурсов — FAIL", "Коммуникации 3 без кейсов сопротивления — WARN".
Each flag: severity icon, message, recommendation, status pill.

SECTION "Обоснование (1 страница)": readable prose block — why each factor level was
chosen, anchor comparison, risks, data to confirm.

SECTION "Вопросы на уточнение": numbered list of clarifying questions for HR/manager.

FOOTER recommendation banner: "Рекомендация для Оценочного комитета" with the chosen
action highlighted (Рассмотреть на комитете / Вернуть досье / Провести интервью /
Калибровка с якорями).

Use realistic Russian content for a role like "Начальник управления ТОиР актива",
total 554, grade 14, profile A.
```

---

## Экран 2 — «Gate 0 / проверка полноты» (детальный промпт)

```
On the position form, design a right-side sticky panel "Готовность к оценке (Gate 0)".
It shows a checklist of required blocks, each with a status: PASS (green check),
PARTIAL (amber), FAIL (red). Items: Цель должности, Ключевые результаты, Описание
функций, Оргструктура, Полномочия, Масштаб, KPI/показатели, Решения «сам/согласует»,
Стейкхолдеры, Якорные должности. At the bottom a verdict banner:
  - green "Готово к оценке"
  - amber "Требуются уточнения"
  - red "Оценка невозможна без данных" (with the rule «нет понимания — нет оценки»).
Plus a primary button "Запустить предварительную оценку" (disabled while FAIL).
```

---

## Подсказки по доработке

- «Make it denser / more spacious» — регулировать плотность таблиц.
- «Add a dark sidebar variant» — если нужен тёмный левый навбар в корпоративном синем.
- «Generate empty states» — пустой дашборд, ошибка загрузки, нет результатов фильтра.
- «Mobile 390px» — узкие версии дашборда и карточки оценки.

## Карта экранов → API (для разработки UI)

| Экран                     | Эндпоинт бэкенда (FastAPI)        |
|---------------------------|-----------------------------------|
| Дашборд                   | `GET /api/positions`              |
| Создание должности        | `POST /api/positions`             |
| Gate 0 / проверка         | `POST /api/positions/{id}/gate`   |
| Запуск оценки             | `POST /api/evaluations`           |
| Карточка оценки           | `GET /api/evaluations/{id}`       |
