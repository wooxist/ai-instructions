# 08. 성능 최적화 — 비용·속도·품질의 공존 전략

목표
- 파워유저 관점에서 모델 호출 구조와 파이프라인을 최적화해 비용/지연을 낮추고 품질을 보장한다.

핵심 전략
- 샘플→확장: 작은 배치로 가설 검증 후 전체 실행
- 캐싱: 입력 해시 기반 결과 재사용, 동일 입력 재생성 차단
- 라우팅: 경량→고성능 단계적 승급, 고난도만 고비용 경로 사용
- 구조화 출력: 후처리 비용 감소, 실패 재시도 범위를 좁힘

캐시 키 설계(개념)
```python
import hashlib, json
def cache_key(prompt, vars, model):
    src = json.dumps({"p":prompt, "v":vars, "m":model}, sort_keys=True)
    return hashlib.sha256(src.encode()).hexdigest()
```

프로파일링(E2E 요약치)
```bash
cd expert-book/lab
python3 runner.py
python3 tests/eval_regression.py logs/generate.jsonl
cat logs/route_summary.json
```

비용/속도 가드레일(개념)
```yaml
# workflow.yaml (발췌)
budget:
  max_calls: 500
  max_tokens: 200_000
  max_seconds: 600
when_exceeded: pause_and_notify
```

로컬 LLM 프리필터 → 클라우드 정제
- 로컬 모델로 요약/태깅/중복제거 → 클라우드 모델로 최종 생성
- 비용 절감과 지연 완화, 데이터 유출면적 축소

실패 재시도 정책
- 포맷 실패: 즉시 재프롬프트(시드/지시 강화) 1~2회
- 내용 실패: 컨텍스트/예시 강화 후 1회
- 그 외: 격리 후 Human-in-the-Loop로 승격

관측 지표 추천
- 품질: 검증 통과율(accept_rate), 레이블 일치율(있는 경우)
- 비용: 호출 수, 추정 토큰, 총액(가능할 때)
- 속도: 단계별 지연(ms), 병목 구간

연관 챕터
- [07. 워크플로우 패턴](07-process-workflow.md)
- [12. 도구 통합](12-tools.md)
- [13. Workflow as Code](13-workflow-as-code.md)

