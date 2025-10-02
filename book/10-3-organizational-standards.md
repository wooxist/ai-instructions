# 10장 3부: 확장 패턴 - 조직 표준 시스템

---

## 들어가며: 개인의 노하우를 조직의 자산으로

1부에서는 단일 에이전트가 개인의 생산성을 높이는 방법을, 2부에서는 여러 에이전트가 협력하여 팀의 복잡한 과업을 자동화하는 방법을 살펴보았습니다. 이제 3부에서는 한 걸음 더 나아가, 개인이나 팀의 인스트럭션을 **조직 전체의 표준 자산**으로 확장하는 패턴을 다룹니다.

이는 단순히 AI를 사용하는 것을 넘어, AI를 활용한 업무 방식을 표준화하고, 조직 전체의 일관성과 효율성을 극대화하며, 새로운 팀원이 빠르게 업무에 적응할 수 있도록 돕는 '지식 관리'의 영역입니다. 여기서는 '간단/일상'적인 회의록 요약부터 '복잡/중요'한 고객 리뷰 분석 시스템까지, 조직 표준으로서 인스트럭션이 어떻게 설계되고 활용될 수 있는지 구체적인 예시를 통해 살펴보겠습니다.

---

## 10.7 [사례 7] 조직 표준, 간단/일상

- **상황:** 조직 내 모든 팀에서 공통적으로 사용하는 회의록 요약 규칙.

#### 최종 인스트럭션 시스템 예시

이 사례는 자동화된 워크플로우가 아닌, 조직의 '표준 자산(Standard Asset)'을 관리하는 시스템으로 설계할 수 있습니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/meeting_summary_standard/
└── template.md  # 1. 조직의 표준 회의록 요약 템플릿 (v1.2)
```

**2. 표준 템플릿 정의 (`template.md`)**
조직의 위키(Confluence 등)나 공유 문서에 아래 템플릿을 저장하고, 모든 팀원이 회의록 요약 시 이 템플릿을 사용하도록 안내합니다.

```markdown
# 회의록 요약 표준 인스트럭션 (v1.2)

# 목표
주어진 회의록 텍스트를 지정된 형식에 맞춰 요약한다.

# 출력 형식
## 회의 핵심 결정사항 (3가지)
- [결정사항 1]
- [결정사항 2]
- [결정사항 3]

## Action Items (담당자, 기한 명시)
- [할 일 1] - 담당자: [이름], 기한: [YYYY-MM-DD]
- [할 일 2] - 담당자: [이름], 기한: [YYYY-MM-DD]
```

**3. 전체 시스템 흐름 요약**
이 시스템은 특정 워크플로우를 자동 실행하는 대신, 조직의 공유 지식 베이스(예: Confluence, Notion)에 저장된 **표준 템플릿(`template.md`)**을 제공합니다. 조직 구성원은 이 템플릿을 활용하여 일관된 품질과 형식의 회의록 요약본을 생성합니다.

#### 실행 시나리오 (Execution Model)
이 인스트럭션은 '실행'된다기보다는 조직의 공유 지식 베이스(예: Confluence, Notion, 사내 위키)에 **'표준 템플릿'**으로 게시되어 활용됩니다. 
1.  **[팀원]** ➡️ 회의록 요약이 필요할 때, 공유 지식 베이스에서 이 표준 템플릿을 찾습니다.
2.  **[팀원]** ➡️ 템플릿 내용을 복사하여 자신이 사용하는 AI 도구(ChatGPT, Claude 등)에 붙여넣습니다.
3.  **[팀원]** ➡️ 템플릿 아래에 회의록 원문을 붙여넣고 실행하여, 표준화된 형식의 요약본을 얻습니다.
4.  **[팀원]** ➡️ 결과물을 팀 스페이스에 공유합니다.

#### 설계 분석
- **메타 원칙 (4장):** **SSOT(Single Source of Truth)** 원칙이 가장 중요하게 작용합니다. 중앙의 단일 템플릿을 통해 모든 조직원이 동일한 품질과 형식의 결과물을 얻도록 보장합니다. **점진적 개선** 원칙에 따라, 템플릿은 버전(v1.2) 관리되며 조직의 필요에 따라 지속적으로 발전할 수 있습니다.
- **에이전트 설계 (5장):** 이 시스템에서는 AI 에이전트의 페르소나보다는, 템플릿을 사용하는 '사람'이 따라야 할 **책임**과 **규칙**이 더 강조됩니다. AI는 이 규칙을 충실히 이행하는 '도구' 역할을 합니다.
- **입/출력 설계 (6장):** **출력** 형식이 매우 엄격하게 정의되어 있어, 누가 어떤 AI로 실행하든 일관된 구조의 결과물을 보장하는 것이 핵심입니다.
- **워크플로우 설계 (7장):** 자동화된 워크플로우는 없지만, '템플릿 복사 → AI에 붙여넣기 → 결과 공유'라는 **사람이 따르는 표준 운영 절차(SOP)**를 정의합니다.

---

## 10.8 [사례 8] 조직 표준, 표준/전문

- **상황:** 사내의 복잡한 규정이나 프로세스에 대해 직원들의 질문에 답변하는 Q&A 봇.

#### 최종 인스트럭션 시스템 예시

이 사례는 검색 증강 생성(RAG) 기술을 활용하는 Q&A 봇 시스템으로 설계할 수 있습니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/internal_qa_bot/
├── workflow.yaml        # 1. 전체 워크플로우의 순서와 규칙을 정의
└── agents/              # 2. 답변 생성을 담당하는 에이전트
    └── 01_rag_qa_agent.md
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
`workflow.yaml`은 사용자의 질문을 받아 내부 문서를 검색하고, 그 결과를 바탕으로 답변을 생성하는 과정을 정의합니다.

```yaml
# workflow.yaml
name: Internal Regulation Q&A Bot
trigger: User Query

