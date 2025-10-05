# 출력 스키마 제안 프롬프트 (Output Schema Synthesis)

목표: 결과물을 기계가 검증 가능하도록 JSON Schema를 제안한다.

입력(JSON)
```json
{
  "output_format": "JSON",
  "fields": ["summary", "insights", "risks"],
  "constraints": ["summary:500자 이내", "insights:3개", "risks:2개"]
}
```

출력(JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "summary": { "type": "string", "maxLength": 1000 },
    "insights": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 3 },
    "risks": { "type": "array", "items": { "type": "string" }, "minItems": 2, "maxItems": 2 }
  },
  "required": ["summary", "insights", "risks"]
}
```
