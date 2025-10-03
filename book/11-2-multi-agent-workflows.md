# 10장 2부: 협력 패턴 - 다중 에이전트 워크플로우

---

## 들어가며: '만능 칼'에서 '전문가 팀'으로

1부에서는 하나의 '만능 스위스 아미 나이프'처럼, 단일 에이전트만으로도 다양한 문제를 해결하는 방법을 살펴보았습니다. 하지만 현실의 복잡한 문제는 여러 분야의 전문가들이 협력해야 해결할 수 있듯, AI 시스템 역시 각자의 전문성을 가진 여러 에이전트가 '팀'을 이루어 협력할 때 더 큰 힘을 발휘합니다.

2부에서는 이처럼 여러 에이전트가 정해진 '업무 절차(워크플로우)'에 따라 협력하여, 더 복잡하고 가치 있는 문제를 해결하는 '다중 에이전트 워크플로우' 설계 패턴을 본격적으로 다룹니다.

---

## 10.4 [사례 4] 다중 에이전트, 간단/일상

- **상황:** 아이디어를 간단한 트윗(X) 포스트로 만드는 콘텐츠 생성 파이프라인. 초기 아이디어를 구체화하고, 트윗 형식에 맞게 다듬고, 관련 해시태그까지 추천받고 싶다.

#### 최종 인스트럭션 시스템 예시

이 단계의 인스트럭션은 간단한 아이디어를 구체적인 소셜 미디어 콘텐츠로 발전시키는 자동화된 파이프라인 시스템으로 설계할 수 있습니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/tweet_creation/
├── workflow.yaml        # 1. 전체 워크플로우의 순서와 규칙을 정의
└── agents/              # 2. 각 역할을 수행할 에이전트들의 인스트럭션
    ├── 01_idea_expander.md
    ├── 02_tweet_writer.md
    └── 03_hashtag_recommender.md
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
시스템의 워크플로우 파일은 각 에이전트를 어떤 순서로 실행할지 정의합니다.

```yaml
# workflow.yaml
name: Tweet Content Generation Pipeline
trigger: Manual

variables:
  - idea: "AI 지침 설계에 대한 트윗" # 파라미터로 외부에서 주입 가능
  - expanded_ideas: null
  - selected_idea: null
  - tweet_draft: null
  - hashtags: null

steps:
  - name: 1. Expand Idea
    agent: agents/01_idea_expander.md
    inputs:
      - idea: "{{idea}}"
    outputs:
      - variable: expanded_ideas

  - name: 2. User Selects Idea
    type: human_in_the_loop
    instructions: "다음 3가지 아이디어 중 하나를 선택해주세요: {{expanded_ideas}}"
    outputs:
      - variable: selected_idea

  - name: 3. Draft Tweet
    agent: agents/02_tweet_writer.md
    inputs:
      - idea: "{{selected_idea}}" # 사용자가 선택한 아이디어를 입력으로 사용
    outputs:
      - variable: tweet_draft

  - name: 4. Recommend Hashtags
    agent: agents/03_hashtag_recommender.md
    inputs:
      - text: "{{tweet_draft}}"
    outputs:
      - variable: hashtags

  - name: 5. Finalize
    type: format
    template: |
      {
        "tweet": "{{tweet_draft}}",
        "hashtags": {{hashtags}}
      }
    outputs:
      - file: final_tweet.json
```

**3. 에이전트 인스트럭션 예시**
- **`agents/01_idea_expander.md` (아이디어 확장 에이전트)**
```markdown
# 역할: 창의적인 콘텐츠 전략가
# 태스크: 입력된 아이디어를 바탕으로, (1) 질문형, (2) 정보 제공형, (3) 논란 유발형의 3가지 다른 각도의 접근법을 제안한다.
# 출력: 3가지 접근법 목록 (JSON 형식)
```

- **`agents/02_tweet_writer.md` (트윗 작성 에이전트)**
```markdown
# 역할: 재치 있는 소셜 미디어 전문가
# 태스크: 선택된 접근법을 140자 이내의 간결하고 흡입력 있는 트윗 문장으로 다듬고, 이모지를 1~2개 포함한다.
# 출력: 최종 트윗 문장 (문자열)
```

