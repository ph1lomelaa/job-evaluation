FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*
# fonts-dejavu-core: кириллица для PDF-экспорта (jeval/export/pdf.py) —
# встроенные шрифты ReportLab (Helvetica/Times) не содержат кириллических глифов.

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY pyproject.toml ./
COPY jeval ./jeval

RUN useradd -m -u 10001 appuser \
    && mkdir -p /app/uploads \
    && chown -R appuser:appuser /app
# Каталог должен существовать и принадлежать appuser ДО монтирования тома
# backend_uploads:/app/uploads (docker-compose.yml) — иначе Docker создаёт
# точку монтирования от root при первом старте, и appuser не может туда
# писать (PermissionError при загрузке документов).

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

CMD ["uvicorn", "jeval.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
