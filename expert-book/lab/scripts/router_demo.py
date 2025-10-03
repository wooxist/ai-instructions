#!/usr/bin/env python3
import os, sys, json, shutil

def which(cmd):
    return shutil.which(cmd) is not None

def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    text = text.strip() or "Summarize this short text."
    n = len(text)
    has_openai = bool(os.environ.get('OPENAI_API_KEY')) and which('openai')
    has_anthropic = bool(os.environ.get('ANTHROPIC_API_KEY')) and which('anthropic')
    has_ollama = which('ollama')

    choice = 'local-dummy'
    reason = 'fallback: no providers available'
    if n <= 280 and has_ollama:
        choice, reason = 'ollama', 'short input, low-risk → local model'
    elif has_openai:
        choice, reason = 'openai', 'default cloud route'
    elif has_anthropic:
        choice, reason = 'anthropic', 'openai unavailable → anthropic'

    out = {
        'input_chars': n,
        'choice': choice,
        'reason': reason,
        'available': {
            'ollama': has_ollama,
            'openai': has_openai,
            'anthropic': has_anthropic,
        }
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

