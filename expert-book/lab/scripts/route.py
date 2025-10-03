#!/usr/bin/env python3
import sys, json, pathlib

def main():
    if len(sys.argv) < 2:
        print("Usage: route.py <verify.jsonl>", file=sys.stderr)
        sys.exit(2)
    p = pathlib.Path(sys.argv[1])
    ok = 0
    total = 0
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get('ok'):
            ok += 1
    rate = (ok / total) if total else 0.0
    print(json.dumps({"accept_rate": rate, "ok": ok, "total": total}))

if __name__ == '__main__':
    main()

