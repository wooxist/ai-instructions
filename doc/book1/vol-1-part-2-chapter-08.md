# 8장. 워크플로우 설계: 에이전트 협업 시스템 구축

**Part 2: 설계 원칙과 구성 요소**

에이전트가 단독으로 작업을 수행하는 것을 넘어, 여러 에이전트가 협력하여 더 복잡한 문제를 해결하는 방법을 알아봅니다. 이번 장에서는 가장 기본적이면서도 강력한 두 가지 협업 방식인 '파이프라인(Pipeline)'과 '생성-검증(Generate-and-Verify)' 패턴을 소개합니다. 이러한 협업의 전체적인 흐름을 [워크플로우(Workflow)](glossary.md#워크플로우-workflow)라고 합니다. 또한, 이러한 워크플로우를 코드가 아닌 설정 파일로 정의하고 관리하는 방법을 배웁니다.

## 8.1 파이프라인(Pipeline) 패턴

파이프라인은 가장 직관적인 협업 방식으로, 여러 에이전트가 작업을 순차적으로 처리하는 모델입니다. 마치 공장의 컨베이어 벨트처럼, 한 에이전트의 작업 결과(output)가 다음 에이전트의 입력(input)으로 전달됩니다.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1f77b4',
    'lineColor': '#6c757d',
    'background': 'transparent',
    'edgeLabelBackground': '#2ca02c'
  }
}}%%
graph TD
    A("데이터 수집 에이전트") --> B("데이터 정제 에이전트")
    B --> C("핵심 정보 추출 에이전트")
    C --> D("보고서 생성 에이전트")

    %% 클래스 정의 및 적용 (WRITER 부록 A 기준)
    classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
    classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
    classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
    classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
    classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
    classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
    class A,B,C,D agent;
```

이 패턴은 다음과 같은 단계로 구성된 작업에 매우 효과적입니다.

1.  **데이터 수집 에이전트**: 웹이나 문서에서 정보를 수집합니다.
2.  **데이터 정제 에이전트**: 수집된 정보에서 불필요한 부분을 제거하고 형식을 표준화합니다.
3.  **핵심 정보 추출 에이전트**: 정제된 데이터에서 핵심 내용을 요약하거나 특정 정보를 추출합니다.
4.  **보고서 생성 에이전트**: 추출된 정보를 바탕으로 최종 보고서를 작성합니다.

각 에이전트는 자신의 역할에만 집중하므로, 전체 프로세스의 효율성과 명확성이 높아집니다.

## 8.2 생성-검증(Generate-and-Verify) 패턴

'생성-검증' 패턴은 한 에이전트가 결과물을 만들면(Generate), 다른 에이전트가 그 결과물을 검증하고 피드백을 주는(Verify) 협업 모델입니다. 이 패턴은 결과물의 품질을 높이는 데 매우 중요한 역할을 하며, '피드백 루프(Feedback Loop)'를 만드는 가장 기본적인 방법입니다.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1f77b4',
    'lineColor': '#6c757d',
    'background': 'transparent',
    'edgeLabelBackground': '#2ca02c'
  }
}}%%
graph TD
    subgraph "생성-검증 루프"
        A("생성 에이전트") -- "초안 전달" --> B("검증 에이전트")
        B -- "수정 요청" --> A
    end
    B -- 최종 승인 --> C[완료]

    %% 클래스 정의 및 적용 (WRITER 부록 A 기준)
    classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
    classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
    classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
    classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
    classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
    classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
    class A,B agent;
```

예를 들어, 다음과 같은 시나리오에 적용할 수 있습니다.

*   **콘텐츠 생성**: '작가 에이전트'가 블로그 포스트 초안을 작성하면, '편집자 에이전트'가 문법 오류나 어색한 표현을 찾아 수정 제안을 합니다.
*   **코드 리뷰**: '개발자 에이전트'가 새로운 기능에 대한 코드를 작성하면, '리뷰어 에이전트'가 코드의 버그 가능성이나 스타일 가이드 위반 여부를 검토하고 개선점을 제안합니다.

이 패턴은 한 번에 끝나지 않고, 검증 에이전트의 피드백을 바탕으로 생성 에이전트가 결과물을 수정하고 다시 검증받는 과정을 여러 번 반복할 수 있습니다.

## 8.3 라우팅 패턴

