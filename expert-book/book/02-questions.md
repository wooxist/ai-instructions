# 02. 질문 설계 — 유형을 자동화 객체로 다루기

목적
- 질문을 ‘설명’이 아니라 ‘자동화 가능한 단위’로 정의한다. 팀/개인의 반복 문제를 질문 템플릿·스키마·워크플로우로 고정하여 재현 가능한 품질을 만든다.

핵심 아이디어
- 질문 유형(폐쇄형/개방형/탐색형/비교형/맥락 의존형/메타)을 코드/템플릿/스키마로 캡슐화한다.
- 인풋 변수와 출력 계약을 함께 정의하고, CLI·스크립트·워크플로우로 실행한다.

사전 준비
- jq/yq, curl, Python 3.10+, 선택: `just` 또는 `make`, 선택: `openai` CLI 또는 `ollama`

---

폐쇄형 질문(Closed-ended) — 품질게이트/체크리스트에 적합
- 목적: 예/아니오, Pass/Fail 판단과 근거 1줄
- 템플릿(예):
```
이 문서/PR이 다음 기준을 모두 충족합니까? 예/아니오로 답하고 각 항목에 1줄 근거를 남기세요.
기준:
- 입력 검증(Validation)
- 비밀번호 해시 처리
- 로그 민감정보 마스킹
- 비밀키 노출 금지
출력 형식: JSON { overall: boolean, checks: [{name, pass, reason}] }
```
- 자동화 스니펫: 검증 결과를 JSONL로 로깅하고 실패 시 CI를 중단
```bash
# inputs: file path in $TARGET
prompt=$(cat <<'P'
해당 파일이 기준을 충족하는지 점검하세요. 
대답은 JSON으로만:
{"overall": <true|false>, "checks": [{"name":"...","pass":true,"reason":"..."}]}

코드:
{{code}}
P
)

code=$(sed -n '1,200p' "$TARGET")
payload=$(jq -R -s --arg code "$code" --arg p "$prompt" '{model:"gpt-4o-mini",messages:[{role:"user",content:($p|gsub("\\{\\{code\\}\\}"; $code))}] }')

# 예: openai CLI (선택)
# openai chat.completions.create -q --input "$payload" | jq -r '.choices[0].message.content' > out.json

# 로깅 (네트워크 호출 대신 예시 JSON 구조만 확인)
echo "$(date -Iseconds) $TARGET" | jq -R --arg target "$TARGET" '{ts:., target:$target}' >> checks.jsonl
```

개방형(Open-ended) — 요약/서술/설명 자동화
- 목적: 범위가 있는 요약과 액션 제안
- 템플릿(예):
```
대상: 프로젝트 A 주간 보고 (지난 7일)
형식: 5줄 불릿 + 마지막 줄 ‘다음 액션 1개’
톤: 간결, 결정지향
출력: Markdown 불릿만
```
- 자동화 스니펫: 동일 주제를 날짜 필터로 배치 처리
```bash
just summarize WEEK_START=2025-10-01 WEEK_END=2025-10-07
# justfile
summarize:
  @echo "요약 자동화 ({{WEEK_START}}~{{WEEK_END}})";
  # 예시: 로그/이슈를 jq로 수집 후 프롬프트로 주입
  jq -s '.' data/events_{{WEEK_START}}_{{WEEK_END}}/*.json > /tmp/events.json
  # openai/ollama 호출부를 여기에 추가
```

탐색형(Exploratory) — 아이디어/대안 탐색을 체계화
- 목적: 후보 N개 + 난이도/가치/리스크 평가
- YAML 스펙 + Jinja 템플릿
```yaml
# ideas.yaml
title: MVP 후보 발굴
count: 5
criteria: [effort, value, risk]
constraints:
  - no duplicates
  - practical within 2 weeks
```
```jinja
{# ideas.md.j2 #}
{{title}}
요청: {{count}}개 후보를 제시하고 {{criteria}} 기준으로 표를 작성. 제약: {{constraints|join(', ')}}
출력: Markdown 테이블
```
```bash
python - <<'PY'
from jinja2 import Template
import yaml, sys
cfg=yaml.safe_load(open('ideas.yaml'))
tpl=Template(open('ideas.md.j2').read())
print(tpl.render(**cfg))
PY
```