- **`agents/03_hashtag_recommender.md` (해시태그 추천 에이전트)**
```markdown
# 역할: 트렌드 분석가
# 태스크: 트윗 내용과 관련된 해시태그 5개를 추천한다.
# 출력: 추천 해시태그 목록 (JSON 배열)
```

**4. 전체 시스템 흐름 요약**
이 시스템은 `workflow.yaml`의 정의에 따라, **아이디어 확장 → 트윗 초안 작성 → 해시태그 추천**의 순서로 각 전문 에이전트가 자신의 역할을 수행하며 결과물을 다음 단계로 전달하는 자동화된 콘텐츠 생성 파이프라인입니다.

#### 실행 시나리오 (Execution Model)
이 워크플로우는 **매니저 에이전트(Manager Agent)**에 의해 자동으로 실행됩니다.

1.  **[사용자]** ➡️ **[매니저 에이전트]**에게 작업을 지시합니다: "AI 지침 설계에 대한 트윗 아이디어 좀 내줘."
2.  **[매니저 에이전트]** ➡️ `workflow.yaml` 파일을 읽고, **1단계(Idea Expander)**를 실행하여 `expanded_ideas.json`을 생성합니다.
3.  **[매니저 에이전트]** ➡️ **2단계(Tweet Writer)**를 실행합니다. 이전 단계의 출력인 `expanded_ideas.json`을 입력으로 하여 `tweet_draft.txt`를 생성합니다.
4.  **[매니저 에이전트]** ➡️ **3단계(Hashtag Recommender)**를 실행하여 최종 `hashtags.json`을 생성합니다.
5.  **[매니저 에이전트]** ➡️ 모든 결과물을 취합하여 최종 결과(예: 단일 JSON 객체)를 사용자에게 보여줍니다.

#### 설계 분석
- **메타 원칙 (4장):** **SoC(관심사 분리)** 원칙을 적용해 **각 에이전트가 한 가지 일에만 집중하게 만들었습니다.** 아이디어 생성, 문장 다듬기, 키워드 추천을 분리하면 각 단계의 전문성이 높아지고, 나중에 특정 기능만 수정하거나 개선하기도 용이해집니다. 또한 **점진적 개선** 원칙에 따라, 추상적인 아이디어가 구체적인 트윗과 해시태그로 단계적으로 발전하므로 복잡한 문제를 체계적으로 해결할 수 있습니다.
- **에이전트 설계 (5장):** 각 에이전트에게 '콘텐츠 전략가', '소셜 미디어 전문가' 등 명확히 구분되는 **역할**을 부여했습니다. 이는 각 에이전트가 자신의 임무에 맞는 최적의 결과물을 생성하도록 유도하는 효과적인 방법입니다.
- **입/출력 설계 (6장):** 에이전트 간 데이터를 주고받을 때, 사람이 읽기도 쉽고 기계가 처리하기도 쉬운 **JSON 형식을 사용**했습니다. 이렇게 입출력 형식을 명확히 정의하면, 각 단계가 오류 없이 안정적으로 연결되어 전체 워크플로우의 신뢰성이 높아집니다.
- **워크플로우 설계 (7장):** 세 에이전트를 순차적으로 연결하는 간단한 **파이프라인 패턴(A→B→C)**을 사용했습니다. 이는 '아이디어만 입력하면 완성된 트윗과 해시태그가 나온다'는 명확한 작업 흐름을 만들어, 단순 반복 업무를 자동화하고 결과물의 품질을 일관되게 유지하는 데 매우 효과적입니다.

---

## 10.5 [사례 5] 다중 에이전트, 표준/전문

- **상황:** 사용자의 요구사항에 맞는 Python 코드를 생성하고, 자체적으로 리뷰까지 수행하는 워크플로우.

#### 최종 인스트럭션 시스템 예시

이 단계의 인스트럭션은 코드 생성과 리뷰라는 두 가지 명확한 역할을 분리하고, 둘을 피드백 루프로 연결한 자동화 시스템으로 설계할 수 있습니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/code_generation_review/
├── workflow.yaml        # 1. 전체 워크플로우의 순서와 규칙을 정의
└── agents/              # 2. 각 역할을 수행할 에이전트들의 인스트럭션
    ├── 01_code_generator.md
    └── 02_code_reviewer.md
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
`workflow.yaml` 파일은 코드 생성과 리뷰, 그리고 조건에 따른 반복(루프)을 정의합니다.