워크플로우가 항상 정해진 길로만 가는 것은 아닙니다. 상황에 따라 다른 길로 안내하는 '교통 경찰'이나 '분류 담당자'가 필요합니다. 우리는 코드가 아닌, 명확한 지시를 받은 **라우팅 에이전트(Routing Agent)**를 통해 이러한 의사결정을 자동화할 수 있습니다.

### 8.3.1 분류 기반 라우팅 (Triage Routing)

가장 흔한 라우팅 방식으로, 들어온 작업의 내용을 보고 어떤 에이전트가 처리해야 할지 결정하는 패턴입니다. 마치 우체국에서 편지의 주소를 보고 담당 지역으로 보내거나, 고객센터에서 문의 유형에 따라 담당 팀으로 연결하는 것과 같습니다.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1f77b4',
    'lineColor': '#6c757d',
    'background': 'transparent',
    'edgeLabelBackground': '#2ca02c'
  }
}}%%
graph TD
    A[("입력<br/>고객 지원 티켓")] --> B{라우팅 에이전트<br/>분류 담당자}
    B -- "환불/결제 문의" --> C("결제팀 에이전트")
    B -- "기술적 오류" --> D("기술지원팀 에이전트")
    B -- "기타" --> E("일반문의팀 에이전트")

    %% 클래스 정의 및 적용 (WRITER 부록 A 기준)
    classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
    classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
    classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
    classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
    classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
    classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
    class B decision;
    class C,D,E agent;
```

**예시: 고객 지원 티켓 분류**

1.  **라우팅 에이전트 (분류 담당자)**가 이메일 내용을 읽습니다.
2.  내용이 '환불'에 관한 것이면, '결제팀' 에이전트에게 작업을 전달하도록 지시합니다.
3.  내용이 '기술적 오류'에 관한 것이면, '기술지원팀' 에이전트에게 전달하도록 지시합니다.

**인스트럭션 예시:**
> "당신은 고객 지원 티켓 분류 담당자입니다. 주어진 티켓의 내용을 읽고, '환불/결제' 관련 문의는 '결제팀'으로, '오류/장애' 관련 문의는 '기술지원팀'으로, 그 외에는 '일반문의팀'으로 분류하여 전달하세요."

### 8.3.2 조건부 라우팅 (Conditional Routing)

이전 단계의 결과에 따라 다음 행동을 결정하는 패턴입니다. 주로 `생성-검증` 패턴과 함께 사용되며, 검증 결과가 '성공'인지 '실패'인지에 따라 워크플로우를 분기시킵니다.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1f77b4',
    'lineColor': '#6c757d',
    'background': 'transparent',
    'edgeLabelBackground': '#2ca02c'
  }
}}%%
graph TD
    A("초안 작성 에이전트") --> B("검증 에이전트")
    B --> C{라우팅 에이전트<br/>팀장}
    C -- "결과: 승인" --> D("최종 발행 에이전트")
    C -- "결과: 수정 필요" --> A

    %% 클래스 정의 및 적용 (WRITER 부록 A 기준)
    classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
    classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
    classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
    classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
    classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
    classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
    class A,B,D agent;
    class C decision;
```

**예시: 보고서 승인 프로세스**

1.  '초안 작성 에이전트'가 보고서를 작성합니다.
2.  '검증 에이전트'가 보고서를 평가하고 '승인' 또는 '수정 필요' 태그를 붙입니다.
3.  **라우팅 에이전트 (팀장)**가 이 태그를 확인합니다.
    *   '승인' 태그가 있으면, '최종 발행 에이전트'에게 전달합니다.
    *   '수정 필요' 태그가 있으면, 피드백과 함께 '초안 작성 에이전트'에게 되돌려 보냅니다.

**인스트럭션 예시:**
> "당신은 보고서 승인 프로세스를 관리하는 팀장입니다. '검증 에이전트'의 평가 결과를 확인하세요. 결과가 '승인'이면 다음 단계로 보내고, '수정 필요'이면 작성자에게 반려하세요."

## 8.4 워크플로우 정의 (`workflow.yaml`)

워크플로우가 복잡해질수록, 각 단계를 코드에 직접 하드코딩하는 것은 비효율적이고 유지보수가 어렵습니다. 대신, 워크플로우의 구조와 각 단계에서 실행될 에이전트를 별도의 설정 파일로 정의하는 것이 좋습니다.

