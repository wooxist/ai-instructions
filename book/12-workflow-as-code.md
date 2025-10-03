# 12장. 워크플로우 자동화와 코드형 인프라 (IaC)

**Part 3: 인스트럭션 시스템의 확장과 운영**

**목적:** 수동으로 실행하던 인스트럭션과 워크플로우를 '코드'로 관리하고, 이를 통해 전체 프로세스를 자동화, 테스트, 배포하는 '코드형 인스트럭션(Instruction as Code, IaC)'의 개념과 실용적인 구현 방법을 학습합니다.

### 이 장에서 배우는 것
- 인스트럭션을 코드로 관리할 때의 장점(버전 관리, 재사용성, 자동화).
- `workflow.yaml`과 같은 선언적 파일을 사용하여 다중 에이전트 워크플로우를 정의하는 방법.
- GitHub Actions와 같은 CI/CD 도구를 활용하여 인스트럭션의 변경 사항을 자동으로 테스트하고 배포하는 방법.
- 인스트럭션 시스템을 위한 간단한 DevOps(Instruction DevOps) 파이프라인 구축 아이디어.

---

## 12.1 왜 인스트럭션을 코드로 관리해야 하는가?

지금까지 우리는 인스트럭션을 사람이 읽고 이해할 수 있는 마크다운(`.md`) 파일로 작성했습니다. 이는 팀원 간의 공유와 이해에는 유용하지만, 복잡한 워크플로우를 매번 수동으로 실행해야 하는 한계가 있습니다. '코드형 인스트럭션(Instruction as Code)'은 이러한 수동 작업을 자동화하고, 인스트럭션 시스템 전체를 하나의 소프트웨어 프로젝트처럼 체계적으로 관리하기 위한 접근법입니다.

이는 마치 서버를 관리할 때, 수동으로 클릭하여 설정하는 대신 설정 파일을 코드로 작성하여 관리하는 '코드형 인프라(Infrastructure as Code, IaC)'[^1]와 같은 철학을 공유합니다. 인스트럭션을 코드로 관리하면 다음과 같은 강력한 이점을 얻을 수 있습니다.

- **버전 관리 (Versioning):** 모든 변경 사항이 Git을 통해 추적되므로, 언제 누가 무엇을 왜 바꿨는지 명확히 알 수 있고, 문제가 생겼을 때 이전 버전으로 쉽게 되돌릴 수 있습니다.
- **자동화 (Automation):** `workflow.yaml`과 같은 설정 파일을 기반으로, 워크플로우 엔진이 전체 프로세스를 사람의 개입 없이 자동으로 실행할 수 있습니다.
- **재사용성 (Reusability):** 잘 만들어진 에이전트 인스트럭션이나 워크플로우는 다른 프로젝트에서 쉽게 가져와 재사용할 수 있는 '모듈'이 됩니다.
- **테스트 용이성 (Testability):** 9장에서 배운 '평가 에이전트'를 자동화된 테스트 스크립트로 만들어, 인스트럭션이 변경될 때마다 기존 기능이 망가지지 않았는지(회귀 테스트) 자동으로 검증할 수 있습니다.

## 12.2 워크플로우를 코드로 정의하기: `workflow.yaml`

10장에서 여러 번 등장했던 `workflow.yaml` 파일은 다중 에이전트 시스템의 '설계도'이자 '실행 스크립트' 역할을 합니다. 이 파일은 사람이 읽고 이해하기 쉬우면서도, 기계가 파싱하여 실행할 수 있는 선언적인(declarative) 구조를 가집니다.

### 12.2.1 DSL 설계: YAML vs. Markdown

워크플로우 DSL[^2]을 설계할 때 YAML과 Markdown 중 어떤 것을 선택할지는 중요한 결정입니다. 우리는 두 가지를 모두 사용하는 하이브리드 접근법을 채택했습니다.

- **YAML (`workflow.yaml`):** 워크플로우의 '구조'를 정의하는 데 사용됩니다. 단계(steps), 입/출력(inputs/outputs), 조건(conditions) 등 명확한 구조를 가진 정보를 표현하는 데 매우 효과적입니다. GitHub Actions나 Kubernetes 등 이미 많은 자동화 도구에서 표준으로 사용되고 있어 익숙하고, 기계가 파싱하기에 용이합니다.
- **Markdown (`agents/*.md`):** 에이전트의 '지침'처럼, 사람이 읽고 이해해야 하는 서술적인 내용을 담는 데 사용됩니다. 역할, 처리 방법, 제약 조건 등 줄글로 된 설명은 Markdown으로 작성하는 것이 가독성과 유지보수성 면에서 훨씬 유리합니다.

이처럼 **워크플로우의 뼈대는 YAML로, 각 에이전트의 상세한 지침은 Markdown으로** 역할을 분리하는 것이 이 책에서 제시하는 핵심 설계 패턴입니다.

### 12.2.2 단일 에이전트 자동화: `yaml`이 필요한 이유