```yaml
# workflow.yaml
name: Python Code Generation and Review
trigger: Manual

max_retries: 3 # 무한 루프 방지를 위한 안전장치 추가
steps:
  - name: 1. Generate Code
    agent: agents/01_code_generator.md
    inputs:
      - requirements: "S3 버킷의 모든 이미지 파일에 대해 썸네일을 생성하는 함수"
    outputs:
      - file: generated_code.py

  - name: 2. Review Code
    agent: agents/02_code_reviewer.md
    inputs:
      - file: generated_code.py # 이전 단계의 출력을 입력으로 사용
    outputs:
      - file: review_result.json

  - name: 3. Check Review and Loop
    type: condition
    check: "review_result.json['status'] == '수정 필요'"
    on_true:
      # 리뷰 결과가 '수정 필요'일 경우, 피드백과 함께 1단계로 돌아감
      next_step: 1
      inputs:
        - requirements: "이전 요구사항과 다음 피드백을 반영하여 코드 수정: {{review_result.json['feedback']}}"
    on_false:
      # '통과'일 경우 워크플로우 종료
      next_step: null
```

**3. 에이전트 인스트럭션 예시**
- **`agents/01_code_generator.md` (코드 생성 에이전트)**
```markdown
# 역할: 10년차 Python 개발자
# 태스크: 요구사항에 맞는 함수 코드를 생성한다. boto3 라이브러리를 사용한다.
# 출력: `generated_code.py`
```

- **`agents/02_code_reviewer.md` (코드 리뷰 에이전트)**
```markdown
# 역할: 깐깐한 시니어 동료 개발자
# 태스크: 입력된 코드에 대해 PEP 8 스타일 가이드 준수 여부, 하드코딩된 값(API 키, 버킷 이름) 존재 여부, 예외 처리(try-except) 누락 여부를 검토한다.
# 출력: 리뷰 결과 (JSON 형식, '통과' 또는 '수정 필요' 상태와 수정 제안 목록 포함)
```

**4. 전체 시스템 흐름 요약**
이 시스템은 `workflow.yaml`의 정의에 따라, **코드 생성 → 코드 리뷰**를 수행하고, 리뷰 결과가 '통과'될 때까지 수정 과정을 자동으로 반복하는 코드 품질 관리 파이프라인입니다.

#### 실행 시나리오 (Execution Model)
이 워크플로우는 **매니저 에이전트(Manager Agent)**에 의해 자동으로 실행됩니다.

1.  **[사용자]** ➡️ **[매니저 에이전트]**에게 요구사항을 전달합니다: "S3 버킷의 모든 이미지 파일에 대해 썸네일을 생성하는 함수를 만들어줘."
2.  **[매니저 에이전트]** ➡️ `workflow.yaml`에 따라 **1단계(Code Generator)**를 실행하여 `generated_code.py`를 생성합니다.
3.  **[매니저 에이전트]** ➡️ **2단계(Code Reviewer)**를 실행하여 `review_result.json`을 생성합니다.
4.  **[매니저 에이전트]** ➡️ **3단계(Condition Check)**를 수행합니다.
    -   리뷰 결과가 `'수정 필요'`이면, 수정 제안과 함께 **1단계**로 다시 작업을 요청합니다. 이 과정은 리뷰 결과가 `'통과'`가 될 때까지 반복됩니다.
    -   리뷰 결과가 `'통과'`이면, 워크플로우를 종료하고 최종 코드를 사용자에게 전달합니다.

