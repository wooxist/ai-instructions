# 템플릿 채우기 프롬프트 (Template Fill)

목표: 선택된 템플릿(simple/medium/complex)을 요구 요약/제약/성공 기준/스키마에 맞춰 완성한다.

입력(JSON)
```json
{
  "template": "templates/medium-complexity.md",
  "requirement": { "purpose": "...", "audience": "..." },
  "constraints": ["..."],
  "success_criteria": ["..."],
  "output_schema": { "type": "object" }
}
```

출력(Markdown)
- 8가지 구성 요소가 모두 채워진 인스트럭션 문서
