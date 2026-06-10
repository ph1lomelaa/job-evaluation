# Платформа оценки должностей (Korn Ferry Hay Group)

ИИ-агент предварительной оценки должностей КЦ и ДЗО КМГ по методике
**Hay Group Guide Chart–Profile Method** (3 фактора: Знания и умения, Решение
вопросов, Ответственность). Агент готовит **предварительную** факторную оценку,
доказательства, QC-флаги и рекомендацию; итоговый грейд утверждает Оценочный комитет.

> Переписано с TypeScript на Python. Бэкенд — в [backend/](backend/), будущий UI —
> в [frontend/](frontend/) (см. [frontend/FIGMA_PROMPT.md](frontend/FIGMA_PROMPT.md)).

## Ключевой принцип

**LLM выбирает только уровни факторов, баллы и грейд считает код.**
Claude читает JE-досье и возвращает уровни (A–H, 1–5, P/S/C/R) + доказательства +
уверенность. Детерминированный движок ([backend/jeval/scoring](backend/jeval/scoring))
делает подстановку по таблицам Hay → баллы → грейд. Это требование методики
(«баллы только через разрешённые таблицы») и делает оценку воспроизводимой.

## Структура

```
backend/            Python-бэкенд (FastAPI + Pydantic + Anthropic SDK)
  jeval/
    domain/         модели и enum-ы (JE-досье, факторы, оценка)
    scoring/        движок: таблицы Hay, грейд-матрица, расчёт
    gate.py         Gate 0 — допуск к оценке («нет понимания — нет оценки»)
    qc.py           QC-флаги (раздел 9 инструкции)
    agent/          системный промпт + вызов Claude (structured tool-use)
    orchestrator.py досье → Gate 0 → агент → движок → QC → карточка
    store.py        persistence (SQLite / in-memory)
    api/            FastAPI-эндпоинты
  tests/            pytest (38 тестов)
  scripts/demo.py   сквозное демо без сети
frontend/           UI (React + TS + Tailwind): дашборд, форма+Gate 0, карточка, сравнение
docs/               архитектура и API
```

### Фронтенд

```bash
cd frontend
npm install
cp .env.example .env             # VITE_API_URL → адрес бэкенда
npm run dev                      # http://localhost:5173
```

Тёмная/светлая темы, glass-дизайн, акцент `#ff3d00`. Все экраны работают на реальном
API (дашборд, форма с Gate 0 и запуском оценки, карточка оценки, сравнение с якорями).
Подробности — в [frontend/README.md](frontend/README.md).

## Быстрый старт

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e .                 # ставит jeval + зависимости
cp .env.example .env             # добавьте ANTHROPIC_API_KEY для реального агента

python scripts/demo.py           # сквозное демо БЕЗ ключа (фейковый агент)
pytest -q                        # тесты
uvicorn jeval.api.main:app --reload   # API на http://127.0.0.1:8000/docs
```

## Конвейер оценки

1. **Gate 0** — проверка полноты JE-досье. Нет критических данных → оценка не
   проводится (`CANNOT_EVALUATE`).
2. **Агент** — Claude выбирает уровни факторов, доказательства, уверенность.
3. **Движок** — баллы по подстановочным таблицам → Total → профиль (A/P/L) → грейд.
4. **QC** — проверка персонализации, влияния оплаты, нелогичных связок, правил типа влияния.
5. **Карточка** — статус, факторная таблица, формула, профиль, QC-флаги, вопросы,
   рекомендация для Оценочного комитета.

## ⚠️ Точность таблиц

В [backend/jeval/scoring/tables.py](backend/jeval/scoring/tables.py) флаг
`TABLES_VERIFIED = False`. **Точны и сверены:** грейд-матрица (0–31) и матрица
Problem Solving %. **Предварительны:** таблицы Know-How и Accountability (собраны по
аддитивно-шаговой модели Hay) — их нужно сверить с официальным чартом Korn Ferry
перед боевым использованием. Замена = правка констант в одном файле.

## API (основное)

| Метод | Путь | Назначение |
|-------|------|-----------|
| POST | `/api/positions` | создать должность (JE-досье) |
| GET  | `/api/positions` · `/api/positions/{id}` | список / карточка |
| POST | `/api/positions/{id}/gate` | проверка Gate 0 |
| POST | `/api/evaluations` | запустить предварительную оценку |
| GET  | `/api/evaluations` · `/api/evaluations/{id}` | список (фильтр `?position_id=`) / оценка |

Без `ANTHROPIC_API_KEY` оценка работает в офлайн-режиме `JEVAL_FAKE_AGENT=1`
(уровни выбирает детерминированная заглушка — только для демо/разработки).

## Лицензия

MIT
