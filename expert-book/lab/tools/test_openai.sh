#!/usr/bin/env bash
set -euo pipefail
echo "[openai] checking availability..."
if ! command -v openai >/dev/null 2>&1; then
  echo "openai CLI not found. Install via: pipx install openai" >&2
  exit 2
fi
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY not set. Export it or set in .env" >&2
  exit 3
fi
echo "[openai] simple completion (short)"
openai chat.completions.create -m gpt-4o-mini -g user "reply 'hello from openai' in one short line" \
  | sed -n '1,40p'

