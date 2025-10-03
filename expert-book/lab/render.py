#!/usr/bin/env python3
import sys, yaml, re

def render(template: str, vars: dict) -> str:
    out = template
    for k, v in vars.items():
        out = re.sub(r"\{\{\s*" + re.escape(k) + r"\s*\}\}", str(v), out)
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: render.py <spec.yaml>", file=sys.stderr)
        sys.exit(2)
    spec = yaml.safe_load(open(sys.argv[1], 'r', encoding='utf-8'))
    template = spec.get('template', '')
    vars = spec.get('vars', {})
    print(render(template, vars))

if __name__ == '__main__':
    main()