그렇다면 단일 에이전트 작업에도 `workflow.yaml`이 필요할까요? **수동으로 실행할 때는 필요 없습니다.** 10.1절의 예시처럼 `agents/01_email_summarizer.md` 파일의 내용을 복사해 AI에게 직접 지시할 수 있습니다.

하지만 이 작업을 **자동화**하고 싶다면 `workflow.yaml`이 필요합니다.

```yaml
# /workflows/summarize_email.yaml
name: Summarize Single Email
trigger: API Call

steps:
  - name: 1. Summarize
    agent: agents/01_email_summarizer.md
    inputs:
      - email_body: "{{trigger.payload.body}}" # API로 전달된 이메일 본문
    outputs:
      - variable: summary_text
```

이처럼 `workflow.yaml`은 에이전트가 하나일 때도, 그 작업을 **언제(`trigger`), 어떤 데이터로(`inputs`), 어떻게 실행할지** 정의하는 '실행기' 역할을 합니다. 이렇게 설계하면 나중에 이 요약 에이전트를 더 큰 워크플로우의 한 부분으로 쉽게 재사용할 수 있습니다.

### `workflow.yaml`의 핵심 구성 요소

```yaml
# /instructions/quarterly_report/workflow.yaml

name: Quarterly Financial Report Generation # 1. 워크플로우의 이름
trigger: Manual # 2. 실행 트리거 (수동, 매주, API 호출 등)

steps: # 3. 실행 단계 목록
  - name: 1. Extract Sales Data # 단계의 이름
    agent: agents/01_extractor.md # 이 단계를 수행할 에이전트
    inputs: # 에이전트에게 전달할 입력
      - quarter: "2024-Q3"
    outputs: # 이 단계의 결과물
      - file: sales_data.csv

  - name: 2. Analyze and Visualize Data
    agent: agents/02_analyzer.md
    inputs:
      - file: sales_data.csv # 이전 단계의 출력을 입력으로 사용
    outputs:
      - file: summary.json
      - file: chart.png

  - name: 3. Human Approval # 4. 인간 개입 단계
    type: human_in_the_loop # 4장에서 정의한 'Human-in-the-Loop' 원칙의 구체적인 구현
    instructions: "분석 결과와 차트를 검토하고 승인해주세요."
    inputs:
      - file: summary.json
      - file: chart.png
```

1.  **`name`**: 워크플로우를 식별하는 고유한 이름입니다.
2.  **`trigger`**: 워크플로우가 언제 시작되는지를 정의합니다. (예: `Manual`, `Weekly`, `OnCommit`)
3.  **`steps`**: 워크플로우를 구성하는 각 단계의 목록입니다. 각 단계는 특정 `agent`를 호출하고, `inputs`와 `outputs`를 통해 데이터를 주고받습니다. 이는 7장에서 배운 **파이프라인 패턴**과 **핸드오프** 개념을 코드로 구현한 것입니다.
4.  **`type: human_in_the_loop`**: AI가 자동으로 처리할 수 없거나, 반드시 사람의 검토가 필요한 중요한 의사결정 지점을 명시합니다. 이는 4장의 **검증 및 책임 원칙**에서 강조한 **Human-in-the-Loop**를 실제 워크플로우에 코드로 내장하는 방법으로, 시스템의 안전성과 신뢰성을 확보하는 핵심 장치입니다.

## 12.3 고급 제어 흐름: 루프와 조건

실제 업무는 단순한 순차 실행(A→B→C)만으로 해결되지 않는 경우가 많습니다. `workflow.yaml`은 조건 분기와 반복(루프) 같은 고급 제어 흐름을 정의하여, 더 동적이고 지능적인 자동화를 구현할 수 있습니다.

### `do-while` 반복문 구현하기

사용자께서 궁금해하신 `do-while` 루프는 "결과물이 특정 품질 기준을 만족할 때까지 작업을 반복하라"와 같은 시나리오에 매우 유용합니다. 이는 10.5절의 '코드 생성 및 리뷰' 예제처럼, '생성-검증' 패턴을 자동화하는 핵심 로직입니다.

```yaml
# /instructions/code_generation_review/workflow.yaml
name: Self-Correcting Code Generation
trigger: Manual

variables:
  - requirements: "S3 버킷의 모든 이미지 파일에 대해 썸네일을 생성하는 함수"
  - generated_code: null
  - review_result: null
  - retry_count: 0

steps:
  - name: 1. Generate Code
    agent: agents/01_code_generator.md
    inputs:
      - requirements: "{{requirements}}"
    outputs:
      - variable: generated_code

  - name: 2. Review Code
    agent: agents/02_code_reviewer.md
    inputs:
      - code: "{{generated_code}}"
    outputs:
      - variable: review_result

  - name: 3. Check and Loop
    type: condition
    # 조건: 리뷰 상태가 '수정 필요'이고, 재시도 횟수가 3회 미만인가?
    check: "{{review_result.status == '수정 필요' and retry_count < 3}}"
    on_true:
      # 조건을 만족하면, 피드백을 포함하여 1단계로 돌아간다.
      next_step: 1
      inputs:
        - requirements: "이전 요구사항과 다음 피드백을 반영하여 코드 수정: {{review_result.feedback}}"
        - retry_count: "{{retry_count + 1}}" # 재시도 횟수 증가
```

