#!/usr/bin/env python3
import sys, pathlib, json, re

def heuristics(text: str):
    lines = text.splitlines()
    reasons = []
    # Basic length
    if len(lines) < 3:
        reasons.append("too_few_lines")
    # Headings
    has_heading = any(re.match(r"^#{1,6} ", l) for l in lines)
    if not has_heading:
        reasons.append("no_heading")
    # Bullets
    has_bullets = any(re.match(r"^\s*[-*] ", l) for l in lines)
    if not has_bullets:
        reasons.append("no_bullets")
    # Code fences
    has_code = text.count("```") >= 2
    if not has_code:
        reasons.append("no_code_fence")
    # Structured hint (json-like)
    has_struct = bool(re.search(r"\{\s*\"[A-Za-z0-9_]+\"\s*:\s*", text))
    if not has_struct:
        reasons.append("no_structured_snippet")
    ok = len(reasons) <= 2  # allow up to 2 misses to pass
    return ok, reasons

def main():
    if len(sys.argv) < 2:
        print("Usage: structure_check.py <path> [--json]", file=sys.stderr)
        sys.exit(2)
    json_mode = '--json' in sys.argv
    target = next((a for a in sys.argv[1:] if not a.startswith('-')), None)
    p = pathlib.Path(target) if target else None
    txt = p.read_text(encoding='utf-8', errors='ignore') if (p and p.exists()) else ''
    ok, reasons = heuristics(txt)
    if json_mode:
        print(json.dumps({"ok": ok, "reasons": reasons}))
    else:
        print('OK' if ok else f'FAIL: {",".join(reasons)}')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()

