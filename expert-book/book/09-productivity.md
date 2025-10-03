# 09. 생산성 확장 — 편집기·매크로·캐시·템플릿

목표
- 반복 업무를 ‘명령 한 번’으로 축소한다. 에디터/CLI/템플릿을 엮어 생성→검증→적용까지 단축키로 실행.

VS Code Tasks로 원클릭 러닝
```json
{
  "version": "2.0.0",
  "tasks": [
    {"label":"WF: run","type":"shell","command":"python3 runner.py"},
    {"label":"WF: eval","type":"shell","command":"python3 tests/eval_regression.py logs/generate.jsonl"}
  ]
}
```

템플릿에서 질문 생성 자동화
```bash
# scripts/new_question.sh
name=${1:?usage: new_question.sh <name>}
mkdir -p questions/$name
cat > questions/$name/spec.yaml <<'Y'
name: ${name}
template: |
  대상: {{target}}
  기간: {{start}}~{{end}}
  형식: {{format}}
  출력: {{output}}
vars:
  target: "프로젝트 A"
  start:  "2025-10-01"
  end:    "2025-10-07"
  format: "5줄 불릿 + 마지막 줄 액션"
  output: "Markdown 불릿만"
Y
echo "created: questions/$name/spec.yaml"
```

캐시 기본기
- 프롬프트+변수+모델로 해시를 만들고 같은 키면 재사용
- 캐시 디렉토리 구조: `.cache/<workflow>/<hash>.json`

작업 큐와 배치
- JSONL 스트림을 표준으로 하여 병렬/배치 처리를 단순화
- 실패 레코드만 분리 저장해 재시도

스니펫 팁
- 스키마/룰/출력 계약을 스니펫으로 고정해 일관성 확보
- 예: “JSON 한 줄만 출력” 문구를 공용 스니펫으로 배포

Human‑in‑the‑Loop
- `apply` 전 변경 요약 팝업(또는 미리보기 diff) 제공 → 승인/반려/수정 요청 루프의 클릭 수 최소화

연관 챕터
- [12. 도구 통합](12-tools.md)
- [13. Workflow as Code](13-workflow-as-code.md)

