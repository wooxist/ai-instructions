# 13장. 도메인 특화 언어(DSL) 설계: AI와 소통하는 우리만의 언어

**Part 5: 시스템 확장과 운영**

**목적:**
- 도메인 특화 언어(Domain-Specific Language, DSL)의 기본 개념을 이해합니다.
- 왜 AI 에이전트 시스템을 위해 우리만의 언어(DSL)를 설계해야 하는지 그 필요성을 배웁니다.
- YAML과 마크다운을 조합하여, 사람이 읽기 쉽고 기계가 처리하기 쉬운 실용적인 DSL을 설계하는 방법을 학습합니다.
- DSL의 검증 방법과 오류 처리 전략을 익힙니다.

---

## 13.1 도메인 특화 언어(DSL)란 무엇인가?

**도메인 특화 언어(Domain-Specific Language, DSL)**는 말 그대로 '특정 영역(Domain)의 문제를 해결하는 데 특화된 컴퓨터 언어'입니다. 이는 파이썬(Python)이나 자바(Java)처럼 어떤 문제든 해결할 수 있는 '범용 언어(General-Purpose Language, GPL)'와는 다른 개념입니다.

비유하자면, 범용 언어는 어떤 요리든 만들 수 있는 전문가용 주방과 같습니다. 다양한 도구와 재료가 있지만, 이를 제대로 사용하려면 전문적인 지식과 경험이 필요합니다. 반면, DSL은 '캡슐 커피 머신'과 같습니다. 커피를 내린다는 특정 목적에 완벽하게 맞춰져 있어, 누구나 버튼 몇 번만 누르면 쉽고 일관되게 맛있는 커피를 만들 수 있습니다.

우리에게 익숙한 DSL의 예시는 다음과 같습니다.

- **HTML:** 웹 페이지의 '구조'를 표현하는 데 특화된 언어입니다. 우리는 HTML로 게임을 만들지는 않지만, 웹 페이지를 만드는 데는 이보다 더 좋은 언어가 없습니다.
- **SQL:** 데이터베이스에 데이터를 '요청'하는 데 특화된 언어입니다. `SELECT * FROM users WHERE age > 30;` 라는 구문은 "30세 이상인 모든 사용자의 정보를 보여줘"라는 명확한 의도를 표현합니다.
- **CSS:** 웹 페이지의 '스타일'을 꾸미는 데 특화된 언어입니다.

이 책에서 우리가 `workflow.yaml`을 통해 정의하는 언어 역시, **'AI 에이전트들의 협업 방식을 정의'**하는 데 특화된 우리만의 DSL입니다.

## 13.2 왜 우리만의 언어(DSL)가 필요한가?

그렇다면 왜 복잡하게 우리만의 언어를 만들어야 할까요? 그냥 파이썬 같은 범용 언어로 모든 것을 처리하면 안 될까요? 특히 이 책의 핵심 독자인 '일반 사용자'에게 DSL이 필요한 이유는 다음과 같습니다.

### 1. 복잡성 추상화 (Hiding Complexity)

가장 큰 이유는 **복잡한 내부 구현을 감추고, 사용자가 자신의 '의도'에만 집중하게 만들기 위함**입니다.

예를 들어, 10장에서 본 `type: parallel`이라는 한 줄의 코드를 생각해 봅시다. 만약 이를 범용 언어로 직접 구현하려면, 여러 에이전트를 동시에 실행하고(멀티스레딩 또는 비동기 처리), 모든 작업이 끝날 때까지 기다렸다가, 그 결과들을 다시 하나로 합치는 복잡한 코드를 작성해야 합니다.

하지만 DSL을 사용하면, 사용자는 그저 "이 단계들을 동시에 실행해줘"라는 의도만 `type: parallel`로 선언하면 됩니다. 복잡한 실행 과정은 DSL을 해석하는 '워크플로우 엔진'이 알아서 처리해 줍니다. 이는 마치 자동차 운전자가 엔진의 원리를 몰라도 운전할 수 있는 것과 같습니다.

### 2. 인간과 기계 모두를 위한 공용어 (Human & Machine Readable)

잘 설계된 DSL은 **사람이 읽고 이해하기 쉬우면서도, 동시에 기계가 정확하게 해석하여 실행할 수 있는** 이중의 장점을 가집니다.

