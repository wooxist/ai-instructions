# 10장 4부: 미래를 향한 아키텍처

---

## 10.10 계층적 에이전트 협력 시스템

- **상황:** 신제품 출시를 위한 종합 마케팅 캠페인을 기획하고 실행하는 프로젝트. 보스-비서-매니저-워커의 4계층 구조를 활용하며, 각자의 역할과 책임에 따라 명확한 보고 및 지시 라인을 따릅니다.

#### 최종 인스트럭션 시스템 예시

이 시스템은 각 계층의 역할과 데이터 흐름을 명확히 정의한 워크플로우 기반 시스템으로 설계됩니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/new_product_campaign/
├── workflow.yaml
└── agents/
    ├── 01_boss.md
    ├── 02_secretary.md
    ├── 03_content_manager.md
    ├── 04_performance_manager.md
    └── 05_pr_manager.md
    # ... 워커 에이전트들은 매니저가 동적으로 호출한다고 가정
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
`workflow.yaml`은 보스의 목표 설정을 시작으로 비서의 계획 수립, 매니저들의 병렬 실행, 다시 비서의 취합 및 보고, 최종 보스의 의사결정으로 이어지는 전체 흐름을 정의합니다.

```yaml
# workflow.yaml
name: New Product Marketing Campaign
trigger: Manual

steps:
  - name: 1. Set Goal
    agent: agents/01_boss.md
    inputs:
      - product_info: "신제품 '오토 클린봇'은 AI 기반 자동 청소 로봇..."
    outputs:
      - file: campaign_goal.json

  - name: 2. Create Action Plan
    agent: agents/02_secretary.md
    inputs:
      - file: campaign_goal.json
    outputs:
      - file: plan_for_content_manager.md
      - file: plan_for_performance_manager.md
      - file: plan_for_pr_manager.md

  - name: 3. Execute Plans (Parallel)
    type: parallel
    steps:
      - name: 3a. Content Team Execution
        agent: agents/03_content_manager.md
        inputs:
          - file: plan_for_content_manager.md
        outputs:
          - file: content_report.json

      - name: 3b. Performance Team Execution
        agent: agents/04_performance_manager.md
        inputs:
          - file: plan_for_performance_manager.md
        outputs:
          - file: performance_report.json

      - name: 3c. PR Team Execution
        agent: agents/05_pr_manager.md
        inputs:
          - file: plan_for_pr_manager.md
        outputs:
          - file: pr_report.json

  - name: 4. Consolidate Reports
    agent: agents/02_secretary.md # 비서 에이전트 재사용
    inputs:
      - file: content_report.json
      - file: performance_report.json
      - file: pr_report.json
    outputs:
      - file: final_summary_for_boss.md

  - name: 5. Make Final Decision
    agent: agents/01_boss.md # 보스 에이전트 재사용
    inputs:
      - file: final_summary_for_boss.md
    outputs:
      - text: final_decision.txt
```

**3. 에이전트 인스트럭션 예시**

- **`agents/01_boss.md` (보스 에이전트)**
```markdown
# 역할: 마케팅 총괄 디렉터

# 목표
입력된 정보(신제품 정보 또는 종합 보고서)를 바탕으로, 캠페인의 최종 목표를 설정하거나 다음 단계를 의사결정한다.

# 처리 방법
- **입력이 [신제품 정보]일 경우:** "출시 3개월 내 10,000명의 얼리어답터 확보"와 같이 명확하고 측정 가능한 목표를 설정한다.
- **입력이 [종합 보고서]일 경우:** 보고서 내용을 바탕으로 "캠페인 승인", "전략 수정 후 재보고", "캠페인 보류" 중 하나를 결정하고 그 이유를 간략히 서술한다.
```

- **`agents/02_secretary.md` (비서 에이전트)**
```markdown
# 역할: 전략 보좌관

# 목표
보스의 지시를 이행 가능한 계획으로 만들거나, 매니저들의 보고를 종합하여 보스가 의사결정하기 쉽게 만든다.

# 처리 방법
- **입력이 [캠페인 목표]일 경우:** 목표를 달성하기 위해 콘텐츠, 퍼포먼스 마케팅, PR 각 팀이 수행해야 할 핵심 과업과 KPI를 담은 실행 계획안(마크다운)을 각각 생성하여 전달한다.
- **입력이 [팀별 보고서]일 경우:** 3개 팀의 보고서를 모두 취합하여, 캠페인 목표 달성률, 핵심 성과, 문제점, 다음 단계 제안을 포함한 단일 요약 보고서(마크다운)를 생성한다.
```

- **`agents/03_content_manager.md` (매니저 에이전트 예시)**
```markdown
# 역할: 콘텐츠 마케팅 매니저

# 목표
비서에게 전달받은 실행 계획에 따라, 필요한 워커 에이전트들을 오케스트레이션하여 콘텐츠를 생산하고 결과를 보고한다.

# 처리 방법
1. 실행 계획을 분석하여 필요한 콘텐츠 목록(블로그, 영상, SNS)을 확정한다.
2. **[오케스트레이션]** 각 콘텐츠에 맞는 워커 에이전트(블로그 작성 워커, 영상 스크립트 워커 등)를 순차적 또는 병렬적으로 호출한다.
3. 워커들의 결과물을 취합하고 품질을 검수한다.
4. 계획 대비 달성률, 생성된 콘텐츠 목록, 주요 성과(조회수, 참여율)를 담은 `content_report.json`을 생성하여 비서에게 보고한다.
```

