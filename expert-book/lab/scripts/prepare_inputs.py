#!/usr/bin/env python3
import sys, os, json, pathlib

def main():
    if len(sys.argv) < 2:
        print("Usage: prepare_inputs.py <input_dir>", file=sys.stderr)
        sys.exit(2)
    in_dir = pathlib.Path(sys.argv[1])
    if not in_dir.exists():
        print(f"Input dir not found: {in_dir}", file=sys.stderr)
        sys.exit(1)
    for path in sorted(in_dir.glob('*')):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            text = f"<read_error:{e}>"
        rec = {"id": path.stem, "path": str(path), "text": text.strip()}
        print(json.dumps(rec, ensure_ascii=False))

if __name__ == "__main__":
    main()

