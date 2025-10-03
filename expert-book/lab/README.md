# Expert-Book Lab

실행 가능한 모든 예제와 스크립트는 이 디렉토리에 정리되어 있습니다.

구성
- runner: `runner.py` — 생성→검증→라우팅→적용 파이프라인
- orchestrator: `Justfile` — run/render/eval 타깃 제공
- scripts/: 데이터 준비/생성/검증/라우팅/적용 유틸리티
- schemas/: 구조화 출력 스키마(JSON Schema)
- checks/: 문서 구조 점검 등 경량 검사기
- tools/: 프롬프트/시크릿 스캔/기준선 승격 도구
- tests/: 경량 평가 스크립트
- questions/: 템플릿 스펙 예시
- data/, logs/, .cache/: 러너 실행 산출물과 캐시가 생성되는 작업 디렉토리
- ai-agents/: 메타 에이전트 정의와 우선순위·배정 정보
- .github/workflows/: 샘플 GitHub Actions 워크플로우 (참고용)
- .vscode/tasks.json: 이 랩 디렉토리 기준 VS Code 태스크 (참고용)

빠른 시작
```bash
cd expert-book/lab
python3 runner.py
```

평가/승격
```bash
cd expert-book/lab
python3 tests/eval_regression.py logs/generate.jsonl > .cache/metrics.json
python3 tools/promote_baseline.py
```

보고서 생성
- 호출 로그와 검증 결과를 요약합니다.
  ```bash
  cd expert-book/lab
  python3 tools/report.py
  # 또는 just report (just 설치 시)
  ```

VS Code 통합
- 이 디렉토리에는 `.vscode/tasks.json`이 포함됩니다. 이 파일은 ‘랩’ 폴더를 워크스페이스로 열었을 때 인식됩니다.
- 루트 워크스페이스에서 사용하려면 `expert-book/lab/.vscode/tasks.json`을 `.vscode/tasks.json`으로 복사하세요.

GitHub Actions (샘플)
- 샘플 워크플로우는 `expert-book/lab/.github/workflows/workflow-ci.yml`에 있습니다.
- 실제 CI로 동작시키려면 해당 파일을 루트 `.github/workflows/` 아래로 이동하세요.
  ```bash
  mv expert-book/lab/.github/workflows/workflow-ci.yml .github/workflows/
  ```

환경 설정(.env)
- 이 디렉토리의 `.env.sample`을 복사해 `.env`를 만들고 값을 채우면, 스크립트/태스크에서 환경변수를 사용할 수 있습니다.
  ```bash
  cd expert-book/lab
  cp .env.sample .env
  # 필요한 키/옵션 설정: OPENAI_API_KEY, ANTHROPIC_API_KEY, OLLAMA_HOST, MODEL 등
  ```
- direnv 사용 시, `.envrc`에서 `dotenv .env`를 선언하면 폴더 진입 시 자동 로드됩니다.
  ```sh
  echo 'dotenv .env' > .envrc && direnv allow
  ```

로컬 LLM (Ollama) 빠른 시작
- 설치: https://ollama.ai 에서 설치 후 터미널 재시작
- 모델 준비/테스트:
  ```bash
  cd expert-book/lab
  just ollama-test            # 기본: llama3.1:8b
  # 또는 직접:
  ollama pull llama3.1:8b
  echo 'hello' | ollama run llama3.1:8b
  ```

OpenAI CLI 빠른 시작(선택)
- 설치(권장): `pipx install openai` (또는 `pip install --user openai`)
- 키 설정: `.env`에 `OPENAI_API_KEY` 추가 후 로드
- 테스트:
  ```bash
  cd expert-book/lab
  just openai-test
  ```

Anthropic CLI 빠른 시작(선택)
- 설치(권장): `pipx install anthropic`
- 키 설정: `.env`에 `ANTHROPIC_API_KEY` 추가 후 로드
- 테스트:
  ```bash
  cd expert-book/lab
  just anthropic-test
  ```

모델 라우팅 데모
- 입력 길이와 사용 가능한 도구/키를 기준으로 간단한 라우팅 결정을 시뮬레이션합니다.
  ```bash
  cd expert-book/lab
  just route-demo TEXT="Short input for local"
  # 또는 표준 입력 사용
  echo 'Longer input...' | python3 scripts/router_demo.py
  ```

라우팅 설정(환경 변수)
- `.env`에서 다음 변수를 통해 라우팅 기준/우선순위를 제어할 수 있습니다.
  - `ROUTE_FORCE`: `ollama|openai|anthropic|dummy` 중 하나로 강제 라우팅(해당 경로 가용 시)
  - `ROUTE_OLLAMA_MAX_CHARS`: 로컬(ollama) 사용 허용 최대 입력 길이(기본 280)
  - `ROUTE_ORDER`: 가용성 검사 순서(기본 `ollama,openai,anthropic`)
  - 모델 변수: `OLLAMA_MODEL`(기본 llama3.1:8b), `MODEL`(OpenAI 기본 gpt-4o-mini), `ANTHROPIC_MODEL`(기본 claude-3-5-sonnet-latest)

자동 라우팅 생성기
- 러너의 `generate` 단계는 `scripts/auto_generate.py`를 사용합니다. 위 환경 변수를 반영하여 경로를 선택하고, 각 경로 실패 시 안전하게 더미 요약으로 폴백합니다.
