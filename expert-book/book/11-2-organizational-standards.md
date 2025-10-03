# 11-2. 조직 표준 — 보안·컴플라이언스·비밀·로그 정책

목표
- 팀 단위로 AI 자동화를 안전하고 일관되게 운영하기 위한 최소 표준을 수립한다.

비밀/자격증명
- 원칙: 코드/프롬프트/로그에 비밀을 남기지 않기
- 방법: `.env`/CI 시크릿, `direnv`로 개발환경 자동 로드, 토큰 마스킹

로그 정책
- JSONL 단일 포맷: `ts, step, input_hash, model, latency_ms, cost, verdict`
- PII 마스킹: 이메일/전화/키 패턴은 저장 전 토큰화

데이터 거버넌스
- 허용 도메인/목적 제한: 외부 호출은 허용 목록·목적 표기
- 데이터 보존: 민감 로그는 TTL 후 파기, 장기 보존은 요약/익명화본만 유지

표준 프롬프트 가드레일
```yaml
style:
  tone: concise
  forbidden_terms: ["password_plain", "api_secret"]
output:
  require_json: true
  schema: schemas/output.schema.json
```

리뷰 게이트(예)
```yaml
steps:
  - name: verify
  - name: security_check
    run: tools/scan_prompt_for_secrets.sh
  - name: human_approval
    run: tools/prepare_change_summary.py
```

감사/추적성
- 변경 요약, 리스크, 승인자 기록을 아티팩트로 보존
- 회귀 테스트와 결합해 품질 저하를 조기 감지

연관 챕터
- [13. Workflow as Code](13-workflow-as-code.md)
- [14. 진화](14-evolution.md)

