#!/bin/zsh
set -eu

ROOT="${0:A:h:h:h}"
BACKEND_LOG=/tmp/jeval-backend-visual.log
FRONTEND_LOG=/tmp/jeval-frontend-visual.log

cd "$ROOT/backend"
.venv/bin/uvicorn jeval.api.main:app --host 127.0.0.1 --port 8000 >"$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!

cd "$ROOT/frontend"
npm run dev -- --host 127.0.0.1 --port 5173 >"$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

for attempt in {1..30}; do
  if curl -fsS http://127.0.0.1:8000/health >/dev/null 2>&1 && curl -fsS http://127.0.0.1:5173/ >/dev/null 2>&1; then
    npm run verify:multi-company
    exit 0
  fi
  sleep 0.5
done

echo "Локальные сервисы не запустились" >&2
cat "$BACKEND_LOG" >&2
cat "$FRONTEND_LOG" >&2
exit 1