이 워크플로우는 다음과 같이 `do-while` 루프를 구현합니다.
1.  **Do (실행):** 먼저 1단계(코드 생성)와 2단계(코드 리뷰)를 무조건 한 번 실행합니다.
2.  **While (조건 확인):** 3단계에서 리뷰 결과가 '수정 필요'인지, 그리고 최대 재시도 횟수를 넘지 않았는지 **조건을 확인**합니다.
3.  **Loop (반복):** 조건이 참이면, 리뷰 피드백을 새로운 요구사항으로 만들어 1단계로 돌아가 작업을 반복합니다. 조건이 거짓이면(리뷰 통과 또는 최대 재시도 도달), 루프를 탈출하고 워크플로우가 종료됩니다.

이처럼 `workflow.yaml`에 `condition`과 `next_step`을 조합하여 사용하면, 단순한 선언적 파일을 넘어 프로그래밍 언어와 유사한 동적 제어 구조를 만들 수 있습니다.

## 12.4 자동화된 테스트와 배포 (Instruction DevOps)

인스트럭션을 코드로 관리하면, 소프트웨어 개발에서 사용하는 CI/CD(지속적 통합/지속적 배포) 파이프라인을 도입하여 'Instruction DevOps'를 구축할 수 있습니다.

### GitHub Actions를 활용한 자동화 파이프라인 예시

다음은 GitHub Actions를 사용하여, 인스트럭션이 변경될 때마다 자동으로 품질을 검증하는 파이프라인의 예시입니다.

```yaml
# .github/workflows/instruction_validation.yml

name: Instruction Quality Check

on:
  push:
    branches: [ main ] # main 브랜치에 변경사항이 푸시될 때마다 실행
  pull_request:
    branches: [ main ] # main 브랜치로 PR이 생성될 때마다 실행

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Run Evaluation Agent # 9장에서 설계한 평가 에이전트 실행
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pip install -r requirements.txt
        python scripts/evaluation_agent.py --target-instruction "all"

    - name: Check Regression
      run: |
        # 평가 결과 리포트를 분석하여, 이전보다 성능이 저하되었는지 확인
        # 만약 성능이 저하되었다면, 파이프라인을 실패 처리하여 변경사항이 병합되지 않도록 함
        python scripts/check_regression.py --report "evaluation_report.json"
```

이 자동화 파이프라인은 다음과 같이 작동합니다.
1.  개발자가 인스트럭션(`*.md`)이나 워크플로우(`*.yaml`) 파일을 수정하여 `main` 브랜치에 푸시합니다.
2.  GitHub Actions가 변경을 감지하고, `Instruction Quality Check` 워크플로우를 자동으로 실행합니다.
3.  9장에서 만든 `evaluation_agent.py` 스크립트가 실행되어, 변경된 인스트럭션의 품질, 비용, 속도를 자동으로 측정합니다.
4.  `check_regression.py` 스크립트가 평가 결과를 이전 결과와 비교하여, 성능이 오히려 나빠졌는지(회귀) 확인합니다.
5.  만약 성능이 저하되었다면, 파이프라인은 '실패' 상태가 되고, 해당 변경사항이 운영 환경에 배포되는 것을 막습니다.

이처럼 'Instruction DevOps' 파이프라인을 구축하면, 인스트럭션 시스템의 품질과 안정성을 사람의 '꼼꼼함'이 아닌, 자동화된 '시스템'으로 보장할 수 있게 됩니다.

## 12.5 실무 예제로 이어보기

이 장에서 다룬 `workflow.yaml`과 자동화 개념은 10장 4부: 고급 아키텍처와 실전 구현에서 소개될 '메타 에이전트'의 핵심 기반이 됩니다. 메타 에이전트는 바로 이 `workflow.yaml` 파일 자체를 동적으로 생성하고 수정함으로써, 시스템 스스로가 발전하고 적응하는 고도의 자율성을 구현합니다.

---

[^1]: **코드형 인프라(IaC, Infrastructure as Code):** 서버, 네트워크, 데이터베이스 등의 IT 인프라를 수동으로 관리하는 대신, 코드를 통해 정의하고 관리하는 방식. 이 책에서는 인스트럭션과 워크플로우를 '인프라'로 간주하고 코드로 관리하는 개념으로 확장하여 사용한다.

[^2]: **DSL(Domain-Specific Language):** '특정 영역에 특화된 언어'라는 의미. `workflow.yaml`은 'AI 에이전트 워크플로우 정의'라는 특정 목적을 위해 설계된 DSL의 한 예이다. HTML이 웹 페이지 구조 표현에 특화된 DSL인 것과 같다.