#### 설계 분석
- **메타 원칙 (4장):** **SoC(관심사 분리)** 원칙에 따라 보스(전략), 비서(조율/정보), 매니저(전술), 워커(실행)의 역할이 명확히 분리되었습니다. `workflow.yaml`이 **SSOT(단일 진실 공급원)** 역할을 하여 전체 프로세스의 흐름을 정의합니다.
- **에이전트 설계 (5장):** 각 에이전트는 명확한 **책임**을 가집니다. 특히 비서는 상위 목표를 구체적인 실행 계획으로 '번역'하고 하위 보고를 다시 상위 레벨의 정보로 '요약'하는 '정보의 허브' 역할을, 매니저는 하위 워커들을 관리하는 '오케스트레이터' 역할을 수행하도록 설계되었습니다.
- **입/출력 설계 (6장):** 각 단계의 입출력이 명확한 파일(`.json`, `.md`)로 정의되어, 에이전트 간의 데이터 **핸드오프**가 안정적으로 이루어집니다.
- **워크플로우 설계 (7장):** **파이프라인 패턴**을 기반으로 하되, 3개의 매니저가 동시에 작업을 수행하는 **병렬 처리 패턴**을 도입하여 효율성을 높였습니다. 또한 비서와 보스 에이전트가 워크플로우의 다른 단계에서 **재사용**되는 모습을 보여줍니다.

#### 현실적인 구현의 어려움: '매니저'의 지능과 오케스트레이션
이 계층적 모델은 개념적으로 강력하지만, 실제 구현 시에는 **'매니저 에이전트'의 지능**이 가장 큰 허들로 작용합니다. 매니저는 단순히 주어진 일을 하는 것을 넘어, 다음과 같은 고차원적인 '오케스트레이션' 역할을 수행해야 합니다.

- **동적 작업 분해:** 비서에게 받은 추상적인 계획(`plan_for_content_manager.md`)을 보고, 이를 실행 가능한 구체적인 하위 태스크(예: '블로그 초안 작성', 'SNS 이미지 생성')로 스스로 분해해야 합니다.
- **워커 조율:** 분해된 태스크에 가장 적합한 워커 에이전트를 선택하고, 이들의 작업 순서(순차/병렬)를 결정하며, 작업 상태를 관리해야 합니다.
- **결과 종합 및 보고:** 여러 워커의 결과물을 취합하고 품질을 검수한 뒤, 상위 계층(비서)이 이해할 수 있는 형태의 보고서로 종합해야 합니다.

이러한 역할은 LLM의 추론 능력만으로 완전 자동화하기에는 아직 어려움이 따르며, 예측 불가능한 비용과 지연 시간을 초래할 수 있습니다.

#### 해결책: 인간과 협력하는 계층 모델
이러한 어려움은 **'인간의 개입(Human-in-the-Loop)'**을 통해 해결할 수 있습니다. AI가 모든 의사결정을 자율적으로 수행하는 대신, 인간 관리자를 보조하는 '지능형 팀장' 역할을 맡는 것입니다.

- **인간이 '보스'가 되다:** 워크플로우의 시작인 `1. Set Goal`과 마지막인 `5. Make Final Decision` 단계는 AI가 아닌 **인간 관리자**가 직접 수행합니다. AI '보스 에이전트'는 인간의 결정을 시스템이 이해할 수 있는 `campaign_goal.json` 형식으로 변환해주는 '비서' 역할을 합니다.
- **인간이 '매니저'를 감독하다:** AI '매니저 에이전트'가 생성한 작업 계획(1단계)이나 워커들의 결과물(3단계)이 중요한 분기점마다 인간 팀장의 검토와 승인을 받도록 워크플로우에 `approval` 단계를 추가할 수 있습니다.

이처럼 인간이 시스템의 핵심적인 의사결정 지점에 위치함으로써, AI는 복잡한 추론의 부담을 덜고 자신이 가장 잘하는 '실행'에 집중할 수 있습니다. 이로써 계층적 협력 모델은 더 이상 미래의 아키텍처가 아닌, 지금 당장 조직의 복잡한 문제를 해결하는 데 적용할 수 있는 매우 실용적인 패턴이 됩니다.

---

## 10.11 수평적 에이전트 협력 시스템

- **상황:** 스타트업 투자 검토를 위한 실사(Due Diligence). 법률, 재무, 기술, 시장 4개 영역의 전문가 에이전트가 동등한 위치에서 협력하며, 코디네이터가 전체 프로세스를 오케스트레이션합니다.

#### 최종 인스트럭션 시스템 예시

이 시스템은 전문가들의 병렬 분석과 그 결과를 종합하는 명확한 2단계 워크플로우로 설계됩니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/due_diligence/
├── workflow.yaml
└── agents/
    ├── 00_coordinator.md      # 전체 프로세스를 지휘하는 코디네이터
    ├── 01_legal_expert.md
    ├── 02_financial_expert.md
    ├── 03_technical_expert.md
    ├── 04_market_expert.md
    └── 05_synthesizer.md      # 4개의 보고서를 종합하는 에이전트
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
`workflow.yaml`은 전문가들의 병렬 분석(Fork)과 종합 에이전트의 결과 취합(Join) 과정을 정의합니다.

