# 인스트럭션 평가 체크리스트 프롬프트

입력
- 대상 인스트럭션 텍스트
- 사용 목표/맥락(선택)

출력(JSON)
```json
{
  "scores": {
    "clarity": 0,
    "specificity": 0,
    "goal_oriented": 0,
    "consistency": 0
  },
  "issues": ["..."],
  "improvements": [
    {
      "issue": "...",
      "before": "...",
      "after": "...",
      "rationale": "..."
    }
  ]
}
```