- **사람을 위해:** `workflow.yaml`은 프로젝트의 전체 흐름을 보여주는 '업무 계획서'나 '설계도' 역할을 합니다. 개발자가 아니더라도 기획자, 마케터, 매니저 등 누구나 파일을 열어보고 "아, 재무팀의 보고서가 나와야 마케팅팀의 작업이 시작되는구나"라고 쉽게 이해할 수 있습니다. 즉, DSL은 팀원 간의 소통과 협업을 위한 훌륭한 '공용어'가 됩니다.

- **기계를 위해:** YAML 형식은 기계가 파싱(해석)하고 검증하기에 매우 용이한 구조입니다. 워크플로우 엔진은 이 파일을 읽어, 각 단계가 유효한지, 필요한 입력값은 모두 있는지 등을 확인하고 자동화된 프로세스를 실행할 수 있습니다.

### 3. 의도의 명확한 표현 (Clear Expression of Intent)

범용 언어로 작성된 코드는 '어떻게(How)' 동작하는지는 보여주지만, '왜(Why)' 그렇게 하는지에 대한 '의도'는 숨겨져 있는 경우가 많습니다. 반면, DSL은 사용자가 자신의 의도를 명확하게 표현하도록 유도합니다.

- `type: human_in_the_loop`: "이 단계는 위험하니, 반드시 사람의 승인이 필요하다"는 의도를 명확히 합니다.
- `type: handoff`: "여기까지가 우리 팀의 책임이고, 이제부터는 다른 팀의 책임이다"라는 조직 간의 업무 경계를 명확히 합니다.
- `retry: 3`: "이 작업은 가끔 실패할 수 있으니, 3번까지는 다시 시도해봐도 괜찮다"는 실패 처리 의도를 명확히 합니다.

이처럼 의도가 명시적으로 드러나면, 다른 사람이 워크플로우를 유지보수하거나 인수인계받을 때 훨씬 더 쉽고 안전하게 시스템을 이해할 수 있습니다.

### 4. 안전성과 제약 (Safety through Constraints)

DSL은 특정 도메인에 필요한 기능만 제공하고, 그 외의 위험한 행동은 원천적으로 '제약'함으로써 시스템의 안정성을 높입니다.

범용 언어는 자유도가 높은 만큼, 실수로 시스템의 중요 파일을 삭제하거나 무한 루프에 빠지는 등의 위험한 코드를 작성할 가능성도 열려 있습니다.

하지만 우리가 설계한 `workflow.yaml` DSL에서는 `agent`, `inputs`, `outputs` 등 미리 약속된 키워드만 사용할 수 있습니다. 만약 사용자가 `delete_all_files: true`와 같은 임의의 명령어를 추가하더라도, 워크플로우 엔진은 이를 알 수 없는 명령어로 인지하고 실행을 거부할 것입니다. 이러한 '제약'은 사용자를 실수로부터 보호하는 안전장치(Guardrail) 역할을 합니다.

---

## 13.3 YAML과 마크다운을 활용한 실용적 DSL 설계

이제 구체적으로 우리의 워크플로우 DSL을 어떻게 설계할지 알아봅시다. 우리는 두 가지 형식을 조합하여 DSL을 구축합니다.

- **YAML**: 워크플로우의 '구조'와 '실행 흐름'을 정의
- **마크다운**: 각 에이전트의 '역할'과 '세부 지시사항'을 정의

### 13.3.1 워크플로우 구조 정의 (workflow.yaml)

`workflow.yaml` 파일은 전체 워크플로우의 청사진입니다. 이 파일에서 우리는 다음을 정의합니다:

1. **메타데이터**: 워크플로우의 이름, 버전, 설명
2. **단계(steps)**: 실행될 작업의 순서
3. **실행 타입**: 각 단계가 어떻게 실행되는지 (순차, 병렬, 조건부 등)

**기본 템플릿:**

```yaml
# 워크플로우 메타데이터
name: "콘텐츠 제작 워크플로우"
version: "1.0.0"
description: "블로그 포스트를 리서치부터 최종 검수까지 자동화"

# 워크플로우 실행 흐름
workflow:
  # 단계 1: 리서치
  - step_id: "research"
    agent: "research-agent"
    agent_instruction: "agents/workers/researcher.md"
    inputs:
      topic: "${user_input.topic}"
    outputs:
      - "research_notes.md"
    
  # 단계 2: 초안 작성
  - step_id: "draft"
    agent: "writer-agent"
    agent_instruction: "agents/workers/writer.md"
    inputs:
      research: "research_notes.md"
    outputs:
      - "draft_post.md"
    depends_on: ["research"]
    
  # 단계 3: 검수
  - step_id: "review"
    agent: "editor-agent"
    agent_instruction: "agents/workers/editor.md"
    inputs:
      draft: "draft_post.md"
    outputs:
      - "review_feedback.json"
    depends_on: ["draft"]
```