`YAML`이나 `JSON` 형식의 설정 파일을 사용하면, 코드 수정 없이 워크플로우의 순서를 바꾸거나 새로운 단계를 추가하는 등 유연한 변경이 가능합니다.

다음은 `workflow.yaml` 파일에 파이프라인 패턴을 정의한 간단한 예시입니다.

```yaml
# workflow.yaml — 파이프라인 예시 (Pipeline)
name: "콘텐츠 생성 파이프라인"
workflow:
  - id: research
    agent: "리서치 에이전트"
    # 지시 요약: 최신 동향 조사 → 텍스트 산출
    prompt: "AI 에이전트 협업의 최신 동향을 조사해줘."
    output: "research_result.txt"

  - id: draft
    agent: "초안 작성 에이전트"
    # 입력 파일을 기반으로 초안 작성
    input: "research_result.txt"
    prompt: "research_result.txt 파일을 기반으로 블로그 포스트 초안을 작성해줘."
    output: "draft.md"

  - id: human_review
    type: human-approval  # Human-in-the-Loop 지점
    input: "draft.md"
    instructions: "초안을 검토하고 승인 여부를 선택하세요."
    output: "draft_approved.md"

  - id: edit
    agent: "검수 에이전트"
    # 승인본을 기반으로 최종 교정
    input: "draft_approved.md"
    prompt: "문법/사실 관계를 확인하고 개선점을 반영해 최종 원고를 제출해줘."
    output: "final.md"
```

추가로, 생성-검증 + 조건부 라우팅을 YAML로 표현한 예시는 다음과 같습니다.

```yaml
# workflow.yaml — 생성-검증 + 조건부 라우팅 예시
name: "보고서 생성-검증 루프"
workflow:
  - id: generate
    agent: "생성 에이전트"
    prompt: "요구사항에 맞춰 초안 보고서를 작성해줘."
    output: "draft.md"

  - id: verify
    agent: "검증 에이전트"
    input: "draft.md"
    prompt: "초안을 평가하고, 승인/수정 필요 중 하나의 결과와 피드백을 JSON으로 출력해줘."
    output: "review.json"  # { "status": "approved"|"revise", "feedback": "..." }

  - id: route
    type: router
    input: ["draft.md", "review.json"]
    rules:
      - if: "$.review.status == 'approved'"
        then:
          next: publish
      - if: "$.review.status == 'revise'"
        then:
          next: revise

  - id: revise
    agent: "생성 에이전트"
    input: ["draft.md", "review.json"]
    prompt: "review.json의 피드백을 반영해 초안을 수정해줘."
    output: "draft.md"
    next: verify  # 루프

  - id: publish
    agent: "발행 에이전트"
    input: "draft.md"
    prompt: "최종본을 포맷팅해 출판용 문서로 변환해줘."
    output: "report_final.pdf"
```

이처럼 워크플로우를 코드가 아닌 데이터로 정의함으로써, 전체 시스템의 유연성과 확장성을 크게 높일 수 있습니다.

---

이번 장에서 다룬 기본 워크플로우 패턴들은 실무 협업의 기초가 됩니다. 특히 파이프라인, 생성-검증, 라우팅과 같은 패턴들은 다양한 실무 상황에서 활용됩니다.

**1권에서의 학습 경로**: 8장에서 배운 워크플로우는 5, 6, 7장에서 배운 에이전트 설계, 입출력 설계, 실전 패턴을 종합적으로 활용하는 최종 단계입니다.

**2권에서는**: 다중 에이전트 협업, 파일 기반 시스템, 계층적 조직 설계 등 더 복잡한 협업 패턴을 다룹니다.

---

## 실습 체크리스트
> 참고: 심화 과제는 [실습 과제 모음](practice-guide.md)을 참고하세요.

