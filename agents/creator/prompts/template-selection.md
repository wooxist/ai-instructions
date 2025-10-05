# 템플릿 선택 프롬프트

목표: 사용자 요구를 간단/중간/복잡 중 하나로 분류하고 적합한 템플릿을 고른다.

입력
- 요구 요약: 목적/대상/분량/형식/마감
- 제약/도메인: 필수/금지/규정

출력(JSON)
```json
{
  "complexity": "simple|medium|complex",
  "chosen_template": "templates/simple-task.md|templates/medium-complexity.md|templates/complex-workflow.md",
  "missing_fields": ["..."],
  "rationale": "..."
}
```
