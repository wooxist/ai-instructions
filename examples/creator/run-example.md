# Creator Agent 실행 예시

## 요구 요약 입력
```json
{
  "purpose": "경영진을 위한 분기 실적 1페이지 요약",
  "audience": "비개발 경영진",
  "length": "1페이지",
  "format": "Markdown",
  "constraints": ["숫자 근거 인용", "500단어 이내"],
  "references": ["reports/Q2.pdf"]
}
```

## 예상 산출
- 선택 템플릿: templates/medium-complexity.md
- 인스트럭션 초안(Markdown)
- 성공 기준(JSON) 5개 이상