steps:
  - name: 1. Search Relevant Documents
    tool: vector_db_retriever
    inputs:
      - query: "{{user_question}}"
      - knowledge_base: "internal_regulations_v3.4"
      - top_k: 3
    outputs:
      - context: "retrieved_documents"

  - name: 2. Generate Answer
    agent: agents/01_rag_qa_agent.md
    inputs:
      - question: "{{user_question}}"
      - context: "{{retrieved_documents}}" # 검색된 문서 조각을 입력으로 사용
    outputs:
      - text: "final_answer"
```

**3. 에이전트 인스트럭션 예시**
- **`agents/01_rag_qa_agent.md` (RAG 답변 에이전트)**
  ```markdown
  # 역할: [우리 회사] 인사규정 전문 비서

  # 처리 방법
  1. 사용자의 질문과 주어진 `[컨텍스트 문서]`를 분석한다.
  2. `[컨텍스트 문서]`의 내용만으로 답변을 생성한다. 절대 추측하거나 기존 지식을 사용하지 않는다.
  3. 답변의 마지막에는 반드시 참고한 문서의 제목과 페이지 번호를 출처로 명시한다.

  # 제약 조건
  - 만약 주어진 문서로 답변을 할 수 없다면, "죄송합니다. 해당 내용은 규정집에서 찾을 수 없습니다. 인사팀에 문의해주세요."라고만 답변한다.
  - 연봉, 개인 평가 등 민감 정보와 관련된 질문에는 답변을 거부한다.
  ```

**4. 전체 시스템 흐름 요약**
이 시스템은 `workflow.yaml`의 정의에 따라, 사용자의 질문이 들어오면 **내부 문서 검색(RAG) → 검색된 내용을 기반으로 답변 생성**의 순서로 작동하는 자동화된 Q&A 봇입니다.

#### 실행 시나리오 (Execution Model)
이 인스트럭션은 사내 Q&A 챗봇 애플리케이션의 **'시스템 프롬프트'**로 내장되어 실행됩니다.
1.  **[사용자]** ➡️ 챗봇에 질문을 입력합니다: "육아휴직은 최대 몇 개월까지 가능한가요?"
2.  **[워크플로우 엔진/애플리케이션]** ➡️ `workflow.yaml`을 실행합니다.
3.  **[워크플로우 엔진]** ➡️ **1단계(Search)**를 실행하여, 사용자의 질문과 가장 관련 있는 내부 규정 문서 조각 3개를 벡터 DB에서 검색합니다.
4.  **[워크플로우 엔진]** ➡️ **2단계(Generate Answer)**를 실행합니다. 검색된 문서 조각들과 사용자의 질문, 그리고 `01_rag_qa_agent.md` 인스트럭션을 함께 LLM API에 전달하여 최종 답변을 생성합니다.
5.  **[LLM]** ➡️ 생성된 답변("최대 12개월까지 가능합니다. (출처: 내부 인사 규정 v3.4, 52페이지)")을 반환하고, 챗봇이 사용자에게 보여줍니다.

#### 설계 분석
- **메타 원칙 (4장):** **SSOT(Single Source of Truth)** 원칙에 따라 답변의 근거가 되는 지식 소스를 중앙에서 관리되는 `내부 규정 문서` 벡터 DB로 한정하여 답변의 일관성과 정확성을 보장합니다. **피드백 루프** 원칙에 따라, 답변 불가 시 명확한 다음 행동(인사팀 문의)을 안내하여 사용자 경험을 개선합니다.
- **에이전트 설계 (5장):** AI는 '인사규정 전문 비서'라는 명확한 **역할**을 수행하며, 추측 금지, 민감 정보 답변 거부 등 조직의 정책을 반영한 **윤리적/운영적 제약** 하에 작동합니다.
- **입/출력 설계 (6장):** 사용자의 자연어 질문이 **입력**이고, 근거(출처)가 명시된 답변이 **출력**입니다. RAG 기술을 활용하여 입력된 질문에 가장 적합한 컨텍스트를 동적으로 구성하여 할루시네이션을 최소화합니다.
- **워크플로우 설계 (7장):** '질문 분석 → 문서 검색 → 답변 생성'의 간단한 **파이프라인 패턴**을 따르며, 이는 RAG 기반 시스템의 가장 표준적인 워크플로우입니다.

---

## 10.9 [사례 9] 조직 표준, 복잡/중요

- **상황:** 전사적으로 사용하는, 여러 부서(제품, 마케팅, CS)의 데이터가 통합되는 '주간 고객 리뷰 분석 시스템'.

#### 최종 인스트럭션 시스템 예시

이 단계의 인스트럭션은 더 이상 하나의 '글'이 아닌, 여러 부품이 유기적으로 연결된 하나의 '소프트웨어 시스템'과 같은 형태를 띠게 됩니다. 각 파일은 특정 에이전트의 지시나 워크플로우의 규칙을 담게 됩니다.

**1. 시스템의 디렉토리 구조 예시**
```
/instructions/weekly_review_report/
├── workflow.yaml        # 1. 전체 워크플로우 정의
├── agents/              # 2. 각 에이전트 정의 폴더
│   ├── 01_classifier.md
│   ├── 02_extractor.md
│   └── 03_summarizer.md
└── schemas/             # 3. 데이터 스키마 폴더
    └── report.schema.json
