#!/usr/bin/env python3
import json, pathlib, sys

def main():
    metric_path = pathlib.Path('.cache/metrics.json')
    if not metric_path.exists():
        print("missing .cache/metrics.json; run eval first", file=sys.stderr)
        sys.exit(2)
    cur = json.loads(metric_path.read_text(encoding='utf-8'))
    basep = pathlib.Path('baselines/metrics.json')
    base = json.loads(basep.read_text(encoding='utf-8')) if basep.exists() else None
    ok = (base is None) or (cur.get('mean_confidence', 0) >= (base.get('mean_confidence', 0) - 0.02))
    print(json.dumps({'ok': ok, 'current': cur, 'baseline': base}, ensure_ascii=False))
    if ok:
        basep.parent.mkdir(parents=True, exist_ok=True)
        basep.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()

