#!/usr/bin/env bash
set -euo pipefail
target=${1:-.cache/prompt.txt}
if [[ ! -f "$target" ]]; then echo "missing:$target"; exit 0; fi
if grep -Eqi '(api[_-]?key|secret|password|Bearer\s+[A-Za-z0-9._-]+)' "$target"; then
  echo "FAIL: potential secret detected in $target"
  exit 2
fi
echo "OK"