### 13.3.2 핵심 키워드 정의

우리 DSL의 핵심 키워드들과 그 의미를 정리하면 다음과 같습니다:

| 키워드 | 역할 | 예시 | 필수 여부 |
|---|---|---|---|
| `name` | 워크플로우 이름 | `"고객 지원 티켓 처리"` | 필수 |
| `version` | 버전 관리 | `"2.1.0"` | 필수 |
| `description` | 간단한 설명 | `"티켓 분류부터 응답까지 자동화"` | 선택 |
| `workflow` | 실행 단계 목록 | 배열 형태 | 필수 |
| `step_id` | 단계 고유 식별자 | `"categorize"` | 필수 |
| `agent` | 담당 에이전트 이름 | `"category-agent-v1"` | 필수 |
| `agent_instruction` | 에이전트 정의 파일 경로 | `"agents/workers/categorizer.md"` | 필수 |
| `inputs` | 입력 데이터 정의 | 객체 형태 | 필수 |
| `outputs` | 출력 파일 목록 | 배열 형태 | 필수 |
| `depends_on` | 선행 단계 지정 | `["step1", "step2"]` | 선택 |
| `type` | 실행 방식 | `"parallel"`, `"conditional"` | 선택 (기본: sequential) |
| `retry` | 재시도 횟수 | `3` | 선택 (기본: 0) |
| `timeout` | 제한 시간 (초) | `300` | 선택 |
| `on_failure` | 실패 시 행동 | `"rollback"`, `"continue"`, `"stop"` | 선택 (기본: stop) |

### 13.3.3 고급 패턴: 실행 타입 정의

7장에서 배운 다양한 워크플로우 패턴을 DSL로 표현하는 방법입니다.

**1) 병렬 실행 (Parallel Execution)**

```yaml
workflow:
  - step_id: "parallel_analysis"
    type: "parallel"
    steps:
      - step_id: "sentiment_analysis"
        agent: "sentiment-agent"
        # ... 세부 정의
      
      - step_id: "keyword_extraction"
        agent: "keyword-agent"
        # ... 세부 정의
    
    # 모든 병렬 작업 완료 후 실행
    on_complete: "merge_results"
```

**2) 조건부 분기 (Conditional Routing)**

```yaml
workflow:
  - step_id: "quality_check"
    agent: "qa-agent"
    outputs:
      - "qa_result.json"
  
  - step_id: "routing_decision"
    type: "conditional"
    condition: "${qa_result.status}"
    branches:
      approved:
        next_step: "publish"
      needs_revision:
        next_step: "revise"
      rejected:
        next_step: "notify_failure"
```

**3) 사람 개입 (Human-in-the-Loop)**

```yaml
workflow:
  - step_id: "final_approval"
    type: "human_in_the_loop"
    agent: "approval-request-agent"
    approval_required: true
    timeout_hours: 24
    on_timeout: "escalate_to_manager"
```

### 13.3.4 에이전트 정의 (마크다운 형식)

각 에이전트의 세부 역할과 지시사항은 별도의 마크다운 파일로 관리합니다. 이는 **관심사 분리(SoC)** 원칙을 따르며, 에이전트 정의를 재사용 가능하게 만듭니다.

**예시: `agents/workers/researcher.md`**

```markdown
# 역할: 전문 리서처

## 목적
주어진 주제에 대한 최신 정보와 신뢰할 수 있는 출처를 조사하여 
구조화된 리서치 노트를 작성한다.

## 입력
- `topic`: 조사할 주제 (문자열)

## 처리 방법
1. 주제와 관련된 최신 기사, 논문, 블로그를 검색한다.
2. 각 출처의 신뢰도를 평가한다 (공식 기관 > 학술지 > 일반 블로그).
3. 핵심 정보를 주제별로 분류하여 정리한다.

## 출력 형식
마크다운 파일로 다음 구조를 따른다:

\`\`\`markdown
# [주제명] 리서치 노트

## 핵심 발견사항
- 발견 1
- 발견 2

## 주요 출처
1. [출처 제목](링크) - 간단한 설명
2. ...

## 추가 조사 필요 항목
- 항목 1
\`\`\`

## 제약 조건
- 출처는 최소 3개 이상, 최대 10개 이하
- 모든 출처에 대해 URL 링크를 반드시 포함
- 출판일이 1년 이내인 자료 우선
```

