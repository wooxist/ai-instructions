#!/usr/bin/env python3
import sys, yaml, pathlib

def main():
    if len(sys.argv) < 3:
        print("Usage: prompt_compose.py <content.txt> <policy.yaml> [<policy2.yaml> ...]", file=sys.stderr)
        sys.exit(2)
    content_path = pathlib.Path(sys.argv[1])
    pol = {}
    for p in sys.argv[2:]:
        with open(p, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            pol.update(data)
    content = content_path.read_text(encoding='utf-8', errors='ignore')
    out = """[POLICY]
{policy}
[CONTENT]
{content}
""".format(policy=yaml.safe_dump(pol, allow_unicode=True), content=content)
    sys.stdout.write(out)

if __name__ == '__main__':
    main()

