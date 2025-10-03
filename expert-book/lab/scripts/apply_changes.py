#!/usr/bin/env python3
import sys, json, pathlib

def main():
    if len(sys.argv) < 2:
        print("Usage: apply_changes.py <files...>", file=sys.stderr)
        sys.exit(2)
    outdir = pathlib.Path('data/applied')
    outdir.mkdir(parents=True, exist_ok=True)
    combined = []
    for arg in sys.argv[1:]:
        for p in pathlib.Path().glob(arg):
            try:
                obj = json.loads(p.read_text(encoding='utf-8'))
            except Exception:
                continue
            combined.append(obj)
    (outdir / 'applied.json').write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"applied: {len(combined)} items -> {outdir/'applied.json'}")

if __name__ == '__main__':
    main()

