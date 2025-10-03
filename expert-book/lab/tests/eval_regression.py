#!/usr/bin/env python3
import sys, json, statistics, pathlib

def load_jsonl(path):
    for line in pathlib.Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except Exception:
            continue

def main():
    if len(sys.argv) < 2:
        print("Usage: eval_regression.py <generate.jsonl>", file=sys.stderr)
        sys.exit(2)
    data = list(load_jsonl(sys.argv[1]))
    n = len(data)
    confs = [d.get('confidence', 0) for d in data]
    mean_conf = round(statistics.mean(confs), 3) if confs else 0
    print(json.dumps({"count": n, "mean_confidence": mean_conf}, ensure_ascii=False))

if __name__ == '__main__':
    main()

