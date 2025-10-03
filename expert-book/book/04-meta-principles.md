# 04. 인스트럭션 메타 원칙 — 운영 환경에서의 원칙 적용

요약
- 원칙은 실행으로 증명해야 한다. 정책/계약/검증/관측성을 코드로 고정하고, 실패를 정상 경로로 설계한다.

핵심 원칙의 운영화
- 정책 주입(Policy Injection): 안전·윤리·보안 규칙을 프롬프트 조각/룰 파일로 관리하고 자동 삽입
- 출력 계약(Contract First): 구조화 출력과 스키마 검증을 우선 설계
- 관측성(Observability): 모든 단계의 로그를 JSONL로 수집하고, 품질/비용/지연을 계량화
- 복구 가능성(Recovery): 생성→검증→재프롬프트 루프를 표준화하고, 실패 샘플을 회귀 입력으로 축적

정책 주입 스펙 예시
```yaml
# policies/base.yaml
safety:
  pii_masking: true
  forbidden_terms: ["password_plain", "credit_card"]
style:
  tone: concise
  output_format: markdown
```

프롬프트 조합기(간소화)
```python
# tools/prompt_compose.py (개념)
import yaml
def compose(content, *policy_files):
    pol = {}
    for f in policy_files:
        pol.update(yaml.safe_load(open(f)))
    return f"""[POLICY]\n{yaml.safe_dump(pol)}\n[CONTENT]\n{content}\n"""
```

출력 계약과 검증
- 스키마는 `schemas/output.schema.json` 참조. 생성물은 `scripts/verify.py`로 검증한다.
```bash
cd expert-book/lab
python3 scripts/generate.py --model dummy --in data/inputs.jsonl \
  | python3 scripts/verify.py --schema schemas/output.schema.json \
  | tee logs/verify.jsonl
```

관측성과 기준선
- `logs/*.jsonl`에 누적하고, 요약치(accept_rate, latency, 오류 유형)를 주기적으로 집계한다.
```bash
cd expert-book/lab
python3 scripts/route.py logs/verify.jsonl > logs/route_summary.json
cat logs/route_summary.json
```

실패를 정상 경로로 — 재프롬프트 예시(개념)
```yaml
# workflow.yaml (개념)
steps:
  - name: generate
  - name: verify
  - name: fix-and-retry
    when: "verify.ok == false"
    run: tools/rewrite_prompt.py
```

Human-in-the-Loop
- `apply` 전 요약/근거/리스크를 생성해 승인자가 검토. 승인/거절은 추후 규칙(예외/패턴)으로 반영.

연관 챕터
- [06. 입력/출력 계약](06-input-output.md)
- [07. 워크플로우 패턴](07-process-workflow.md)
- [11-2. 조직 표준](11-2-organizational-standards.md)
- [13. Workflow as Code](13-workflow-as-code.md)
- [14. 진화](14-evolution.md)