### 13.3.5 두 형식의 조합 전략

YAML과 마크다운의 역할을 명확히 분리하면 다음과 같은 장점이 있습니다:

| 관점 | YAML (workflow.yaml) | 마크다운 (agent instructions) |
|---|---|---|
| **역할** | 워크플로우 오케스트레이션 | 에이전트 행동 정의 |
| **초점** | "누가, 언제, 무엇을" | "어떻게, 왜" |
| **변경 빈도** | 낮음 (프로세스 재설계 시) | 높음 (지시사항 개선 시) |
| **재사용성** | 프로젝트별 | 에이전트별 (여러 워크플로우에서 재사용) |
| **검증 방법** | 스키마 검증 | 템플릿 일관성 확인 |

**모범 사례:**
- 워크플로우 구조가 바뀔 때만 `workflow.yaml`을 수정
- 에이전트의 지시사항을 개선할 때는 해당 `.md` 파일만 수정
- 같은 역할의 에이전트는 여러 워크플로우에서 재사용
- 에이전트 파일명은 역할을 명확히 반영: `categorizer.md`, `summarizer.md`

---

## 13.4 DSL 검증 및 오류 처리

아무리 잘 설계된 DSL이라도, 사용자가 잘못 작성하면 문제가 발생합니다. 따라서 **검증(Validation)**과 **명확한 오류 메시지**가 필수적입니다.

### 13.4.1 스키마 검증 (JSON Schema)

YAML 파일의 구조가 올바른지 확인하기 위해 **JSON Schema**를 활용할 수 있습니다.

**예시: `workflow.schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Workflow Definition",
  "type": "object",
  "required": ["name", "version", "workflow"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "description": "워크플로우의 이름"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "시맨틱 버전 (예: 1.0.0)"
    },
    "workflow": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["step_id", "agent", "agent_instruction"],
        "properties": {
          "step_id": {
            "type": "string",
            "pattern": "^[a-z0-9_]+$"
          },
          "agent": {
            "type": "string"
          },
          "agent_instruction": {
            "type": "string",
            "pattern": "^agents/.+\\.md$"
          },
          "retry": {
            "type": "integer",
            "minimum": 0,
            "maximum": 5
          }
        }
      }
    }
  }
}
```

### 13.4.2 일반적인 오류 패턴과 해결

| 오류 유형 | 원인 | 좋은 오류 메시지 예시 | 해결 방법 |
|---|---|---|---|
| **순환 의존성** | `step_A` → `step_B` → `step_A` | "순환 의존성 발견: research → draft → research. 단계 간 의존 관계를 확인하세요." | `depends_on` 관계 재검토 |
| **존재하지 않는 파일 참조** | 경로 오타 | "에이전트 정의 파일을 찾을 수 없음: 'agents/workers/writter.md'. 파일명을 확인하세요. (힌트: 'writer'가 맞나요?)" | 파일명/경로 수정 |
| **타입 불일치** | 숫자에 문자열 입력 | "step 'analysis'의 'retry' 값이 잘못되었습니다. 예상: 숫자(0-5), 실제: 'three'" | 데이터 타입 수정 |
| **필수 필드 누락** | `step_id` 없음 | "2번째 단계에 필수 필드 'step_id'가 없습니다. 각 단계에 고유 ID를 지정하세요." | 필드 추가 |
| **중복 ID** | 같은 `step_id` 재사용 | "중복된 step_id 발견: 'review'. 각 단계는 고유한 ID를 가져야 합니다." | ID를 고유하게 변경 |

### 13.4.3 오류 메시지 설계 원칙

좋은 오류 메시지는 다음 4가지 요소를 포함해야 합니다:

1. **무엇이 잘못되었는가** (What): "필수 필드 'agent'가 없습니다"
2. **어디서 문제가 발생했는가** (Where): "3번째 단계(step_id: 'review')"
3. **왜 문제인가** (Why): "모든 단계는 담당 에이전트를 지정해야 합니다"
4. **어떻게 고칠 수 있는가** (How): "해당 단계에 'agent: 에이전트명' 필드를 추가하세요"

**나쁜 예:**
```
Error: Invalid workflow
```