```yaml
# workflow.yaml
name: Startup Due Diligence
trigger: Manual

steps:
  - name: 1. Expert Analysis (Parallel)
    type: parallel
    steps:
      - name: 1a. Legal Review
        agent: agents/01_legal_expert.md
        inputs:
          - company_data: "{{initial_data}}"
        outputs:
          - file: legal_report.json

      - name: 1b. Financial Review
        agent: agents/02_financial_expert.md
        inputs:
          - company_data: "{{initial_data}}"
        outputs:
          - file: financial_report.json

      - name: 1c. Technical Review
        agent: agents/03_technical_expert.md
        inputs:
          - company_data: "{{initial_data}}"
        outputs:
          - file: technical_report.json

      - name: 1d. Market Review
        agent: agents/04_market_expert.md
        inputs:
          - company_data: "{{initial_data}}"
        outputs:
          - file: market_report.json

  - name: 2. Synthesize and Conclude
    agent: agents/05_synthesizer.md
    inputs:
      - file: legal_report.json
      - file: financial_report.json
      - file: technical_report.json
      - file: market_report.json
    outputs:
      - file: final_investment_report.json
```

**3. 에이전트 인스트럭션 예시**

- **`agents/00_coordinator.md` (코디네이터 에이전트)**
```markdown
# 역할: 투자 실사 프로세스 코디네이터

# 목표
사용자로부터 투자 대상 회사 정보를 입력받아, `workflow.yaml`에 정의된 전체 실사 프로세스를 실행하고 최종 보고서를 사용자에게 전달한다.

# 처리 방법
1. `workflow.yaml`을 로드한다.
2. **[1단계: 병렬 분석]** 4개의 전문가 에이전트(법률, 재무, 기술, 시장)를 동시에 호출하여 각자의 분석을 지시한다.
3. 4개의 보고서가 모두 생성될 때까지 대기한다.
4. **[2단계: 종합]** 4개의 보고서를 입력으로 하여 `05_synthesizer.md` 에이전트를 호출한다.
5. `Synthesizer`로부터 최종 보고서를 받으면, 사용자에게 전달하고 프로세스를 종료한다.
```

- **`agents/05_synthesizer.md` (종합 에이전트)**
```markdown
# 역할: 수석 투자 애널리스트

# 목표
4개의 전문가 보고서를 종합하여, 교차 검증을 수행하고 최종 투자 추천안을 생성한다.

# 처리 방법
1. 4개의 보고서(법률, 재무, 기술, 시장)를 모두 입력받는다.
2. 각 보고서의 점수와 핵심 내용을 요약한다.
3. **[교차 검증]** 보고서 간의 연관성이나 모순점을 분석한다.
   - 예: "기술 보고서의 '높은 기술 부채'는 재무 보고서의 '향후 R&D 비용 증가' 리스크와 직접적으로 연결됨."
4. 미리 정의된 가중치(예: 기술 40%, 시장 30%, 재무 20%, 법률 10%)를 적용하여 종합 점수를 계산한다.
5. 종합 점수와 핵심 위험 요인('Red Flags')을 바탕으로 최종 투자 의견('투자', '보류', '거부')을 결정한다.
6. 최종 결과를 `final_investment_report.json` 스키마에 맞춰 생성한다.
```

#### 설계 분석
- **메타 원칙 (4장):** **MECE** 원칙에 따라 4개 전문가 영역이 상호 배타적이면서 전체를 포괄합니다. **SoC(관심사 분리)** 원칙은 프로세스 관리(코디네이터), 전문 분석(전문가), 종합 판단(종합 에이전트)의 역할을 명확히 나눕니다.
- **에이전트 설계 (5장):** 각 에이전트는 명확한 **책임**을 가집니다. 특히 코디네이터는 계층적 구조의 '비서'와 달리, 목표를 해석하는 대신 정해진 **프로세스를 충실히 실행**하는 역할에 집중합니다. 전문가들은 동등한 위치에서 각자의 전문성을 발휘합니다.
- **워크플로우 설계 (7장):** **병렬 처리(Fork-Join) 패턴**을 사용하여, 독립적인 작업들을 동시에 수행함으로써 전체 프로세스의 시간을 단축합니다. 이는 각 전문가의 분석이 서로에게 영향을 주지 않는 상황에 매우 효과적인 설계입니다.

---

## 미래를 향한 아키텍처: 자기 생성 및 개선 시스템

---

## 10.12 시스템을 '생성'하는 메타 에이전트 (아키텍트)

이 패턴에서 메타 에이전트는 한 단계 더 나아가, 새로운 비즈니스 요구사항에 맞춰 시스템의 구성요소(새로운 에이전트, 스키마, 워크플로우)를 **'설계하고 생성'**하는 아키텍트 역할을 합니다.

- **상황:** `10.9`의 '주간 고객 리뷰 분석 시스템'에 마케팅팀으로부터 "고객 리뷰에 언급된 경쟁사 제품과 그에 대한 감성을 분석하는 기능을 추가해달라"는 새로운 요구사항이 접수되었다.
- **에이전트 역할:** AI 시스템 아키텍트 에이전트 (메타 에이전트)

