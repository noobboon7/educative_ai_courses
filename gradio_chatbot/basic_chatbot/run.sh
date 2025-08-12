#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$ROOT_DIR")"
VENV_BIN="$PROJECT_DIR/.venv_chatbot/bin"

if [[ ! -x "$VENV_BIN/python" ]]; then
  echo "Virtualenv not found at $VENV_BIN. Please create it first." >&2
  exit 1
fi

exec "$VENV_BIN/python" "$ROOT_DIR/app.py"