비교형(Comparative) — 의사결정용 표준 포맷
- 목적: 대안 × 기준 매트릭스 + 최종 추천
- 표준 프롬프트 조각:
```
대안: {{options}}
비교 기준: {{criteria}}
출력: JSON {table:[{name, scores:{criterion:int}, pros, cons}], recommendation:{option, reason}}
```
- 후처리/검증: JSON 스키마로 자동 검증
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "table": {"type":"array"},
    "recommendation": {"type":"object","required":["option","reason"]}
  },
  "required": ["table","recommendation"]
}
```

맥락 의존형(Context-dependent) — 실행 가능성을 높이는 환경 전제
- 목적: 시간/예산/스택/정책 제약 내 실행계획 도출
- 템플릿(예):
```
환경: macOS, Python 3.10, 인터넷 제한, 주당 2시간
목표: 데이터 정제 자동화의 최소 실행 단계
출력: 단계 체크리스트 + 예상 시간/리스크
```

메타 질문(Meta) — 다음 질문의 품질을 높이는 루프
- 목적: 질문을 스스로 개선, 누락/모호 요소 보완
- 템플릿(예):
```
내 질문을 개선해줘. 목적/대상/범위/형식/성공기준 5요소로 재구성하고, 개선 전/후를 나란히 보여줘.
```

---

템플릿을 워크플로우로 운영하기
실행 위치: `expert-book/lab`
1) 스펙: 질문 템플릿과 변수 정의를 소스 관리
```yaml
# questions/spec.yaml
name: Weekly Report Summarizer
template: |
  대상: {{target}}
  기간: {{start}}~{{end}}
  형식: {{format}}
  출력: {{output}}
vars:
  target: "프로젝트 A"
  start:  "2025-10-01"
  end:    "2025-10-07"
  format: "5줄 불릿 + 마지막 줄 액션"
  output: "Markdown 불릿만"
```

2) 워크플로우: 생성→자체검증→루팅
```yaml
# workflow.yaml (발췌)
name: Question-Driven Automation
version: 1
steps:
  - name: render-prompt
    run: python render.py questions/spec.yaml > .cache/prompt.txt
  - name: generate
    run: |
      echo "<MODEL_CALL>" > .cache/output.txt  # openai/ollama 등 교체
  - name: self-check
    run: python checks/structure_check.py .cache/output.txt
  - name: route
    when: "result.self_check == 'fail'"
    run: python tools/rewrite_prompt.py .cache/prompt.txt > .cache/prompt_retry.txt
```

3) 러너(미니멀) — 파이썬 50줄 내 실행기
```python
# runner.py
import subprocess, sys, json, pathlib
def sh(cmd):
  return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True).stdout
def main():
  steps = [
    ("render-prompt", "python render.py questions/spec.yaml > .cache/prompt.txt"),
    ("generate", "echo '<MODEL_CALL>' > .cache/output.txt"),
    ("self-check", "python checks/structure_check.py .cache/output.txt")
  ]
  pathlib.Path('.cache').mkdir(exist_ok=True)
  for name, cmd in steps:
    try:
      print(f"==> {name}")
      out = sh(cmd)
      print(out, end='')
      print(json.dumps({"step":name, "ok":True}))
    except subprocess.CalledProcessError as e:
      print(e.stdout); print(e.stderr, file=sys.stderr)
      print(json.dumps({"step":name, "ok":False}))
      sys.exit(1)
if __name__ == "__main__":
  main()
```

트러블슈팅/운영 팁
- 질문 템플릿은 ‘출력 계약(형식/스키마)’을 포함하라. 후처리/검증이 쉬워진다.
- JSONL 로깅으로 회귀 테스트를 준비하라: `ts, prompt_hash, model, cost, latency, verdict`를 남긴다.
- 실패는 정상 경로다. ‘생성→검증→재프롬프트’ 루프를 표준화하라.
- 비용/속도 최적화: 샘플 크기 N을 줄여 빠르게 가설 검증 후 확장, 필요 시 로컬 LLM으로 프리필터링.

Human-in-the-Loop
- 의사결정/배포 전 마지막 승인자는 인간. 자동화가 제시한 근거/대안/리스크를 요약해 보여주는 뷰를 마련하라.

연관 챕터
- [06. 입력/출력 계약](06-input-output.md)
- [07. 워크플로우 패턴](07-process-workflow.md)

