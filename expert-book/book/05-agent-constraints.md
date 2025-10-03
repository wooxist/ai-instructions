# 05. 에이전트와 제약 — 책임 경계와 실패 안전장치

목표
- ‘에이전트’는 기술이 아니라 계약이다. 역할/입력/출력/제약/실패 처리까지 계약으로 고정해 예측 가능성을 높인다.

에이전트 명세 스켈레톤
```yaml
# agents/specs/example.yaml
name: Code Reviewer
inputs:
  - path: string
  - rules: [string]
outputs:
  - verdict: pass|fail
  - checks: [{name, pass, reason}]
constraints:
  time_budget: "5s"
  policy: policies/base.yaml
failure:
  retry: 1
  on_fail: isolate_and_notify
```

계약 검증기(경량)
```python
# tools/contract_check.py
import sys, json
SCHEMA = {
  'required': ['verdict','checks']
}
obj=json.load(sys.stdin)
missing=[k for k in SCHEMA['required'] if k not in obj]
print(json.dumps({'ok': not missing, 'missing': missing}))
sys.exit(0 if not missing else 1)
```

실행 예 — 생성→검증→라우팅
```bash
cd expert-book/lab
python3 scripts/generate.py --model dummy --in data/inputs.jsonl \
  | tee .cache/out.jsonl > /dev/null
cat .cache/out.jsonl | python3 scripts/verify.py --schema schemas/output.schema.json \
  | tee logs/verify.jsonl
python3 scripts/route.py logs/verify.jsonl | tee logs/route_summary.json
```

제약 설계 체크리스트
- 책임경계: 입력/출력·권한·데이터 접근 범위를 문서화
- 리소스: 시간/토큰/비용 상한(초과 시 안전 정지)
- 품질: 스키마 검증, 규정 준수, 금칙어, 근거 요구 수준
- 실패 경로: 재시도 정책, 격리, Human‑in‑the‑Loop 승격

안전 가드레일(프롬프트 주입)
```text
정책 준수 필수: PII 마스킹, 금칙어 사용 금지, JSON 형식만 출력. 불확실하면 "insufficient_context" 사유로 실패를 보고.
```

Human‑in‑the‑Loop
- 실패/경계 케이스는 자동으로 ‘검토 대기열’로 이동, 승인자에게 요약·근거·리스크를 제공.

연관 챕터
- [06. 입력/출력 계약](06-input-output.md)
- [11-2. 조직 표준](11-2-organizational-standards.md)

