#!/usr/bin/env python3
import json, pathlib, statistics

def load_jsonl(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    out=[]
    for line in p.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out

def main():
    calls = load_jsonl('logs/calls.jsonl')
    verifs = load_jsonl('logs/verify.jsonl')
    accept_rate = None
    if verifs:
        oks = sum(1 for r in verifs if r.get('ok'))
        accept_rate = round(oks/len(verifs), 3)
    providers = {}
    total_cost = 0.0
    for c in calls:
        key = c.get('provider')
        providers.setdefault(key, {'count':0,'latencies':[],'cost':0.0,'tokens_in':0,'tokens_out':0})
        providers[key]['count'] += 1
        if 'latency_ms' in c:
            providers[key]['latencies'].append(c['latency_ms'])
        providers[key]['cost'] += float(c.get('cost_usd', 0) or 0)
        providers[key]['tokens_in'] += int(c.get('tokens_in', 0) or 0)
        providers[key]['tokens_out'] += int(c.get('tokens_out', 0) or 0)
        total_cost += float(c.get('cost_usd', 0) or 0)
    print("# Lab Report\n")
    if accept_rate is not None:
        print(f"- Accept rate: {accept_rate}")
    if providers:
        print("- Provider usage, avg latency, est cost:")
        for k,v in providers.items():
            avg = round(statistics.mean(v['latencies']),1) if v['latencies'] else 0
            print(f"  - {k}: {v['count']} calls, avg {avg} ms, tokens in/out {v['tokens_in']}/{v['tokens_out']}, cost ${v['cost']:.6f}")
    print(f"\n- Total estimated cost: ${total_cost:.6f}")

if __name__ == '__main__':
    main()
