# 12. 도구 통합 — CLI/VS Code/로컬 LLM/관측성

목표
- 파워유저 환경에서 바로 쓰는 도구 조합을 제시: CLI 호출, 로컬 모델, 에디터 연결, 관측성/로깅.

CLI 호출 추상화
- curl + jq: 가장 이식성 높은 조합
```bash
MODEL=${MODEL:-gpt-4o-mini}
PROMPT='다음 텍스트를 5줄 불릿으로 요약: ...'

# 의도 표현용 예시(네트워크 호출은 주석)
# curl https://api.openai.com/v1/chat/completions \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -H 'Content-Type: application/json' \
#   -d '{"model":"'$MODEL'","messages":[{"role":"user","content":"'$PROMPT'"}]}' \
# | jq -r '.choices[0].message.content'
```

로컬 LLM(ollama)
- 비용/프라이버시/속도 이점. 프리필터/라벨링/요약 전처리에 적합
```bash
# ollama pull llama3.1:8b
echo "$PROMPT" | ollama run llama3.1:8b
```

템플릿 엔진
- Jinja2/ytt/yttx 등. 변수와 프롬프트 스니펫을 조합해 프롬프트 표준화
```bash
python - <<'PY'
from jinja2 import Template
print(Template('대상: {{t}}').render(t='리포트'))
PY
```

관측성/로깅
- 모든 호출을 JSONL로 남긴다: `ts, tool, model, input_hash, tokens, latency_ms, cost`
```bash
ts=$(date -Iseconds)
hash=$(printf "%s" "$PROMPT" | shasum -a 256 | cut -d' ' -f1)
jq -n --arg ts "$ts" --arg h "$hash" '{ts:$ts, input_hash:$h, tool:"ollama"}' >> logs/calls.jsonl
```

VS Code 스니펫/Tasks
- 반복 인스트럭션/프롬프트를 에디터 스니펫/Tasks로 노출해 진입장벽을 낮춘다
```json
{
  "version": "2.0.0",
  "tasks": [
    {"label": "Summarize Week", "type": "shell", "command": "just summarize"}
  ]
}
```

보안/비밀
- `.env` + direnv로 로컬에서만 로드. 로그에는 토큰 마스킹
- 프롬프트에 정책/금칙어를 주입해 안전가드 일관성 유지

