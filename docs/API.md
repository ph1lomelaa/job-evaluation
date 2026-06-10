# API (FastAPI)

Base URL: `http://127.0.0.1:8000` · Интерактивная документация: `/docs` (Swagger UI).

Все тела запросов/ответов — JSON по Pydantic-моделям из `jeval/domain/models.py`.

## Должности

### POST /api/positions
Создать должность (JE-досье). Минимум — `name`; для прохождения Gate 0 нужны
критические блоки (см. ниже). `id` генерируется, если не передан.

```json
{
  "name": "Начальник управления ТОиР актива",
  "dzo": "ДЗО Добыча",
  "purpose": "Обеспечивать надёжность и готовность оборудования актива.",
  "key_results": ["План ТОиР выполнен", "Аварийность снижена"],
  "responsibilities": ["Планирование ТОиР", "Управление подрядчиками"],
  "kpis": ["Коэффициент готовности", "LTIFR"],
  "authorities": { "decides_alone": ["Оперативные решения по ремонту"] },
  "scope": { "annual_opex": 4000000000, "headcount": 120 },
  "organizational_context": "Операторская модель, CAPEX утверждает комитет."
}
```

### GET /api/positions · GET /api/positions/{id}
Список / одна должность (`404`, если не найдена).

### POST /api/positions/{id}/gate
Проверка Gate 0. Ответ — `GateResult`: `status` (`ready` / `needs_clarification` /
`cannot_evaluate`), `checks[]`, `missing_fields[]`, `warnings[]`.

## Оценка

### POST /api/evaluations
Запустить предварительную оценку.

```json
{ "position_id": "uuid" }
```

Ответ — `Evaluation`: `status`, `gate`, `selections` (уровни факторов), `score`
(`know_how`/`problem_solving`/`accountability`/`total_points`/`profile`/`grade`),
`qc_flags[]`, `confidence`, `reasoning`, `clarifying_questions[]`, `recommendation`.

Если Gate 0 не пройден (`cannot_evaluate`), агент не вызывается: `score` и
`selections` будут `null`, а в `clarifying_questions` — список недостающих данных.

### GET /api/evaluations/{id}
Получить ранее сохранённую оценку (`404`, если не найдена).

### GET /api/evaluations?position_id={id}
Список оценок; `position_id` — необязательный фильтр. Фронтенд берёт последнюю
по `created_at` как актуальную оценку должности.

## Агент
Для реального вызова Claude нужен `ANTHROPIC_API_KEY` в `backend/.env`.
Без ключа: `JEVAL_FAKE_AGENT=1` включает офлайн-заглушку (уровни фиксированы,
карточка помечается «офлайн-режим»); иначе `POST /api/evaluations` вернёт `503`.

## Ошибки
Стандартный формат FastAPI: `{ "detail": "..." }` со статусами `404` / `422` /
`503` (нет ключа агента) / `502` (ошибка вызова агента).
