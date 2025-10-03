#!/usr/bin/env bash
set -euo pipefail
echo "[anthropic] checking availability..."
if ! command -v anthropic >/dev/null 2>&1; then
  echo "anthropic CLI not found. Install via: pipx install anthropic" >&2
  exit 2
fi
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "ANTHROPIC_API_KEY not set. Export it or set in .env" >&2
  exit 3
fi
echo "[anthropic] listing models (truncated)"
anthropic models list 2>/dev/null | head -n 10 || echo "(models list may not be supported in your CLI version)"
echo "[anthropic] sample: create a short reply (dry-run guidance)"
echo "Run a message create like:\n  anthropic messages.create -m claude-3-5-sonnet-latest -p 'say hello in one line'"