#### 설계 분석
- **메타 원칙 (4장):** 이 워크플로우는 **SoC(관심사 분리)** 원칙에 따라 '코드를 짜는 일(생성)'과 '코드를 검토하는 일(검증)'의 책임을 명확히 분리했습니다. 덕분에 각 에이전트는 자신의 전문성에만 집중할 수 있습니다. 또한, 리뷰 기준을 구체적인 항목으로 나눈 것은 **원자성** 원칙을 따른 것으로, 무엇이 잘못되었는지 명확하게 지적하고 수정하도록 돕습니다.
- **에이전트 설계 (5장):** 각 에이전트에게 '코드를 잘 짜는 개발자'와 '실수를 꼼꼼히 찾아내는 동료'라는 구체적인 **역할(페르소나)**을 부여했습니다. 이는 마치 실제 개발팀이 협업하는 것처럼, 각자의 **책임**에 맞는 고품질 결과물을 만들어내도록 유도하는 효과적인 방법입니다.
- **입/출력 설계 (6장):** 리뷰 결과라는 **출력**을 컴퓨터가 이해하기 쉬운 `JSON` 형식으로 약속(구조화)한 것이 중요합니다. '수정 필요'와 같은 명확한 상태 값이 담겨있기 때문에, 다음 단계인 **조건 분기**에서 '이번엔 통과시킬까, 아니면 수정을 위해 돌려보낼까?'를 기계가 자동으로 판단할 수 있습니다.
- **워크플로우 설계 (7장):** 이 설계는 **'생성-검증' 패턴**과 **'분기 패턴'**을 결합하여, **스스로 결과물을 평가하고 문제가 발견되면 알아서 수정하는 지능형 워크플로우**를 구현합니다. 이는 한번 실행하고 끝나는 단순 자동화를 넘어, 정해진 품질 기준을 만족할 때까지 작업을 반복하는 한 단계 높은 수준의 자동화 방식입니다.

---

## 10.6 [사례 6] 다중 에이전트, 복잡/중요

- **상황:** 분기별 매출 데이터를 분석하고, 시각화 자료를 포함한 보고서 초안을 생성하며, 최종적으로 경영진에게 보낼 이메일까지 작성하는 복잡한 재무 보고 프로세스.

#### 최종 인스트럭션 시스템 예시

이 단계의 인스트럭션은 더 이상 하나의 '글'이 아닌, 여러 부품이 유기적으로 연결된 하나의 '소프트웨어 시스템'과 같은 형태를 띠게 됩니다. 각 파일은 특정 에이전트의 지시나 워크플로우의 규칙을 담게 됩니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/quarterly_report/
├── workflow.yaml        # 1. 전체 워크플로우의 순서와 규칙을 정의
├── agents/              # 2. 각 역할을 수행할 에이전트들의 인스트럭션
│   ├── 01_extractor.md
│   ├── 02_analyzer.md
│   ├── 03_report_writer.md
│   └── 04_email_writer.md
└── tools/               # 3. 에이전트들이 사용할 도구의 코드
    ├── db_connector.py
    └── data_visualizer.py
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
시스템의 심장 역할을 하는 `workflow.yaml` 파일은 각 에이전트를 어떤 순서로, 어떤 데이터를 주고받으며 실행할지 정의합니다.

```yaml
# workflow.yaml
name: Quarterly Financial Report Generation
trigger: Manual (Quarterly)

steps:
  - name: 1. Extract Sales Data
    agent: agents/01_extractor.md
    inputs:
      - quarter: "2024-Q3" # 파라미터로 외부에서 주입 가능
    outputs:
      - file: sales_data.csv

  - name: 2. Analyze and Visualize Data
    agent: agents/02_analyzer.md
    inputs:
      - file: sales_data.csv # 이전 단계의 출력을 입력으로 사용
    outputs:
      - file: summary.json
      - file: chart.png

  - name: 3. Draft Report
    agent: agents/03_report_writer.md
    inputs:
      - file: summary.json
      - file: chart.png
    outputs:
      - file: report_draft.md

  - name: 4. Draft Email
    agent: agents/04_email_writer.md
    inputs:
      - file: report_draft.md
    outputs:
      - text: email_draft.txt

  - name: 5. Human Approval
    type: approval
    inputs:
      - file: report_draft.md
      - text: email_draft.txt
    instructions: "담당자는 최종 보고서와 이메일을 검토하고 승인 후 발송합니다."
```

