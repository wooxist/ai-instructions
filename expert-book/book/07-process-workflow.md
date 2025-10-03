# 07. 워크플로우 패턴 — 파이프라인/생성-검증/라우팅 실전화

목표
- LLM을 ‘한 번 호출’이 아니라 ‘운영 가능한 프로세스’로 만든다: 파이프라인 설계, 검증 루프, 라우팅, 관측성, 실패 복구.

필수 전제
- Python 3.10+, jq/yq, just 또는 make, 선택: openai/anthropic CLI, 로컬: ollama

---

표준 워크플로우 스키마(요지)
```yaml
name: My Workflow
version: 1
env:
  MODEL: gpt-4o-mini
  CACHE_DIR: .cache
steps:
  - id: prepare
    run: python scripts/prepare_inputs.py data/raw > data/inputs.jsonl

  - id: generate
    needs: [prepare]
    foreach: data/inputs.jsonl
    run: |
      # 예시: 모델 호출을 추상화 (실서비스에서는 openai/ollama 등 대체)
      python scripts/generate.py --model "$MODEL" --input "{{item}}" \
        | tee -a logs/generate.jsonl > "$CACHE_DIR/out_{{i}}.json"

  - id: verify
    needs: [generate]
    foreach: logs/generate.jsonl
    run: python scripts/verify.py --schema schemas/output.schema.json --input "{{item}}" \
         | tee -a logs/verify.jsonl

  - id: route
    needs: [verify]
    run: python scripts/route.py logs/verify.jsonl > logs/route_summary.json

  - id: apply
    needs: [route]
    when: "outputs.route_summary.accept_rate > 0.9"
    run: python scripts/apply_changes.py "$CACHE_DIR"/out_*.json
```

파이프라인(Pipeline) — 순차/병렬/배치 처리
- `needs`로 선후관계를 명시하고, `foreach`로 JSONL 스트림을 배치 처리
- 캐시 디렉토리와 로그(JSONL)를 표준화하여 재현성과 관측성을 확보

생성-검증(Generate-and-Verify) — 신뢰성의 기본 루프
- 출력 계약(스키마)을 먼저 정의하고, 검증 실패 시 재프롬프트 또는 축소된 프롬프트로 리트라이
```python
# scripts/verify.py (요지)
import json, sys, jsonschema
schema=json.load(open(sys.argv[sys.argv.index('--schema')+1]))
doc=json.loads(open(sys.argv[sys.argv.index('--input')+1]).read()) if '--input' in sys.argv else json.load(sys.stdin)
try:
  jsonschema.validate(doc, schema)
  print(json.dumps({"ok":True,"id":doc.get("id")}))
except Exception as e:
  print(json.dumps({"ok":False,"error":str(e)}))
  sys.exit(1)
```

라우팅(Routing) — 다중 모델/프롬프트/경로 선택
- 간단한 휴리스틱: 길이/주제/리스크에 따라 로컬→클라우드로 승급
- 비용/대기시간을 줄이기 위해 가벼운 모델로 1차 필터링 후 고성능 모델로 최종화
```python
# scripts/route.py (개념)
import json, sys
oks=sum(1 for l in open(sys.argv[1]) if json.loads(l).get('ok'))
total=sum(1 for _ in open(sys.argv[1]))
print(json.dumps({"accept_rate":oks/max(1,total)}))
```

실행기(Runner) — 최소 구성 예시
```bash
# justfile
run:
  @python runner.py

# runner.py (개념)
# - workflow.yaml을 파싱해 순서대로 실행
# - 실패 시 중단/재시도, 로그를 JSONL로 남김
```

관측성/디버깅
- 모든 단계는 JSONL 로그를 남긴다: `ts, step, input_hash, latency_ms, cost, verdict`
- 실패 샘플을 자동 수집해 `fixtures/failures/`로 저장, 회귀 테스트 입력으로 재사용

성능/비용 전략
- 샘플링 → 가설 검증 → 확장: 작은 배치에서 빠르게 검증 후 전체 실행
- 캐시: 동일 입력의 재생성 방지. `hash(prompt+variables)` 키로 파일 캐시
- 라우팅: 로컬 모델/경량 모델로 전처리, 고난이도만 고성능 모델에 위임

보안/안전
- 비밀은 환경변수/전용 시크릿 관리. 프롬프트·로그에서 민감정보 마스킹
- Human-in-the-Loop: `apply` 단계 전 승인자 검토 단계 삽입

연관 챕터
- [13. Workflow as Code](13-workflow-as-code.md)
- [08. 성능 최적화](08-performance.md)
- [10. 고급 협업 아키텍처](10-advanced-collaboration-architectures.md)

