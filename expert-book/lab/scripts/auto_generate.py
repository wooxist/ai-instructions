#!/usr/bin/env python3
import os, sys, json, argparse, hashlib, shutil, time, pathlib, random, re, subprocess as sp

def which(cmd):
    return shutil.which(cmd) is not None

def summarize_local(text: str, words: int = 16) -> str:
    toks = text.split()
    if not toks:
        return ""
    return " ".join(toks[:words]) + ("…" if len(toks) > words else "")

def log_call(provider: str, model: str, ok: bool, latency_ms: int, extra: dict):
    try:
        logdir = pathlib.Path('logs')
        logdir.mkdir(parents=True, exist_ok=True)
        rec = {
            'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'provider': provider,
            'model': model,
            'ok': ok,
            'latency_ms': latency_ms,
        }
        rec.update(extra or {})
        with open(logdir / 'calls.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass

def run_with_timeout(cmd: list, input_text: str, timeout_s: int):
    return sp.run(cmd, input=input_text, capture_output=True, text=True, timeout=timeout_s, check=True)

def backoff_sleep(attempt: int, base_ms: int, factor: float, max_ms: int):
    # exponential backoff with jitter
    delay = min(max_ms, int(base_ms * (factor ** attempt)))
    jitter = random.randint(0, max(1, int(delay * 0.25)))
    time.sleep((delay + jitter) / 1000.0)

def classify_error(stderr: str, exc: Exception) -> (str, str):
    s = (stderr or '').lower()
    if isinstance(exc, sp.TimeoutExpired):
        return 'timeout', 'command timed out'
    if 'invalid api key' in s or 'unauthorized' in s or '401' in s:
        return 'auth', 'authentication failed'
    if 'rate limit' in s or 'too many requests' in s or '429' in s:
        return 'rate_limit', 'rate limited'
    if 'not found' in s or 'no such model' in s:
        return 'not_found', 'model not found'
    if 'connection' in s or 'dns' in s or 'network' in s:
        return 'network', 'network error'
    return 'other', (stderr.strip()[:160] if stderr else 'unknown')

def call_ollama(text: str, model: str, timeout_s: int, retries: int, bo_base: int, bo_factor: float, bo_max: int, retry_policy: dict) -> (str, int, bool, str, str, int, int):
    prompt = f"Summarize the following text in one concise sentence. Output only the sentence.\n\n{text}"
    start = time.time()
    attempt = 0
    max_allowed = retries
    while True:
        try:
            res = run_with_timeout(['ollama','run',model], input_text=prompt, timeout_s=timeout_s)
            lat = int((time.time() - start) * 1000)
            out = res.stdout.strip().splitlines()
            return (out[0] if out else summarize_local(text), lat, True, '', '', 0, 0)
        except Exception as e:
            code, reason = classify_error(getattr(e, 'stderr', '') or '', e)
            max_allowed = max(max_allowed, retry_policy.get(code, retries))
            if attempt >= max_allowed:
                lat = int((time.time() - start) * 1000)
                return (summarize_local(text), lat, False, code, reason, 0, 0)
            backoff_sleep(attempt+1, bo_base, bo_factor, bo_max)
            attempt += 1

def call_openai(text: str, model: str, timeout_s: int, retries: int, bo_base: int, bo_factor: float, bo_max: int, retry_policy: dict) -> (str, int, bool, str, str, int, int):
    prompt = f"Summarize the following text in one concise sentence. Output only the sentence.\n\n{text}"
    start = time.time()
    attempt = 0
    max_allowed = retries
    while True:
        try:
            res = run_with_timeout(['openai','chat.completions.create','-m',model,'-g','user',prompt], input_text="", timeout_s=timeout_s)
            out = res.stdout.strip()
            # Try parsing JSON first
            try:
                data = json.loads(out)
                if isinstance(data, dict) and 'choices' in data and data['choices']:
                    content = data['choices'][0].get('message', {}).get('content')
                    if isinstance(content, str) and content.strip():
                        u = data.get('usage') or {}
                        pt = int(u.get('prompt_tokens') or 0)
                        ct = int(u.get('completion_tokens') or 0)
                        lat = int((time.time() - start) * 1000)
                        return (content.strip(), lat, True, '', '', pt, ct)
            except Exception:
                pass
            # Fallback: first non-empty line
            for line in out.splitlines():
                line=line.strip()
                if line:
                    lat = int((time.time() - start) * 1000)
                    return (line, lat, True, '', '', 0, 0)
        except Exception as e:
            code, reason = classify_error(getattr(e, 'stderr', '') or '', e)
            max_allowed = max(max_allowed, retry_policy.get(code, retries))
            if attempt >= max_allowed:
                lat = int((time.time() - start) * 1000)
                return (summarize_local(text), lat, False, code, reason, 0, 0)
            backoff_sleep(attempt+1, bo_base, bo_factor, bo_max)
            attempt += 1

def call_anthropic(text: str, model: str, timeout_s: int, retries: int, bo_base: int, bo_factor: float, bo_max: int) -> (str, int, bool, str, str):
    prompt = f"Summarize the following text in one concise sentence. Output only the sentence.\n\n{text}"
    start = time.time()
    for attempt in range(retries + 1):
        try:
            res = run_with_timeout(['anthropic','messages.create','-m',model,'-p',prompt], input_text="", timeout_s=timeout_s)
            out = res.stdout.strip()
            # Try parsing JSON first
            try:
                data = json.loads(out)
                if isinstance(data, dict) and 'content' in data and data['content']:
                    seg = data['content'][0]
                    if isinstance(seg, dict):
                        txt = seg.get('text') or seg.get('content') or ''
                        if isinstance(txt, str) and txt.strip():
                            lat = int((time.time() - start) * 1000)
                            return (txt.strip(), lat, True, '', '')
            except Exception:
                pass
            # Fallback: first non-empty line
            for line in out.splitlines():
                line=line.strip()
                if line:
                    lat = int((time.time() - start) * 1000)
                    return (line, lat, True, '', '')
        except Exception as e:
            if attempt >= retries:
                lat = int((time.time() - start) * 1000)
                code, reason = classify_error(getattr(e, 'stderr', '') or '', e)
                return (summarize_local(text), lat, False, code, reason)
            backoff_sleep(attempt+1, bo_base, bo_factor, bo_max)

def call_anthropic(text: str, model: str, timeout_s: int, retries: int, bo_base: int, bo_factor: float, bo_max: int, retry_policy: dict) -> (str, int, bool, str, str, int, int):
    prompt = f"Summarize the following text in one concise sentence. Output only the sentence.\n\n{text}"
    start = time.time()
    attempt = 0
    max_allowed = retries
    while True:
        try:
            res = run_with_timeout(['anthropic','messages.create','-m',model,'-p',prompt], input_text="", timeout_s=timeout_s)
            out = res.stdout.strip()
            try:
                data = json.loads(out)
                if isinstance(data, dict) and 'content' in data and data['content']:
                    seg = data['content'][0]
                    if isinstance(seg, dict):
                        txt = seg.get('text') or seg.get('content') or ''
                        if isinstance(txt, str) and txt.strip():
                            u = data.get('usage') or {}
                            pt = int(u.get('input_tokens') or 0)
                            ct = int(u.get('output_tokens') or 0)
                            lat = int((time.time() - start) * 1000)
                            return (txt.strip(), lat, True, '', '', pt, ct)
            except Exception:
                pass
            for line in out.splitlines():
                line=line.strip()
                if line:
                    lat = int((time.time() - start) * 1000)
                    return (line, lat, True, '', '', 0, 0)
        except Exception as e:
            code, reason = classify_error(getattr(e, 'stderr', '') or '', e)
            max_allowed = max(max_allowed, retry_policy.get(code, retries))
            if attempt >= max_allowed:
                lat = int((time.time() - start) * 1000)
                return (summarize_local(text), lat, False, code, reason, 0, 0)
            backoff_sleep(attempt+1, bo_base, bo_factor, bo_max)
            attempt += 1

def decide_route(text: str) -> str:
    n = len(text)
    has_openai = bool(os.environ.get('OPENAI_API_KEY')) and which('openai')
    has_anthropic = bool(os.environ.get('ANTHROPIC_API_KEY')) and which('anthropic')
    has_ollama = which('ollama')
    force = os.environ.get('ROUTE_FORCE','').strip().lower()
    if force in {'ollama','openai','anthropic','dummy'}:
        # respect force if provider available when applicable
        if force == 'ollama' and not has_ollama:
            return 'dummy'
        if force == 'openai' and not has_openai:
            return 'dummy'
        if force == 'anthropic' and not has_anthropic:
            return 'dummy'
        return force
    try:
        max_chars = int(os.environ.get('ROUTE_OLLAMA_MAX_CHARS','280'))
    except Exception:
        max_chars = 280
    order = [p.strip() for p in os.environ.get('ROUTE_ORDER','ollama,openai,anthropic').split(',') if p.strip()]
    availability = {
        'ollama': has_ollama and (n <= max_chars),
        'openai': has_openai,
        'anthropic': has_anthropic,
    }
    for provider in order:
        if availability.get(provider):
            return provider
    return 'dummy'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True, help='inputs jsonl')
    ap.add_argument('--ollama-model', default=os.environ.get('OLLAMA_MODEL','llama3.1:8b'))
    ap.add_argument('--openai-model', default=os.environ.get('MODEL','gpt-4o-mini'))
    ap.add_argument('--anthropic-model', default=os.environ.get('ANTHROPIC_MODEL','claude-3-5-sonnet-latest'))
    args = ap.parse_args()

    fh = sys.stdin if args.inp == '-' else open(args.inp, 'r', encoding='utf-8')
    timeout_s = int(os.environ.get('ROUTE_TIMEOUT_SECONDS','20'))
    retries = int(os.environ.get('ROUTE_RETRIES','1'))
    bo_base = int(os.environ.get('ROUTE_BACKOFF_BASE_MS','200'))
    bo_factor = float(os.environ.get('ROUTE_BACKOFF_FACTOR','2.0'))
    bo_max = int(os.environ.get('ROUTE_BACKOFF_MAX_MS','2000'))
    retry_policy = {
        'timeout': int(os.environ.get('RETRIES_TIMEOUT', retries)),
        'rate_limit': int(os.environ.get('RETRIES_RATE_LIMIT', retries)),
        'network': int(os.environ.get('RETRIES_NETWORK', retries)),
        'auth': int(os.environ.get('RETRIES_AUTH', 0)),
        'not_found': int(os.environ.get('RETRIES_NOT_FOUND', 0)),
        'other': int(os.environ.get('RETRIES_OTHER', retries)),
    }

    def detect_cjk(text: str) -> bool:
        return bool(re.search(r"[\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7A3]", text))

    def tokens_per_char(provider: str) -> float:
        # env override per provider, else global TOKENS_PER_CHAR, else heuristic
        prov_key = {
            'openai': 'OPENAI_TOKENS_PER_CHAR',
            'anthropic': 'ANTHROPIC_TOKENS_PER_CHAR',
            'ollama': 'OLLAMA_TOKENS_PER_CHAR',
            'dummy': 'DUMMY_TOKENS_PER_CHAR',
        }.get(provider, '')
        val = os.environ.get(prov_key) or os.environ.get('TOKENS_PER_CHAR')
        if val:
            try:
                return float(val)
            except Exception:
                pass
        # heuristic defaults
        return 0.5 if detect_cjk('sample 한글 テスト 中文') else 0.25

    def est_tokens(text: str, provider: str) -> int:
        # hybrid: chars-based + words-based
        tpc = tokens_per_char(provider)
        by_chars = len(text) * tpc
        words = re.findall(r"\w+", text)
        by_words = len(words) * 1.3
        est = int(max(1, round((by_chars + by_words) / 2)))
        return est

    def cost_per(provider: str, direction: str) -> float:
        # direction: 'in' or 'out'
        key_map = {
            ('openai','in'): 'OPENAI_INPUT_COST_PER_1K',
            ('openai','out'): 'OPENAI_OUTPUT_COST_PER_1K',
            ('anthropic','in'): 'ANTHROPIC_INPUT_COST_PER_1K',
            ('anthropic','out'): 'ANTHROPIC_OUTPUT_COST_PER_1K',
            ('ollama','in'): 'OLLAMA_COST_PER_1K',
            ('ollama','out'): 'OLLAMA_COST_PER_1K',
            ('dummy','in'): 'DUMMY_COST_PER_1K',
            ('dummy','out'): 'DUMMY_COST_PER_1K',
        }
        env_key = key_map.get((provider, direction), '')
        try:
            return float(os.environ.get(env_key, '0') or '0')
        except Exception:
            return 0.0

    def est_cost(provider: str, tok_in: int, tok_out: int) -> float:
        cin = cost_per(provider, 'in')
        cout = cost_per(provider, 'out')
        return round((tok_in/1000.0)*cin + (tok_out/1000.0)*cout, 6)
    for line in fh:
        line=line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        text = item.get('text','')
        rid = item.get('id')
        route = decide_route(text)
        if route == 'ollama':
            summary, lat, ok, ecode, ereason, ai_tin, ai_tout = call_ollama(text, args.ollama_model, timeout_s, retries, bo_base, bo_factor, bo_max, retry_policy)
            model = args.ollama_model
            conf = 0.9
            toks_in, toks_out = (ai_tin or est_tokens(text, 'ollama')), (ai_tout or est_tokens(summary, 'ollama'))
            cost = est_cost('ollama', toks_in, toks_out)
            log_call('ollama', model, ok, lat, {'id': rid, 'input_chars': len(text), 'output_chars': len(summary), 'tokens_in': toks_in, 'tokens_out': toks_out, 'cost_usd': cost, 'error_code': ecode, 'error_reason': ereason})
        elif route == 'openai':
            summary, lat, ok, ecode, ereason, ai_tin, ai_tout = call_openai(text, args.openai_model, timeout_s, retries, bo_base, bo_factor, bo_max, retry_policy)
            model = args.openai_model
            conf = 0.92
            toks_in, toks_out = (ai_tin or est_tokens(text, 'openai')), (ai_tout or est_tokens(summary, 'openai'))
            cost = est_cost('openai', toks_in, toks_out)
            log_call('openai', model, ok, lat, {'id': rid, 'input_chars': len(text), 'output_chars': len(summary), 'tokens_in': toks_in, 'tokens_out': toks_out, 'cost_usd': cost, 'error_code': ecode, 'error_reason': ereason})
        elif route == 'anthropic':
            summary, lat, ok, ecode, ereason, ai_tin, ai_tout = call_anthropic(text, args.anthropic_model, timeout_s, retries, bo_base, bo_factor, bo_max, retry_policy)
            model = args.anthropic_model
            conf = 0.92
            toks_in, toks_out = (ai_tin or est_tokens(text, 'anthropic')), (ai_tout or est_tokens(summary, 'anthropic'))
            cost = est_cost('anthropic', toks_in, toks_out)
            log_call('anthropic', model, ok, lat, {'id': rid, 'input_chars': len(text), 'output_chars': len(summary), 'tokens_in': toks_in, 'tokens_out': toks_out, 'cost_usd': cost, 'error_code': ecode, 'error_reason': ereason})
        else:
            summary = summarize_local(text)
            model = 'dummy'
            conf = 0.88
            toks_in, toks_out = est_tokens(text, 'dummy'), est_tokens(summary, 'dummy')
            cost = est_cost('dummy', toks_in, toks_out)
            log_call('dummy', model, True, 0, {'id': rid, 'input_chars': len(text), 'output_chars': len(summary), 'tokens_in': toks_in, 'tokens_out': toks_out, 'cost_usd': cost, 'error_code': '', 'error_reason': ''})
        out = {
            'id': rid,
            'input_hash': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'summary': summary,
            'confidence': conf,
            'model': model,
        }
        print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__':
    main()
