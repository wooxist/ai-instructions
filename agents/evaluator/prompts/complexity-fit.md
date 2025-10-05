# 복잡도/템플릿 적합성 평가 프롬프트 (Complexity Fit)

목표: 대상 인스트럭션이 simple/medium/complex 중 어느 템플릿에 해당하며, 선택이 적절한지 평가한다.

출력(JSON)
```json
{
  "predicted_complexity": "simple|medium|complex",
  "fit": "good|overkill|insufficient",
  "rationale": "...",
  "recommended_template": "templates/...md"
}
```