**좋은 예:**
```
검증 오류: workflow.yaml (3번째 단계)

문제: 필수 필드 'agent'가 없습니다.
위치: step_id 'review'
설명: 모든 단계는 작업을 수행할 에이전트를 지정해야 합니다.
해결: 다음 필드를 추가하세요:
  agent: "editor-agent-v2"
  agent_instruction: "agents/workers/editor.md"
```

### 13.4.4 실행 시 검증 체크리스트

워크플로우 실행 전, 다음 항목을 자동으로 검증하는 것이 좋습니다:

- [ ] YAML 문법이 올바른가?
- [ ] 모든 필수 필드가 존재하는가?
- [ ] `step_id`가 모두 고유한가?
- [ ] 참조된 모든 에이전트 정의 파일이 실제로 존재하는가?
- [ ] `depends_on`에 명시된 단계들이 실제로 존재하는가?
- [ ] 순환 의존성이 없는가?
- [ ] `inputs`에서 참조하는 이전 단계의 `outputs`이 실제로 존재하는가?
- [ ] 데이터 타입이 스키마와 일치하는가?

---

## 13.5 실습 체크리스트
> 참고: 심화 과제는 [실습 과제 모음](practice-guide.md)을 참고하세요.

### 이 장을 완료하셨다면 다음을 확인하세요:

**개념 이해:**
- [ ] DSL이 무엇이고, 왜 범용 언어와 다른지 설명할 수 있다
- [ ] 우리 시스템에서 YAML과 마크다운이 각각 어떤 역할을 하는지 안다
- [ ] 4가지 DSL의 필요성(복잡성 추상화, 공용어, 의도 표현, 안전성)을 이해했다

**실습 능력:**
- [ ] 간단한 3단계 워크플로우를 `workflow.yaml`로 작성할 수 있다
- [ ] 에이전트 정의를 마크다운 파일로 작성할 수 있다
- [ ] 핵심 키워드(`step_id`, `agent`, `depends_on` 등)를 올바르게 사용할 수 있다
- [ ] 순차 실행과 병렬 실행의 차이를 DSL로 표현할 수 있다

**검증 및 디버깅:**
- [ ] 일반적인 5가지 오류 패턴을 알고, 오류 메시지를 해석할 수 있다
- [ ] 실행 전 검증 체크리스트의 항목들을 이해했다
- [ ] JSON Schema의 역할을 알고, 간단한 검증 규칙을 읽을 수 있다

### 실습 과제

**과제 1: 나만의 워크플로우 DSL 작성**

자신의 업무에서 반복되는 3단계 이상의 작업을 선택하여:
1. `workflow.yaml` 파일을 작성하세요 (최소 3개 단계)
2. 각 단계에 필요한 에이전트 정의 파일을 마크다운으로 작성하세요
3. 한 단계는 이전 단계의 출력을 입력으로 사용하도록 `depends_on`을 설정하세요

**과제 2: 오류 시나리오 분석**

다음 잘못된 `workflow.yaml`을 보고, 어떤 오류가 있는지 찾고 수정하세요:

```yaml
name: "테스트 워크플로우"
workflow:
  - step_id: "analysis"
    agent: "analyzer"
    outputs:
      - "result.json"
  
  - step_id: "analysis"  # 오류: 중복 ID
    agent: "reporter"
    inputs:
      data: "result.txt"  # 오류: 존재하지 않는 출력 참조
    depends_on: ["summary"]  # 오류: 존재하지 않는 단계 참조
```

**과제 3: 고급 패턴 적용**

7장에서 배운 '생성-검증' 패턴을 DSL로 구현하세요:
- 1단계: 초안 생성
- 2단계: 검증 및 피드백
- 3단계: 조건부 분기 (승인 시 발행, 수정 필요 시 1단계로 회귀)

---

## 다음 단계

이 장에서는 DSL의 개념과 필요성을 살펴보았습니다.
실제 DSL 설계와 구현 방법(예: `workflow.yaml` 설계 가이드, 스키마 검증, 오류 처리)은 향후 확장 예정입니다.
초판에서는 개념적 이해를 우선하고, 실습 세부 내용은 개정판에서 보강합니다.

## 참고 자료

- Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley Professional.
- Parr, T. (2009). *Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages*. Pragmatic Bookshelf.
 - Ben-Ari, M. (2006). *Understanding Programming Languages*. Weizmann Institute of Science.
 - YAML Official Specification: https://yaml.org/spec/

---