```

**2. 워크플로우 정의 예시 (`workflow.yaml`)**
```yaml
# workflow.yaml
name: Weekly Customer Review Analysis
trigger: Weekly (Sunday 23:00)

steps:
  - name: 1. Classify Reviews
    agent: agents/01_classifier.md
    inputs:
      - source: "customer_reviews_db"
    outputs:
      - file: classified_reviews.json

  - name: 2. Extract Key Information
    agent: agents/02_extractor.md
    inputs:
      - file: classified_reviews.json
    outputs:
      - file: extracted_info.json

  - name: 3. Generate Departmental Summaries
    agent: agents/03_summarizer.md
    inputs:
      - file: extracted_info.json
    outputs:
      - file: weekly_report.json # schemas/report.schema.json 스키마 준수

  - name: 4. Human Approval
    type: approval
    inputs:
      - file: weekly_report.json
    instructions: "제품, 마케팅, CS팀 담당자는 주간 리포트를 검토하고 최종 승인합니다."
```

**3. 에이전트 인스트럭션 및 스키마 예시**
- **`agents/01_classifier.md` (분류 에이전트 예시)**
```markdown
  # 역할: 고객 리뷰 분류 전문가
  # 목표: 주어진 고객 리뷰 텍스트를 '제품', 'CS', '가격', '기타' 네 가지 카테고리 중 가장 적합한 하나로 분류한다.
  # 출력: 분류 결과 (JSON: {"review_id": "...", "category": "제품"})
```

- **`agents/02_extractor.md` (정보 추출 에이전트 예시)**
```markdown
# 역할: 고객 리뷰 분석 전문가

# 목표
입력된 분류된 리뷰 목록(`classified_reviews.json`)에서 각 리뷰별로 제품명, 감성(긍정/부정/중립), 그리고 핵심 키워드를 추출한다.

# 입력 형식 (예시)
```json
[
  {
    "review_id": "R123",
    "category": "제품",
    "text": "새로 나온 '갤럭시 AI폰' 정말 좋네요. 카메라도 선명하고, 특히 통역 기능이 마음에 듭니다. 다만 배터리가 조금 빨리 닳는 것 같아요."
  },
  {
    "review_id": "R124",
    "category": "CS",
    "text": "상담원 연결이 너무 오래 걸려서 불편했습니다."
  }
]
```

# 처리 방법
1. 각 리뷰 텍스트를 분석한다.
2. **제품명**: 텍스트에서 언급된 구체적인 제품명을 식별한다. 제품명이 없으면 `null`로 처리한다.
3. **감성**: 리뷰의 전반적인 톤을 '긍정', '부정', '중립' 중 하나로 판단한다.
4. **핵심 키워드**: 리뷰의 핵심 내용을 나타내는 키워드를 3개 이내로 추출한다.