#### 최종 인스트럭션 예시
```markdown
# 역할: AI 시스템 아키텍트 에이전트

# 목표
주어진 [신규 요구사항]을 충족시키기 위해, '주간 고객 리뷰 분석 시스템'을 분석하고 필요한 구성요소를 새로 생성하여 시스템을 확장한다.

# 입력 데이터
1. **신규 요구사항**: "고객 리뷰에서 경쟁사(예: '타사 클리너', '라이벌 봇')가 언급되는지 추적하고, 해당 리뷰의 감성을 요약해달라."
2. **기존 시스템 구성요소**:
   - `/instructions/weekly_review_report/workflow.yaml`
   - `/instructions/weekly_review_report/schemas/report.schema.json`

# 처리 방법
1. [신규 요구사항]을 분석하여, 필요한 신규 기능(경쟁사 분석)을 정의한다.
2. 기존 시스템에 해당 기능이 없음을 확인하고, **'04_competitor_analyzer.md'** 라는 새로운 에이전트가 필요하다고 판단한다.
3. 신규 에이전트의 역할, 처리 방법, 입출력 형식을 포함하는 인스트럭션(`04_competitor_analyzer.md`)을 **생성**한다.
4. 최종 보고서에 경쟁사 분석 결과를 포함시키기 위해, 기존 `report.schema.json`에 `competitor_summary` 섹션을 추가한 **수정된 스키마(`v2`)**를 **생성**한다.
5. 기존 `workflow.yaml`을 분석하여, 신규 에이전트를 '2단계(정보 추출)'와 '3단계(요약 생성)' 사이에 삽입한 **수정된 워크플로우(`v2`)**를 **생성**한다.

# 출력물
1. **신규 에이전트 파일**: `04_competitor_analyzer.md`의 전체 내용.
2. **수정된 스키마 파일**: `report.schema.v2.json`의 전체 내용.
3. **수정된 워크플로우 파일**: `workflow.v2.yaml`의 전체 내용.
```

#### 설계 분석
- **자기 확장 시스템:** '아키텍트 에이전트'는 단순히 기존 시스템을 수정하는 것을 넘어, 새로운 요구사항에 맞춰 스스로 새로운 '능력'(에이전트)을 만들어내고 시스템의 구조를 변경합니다. 이는 AI 시스템이 외부의 개입 없이도 스스로 발전하고 확장할 수 있는 가능성을 보여주는 매우 강력한 패턴입니다.
- **궁극적인 역할:** 고도로 발전된 아키텍트 에이전트는 비즈니스 과업을 수행하는 에이전트뿐만 아니라, 시스템의 품질과 효율을 관리하는 **'최적화 에이전트(10.13)'**나 **'평가 에이전트(10.14)'**와 같은 **메타 에이전트 자체를 생성**할 수도 있습니다. 이는 시스템이 스스로의 유지보수 체계까지 구축하는 높은 수준의 자율성을 의미합니다.

---

### 현실적인 구현: 인간과 협력하는 아키텍트 에이전트

앞서 설명한 완전 자율적인 아키텍트 에이전트는 구현 난이도가 매우 높습니다. 하지만 여기에 **'인간의 개입(Human-in-the-Loop)'**을 추가하면 훨씬 더 현실적이고 안전한 시스템을 만들 수 있습니다. 즉, AI가 시스템 전체를 '창조'하는 것이 아니라, 인간 아키텍트를 보조하는 '지능형 조수' 역할을 수행하는 것입니다.

#### 협력 워크플로우 예시 (`meta_workflow.yaml`)

아래는 아키텍트 에이전트가 인간과 협력하여 시스템을 확장하는 과정을 정의한 워크플로우입니다.

```yaml
# /instructions/system_management/meta_workflow.yaml
name: Human-Collaborative System Expansion
trigger: Manual

steps:
  - name: 1. Propose Expansion Plan
    agent: agents/architect_agent.md # 10.12의 아키텍트 에이전트
    inputs:
      - request: "고객 리뷰에서 경쟁사 분석 기능 추가"
      - system_structure: "..." # 현재 시스템의 파일 구조 정보
    outputs:
      - file: expansion_plan.md

  - name: 2. Human Approves Plan
    type: human_in_the_loop
    instructions: |
      다음 시스템 확장 계획을 검토하고 승인해주세요.
      수정이 필요하다면, 계획을 직접 수정하여 다음 단계로 전달해주세요.
      ---
      {{ file: expansion_plan.md }}
    outputs:
      - file: approved_plan.md

  - name: 3. Generate Components
    agent: agents/architect_agent.md # 동일한 에이전트 재사용
    inputs:
      - request: "승인된 계획에 따라, 필요한 파일들의 전체 내용을 생성하라."
      - plan: "{{ file: approved_plan.md }}"
    outputs:
      - file: generated_components.json # 생성된 파일들의 내용이 담긴 JSON

  - name: 4. Human Reviews Code
    type: human_in_the_loop
    instructions: |
      AI가 생성한 아래 파일들의 내용을 최종 검토하고 승인해주세요.
      ---
      {{ file: generated_components.json }}
    outputs:
      - file: final_components.json

  - name: 5. Apply Changes
    tool: file_system_writer
    inputs:
      - components: "{{ file: final_components.json }}"
    outputs:
      - status: "Changes applied successfully."
```

#### 설계 분석