### 이 장을 완료하셨다면 다음을 확인하세요:
- [ ] 파이프라인/생성-검증/라우팅의 적용 조건과 장단점을 설명할 수 있다
- [ ] `workflow.yaml` 형태로 단계/에이전트/입출력 연결을 선언할 수 있다
- [ ] [Human-in-the-Loop](glossary.md#human-in-the-loop) 및 조건 분기(승인/수정 필요)를 설계에 반영할 수 있다

### 실습 과제
1. 단일 업무를 파이프라인 3단계로 정의한 `workflow.yaml` 초안을 작성하세요.
2. 동일 업무에 ‘생성-검증’ 루프와 조건부 라우팅을 추가하여 품질 보강 버전을 만드세요.

---

## 🎯 실습 체크리스트

### 이 장을 완료했다면:
- [ ] 파이프라인 패턴과 생성-검증 패턴의 차이를 설명할 수 있다
- [ ] 각 워크플로우 패턴이 어떤 상황에 적합한지 판단할 수 있다
- [ ] 라우팅 에이전트의 역할과 필요성을 이해한다
- [ ] workflow.yaml로 워크플로우를 정의하는 방법을 안다
- [ ] 단일 에이전트로는 해결하기 어려운 문제를 워크플로우로 해결할 수 있다

### 실습 과제

#### 과제 1: 파이프라인 설계하기
자신의 업무에서 순차적 처리가 필요한 작업을 찾아, 3-4단계의 파이프라인으로 설계해보세요.

**예시:**
- 회의록 → 요약 → 할일 추출 → 일정 등록
- 고객 문의 → 카테고리 분류 → 답변 생성 → 검토

**작성 내용:**
1. 각 단계의 에이전트 이름과 역할
2. 각 단계의 입력과 출력 파일
3. 전체 파이프라인 다이어그램 (Mermaid 또는 손그림)

#### 과제 2: 생성-검증 패턴 적용하기
품질 관리가 중요한 작업을 선택하고, 생성-검증 패턴을 적용해보세요.

**작성 내용:**
1. 생성 에이전트의 인스트럭션 초안
2. 검증 에이전트의 체크리스트 (무엇을 검증할 것인가?)
3. 피드백 루프를 몇 번까지 허용할 것인가?

#### 과제 3: workflow.yaml 작성하기
과제 1 또는 과제 2에서 설계한 워크플로우를 `workflow.yaml` 형식으로 작성해보세요.

```yaml
name: "[워크플로우 이름]"
workflow:
  - agent: "[에이전트 이름]"
    prompt: "[프롬프트]"
    input: "[입력 파일]"
    output: "[출력 파일]"
  # 다음 단계 추가...
```

### 심화 과제
- [ ] 라우팅 패턴이 필요한 실제 시나리오를 찾아 설계해보기
- [ ] 파이프라인 + 생성-검증을 결합한 하이브리드 워크플로우 만들어보기
- [ ] 각 패턴의 장단점을 실제 사례로 비교 분석하기

---

## 📖 다음 장 미리보기: 8장. 성능 최적화

**워크플로우를 설계했다면, 이제 어떻게 '더 빠르고, 더 저렴하게, 더 좋은 결과'를 얻을 수 있을까요?**

7장에서 여러 에이전트를 협업시키는 방법을 배웠습니다. 파이프라인으로 작업을 순차 처리하고, 생성-검증으로 품질을 높이고, 라우팅으로 적절한 담당자를 배정하는 법을 익혔죠.

하지만 워크플로우가 늘어날수록 새로운 고민이 생깁니다:

- "모든 단계에 최고급 모델을 쓰니까 비용이 너무 많이 나와요"
- "에이전트가 3개만 돌아가는데도 답변이 너무 느려요"
- "같은 질문을 매번 다시 물어야 하나요?"

**8장에서는 한정된 자원으로 최대의 효과를 내는 실용적인 전략을 배웁니다:**

- **성능의 삼각형**: 품질, 비용, 속도 중 무엇을 우선할지 상황별로 판단하기
- **단계적 모델 사용**: 간단한 작업엔 경량 모델, 중요한 결정엔 고성능 모델 배치
- **수동 캐싱 전략**: 성공적인 결과물을 저장하고 재사용하여 시간과 비용 절약
- **병렬 처리의 힘**: 독립적인 작업을 동시에 실행하여 대기 시간 단축

**예를 들어**, 7장에서 만든 "콘텐츠 생성 파이프라인"을 개선한다면:
- ✅ 리서치 단계는 빠른 모델로 (5초 → 2초)
- ✅ 최종 검수만 고급 모델 사용 (품질 유지 + 비용 60% 절감)
- ✅ 자주 쓰는 리서치 결과는 저장해두고 재사용

8장은 "일잘러의 성능 튜닝 비법"입니다. 워크플로우는 잘 만들었는데 느리거나 비싸다면, [8장으로 이동하세요 →](vol-1-part-3-chapter-08.md)
