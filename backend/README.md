# backend — jeval

Python-бэкенд платформы оценки должностей по методике Korn Ferry Hay Group.

## Установка и запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # пакет jeval + dev-зависимости
cp .env.example .env             # ANTHROPIC_API_KEY нужен только для реального агента

python scripts/demo.py           # сквозное демо без сети
pytest -q                        # тесты (38)
uvicorn jeval.api.main:app --reload
```

## Архитектура

| Модуль | Ответственность |
|--------|-----------------|
| `jeval/domain` | Pydantic-модели: identity, компании, JE-досье и оценка |
| `jeval/scoring` | Детерминированный расчёт: таблицы Hay, грейд-матрица, профиль |
| `jeval/gate.py` | Gate 0 — допуск к оценке |
| `jeval/agent` | Системный промпт + вызов Claude (structured tool-use) |
| `jeval/qc.py` | QC-флаги (раздел 9 инструкции) |
| `jeval/orchestrator.py` | Сборка всего конвейера в одну `Evaluation` |
| `jeval/security.py` | PBKDF2-пароли и хеширование session-токенов |
| `jeval/store.py` | Реляционное multi-tenant хранилище (SQLite / in-memory) |
| `jeval/api` | FastAPI-эндпоинты |

**Граница LLM / детерминизма:** агент (`jeval/agent`) выбирает только уровни
факторов; все баллы и грейд считает `jeval/scoring`. Тесты движка не требуют сети.

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|-----------|
| `ANTHROPIC_API_KEY` | — | ключ Claude (нужен для реального агента) |
| `JEVAL_MODEL` | `claude-opus-4-8` | модель агента |
| `JEVAL_DB_URL` | `sqlite:///./jeval.db` | хранилище |
| `JEVAL_AUTH_REQUIRED` | `true` | обязательная авторизация закрытых endpoints |
| `JEVAL_SESSION_DAYS` | `30` | срок жизни серверной сессии |
| `JEVAL_HOST` / `JEVAL_PORT` | `127.0.0.1` / `8000` | адрес сервиса |
|' 

## Тесты

```bash
pytest -q                  # всё
pytest tests/test_engine.py tests/test_grades.py   # только движок (без сети)
```