- **역할 변화:** AI는 더 이상 '전지전능한 설계자'가 아닌, '유능한 조수'가 됩니다. AI는 계획을 제안하고 코드를 생성하는 '초안 작성'의 역할을, 인간은 최종 의사결정과 검증의 '책임'을 집니다.
- **안전성 확보:** 2단계(계획 승인)와 4단계(코드 검토)에서 인간이 개입함으로써, AI의 실수로 인해 전체 시스템이 망가지는 치명적인 위험을 방지할 수 있습니다.
- **점진적 자동화:** 처음에는 모든 단계를 인간이 꼼꼼히 검토하지만, 시스템이 안정화되고 AI의 성능이 신뢰를 얻게 되면, 점차 간단한 변경은 자동으로 승인하는 식으로 자동화의 범위를 점진적으로 넓혀갈 수 있습니다.

이처럼 '인간과의 협력'을 전제로 설계하면, 10.12절의 메타 에이전트는 더 이상 먼 미래의 이야기가 아닌, 지금 당장 시도해볼 수 있는 매우 강력하고 실용적인 자동화 패턴이 됩니다.

## 10.13 시스템을 '개선'하는 메타 에이전트 (최적화)

이 패턴에서 메타 에이전트는 기존 시스템의 **'유지보수 및 최적화'** 담당자 역할을 합니다. 시스템의 성능 로그나 비용 데이터를 분석하여, 더 효율적으로 만들기 위해 기존의 인스트럭션이나 워크플로우를 **수정**합니다.

- **상황:** `10.9`의 '주간 고객 리뷰 분석 시스템'이 잘 운영되고 있지만, "API 비용이 너무 많이 나온다"는 새로운 비즈니스 요구사항이 발생했다.
- **에이전트 역할:** AI 시스템 최적화 에이전트 (메타 에이전트)

