#!/usr/bin/env python3
import sys, json, argparse

def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate(obj, schema):
    # Minimal validator for required keys and simple types
    required = schema.get('required', [])
    props = schema.get('properties', {})
    for k in required:
        if k not in obj:
            return False, f"missing:{k}"
    # type checks (string/number only)
    for k, spec in props.items():
        if k in obj and 'type' in spec:
            t = spec['type']
            v = obj[k]
            if t == 'string' and not isinstance(v, str):
                return False, f"type:{k}:expected string"
            if t in ('number','integer') and not isinstance(v, (int,float)):
                return False, f"type:{k}:expected number"
    # range checks (confidence between 0 and 1 if present)
    if 'confidence' in obj:
        try:
            c = float(obj['confidence'])
            if not (0.0 <= c <= 1.0):
                return False, "range:confidence"
        except Exception:
            return False, "type:confidence"
    return True, "ok"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--schema', required=True)
    ap.add_argument('--input', default='-')
    args = ap.parse_args()

    schema = load_schema(args.schema)
    fh = sys.stdin if args.input == '-' else open(args.input, 'r', encoding='utf-8')
    for i, line in enumerate(fh, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"json:{i}:{e}"}))
            continue
        ok, msg = validate(obj, schema)
        out = {"ok": ok, "id": obj.get('id'), "error": None if ok else msg}
        print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__':
    main()

