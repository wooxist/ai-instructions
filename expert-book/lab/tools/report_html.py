#!/usr/bin/env python3
import json, pathlib, statistics, sys, html

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
    gens = load_jsonl('logs/generate.jsonl')
    id_to_summary = {g.get('id'): g.get('summary','') for g in gens if isinstance(g, dict)}
    accept_rate = None
    if verifs:
        oks = sum(1 for r in verifs if r.get('ok'))
        accept_rate = round(oks/len(verifs), 3)
    providers = {}
    total_cost = 0.0
    for c in calls:
        key = c.get('provider')
        providers.setdefault(key, {'count':0,'latencies':[],'cost':0.0})
        providers[key]['count'] += 1
        if 'latency_ms' in c:
            providers[key]['latencies'].append(c['latency_ms'])
        providers[key]['cost'] += float(c.get('cost_usd', 0) or 0)
        total_cost += float(c.get('cost_usd', 0) or 0)
    # Error distribution
    err_counts = {}
    for c in calls:
        if not c.get('ok'):
            code = c.get('error_code') or 'unknown'
            err_counts[code] = err_counts.get(code, 0) + 1
    max_err = max(err_counts.values()) if err_counts else 0
    rows = []
    for k,v in providers.items():
        avg = round(statistics.mean(v['latencies']),1) if v['latencies'] else 0
        rows.append(f"<tr><td>{html.escape(k)}</td><td>{v['count']}</td><td>{avg} ms</td><td>${v['cost']:.6f}</td></tr>")
    # Recent N calls detail
    try:
        recent_n = int(os.environ.get('REPORT_RECENT_N','20'))
    except Exception:
        recent_n = 20
    recent = calls[-recent_n:]
    recent_rows = []
    for c in recent:
        ts = html.escape(str(c.get('ts','')))
        prov = html.escape(str(c.get('provider','')))
        rid = html.escape(str(c.get('id','')))
        ok = '✅' if c.get('ok') else '❌'
        lat = str(c.get('latency_ms',''))
        cost = f"${float(c.get('cost_usd',0) or 0):.6f}"
        t_in = str(c.get('tokens_in',''))
        t_out = str(c.get('tokens_out',''))
        err = html.escape(str(c.get('error_code','') or ''))
        reason = html.escape(str(c.get('error_reason','') or ''))
        summ = html.escape((id_to_summary.get(c.get('id')) or '')[:120])
        recent_rows.append(f"<tr><td>{ts}</td><td>{prov}</td><td>{rid}</td><td>{ok}</td><td>{lat}</td><td>{t_in}/{t_out}</td><td>{cost}</td><td>{err}</td><td title='{reason}'>{reason[:40]}</td><td title='{summ}'>{summ}</td></tr>")
    body = f"""
<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>Lab Report</title>
<style>body{{font-family:system-ui,sans-serif;margin:24px}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:6px 10px}}</style>
</head><body>
<h1>Lab Report</h1>
<ul>
  <li>Accept rate: {accept_rate if accept_rate is not None else 'N/A'}</li>
  <li>Total estimated cost: ${total_cost:.6f}</li>
</ul>
<h2>Provider usage</h2>
<table><thead><tr><th>Provider</th><th>Calls</th><th>Avg Latency</th><th>Est Cost</th></tr></thead>
<tbody>
{''.join(rows) if rows else '<tr><td colspan=4>No data</td></tr>'}
</tbody></table>

<h2>Recent Calls</h2>
<table><thead><tr><th>TS</th><th>Provider</th><th>ID</th><th>OK</th><th>Latency</th><th>Tok in/out</th><th>Cost</th><th>Error</th><th>Reason</th><th>Summary</th></tr></thead>
<tbody>
{''.join(recent_rows) if recent_rows else '<tr><td colspan=10>No recent data</td></tr>'}
</tbody></table>

<h2>Error Distribution</h2>
<div>
{(''.join([f"<div style=\"margin:6px 0;display:flex;align-items:center;\"><div style=\"width:140px\">{html.escape(code)}</div><div style=\"background:#eee;width:320px;\"><div style=\"height:16px;background:#e66;width:{int(300*(cnt/max_err)) if max_err else 0}px\"></div></div><div style=\"margin-left:8px\">{cnt}</div></div>" for code,cnt in err_counts.items()])) if err_counts else '<div>No errors</div>'}
</div>
</body></html>
"""
    out = pathlib.Path('.cache/report.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding='utf-8')
    print(out)

if __name__ == '__main__':
    main()
