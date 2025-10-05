# 구조 검증 프롬프트 (8요소 포함 여부)

목표: 대상 인스트럭션이 8가지 핵심 구성 요소를 모두 포함하는지 검사한다.

출력(JSON)
```json
{
  "has_all_sections": true,
  "missing": ["..."],
  "sections": {
    "purpose": true,
    "role": true,
    "input": true,
    "process": true,
    "output": true,
    "constraints": true,
    "evaluation": true,
    "principles": true
  }
}
```
