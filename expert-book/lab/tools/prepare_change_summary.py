#!/usr/bin/env python3
import json, pathlib, sys

def main():
    src = pathlib.Path('.cache/last.out')
    if not src.exists():
        print("no last output; run workflow first", file=sys.stderr)
        sys.exit(1)
    summaries = []
    for line in src.read_text(encoding='utf-8').splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue
        summaries.append(f"- {obj.get('id')}: {obj.get('summary','')}")
    report = "\n".join([
        "# Change Summary",
        "",
        "## Items",
        *summaries,
        "",
        "## Risk",
        "- Low (dummy pipeline)",
    ])
    out = pathlib.Path('.cache/change_summary.md')
    out.write_text(report, encoding='utf-8')
    print(out)

if __name__ == '__main__':
    main()

