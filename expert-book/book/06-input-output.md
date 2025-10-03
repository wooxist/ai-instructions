# 06. 입력/출력 계약 — 스키마, 검증, 구조화 출력

목표
- LLM 결과를 ‘사람이 읽는 글’이 아닌 ‘프로그램이 다루는 데이터’로 만들기. 구조화 출력, 스키마, 검증 루프를 표준화한다.

계약 우선(Contract First)
- 먼저 출력 계약을 정의한다 → 모델 호출은 계약을 충족하도록 보조하는 수단으로 설계한다.

출력 스키마 예시
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Generated Summary",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "summary": {"type": "string"},
    "confidence": {"type": "number"},
    "model": {"type": "string"}
  },
  "required": ["id", "summary", "confidence"]
}
```

프롬프트에 계약을 명시하기
- “아래 형식의 ‘JSON 한 줄’로만 답하라”는 요구와 필드/타입 힌트를 포함한다.
```text
필수 출력: {"id": string, "summary": string, "confidence": 0..1 number}
JSON 한 줄만 출력. 설명/코드는 금지.
```

검증 루프 구현
```bash
cd expert-book/lab
# 생성
python3 scripts/generate.py --model dummy --in data/inputs.jsonl \
  | tee .cache/gen.jsonl > /dev/null

# 검증
cat .cache/gen.jsonl | python3 scripts/verify.py --schema schemas/output.schema.json \
  | tee logs/verify.jsonl

# 라우팅(요약치)
python3 scripts/route.py logs/verify.jsonl | tee logs/route_summary.json
```

실패 시 조치(패턴)
- 포맷 실패: 스키마에 맞춰 자동 리포맷(예: JSON 복구 프롬프트)
- 내용 실패: 추가 컨텍스트/예시 주입 후 재생성
- 한계: 계약 상 표현 불가 시 실패 샘플로 격리, 인간 검토 후 계약을 현실화

구조화 출력을 쉽게 만드는 요령
- 필드 예시 제공, 기본값/빈 값 처리 규칙 명시
- 값의 범위를 제한(예: confidence 0..1)하여 모델 출력 변동폭 축소
- 선택 필드는 true/false 플래그와 함께 제공해 해석 모호성 제거

파이썬 측 검증 확장
- 필요 시 `pydantic`/`jsonschema`를 도입하되, 경량 환경에선 본 저장소의 `scripts/verify.py`처럼 최소 검증으로 시작

연관 챕터
- [07. 워크플로우 패턴](07-process-workflow.md)
- [08. 성능 최적화](08-performance.md)
- [13. Workflow as Code](13-workflow-as-code.md)