#### 최종 인스트럭션 예시
```markdown
# 역할: AI 시스템 최적화 에이전트 (메타 에이전트)

# 목표
현재 운영 중인 '주간 고객 리뷰 분석 시스템'의 API 비용을 20% 절감하라. 단, 최종 보고서의 품질(정확도)은 5% 이상 하락해서는 안 된다.

# 입력 데이터
1. 현재 시스템의 모든 인스트럭션 파일 (`/instructions/weekly_review_report/`)
2. 지난 1달간의 성능 로그 데이터 (`perf_log.csv`)

# 기초 지식 및 원칙
- **성능의 삼각형 (8장):** 모든 결정은 품질, 비용, 속도 간의 트레이드오프를 고려해야 한다.
- **관심사 분리 (SoC, 4장):** 에이전트의 역할을 분리하거나 통합하는 제안을 할 때, 각 에이전트가 단일 책임을 갖도록 유도해야 한다.
- **산출물 중심 (6장):** 변경을 제안할 때는, 변경된 산출물의 형식과 구조를 명확히 정의해야 한다.
- **점진적 개선 (7장):** 한 번에 많은 것을 바꾸기보다, 측정 가능한 작은 단위를 변경하고 테스트하는 계획을 선호한다.
- **데이터 기반 평가 (9장):** 모든 개선 제안은 반드시 A/B 테스트와 같은 정량적 평가 계획을 동반해야 한다.

# 처리 방법
1. `[#기초 지식 및 원칙]`을 바탕으로, `[#입력 데이터]`를 분석하여 `[#목표]`를 달성하기 위한 계획을 수립한다.
2. 비용이 가장 많이 발생하는 에이전트나 단계를 식별한다.
3. 비용 절감을 위한 개선 가설을 2가지 이상 수립한다.
   - 가설 예시 1: "Classifier 에이전트와 Extractor 에이전트를 하나의 '분류 및 추출' 에이전트로 통합하여, API 호출 횟수를 1회 줄인다."
   - 가설 예시 2: "Summarizer 에이전트의 인스트럭션에 '결과는 최대한 간결하게'라는 제약 조건을 추가하여 출력 토큰을 줄인다."
4. 각 가설에 따라, 관련된 인스트럭션 파일의 수정안(`v2`)을 생성한다.
5. 생성된 수정안을 검증하기 위한 A/B 테스트 실행 계획서를 작성한다.

# 출력물
- 수정된 인스트럭션 파일(들)의 내용.
- A/B 테스트 실행 계획서.
```

#### A/B 테스트 실행 계획서 예시

최적화 에이전트가 생성하는 "A/B 테스트 실행 계획서"는 다음과 같은 구체적인 내용을 담게 됩니다. 이는 '감'이 아닌 데이터에 기반하여 인스트럭션의 변경이 실제로 긍정적인 효과를 가져왔는지 과학적으로 증명하는 과정입니다.

> **A/B 테스트: 'Summarizer' 에이전트 최적화 검증**
>
> - **가설:** `Summarizer` 인스트럭션에 '간결성' 제약을 추가하면, 품질 저하를 최소화하면서 API 비용을 20% 이상 절감할 수 있다.
>
> **1. 테스트 준비 (Prepare)**
> *   **A (기존 버전):** 현재 운영 중인 `Summarizer.md` 인스트럭션.
> *   **B (신규 버전):** "결과는 최대한 간결하게" 제약이 추가된 `Summarizer_v2.md` 인스트럭션.
> *   **평가 데이터:** 지난주 수집된 실제 고객 리뷰 100건 (`golden_dataset.csv`).
>
> **2. 실행 (Execute)**
> *   `golden_dataset.csv`의 모든 리뷰를 A 버전에 입력하여 결과(`results_A.json`)를 생성한다.
> *   동일한 `golden_dataset.csv`를 B 버전에 입력하여 결과(`results_B.json`)를 생성한다.
>
> **3. 측정 및 채점 (Measure)**
> *   **비용 측정:** 각 버전의 API 호출에 사용된 총 토큰 수를 비교한다.
> *   **품질 측정:** `10.14`의 '평가 에이전트' 로직을 사용하여 `results_A.json`과 `results_B.json`을 각각 채점하고 평균 점수를 비교한다.
>
> **4. 판정 기준 (Decide)**
> *   **성공 조건:** B 버전의 비용이 A 버전 대비 **20% 이상 감소**하고, 품질 점수 하락이 **5% 이내**일 경우, 테스트는 '성공'으로 판정한다.
> *   **실패 조건:** 위 조건을 만족하지 못할 경우, '실패'로 판정하고 기존 A 버전을 유지한다.

#### 설계 분석
- **입/출력 설계 (6장):** 이 에이전트의 **입력**은 다른 에이전트의 인스트럭션 파일과 성능 로그 데이터이며, **출력**은 수정된 인스트럭션 파일과 테스트 계획서입니다. 즉, 코드(인스트럭션)를 입력받아 코드를 출력하는 '코드 생성 코드'와 같은 구조입니다.
- **워크플로우 설계 (7장):** '분석 → 가설 수립 → 수정안 생성 → 검증 계획 수립'이라는 고수준의 **워크플로우**를 내부적으로 따릅니다. 특히 마지막 '검증' 단계에서는 **10.14에서 다루는 '평가 에이전트'와 같은 자동화된 평가 시스템을 활용**하여, 자신의 개선안이 실제로 효과가 있었는지 데이터 기반으로 증명합니다.
- **에이전트 설계 (5장):** '시스템 최적화 에이전트'라는 고도의 **역할**을 부여받아, 다른 에이전트들의 설계를 변경하는 메타 작업을 수행합니다.

---

### 현실적인 구현: 인간과 협력하는 최적화 에이전트

완전 자율적인 최적화 에이전트는 데이터 분석, 전략 수립, 트레이드오프 고려 등 매우 높은 수준의 추론 능력을 요구하여 구현이 어렵습니다. 하지만 이 패턴 역시 **'인간의 개입(Human-in-the-Loop)'**을 추가하면, AI를 '유능한 시스템 분석가'로 활용하는 현실적인 시스템으로 만들 수 있습니다.

#### 협력 워크플로우 예시 (`meta_optimizer_workflow.yaml`)

```yaml
# /instructions/system_management/meta_optimizer_workflow.yaml
name: Human-Collaborative System Optimization
trigger: Manual

steps:
  - name: 1. Analyze and Propose Options
    agent: agents/optimizer_agent.md # 10.13의 최적화 에이전트
    inputs:
      - goal: "API 비용 20% 절감"
      - perf_log: "perf_log.csv"
    outputs:
      - file: optimization_options.md # AI가 제안하는 여러 최적화 방안

  - name: 2. Human Selects Strategy
    type: human_in_the_loop
    instructions: |
      다음 최적화 방안들을 검토하고, 가장 합리적인 전략 하나를 선택해주세요.
      각 옵션의 장단점(예상 비용 절감 vs. 품질 저하 리스크)을 고려하여 결정해주세요.
      ---
      {{ file: optimization_options.md }}
    outputs:
      - variable: selected_strategy

  - name: 3. Generate Modified Instructions
    agent: agents/optimizer_agent.md # 동일 에이전트 재사용
    inputs:
      - request: "선택된 전략 '{{selected_strategy}}'에 따라, 관련된 인스트럭션 파일의 수정안과 A/B 테스트 계획을 생성하라."
    outputs:
      - file: modification_plan.json # 수정될 파일 내용과 테스트 계획이 담긴 JSON

  - name: 4. Human Approves Changes
    type: human_in_the_loop
    instructions: |
      AI가 생성한 아래 변경안과 테스트 계획을 최종 검토하고 승인해주세요.
      ---
      {{ file: modification_plan.json }}
    outputs:
      - file: approved_plan.json

  - name: 5. Execute A/B Test
    tool: ab_test_runner # 10.14의 평가 에이전트를 실행하는 도구
    inputs:
      - plan: "{{ file: approved_plan.json }}"
    outputs:
      - file: test_report.md
```

#### 설계 분석

- **역할 재정의:** AI는 더 이상 '자율적인 의사결정자'가 아닌, 데이터에 기반한 여러 '개선 옵션'과 그 장단점을 제시하는 '컨설턴트'가 됩니다. 최종 전략을 선택하는 책임은 인간 관리자에게 있습니다.
- **리스크 관리:** AI가 시스템을 잘못된 방향으로 '최적화'하여 품질을 크게 해치는 위험을 인간의 검토(2단계, 4단계)를 통해 사전에 방지할 수 있습니다.
- **데이터 기반 의사결정:** 인간은 '감'이 아닌, AI가 분석해준 데이터와 예상 효과를 바탕으로 더 합리적인 의사결정을 내릴 수 있습니다. 최종적으로 5단계에서 실행되는 A/B 테스트는 이 결정이 옳았는지 과학적으로 검증하는 역할을 합니다.

## 10.14 '평가 에이전트' 직접 만들어보기

앞선 `10.12`에서는 아키텍트 에이전트가 다른 에이전트를 생성하는 패턴을 살펴보았습니다. 이 섹션에서는 바로 그 아키텍트 에이전트가 **최종 목표물로 삼아야 할 '평가 에이전트'의 구체적인 구현 설계도**를 실제 코드를 통해 알아봅니다. 이 예제는 개념을 구체화하고, 독자가 직접 활용할 수 있는 실용적인 청사진을 제공합니다.

9장에서 우리는 인스트럭션을 객관적으로 평가하는 방법과 '평가 에이전트'의 개념에 대해 배웠습니다. 이 섹션에서는 그 개념을 실제 파이썬 코드로 구현하는 구체적인 예제를 다룹니다. 이 예제를 통해 여러분은 더 이상 '감'이 아닌 데이터로 프롬프트의 성능을 측정하는 방법을 직접 경험하게 될 것입니다.

### 시나리오

비정형 텍스트에서 사용자의 이름과 이메일을 JSON 형식으로 추출하는 작업을 가정해 봅시다. 우리는 두 가지 버전의 프롬프트를 테스트하여 어느 것이 더 안정적으로 정확한 JSON을 생성하는지 평가하고자 합니다.

### 사전 준비물

- **Python 3.7 이상**이 설치된 환경
- **OpenAI API 키:** OpenAI 플랫폼에서 발급받은 API 키가 필요합니다. 스크립트를 실행하기 전에 환경 변수로 키를 설정해야 합니다.
  ```bash
  export OPENAI_API_KEY='sk-...' # 실제 키로 대체
  ```
- **OpenAI 라이브러리 설치:** 
  ```bash
  pip install openai
  ```

### 1단계: 평가 데이터셋과 프롬프트 준비

먼저 테스트에 사용할 '골든 데이터셋'과 성능을 비교할 두 프롬프트를 정의합니다.

- **골든 데이터셋:** 테스트할 입력(input)과, 해당 입력에 대한 완벽한 정답(ground_truth)의 쌍으로 구성됩니다.
- **프롬프트 A:** 간단하고 직접적인 요청.
- **프롬프트 B:** Few-shot 예시와 더 명확한 출력 형식을 포함한 개선된 요청.

### 2단계: '평가 에이전트' 코드 작성 (Python)

이제 전체 프로세스를 자동화하는 파이썬 스크립트를 작성합니다. 이 스크립트가 바로 우리의 '평가 에이전트'입니다.

```python
import os
import json
from openai import OpenAI

# 1. 사전 준비
# ----------------------------------------------------------------------------
# OpenAI 클라이언트 초기화
# 코드가 환경 변수에서 API 키를 자동으로 읽어들입니다.
client = OpenAI()

# 골든 데이터셋 정의
golden_dataset = [
    {
        "id": "case1",
        "input": "제 이름은 김민준이고, 이메일은 mj.kim@example.com 입니다. 연락주세요.",
        "ground_truth": {"name": "김민준", "email": "mj.kim@example.com"}
    },
    {
        "id": "case2",
        "input": "연락처: 이서연 (sy.lee@example.com)",
        "ground_truth": {"name": "이서연", "email": "sy.lee@example.com"}
    },
    {
        "id": "case3",
        "input": "박지훈입니다. 이메일 주소는 없지만, 제 웹사이트는 phoon.co 입니다.",
        "ground_truth": {"name": "박지훈", "email": None}
    }
]

# 프롬프트 버전 정의
prompt_a = """
다음 텍스트에서 이름과 이메일 주소를 추출하여 JSON 형식으로 반환하세요.
TEXT: {text}
"""

prompt_b = """
당신은 텍스트에서 개인 정보를 추출하는 전문 AI입니다.
주어진 텍스트에서 이름(name)과 이메일(email)을 추출하여 JSON 형식으로 반환하세요.

# 예시
- Text: "담당자는 최수빈이고, 이메일은 sb.choi@example.com 입니다."
- Output: {{"name": "최수빈", "email": "sb.choi@example.com"}}

# 규칙
- 만약 이메일 주소가 없다면, email 필드의 값은 null로 설정하세요.
- 다른 말은 절대 하지 말고, JSON 객체만 반환해야 합니다.

TEXT: {text}
"""

prompts = {"prompt_a": prompt_a, "prompt_b": prompt_b}

# 2. 핵심 함수 정의
# ----------------------------------------------------------------------------
def get_llm_response(prompt, text):
    """주어진 프롬프트와 텍스트로 LLM API를 호출하는 함수"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.format(text=text)}
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def judge_response(response_text, ground_truth):
    """LLM-as-a-Judge: 결과물을 평가하고 점수를 매기는 함수"""
    score = 0
    # 평가 기준 1: 유효한 JSON인가?
    try:
        response_json = json.loads(response_text)
        score += 50
    except json.JSONDecodeError:
        return 0 # JSON 파싱 실패 시 0점 처리

    # 평가 기준 2: 추출된 데이터가 정답과 일치하는가?
    if response_json.get("name") == ground_truth.get("name") and \
       response_json.get("email") == ground_truth.get("email"):
        score += 50
    
    return score

# 3. 평가 에이전트 실행
# ----------------------------------------------------------------------------
results = {}

for prompt_name, prompt_template in prompts.items():
    print(f"--- {prompt_name.upper()} 평가 시작 ---")
    total_score = 0
    prompt_results = []

    for item in golden_dataset:
        case_id = item["id"]
        input_text = item["input"]
        truth = item["ground_truth"]

        # 1. LLM으로부터 답변 생성
        response = get_llm_response(prompt_template, input_text)

        # 2. 심판(Judge)을 통해 결과 채점
        score = judge_response(response, truth)
        total_score += score

        prompt_results.append({
            "case_id": case_id,
            "response": response,
            "score": score
        })
        print(f"  Case {case_id}: Score {score}/100")

    results[prompt_name] = {
        "details": prompt_results,
        "average_score": total_score / len(golden_dataset)
    }
    print(f"--- {prompt_name.upper()} 평가 종료 ---
")

# 4. 최종 리포트 생성
# ----------------------------------------------------------------------------
print("========== 최종 평가 리포트 ==========")
for prompt_name, result_data in results.items():
    print(f"프롬프트: {prompt_name}")
    print(f"  평균 점수: {result_data['average_score']:.2f}")
print("======================================")

# 상세 결과 출력 (옵션)
# import pprint
# pprint.pprint(results)

```

### 3단계: 실행 및 결과 리포트 확인

위 스크립트를 `evaluation_agent.py`로 저장하고 터미널에서 실행합니다.

```bash
python evaluation_agent.py
```

스크립트가 실행되면, 각 프롬프트와 각 테스트 케이스에 대한 채점 과정을 볼 수 있습니다. 모든 평가가 끝나면 다음과 같은 최종 리포트를 얻게 됩니다.

```
--- PROMPT_A 평가 시작 ---
  Case case1: Score 100/100
  Case case2: Score 0/100
  Case case3: Score 0/100
--- PROMPT_A 평가 종료 ---

--- PROMPT_B 평가 시작 ---
  Case case1: Score 100/100
  Case case2: Score 100/100
  Case case3: Score 100/100
--- PROMPT_B 평가 종료 ---

========== 최종 평가 리포트 ==========
프롬프트: prompt_a
  평균 점수: 33.33
프롬프트: prompt_b
  평균 점수: 100.00
======================================
```

이 리포트를 통해 우리는 **프롬프트 B가 프롬프트 A보다 훨씬 더 안정적으로 원하는 결과물을 생성한다**는 사실을 '감'이 아닌 '데이터'로 명확히 증명할 수 있습니다. 프롬프트 A는 간단한 케이스는 잘 처리했지만, 형식이 조금만 달라지거나 예외적인 상황(이메일 없음)에서는 실패했기 때문입니다.

#### 설계 분석
- **메타 원칙 (9장):** **데이터 기반 의사결정** 원칙의 핵심을 보여줍니다. '감'에 의존한 프롬프트 튜닝이 아닌, 정량적 데이터를 통해 어떤 버전이 더 나은지 객관적으로 판단할 수 있습니다.
- **에이전트 설계 (5장):** 이 '평가 에이전트'는 최종 사용자에게 결과물을 전달하는 역할이 아닌, 다른 에이전트나 시스템의 품질을 측정하는 **'도구'로서의 에이전트**입니다. 이는 시스템의 신뢰성을 높이는 데 필수적인 내부 구성요소입니다.
- **입/출력 설계 (6장):** **SSOT(단일 진실 공급원)** 원칙에 따라, `golden_dataset`이 '정답'의 기준이 됩니다. 이를 통해 평가의 일관성과 객관성을 확보합니다. 출력은 명확한 점수와 리포트로, 의사결정을 쉽게 만듭니다.

## 마치며: 패턴에서 원칙으로

이 장에서는 4장부터 9장까지 배운 설계 원칙과 방법론이 실제 상황에서 어떻게 적용되는지 9가지 매트릭스 상황과 추가 보충 예제를 통해 살펴보았습니다.

중요한 것은 이 예제들을 '정답'으로 외우는 것이 아니라, **왜 그렇게 설계되었는지**를 이해하는 것입니다. 각 예제의 설계 분석에서 반복적으로 언급된 메타 원칙들—**SoC, MECE, SSOT, 산출물 중심, 피드백 루프, Human-in-the-Loop**—이 바로 좋은 인스트럭션 시스템의 핵심 DNA입니다.

여러분이 마주한 새로운 문제는 이 예제들과 정확히 같지 않을 것입니다. 하지만 이 장에서 본 패턴들을 참고하고, 그 뒤에 숨은 원칙을 적용한다면, 어떤 상황에서도 효과적인 인스트럭션 시스템을 설계할 수 있을 것입니다.

다음 장부터는 인스트럭션 시스템을 실제로 구축하고 관리하는 데 필요한 도구와 프레임워크, 그리고 시스템을 지속적으로 발전시키는 전략을 다룹니다.

## 참고 자료

본 장의 예제들은 다음 자료와 개념을 참고하여 작성되었습니다:

- **RAG (Retrieval-Augmented Generation):** Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Proceedings of NeurIPS 2020*.
- **AI 에이전트 아키텍처:** Anthropic. (2024). "Building effective agents." *Anthropic Documentation*. https://docs.anthropic.com/en/docs/build-with-claude/develop/agentic-systems
- **Multi-Agent Systems:** Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley.
- **실무 사례 연구:** OpenAI. (2024). "GPT Best Practices." *OpenAI Documentation*.
