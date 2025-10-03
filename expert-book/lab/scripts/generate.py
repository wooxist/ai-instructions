#!/usr/bin/env python3
import sys, json, argparse, hashlib

def summarize(text: str, words: int = 12) -> str:
    tokens = text.split()
    if not tokens:
        return ""
    return " ".join(tokens[:words]) + ("…" if len(tokens) > words else "")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='dummy')
    p.add_argument('--in', dest='inp', default='-')
    args = p.parse_args()

    fh = sys.stdin if args.inp == '-' else open(args.inp, 'r', encoding='utf-8')
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = item.get('text', '')
        out = {
            "id": item.get('id'),
            "input_hash": hashlib.sha256(text.encode('utf-8')).hexdigest(),
            "summary": summarize(text),
            "confidence": 0.95 if text else 0.5,
            "model": args.model,
        }
        print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()

