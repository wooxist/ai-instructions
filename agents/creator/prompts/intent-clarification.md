# 의도 확인 프롬프트 (Intent Clarification)

목표: 누락된 필드에 대해 3–5개의 구체적 질문을 생성한다.

입력(JSON)
```json
{
  "missing_fields": ["audience", "length"],
  "context": "경영진 브리핑용 분기 요약"
}
```

출력(Markdown)
- 질문 목록 (번호 목록)
- 각 질문에 왜 필요한지 한 줄 근거
