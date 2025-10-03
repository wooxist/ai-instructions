#!/usr/bin/env python3
import sys, pathlib

HINT = "\n\n[FORMAT]\n- Reply with a single-line JSON only. No prose.\n- Fields: id:string, summary:string, confidence:number(0..1)\n"

def main():
    if len(sys.argv) < 2:
        print("Usage: rewrite_prompt.py <prompt.txt>", file=sys.stderr)
        sys.exit(2)
    p = pathlib.Path(sys.argv[1])
    text = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''
    # naive rewrite: append stricter formatting hint
    if '[FORMAT]' in text:
        sys.stdout.write(text)
    else:
        sys.stdout.write(text.strip() + HINT)

if __name__ == '__main__':
    main()