**3. 에이전트 인스트럭션 및 스키마 예시**
- **`agents/01_extractor.md` (도구 사용 에이전트 예시)**
```markdown
# 역할: 데이터베이스 전문가 (DBA)

# 목표
주어진 분기(quarter)에 해당하는 매출 데이터를 사내 데이터베이스에서 추출하여 `sales_data.csv` 파일로 저장한다.

# 도구 사용 규칙
- `db_connector.py` 도구를 사용하여 데이터베이스에 안전하게 연결하고 쿼리를 실행해야 한다.
- SQL 쿼리는 `SELECT * FROM sales WHERE quarter = '{quarter}';` 형식을 따라야 한다.

# 제약 조건
- 데이터베이스 연결 정보나 개인정보를 로그에 남기지 않는다.
- 쿼리 실행 중 오류가 발생하면, 즉시 작업을 중단하고 "[DB ERROR]" 태그와 함께 오류 메시지를 반환한다.
```

- **`agents/02_analyzer.md` (분석 에이전트 예시)**
```markdown
# 역할: 데이터 분석가

# 목표
주어진 매출 데이터 파일(`sales_data.csv`)을 분석하여, 주요 지표(총 매출, 평균 주문 금액, 고객 수 등)를 계산하고, 시각화 자료(차트)를 생성한다.

# 입력 형식
- CSV 파일: `sales_data.csv`
  - 필드: order_id, customer_id, order_amount, order_date, product_category

# 처리 방법
1. CSV 파일을 읽어들인다.
2. 데이터 유효성 검사를 수행한다(예: 필수 필드 누락, 형식 오류 등).
3. 주요 지표를 계산한다:
   - 총 매출: order_amount의 합계
   - 평균 주문 금액: order_amount의 평균
   - 고객 수: 고유한 customer_id의 수
4. 매출 추이 차트(시간에 따른 총 매출 변화)를 생성한다.
5. 카테고리별 매출 비율 파이차트 생성.

# 출력 형식
- 분석 결과는 `summary.json` 파일에 저장한다.
- 차트 이미지는 `chart.png`로 저장한다.
```

- **`agents/03_report_writer.md` (콘텐츠 생성 에이전트 예시)**
```markdown
# 역할: 5년차 재무 분석가

# 목표
입력된 핵심 분석 지표(`summary.json`)와 매출 추이 그래프(`chart.png`)를 바탕으로, 경영진이 이해하기 쉬운 분기 실적 보고서 초안을 작성한다.

# 처리 방법
	  - `summary.json`의 데이터를 기반으로 보고서의 핵심 내용을 요약한다.
	  - `chart.png` 이미지를 보고서에 포함시키고, 해당 그래프가 의미하는 바를 설명한다.
	  - 보고서의 구조는 '1. 핵심 요약', '2. 상세 지표 분석', '3. 결론 및 제언' 순서를 따른다.

# 출력 형식
- 마크다운 형식으로 작성한다.
- 전문 용어 사용을 최소화하고, 간결하고 명확한 문체를 사용한다.
```

- **`agents/04_email_writer.md` (이메일 작성 에이전트 예시)**
```markdown
# 역할: 커뮤니케이션 전문가

# 목표
작성된 보고서 초안(`report_draft.md`)을 바탕으로, 경영진에게 발송할 이메일 초안을 작성한다.

# 처리 방법
1. 보고서 초안을 읽고, 핵심 메시지와 주요 결과를 파악한다.
2. 경영진이 이해하기 쉬운 언어로 이메일 본문을 작성한다.
3. 이메일 제목, 수신자, 참조인, 첨부파일(보고서 파일) 등을 설정한다.

# 출력 형식
- 이메일 초안은 텍스트 형식으로 작성하며, 제목, 수신자, 본문, 첨부파일 정보가 포함되어야 한다.
```

