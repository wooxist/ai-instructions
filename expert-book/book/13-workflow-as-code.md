# 13. Workflow as Code — 재현성과 팀 운영의 핵심

핵심 메시지
- 워크플로우는 ‘문서’가 아니라 ‘코드’다. 버전 관리, 코드리뷰, 테스트, CI/CD 대상으로 다뤄야 재현성과 품질이 보장된다.

권장 스택
- orchestrator: `just` 또는 `make`
- 언어: Python(유틸)/bash(접착)
- 구조화: YAML/JSON 스키마, JSONL 로그
- 통합: VS Code Tasks, pre-commit, GitHub Actions 또는 로컬 CI

justfile 예시 — 개발/검증/릴리즈 파이프라인
본 저장소의 실습용 Justfile은 `expert-book/lab/Justfile`에 있습니다.
```makefile
set shell := bash

MODEL ?= gpt-4o-mini

prepare:
  @python scripts/prepare_inputs.py data/raw > data/inputs.jsonl

gen:
  @python scripts/generate.py --model $(MODEL) --in data/inputs.jsonl \
    | tee -a logs/generate.jsonl > .cache/last.out

verify:
  @python scripts/verify.py --schema schemas/output.schema.json --in .cache/last.out

route:
  @python scripts/route.py logs/generate.jsonl > logs/route_summary.json

apply:
  @python scripts/apply_changes.py .cache/last.out

all: prepare gen verify route
```

VS Code 통합 — `.vscode/tasks.json`
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "WF: all",
      "type": "shell",
      "command": "just all",
      "problemMatcher": []
    },
    {
      "label": "WF: apply",
      "type": "shell",
      "command": "just apply",
      "problemMatcher": []
    }
  ]
}
```

GitHub Actions (선택) — 회귀 테스트/품질 게이트
```yaml
name: workflow-ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: just prepare gen
      - run: python tests/eval_regression.py logs/generate.jsonl
```

회귀 테스트와 평가(Evals)
- 입력/출력/결론을 JSONL로 축적해 ‘변화에 강한’ 테스트를 만든다.
- 히스토릭 베이스라인과의 편차(정확도/비용/지연) 경보를 설정한다.

비밀/보안
- `.env` 또는 CI 시크릿 사용. 로그/프롬프트에는 비식별 토큰으로 마스킹
- 외부 호출 전 허용 도메인/정책 룰을 명시해 사고면적 축소

Human-in-the-Loop
- `apply` 전 승인단계: 변경 요약·근거·리스크를 생성해 검토자에게 표시
- 승인/거절이 다시 학습 데이터(룰·예외)로 축적되도록 루프화

연관 챕터
- [07. 워크플로우 패턴](07-process-workflow.md)
- [14. 진화](14-evolution.md)

