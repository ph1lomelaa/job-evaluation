# Схема данных платформы Hay Eval

## Модель владения

Единица изоляции данных — `company`. Пользователь не копируется при создании
новой компании: доступ задаёт отдельная membership.

```text
User 1 ── N Membership N ── 1 Company
Company 1 ── N Position 1 ── N Evaluation
Company 1 ── N PublicForm
Company 1 ── N AuditEvent
User 1 ── N Session
```

## Таблицы

### `users`

| Поле | Ограничение | Назначение |
|---|---|---|
| `id` | PK, UUID | глобальный идентификатор пользователя |
| `email` | UNIQUE, NOT NULL | нормализованный email (`casefold`) |
| `display_name` | NOT NULL | имя в интерфейсе |
| `password_hash` | NOT NULL | PBKDF2-SHA256, соль и число итераций |
| `created_at` | NOT NULL | регистрация |
| `last_login_at` | nullable | последний успешный вход |

### `companies`

| Поле | Ограничение | Назначение |
|---|---|---|
| `id` | PK, UUID | tenant key |
| `name` | NOT NULL | отображаемое название |
| `slug` | UNIQUE, NOT NULL | стабильный URL-safe идентификатор |
| `created_by_user_id` | FK users | создатель |
| `onboarding_purpose` | nullable | цель использования |
| `onboarding_role` | nullable | роль создателя в процессе оценки |
| `organization_size` | nullable | сегмент размера |
| `created_at`, `updated_at` | NOT NULL | аудит времени |

### `company_memberships`

Составной PK `(company_id, user_id)` запрещает повторное участие. Роли:
`owner`, `admin`, `evaluator`, `viewer`; статусы: `active`, `invited`, `disabled`.
Индекс `(user_id, status)` обслуживает меню переключения компаний.

### `sessions`

`token_hash` — PK. Исходный bearer-токен не сохраняется. Дополнительно хранятся
`user_id`, `created_at`, `expires_at`, `last_used_at`. Отзыв logout удаляет строку.

### `positions`

Реляционные колонки: `id`, `company_id`, `created_by_user_id`, `name`,
`department`, `function_name`, `review_status`, `updated_at`. `doc` содержит полный
Pydantic JSON `JobDossier`. Основные индексы:

- `(company_id, updated_at DESC)` — список должностей;
- `(company_id, review_status)` — фильтры дашборда.

### `evaluations`

Реляционные колонки: `id`, `company_id`, `position_id`, `created_by_user_id`,
`status`, `grade`, `total_points`, `created_at`. `doc` содержит полную карточку.
Индекс `(company_id, position_id, created_at DESC)` быстро находит актуальную
оценку должности.

### `public_forms`

Хранит `company_id`, token, статус, срок действия и связанную позицию. Публичный
submit определяет tenant только по записи формы. Уникальный индекс token исключает
коллизии ссылок.

### `audit_events`

Append-only журнал значимых действий: actor, tenant, action, тип/ID сущности,
метаданные и время. Пароли, session-токены и содержимое досье в metadata не пишутся.

## Транзакции

- Создание компании и owner-membership выполняется одной транзакцией.
- Первый tenant в мигрированной однопользовательской БД забирает только строки с
  `company_id IS NULL`.
- Upsert должности/оценки обновляет реляционные проекции и JSON одним commit.
- Отправка публичной формы сейчас состоит из двух последовательных upsert; для
  PostgreSQL adapter их следует объединить в одну транзакцию store-уровня.

## Масштабирование

SQLite с WAL подходит для локального запуска, демо и одного backend-инстанса.
Production-вариант:

1. PostgreSQL 16+ и connection pool.
2. Те же PK/FK/unique/index ограничения.
3. Опциональный PostgreSQL RLS по `company_id` как второй барьер после API.
4. S3-compatible object storage для документов с ключом
   `companies/{company_id}/positions/{position_id}/...`.
5. Фоновая очередь для LLM-оценок и импорта больших документов.
6. Retention-политика для sessions/audit и регулярные point-in-time backup.
