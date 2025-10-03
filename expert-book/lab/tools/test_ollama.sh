#!/usr/bin/env bash
set -euo pipefail
model=${1:-llama3.1:8b}
echo "[ollama] checking availability..."
if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama CLI not found. See https://ollama.ai for install." >&2
  exit 2
fi
echo "[ollama] pulling model: $model (if needed)"
ollama pull "$model" >/dev/null || true
echo "[ollama] running test prompt"
echo "Say 'hello from ollama' in one short line." | ollama run "$model" | head -n 3