# 출력 형식
- 아래 JSON 구조를 따라 `extracted_info.json` 파일을 생성한다.
- 각 리뷰에 대한 추출 결과를 배열 형태로 포함한다.

```json
[
  {
    "review_id": "R123",
    "product_name": "갤럭시 AI폰",
    "sentiment": "긍정",
    "keywords": ["카메라", "통역 기능", "배터리"]
  },
  {
    "review_id": "R124",
    "product_name": null,
    "sentiment": "부정",
    "keywords": ["상담원 연결", "불편"]
  }
]
```
```

- **`agents/03_summarizer.md` (요약 보고서 생성 에이전트 예시)**
```markdown
# 역할: 데이터 기반 비즈니스 분석가

# 목표
입력된 추출 정보(`extracted_info.json`)를 바탕으로, 제품팀과 CS팀을 위한 주간 요약 보고서를 생성한다.

# 입력 형식 (예시)
```json
[
  {
    "review_id": "R123",
    "category": "제품",
    "product_name": "갤럭시 AI폰",
    "sentiment": "긍정",
    "keywords": ["카메라", "통역 기능", "배터리"]
  },
  {
    "review_id": "R124",
    "category": "CS",
    "sentiment": "부정",
    "keywords": ["상담원 연결", "불편"]
  },
  {
    "review_id": "R125",
    "category": "제품",
    "product_name": "갤럭시 AI폰",
    "sentiment": "부정",
    "keywords": ["배터리", "발열"]
  }
]
```

# 처리 방법
1. 전체 리뷰를 카테고리('제품', 'CS' 등)별로 그룹화한다.
2. **제품 요약 (product_summary)**:
   - '제품' 카테고리 리뷰들을 종합한다.
   - 가장 많이 언급된 제품의 긍정/부정 리뷰 비율을 계산한다.
   - 주요 긍정 키워드와 부정 키워드를 각각 3개씩 요약한다.
   - 실행 가능한 개선 제안을 1~2가지 도출한다.
3. **CS 요약 (cs_summary)**:
   - 'CS' 카테고리 리뷰들을 종합한다.
   - 주요 불만 사항(키워드)을 요약한다.
   - 고객 경험 개선을 위한 제안을 1~2가지 도출한다.

# 출력 형식
- `schemas/report.schema.json` 스키마를 준수하는 `weekly_report.json` 파일을 생성한다.
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
이 워크플로우는 **'워크플로우 엔진'** 또는 **'오케스트레이터'**에 의해 매주 자동으로 실행됩니다.

1.  **[워크플로우 엔진]** ➡️ 매주 일요일 23시에 `workflow.yaml`에 정의된 워크플로우를 실행합니다.
2.  **[워크플로우 엔진]** ➡️ **Classifier, Extractor, Summarizer** 에이전트를 순차적으로 호출하여 `weekly_report.json`을 생성합니다.
3.  **[워크플로우 엔진]** ➡️ 최종 생성된 리포트를 각 부서 담당자에게 전달하고 승인을 요청합니다.
4.  **[담당자들]** ➡️ 내용을 검토하고 승인하면, 리포트가 경영진에게 자동으로 발송되거나 대시보드에 게시됩니다.

#### 설계 분석
- **메타 원칙 (4장):** **SoC**에 따라 기능이 파일 단위로 분리되고, **SSOT**에 따라 `workflow.yaml`가 전체 구조를 정의합니다. 각 단계는 **원자적**이며, 최종 결과물은 **산출물 중심** 원칙에 따라 스키마로 관리됩니다. **Human-in-the-Loop**를 통한 최종 검증도 가능합니다.
- **에이전트 설계 (5장):** `agents/` 폴더 내에 각 에이전트의 **역할, 책임, 제약**이 개별 파일로 명확히 정의되어, 시스템의 모듈성과 유지보수성을 높입니다.
- **입/출력 설계 (6장):** `schemas/` 폴더에 위치한 `report.schema.json` 파일이 최종 결과물의 구조를 명세화하여, 시스템 전체의 **출력** 일관성을 보장합니다.
- **워크플로우 설계 (7장):** `workflow.yaml` 파일이 **파이프라인 패턴**에 따라 에이전트들의 협력 순서와 데이터 **핸드오프** 규칙, 그리고 각 단계의 **실패 처리** 방안을 명시적으로 정의합니다.

---
[다음으로: 4부 - 고급 아키텍처와 실전 구현](10-4-advanced-architectures.md)
