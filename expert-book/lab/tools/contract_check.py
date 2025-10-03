#!/usr/bin/env python3
import sys, json

SCHEMA = {
    'required': ['verdict', 'checks']
}

def main():
    try:
        obj = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({'ok': False, 'error': f'json:{e}'}))
        sys.exit(1)
    missing = [k for k in SCHEMA['required'] if k not in obj]
    ok = len(missing) == 0
    print(json.dumps({'ok': ok, 'missing': missing}))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()

