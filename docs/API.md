# API (FastAPI)

Base URL: `http://127.0.0.1:8000` · Интерактивная документация: `/docs` (Swagger UI).

Все тела запросов/ответов — JSON по Pydantic-моделям из `jeval/domain/`.

## Авторизация и tenant-контекст

Закрытые endpoints требуют session-cookie, CSRF-заголовок для изменяющих запросов
и tenant-контекст:

```http
Cookie: jeval_session=<session-token>
X-CSRF-Token: <csrf-token>
X-Company-ID: <company-uuid>
```

Исходный session-token возвращается только при регистрации/входе. В БД хранится
его SHA-256 хеш. `X-Company-ID` не является авторизацией: backend дополнительно
проверяет активную membership пользователя в этой компании.

### POST /api/auth/register

```json
{
  "display_name": "Айжан Эксперт",
  "email": "aizhan@company.kz",
  "password": "минимум 8 символов"
}
```

Ответ: `access_token`, `token_type: "cookie"`, `csrf_token`, безопасное
представление `user`, список `companies`.
Новый пользователь получает пустой список и должен создать первую компанию.
Сессия также выставляется в HttpOnly-cookie `jeval_session`.
CSRF-токен возвращается отдельным полем `csrf_token`.

### POST /api/auth/login

```json
{ "email": "aizhan@company.kz", "password": "..." }
```

Также выставляется HttpOnly-cookie `jeval_session`.
CSRF-токен возвращается отдельным полем `csrf_token`.

### GET /api/auth/me · POST /api/auth/logout

Проверка текущей сессии / отзыв текущего токена.

## Компании

### GET /api/companies

Список компаний, где у текущего пользователя есть активная membership.

### POST /api/companies

Создаёт компанию и membership `owner` в одной транзакции.

```json
{
  "name": "АО Компания",
  "purpose": "job-evaluation",
  "user_role": "hr-cb",
  "organization_size": "251-1000"
}
```

Для этих endpoints нужен `Cookie: jeval_session` и `X-CSRF-Token`, но
`X-Company-ID` ещё не требуется.

### POST /api/companies/{id}/activate

Проверяет membership при переключении компании и пишет событие в audit log.

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

Все операции выполняются только внутри `X-Company-ID`. UUID объекта соседней
компании также возвращает `404`, чтобы не раскрывать его существование.

### POST /api/positions/{id}/gate
Проверка Gate 0. Ответ — `GateResult`: `status` (`ready` / `needs_clarification` /
`cannot_evaluate`), `checks[]`, `missing_fields[]`, `warnings[]`.

### POST /api/import/document
Сохраняет файл в `uploads/` и возвращает `DossierImportResult`: `position`,
`raw_text`, `extracted_fields`, `missing_fields`, `notes`.
В `position.import_metadata` дополнительно сохраняются `source_filename`,
`source_type`, `source_mime_type`, `source_size_bytes`, `source_sha256` и
`field_sources`. Это provenance-карта: по ней на фронте и в ИИ-пайплайне видно,
откуда взят каждый факт.

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

## Публичные формы

`GET/POST /api/public/forms/{token}` не требуют авторизации. Компания определяется
по самой форме на сервере; клиент не может выбрать tenant для отправленной должности.

## Ошибки
Стандартный формат FastAPI: `{ "detail": "..." }` со статусами `404` / `422` /
`503` (нет ключа агента) / `502` (ошибка вызова агента). Дополнительно:

- `401` — сессия отсутствует или истекла;
- `400` — не передан `X-Company-ID`;
- `403` — пользователь не состоит в выбранной компании;
- `409` — email уже зарегистрирован или публичная форма уже заполнена.
