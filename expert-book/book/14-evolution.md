# 14. 진화 — 평가·회귀·지속 개선 루프 설계

목표
- ‘한 번 좋았던 설정’이 아니라, 시간과 변화에 강한 시스템을 만든다. 데이터/평가/기준선/승격 루프를 자동화한다.

데이터 축적
- 입력/출력/판정/비용/지연을 JSONL로 저장, 실패 케이스는 `fixtures/failures/`에 보관

평가 스크립트(경량)
```bash
cd expert-book/lab
python3 tests/eval_regression.py logs/generate.jsonl > .cache/metrics.json
cat logs/route_summary.json | jq .
```

기준선 비교 및 승격
```python
# tools/promote_baseline.py
import json, pathlib, sys
cur=json.load(open('.cache/metrics.json'))
basep=pathlib.Path('baselines/metrics.json')
base=json.load(open(basep)) if basep.exists() else None
ok = (base is None) or (cur['mean_confidence'] >= (base['mean_confidence']-0.02))
print(json.dumps({'ok':ok,'current':cur,'baseline':base}))
if ok:
    basep.parent.mkdir(parents=True, exist_ok=True)
    basep.write_text(json.dumps(cur, indent=2), 'utf-8')
```

워크플로우 통합(개념)
```yaml
steps:
  - name: run
  - name: eval
    run: python3 tests/eval_regression.py logs/generate.jsonl > .cache/metrics.json
  - name: promote
    run: python3 tools/promote_baseline.py
```

Human‑in‑the‑Loop
- 기준선 하락이 감지되면 자동 알림 후 사람 검토. 승격은 승인 로그와 함께 기록

