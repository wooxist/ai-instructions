# 요구 수집 프롬프트 (Instruction Intake)

목표: 사용자의 자연어 요구에서 목적/대상/분량/형식/마감/제약/맥락/참고를 추출해 JSON으로 정리한다.

지시
- book/glossary.md의 용어를 기준으로 필드를 해석한다.
- 누락 필드는 `null` 또는 빈 배열로 표기한다.

출력(JSON)
```json
{
  "purpose": "...",
  "audience": "...",
  "length": "...",
  "format": "...",
  "deadline": "YYYY-MM-DD",
  "constraints": ["..."],
  "domain_context": "...",
  "references": ["..."]
}
```