- **`schemas/report.schema.json` (최종 보고서 스키마 예시)**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Weekly Customer Review Report",
  "description": "A weekly summary report of customer reviews, categorized by department.",
  "type": "object",
  "properties": {
    "report_period": {
      "description": "The period the report covers, e.g., '2024-W40'.",
      "type": "string"
    },
    "total_reviews": {
      "description": "Total number of reviews analyzed.",
      "type": "integer"
    },
    "product_summary": {
      "description": "Summary for the product department.",
      "type": "object",
      "properties": {
        "summary_text": {
          "description": "A high-level text summary of product-related feedback.",
          "type": "string"
        },
        "top_product": {
          "description": "The most frequently mentioned product.",
          "type": "string"
        },
        "sentiment_ratio": {
          "description": "Sentiment ratio for the top product.",
          "type": "object",
          "properties": {
            "positive": {"type": "number", "description": "Percentage of positive reviews."},
            "negative": {"type": "number", "description": "Percentage of negative reviews."},
            "neutral": {"type": "number", "description": "Percentage of neutral reviews."}
          },
          "required": ["positive", "negative"]
        },
        "positive_keywords": {
          "description": "Top positive keywords.",
          "type": "array",
          "items": {"type": "string"}
        },
        "negative_keywords": {
          "description": "Top negative keywords.",
          "type": "array",
          "items": {"type": "string"}
        },
        "recommendations": {
          "description": "Actionable recommendations for the product team.",
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["summary_text", "positive_keywords", "negative_keywords", "recommendations"]
    },
    "cs_summary": {
      "description": "Summary for the customer service department.",
      "type": "object",
      "properties": {
        "summary_text": {
          "description": "A high-level text summary of CS-related feedback.",
          "type": "string"
        },
        "top_issues": {
          "description": "Top issues raised in CS reviews.",
          "type": "array",
          "items": {"type": "string"}
        },
        "recommendations": {
          "description": "Actionable recommendations for the CS team.",
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["summary_text", "top_issues", "recommendations"]
    }
  },
  "required": ["report_period", "total_reviews", "product_summary", "cs_summary"]
}
```

**4. 전체 시스템 흐름 요약**
이 시스템은 `workflow.yaml`의 정의에 따라, 매주 자동으로 **리뷰 분류 → 핵심 정보 추출 → 부서별 요약 리포트 생성 → 최종 인간 승인**의 순서로 각 전문 에이전트가 자신의 역할을 수행하며 결과물을 다음 단계로 전달하는 자동화된 데이터 분석 파이프라인입니다.

#### 실행 시나리오 (Execution Model)
이 워크플로우는 **매니저 에이전트(Manager Agent)**에 의해 매주 자동으로 실행됩니다.

1.  **[매니저 에이전트]** ➡️ 매주 일요일 23시에 `workflow.yaml`에 정의된 워크플로우를 실행합니다.
2.  **[매니저 에이전트]** ➡️ **Classifier, Extractor, Summarizer** 에이전트를 순차적으로 호출하여 `weekly_report.json`을 생성합니다.
3.  **[매니저 에이전트]** ➡️ 최종 생성된 리포트를 각 부서 담당자에게 전달하고 승인을 요청합니다.
4.  **[담당자들]** ➡️ 내용을 검토하고 승인하면, 리포트가 경영진에게 자동으로 발송되거나 대시보드에 게시됩니다.

#### 설계 분석
- **메타 원칙 (4장):** **SoC** 원칙에 따라 기능이 파일 단위로 분리되고, **SSOT**에 따라 `workflow.yaml`가 전체 구조를 정의합니다. 각 단계는 **원자적**이며, 최종 결과물은 **산출물 중심** 원칙에 따라 스키마로 관리됩니다. **Human-in-the-Loop**를 통한 최종 검증도 가능합니다.
- **에이전트 설계 (5장):** `agents/` 폴더 내에 각 에이전트의 **역할, 책임, 제약**이 개별 파일로 명확히 정의되어, 시스템의 모듈성과 유지보수성을 높입니다.
- **입/출력 설계 (6장):** `schemas/` 폴더에 위치한 `report.schema.json` 파일이 최종 결과물의 구조를 명세화하여, 시스템 전체의 **출력** 일관성을 보장합니다.
- **워크플로우 설계 (7장):** `workflow.yaml` 파일이 **파이프라인 패턴**에 따라 에이전트들의 협력 순서와 데이터 **핸드오프** 규칙, 그리고 각 단계의 **실패 처리** 방안을 명시적으로 정의합니다.

---
[다음으로: 3부 - 확장 패턴](10-3-organizational-standards.md)
