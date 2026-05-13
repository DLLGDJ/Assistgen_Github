#!/usr/bin/env sh
set -eu

DB_PATH="${ASSISTGEN_DB_PATH:-/app/data/assistgen.sqlite3}"
DB_DIR=$(dirname "$DB_PATH")
mkdir -p "$DB_DIR"

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8100

