# 협업 시스템 설계

> 이 문서는 여러 에이전트가 협력하여 복잡한 문제를 해결하는 시스템을 설계하는 방법을 제공합니다.

## 1. 워크플로우 설계 기본

### 1.1 워크플로우란?

**워크플로우**는 에이전트들이 작업을 수행하는 순서와 방식을 정의한 프로세스입니다.

**핵심 구성 요소**:
- **Steps**: 각 작업 단계
- **Agents**: 각 단계를 수행할 에이전트
- **Inputs/Outputs**: 단계 간 데이터 흐름
- **Conditions**: 분기 조건
- **Error Handling**: 실패 처리 방법

### 1.2 워크플로우 정의 형식 (workflow.yaml)

```yaml
name: "[워크플로우 이름]"
description: "[설명]"
trigger: "[실행 조건]"
version: "1.0"

variables:
  default_timeout: 3600
  max_retries: 3

steps:
  - name: "[단계 이름]"
    type: sequential|parallel|conditional
    agent: "[에이전트 이름]"
    inputs:
      - param1: "{{user_input}}"
      - param2: "{{step1_output}}"
    outputs:
      - file: "output.json"
    validation:
      - condition: "[검증 조건]"
    on_failure:
      - action: retry|skip|escalate
      - max_attempts: 3
    timeout: 1800
```

## 2. 기본 워크플로우 패턴

### 2.1 순차 파이프라인 (Sequential Pipeline)

**특징**: A → B → C 순서대로 실행

**사용 케이스**:
- 데이터 전처리 파이프라인
- 문서 생성 프로세스
- 단계별 승인 워크플로우

**예시**:
```yaml
name: content-generation-pipeline
steps:
  - name: research
    agent: research-worker
    outputs:
      - file: research.json
      
  - name: draft
    agent: writer-worker
    inputs:
      - research_data: "{{research.output}}"
    outputs:
      - file: draft.md
      
  - name: review
    agent: reviewer-worker
    inputs:
      - draft: "{{draft.output}}"
    outputs:
      - file: final.md
```

### 2.2 병렬 실행 (Parallel Execution)

**특징**: 여러 작업을 동시에 실행

**사용 케이스**:
- 다중 언어 번역
- 여러 데이터 소스 동시 조회
- 독립적인 분석 작업

**예시**:
```yaml
name: multi-language-translation
steps:
  - name: parallel-translation
    type: parallel
    wait_for_all: true
    timeout: 600
    tasks:
      - name: translate-korean
        agent: translator-ko
        input: "{{source_text}}"
        output: "ko.txt"
        
      - name: translate-japanese
        agent: translator-ja
        input: "{{source_text}}"
        output: "ja.txt"
        
      - name: translate-chinese
        agent: translator-zh
        input: "{{source_text}}"
        output: "zh.txt"
    
  - name: aggregate
    agent: aggregator
    inputs:
      - files: ["ko.txt", "ja.txt", "zh.txt"]
    outputs:
      - file: "all_translations.json"
```

### 2.3 조건부 분기 (Conditional Branching)

**특징**: 조건에 따라 다른 경로 선택

**사용 케이스**:
- 우선순위별 처리
- 승인/거부 분기
- 유형별 핸들러

**예시**:
```yaml
name: customer-ticket-routing
steps:
  - name: classify
    agent: ticket-classifier
    input: "{{ticket_text}}"
    output: "classification.json"
    
  - name: route
    type: conditional
    based_on: "{{classification.priority}}"
    branches:
      urgent:
        - notify_human
        - agent: urgent-handler
          sla_minutes: 30
      normal:
        - agent: standard-handler
          sla_hours: 4
      low:
        - agent: batch-processor
          scheduled: "daily"
```

### 2.4 생성-검증 루프 (Generate-Verify Loop)

**특징**: 생성과 검증을 반복하여 품질 향상

**사용 케이스**:
- 코드 생성 및 리뷰
- 콘텐츠 작성 및 편집
- 디자인 생성 및 QA

**예시**:
```yaml
name: code-generation-with-review
steps:
  - name: generate-verify-loop
    type: loop
    max_iterations: 3
    exit_condition: "{{review.score}} >= 80"
    
    loop_steps:
      - name: generate
        agent: code-generator
        inputs:
          - requirements: "{{user_requirements}}"
          - previous_feedback: "{{review.feedback}}"
        outputs:
          - file: "code.py"
          
      - name: verify
        agent: code-reviewer
        inputs:
          - code: "{{generate.output}}"
        outputs:
          - review_result: "review.json"
          
      - name: check_quality
        condition: "{{review.score}} >= 80"
        on_true: exit_loop
        on_false: continue_loop
    
  - name: finalize
    agent: formatter
    inputs:
      - code: "{{generate.output}}"
```

## 3. 계층적 협업 아키텍처

### 3.1 3계층 구조

```
메타 에이전트 (Meta Agent)
  ├─ 전략적 목표 설정
  ├─ 아키텍트 선택/생성
  └─ 시스템 전체 모니터링
      ↓
아키텍트 에이전트 (Architect)
  ├─ 목표를 태스크로 분해
  ├─ 워커 선택 및 할당
  ├─ 워커 산출물 검증
  └─ 최종 결과 통합
      ↓
워커 에이전트들 (Workers)
  ├─ 구체적 작업 실행
  └─ 산출물 생성
```

### 3.2 계층별 책임

#### 메타 에이전트
```markdown
## 책임
1. 비즈니스 목표 해석
   - "신규 기능 출시" → 구체적 프로젝트로 분해
   
2. 아키텍트 관리
   - 적합한 아키텍트 선택 또는 생성
   - 여러 프로젝트 병렬 관리
   
3. 시스템 최적화
   - 전체 성능 지표 분석
   - 병목 구간 식별 및 개선

## 의사결정 예시
```yaml
user_goal: "고객 리뷰 분석 시스템 구축"

meta_decision:
  architect: review-analysis-architect
  rationale: "리뷰 분석에 특화된 기존 아키텍트 활용"
  resources:
    - workers: [classifier, sentiment-analyzer, reporter]
    - budget: "medium"
    - deadline: "2 weeks"
```
```

#### 아키텍트 에이전트
```markdown
## 책임
1. Work Breakdown
   ```yaml
   project: "고객 리뷰 분석"
   tasks:
     - classify_reviews  # 분류
     - analyze_sentiment # 감성 분석
     - extract_keywords  # 키워드 추출
     - generate_report   # 보고서 생성
   ```

2. 워커 할당
   ```yaml
   assignments:
     - task: classify_reviews
       worker: review-classifier-v2
       reason: "다중 카테고리 분류 성능 우수"
     - task: analyze_sentiment
       worker: sentiment-analyzer-v1
   ```

3. 검증 및 통합
   - 각 워커 산출물 검증
   - 전체 결과 통합
   - 메타 에이전트에 보고
```

#### 워커 에이전트
```markdown
## 책임
1. 할당받은 단일 태스크 수행
2. 명시된 형식으로 산출물 생성
3. 실패 시 에러 상태 보고

## 인지 범위
- 자신의 작업만 알면 됨
- 전체 워크플로우 몰라도 됨
- 다른 워커 알 필요 없음
```

### 3.3 계층 간 통신

```yaml
# 메타 → 아키텍트
message:
  type: project_assignment
  content:
    goal: "주간 리뷰 분석 보고서 생성"
    deadline: "2024-10-07"
    resources: ["review-db", "worker-pool-A"]

# 아키텍트 → 워커
message:
  type: task_assignment
  content:
    task_id: "task-001"
    agent: "classifier-v2"
    input_file: "reviews.csv"
    output_file: "classified.json"
    deadline: "30 minutes"

# 워커 → 아키텍트
message:
  type: task_completion
  content:
    task_id: "task-001"
    status: "success"
    output_file: "classified.json"
    metadata:
      processed_items: 1500
      duration_seconds: 120

# 아키텍트 → 메타
message:
  type: project_completion
  content:
    project_id: "proj-123"
    status: "completed"
    final_output: "weekly_report.json"
    summary: "1500개 리뷰 분석 완료"
```

## 4. 디렉토리 구조와 산출물 관리

### 4.1 표준 디렉토리 구조

```
/system-root/
├── workflows/              # 워크플로우 템플릿
│   ├── content-generation/
│   │   ├── workflow.yaml
│   │   └── README.md
│   └── review-analysis/
│       ├── workflow.yaml
│       └── README.md
│
├── agents/                 # 에이전트 인스트럭션
│   ├── architects/
│   │   ├── content-architect.md
│   │   └── review-architect.md
│   └── workers/
│       ├── classifier-v2.md
│       ├── sentiment-analyzer-v1.md
│       └── report-generator.md
│
├── schemas/                # 공통 데이터 스키마
│   ├── common.json
│   ├── review-schema.json
│   └── report-schema.json
│
└── jobs/                   # 실행 기록
    ├── 2024-10-03/
    │   ├── job_abc123/
    │   │   ├── _job_log.json
    │   │   ├── input.csv
    │   │   ├── classified.json
    │   │   └── final_report.json
    │   └── job_xyz789/
    └── 2024-10-04/
```

### 4.2 산출물 인터페이스

**개념**: 에이전트 간 소통 규약

**핵심 원칙**:
1. **파일 기반**: 모든 산출물은 파일로 저장
2. **구조화**: JSON/YAML 등 파싱 가능한 형식
3. **메타데이터 포함**: 작업 정보 함께 기록

**표준 산출물 형식**:
```json
{
  "metadata": {
    "task_id": "task-123",
    "agent_name": "classifier-v2",
    "agent_version": "2.1.0",
    "status": "success",
    "timestamp_start": "2024-10-03T10:00:00Z",
    "timestamp_end": "2024-10-03T10:05:12Z",
    "input_source": "reviews.csv",
    "error": null
  },
  "data": {
    "classified_items": [
      {"id": 1, "category": "product", "confidence": 0.95},
      {"id": 2, "category": "delivery", "confidence": 0.88}
    ],
    "statistics": {
      "total": 1500,
      "product": 800,
      "delivery": 450,
      "cs": 250
    }
  }
}
```

### 4.3 작업 로그 (_job_log.json)

모든 작업의 상태를 추적하는 중앙 로그:

```json
{
  "job_id": "job_abc123",
  "workflow_template": "review-analysis",
  "status": "completed",
  "created_at": "2024-10-03T09:00:00Z",
  "completed_at": "2024-10-03T10:30:00Z",
  "current_step": null,
  "history": [
    {
      "step_name": "classify",
      "task_id": "task-001",
      "agent_name": "classifier-v2",
      "status": "success",
      "started_at": "2024-10-03T09:00:00Z",
      "completed_at": "2024-10-03T09:05:00Z",
      "input_file": "reviews.csv",
      "output_file": "classified.json",
      "metrics": {
        "processed_items": 1500,
        "duration_seconds": 300
      }
    },
    {
      "step_name": "analyze",
      "task_id": "task-002",
      "agent_name": "sentiment-analyzer-v1",
      "status": "success",
      "started_at": "2024-10-03T09:06:00Z",
      "completed_at": "2024-10-03T09:20:00Z",
      "input_file": "classified.json",
      "output_file": "analyzed.json"
    },
    {
      "step_name": "report",
      "task_id": "task-003",
      "agent_name": "report-generator",
      "status": "success",
      "started_at": "2024-10-03T09:21:00Z",
      "completed_at": "2024-10-03T10:30:00Z",
      "output_file": "final_report.json"
    }
  ],
  "errors": [],
  "final_output": "final_report.json"
}
```

## 5. 실전 통합 예시

### 5.1 시나리오: 주간 고객 리뷰 분석 시스템

**목표**: 매주 자동으로 고객 리뷰를 분석하여 부서별 요약 보고서 생성

**시스템 구성**:

#### Step 1: 디렉토리 구조 생성

```bash
/ai-system/
├── workflows/
│   └── weekly-review-analysis/
│       └── workflow.yaml
├── agents/
│   ├── architects/
│   │   └── review-analysis-architect.md
│   └── workers/
│       ├── classifier.md
│       ├── sentiment-analyzer.md
│       ├── keyword-extractor.md
│       └── report-generator.md
├── schemas/
│   └── review-report.schema.json
└── jobs/
```

#### Step 2: 워크플로우 정의

**workflows/weekly-review-analysis/workflow.yaml**:
```yaml
name: weekly-review-analysis
description: 주간 고객 리뷰 자동 분석 및 보고서 생성
version: "1.0"
trigger: weekly (Sunday 23:00)
architect: review-analysis-architect

steps:
  - name: classify
    agent: classifier
    inputs:
      - source: "customer_reviews_db"
      - date_range: "last_7_days"
    outputs:
      - file: "classified_reviews.json"
    validation:
      - min_items: 1
    timeout: 600
    
  - name: analyze_sentiment
    agent: sentiment-analyzer
    inputs:
      - file: "classified_reviews.json"
    outputs:
      - file: "sentiment_analysis.json"
    timeout: 900
    
  - name: extract_keywords
    agent: keyword-extractor
    inputs:
      - file: "sentiment_analysis.json"
    outputs:
      - file: "keywords.json"
    
  - name: generate_report
    agent: report-generator
    inputs:
      - classified: "classified_reviews.json"
      - sentiment: "sentiment_analysis.json"
      - keywords: "keywords.json"
    outputs:
      - file: "weekly_report.json"
    validation:
      - schema: "schemas/review-report.schema.json"
    
  - name: human_approval
    type: approval
    required_approvers: ["product_manager", "cs_manager"]
    timeout: 86400  # 24시간
    
  - name: distribute
    agent: email-sender
    inputs:
      - report: "weekly_report.json"
      - recipients: ["executives@company.com"]
```

#### Step 3: 아키텍트 인스트럭션

**agents/architects/review-analysis-architect.md**:
```markdown
# 리뷰 분석 아키텍트

## 목적
주간 고객 리뷰 분석 워크플로우 관리

## 책임
1. 워커 에이전트 조율
2. 각 단계 산출물 검증
3. 최종 보고서 통합

## 관리 대상 워커
- classifier: 리뷰 카테고리 분류
- sentiment-analyzer: 감성 분석
- keyword-extractor: 핵심 키워드 추출
- report-generator: 최종 보고서 생성

## 검증 전략

### Step 1: classify
직접 평가:
```python
assert len(classified_reviews) >= 1, "리뷰 없음"
assert all(r['category'] in ['product', 'delivery', 'cs'] 
           for r in classified_reviews), "잘못된 카테고리"
```

### Step 2-3: analyze, extract
직접 평가: 파일 존재 및 JSON 형식 확인

### Step 4: generate_report
평가자 위임 + 스키마 검증:
```yaml
validation:
  - schema_check: "schemas/review-report.schema.json"
  - evaluator: quality-checker
    threshold: 80
```

## 실패 처리
- 워커 실패: 최대 3회 재시도
- 스키마 불일치: 즉시 재실행
- 3회 연속 실패: 메타 에이전트에 에스컬레이션

## 로깅
작업 디렉토리: `/jobs/YYYY-MM-DD/job_review_HHMMSS/`
로그 파일: `_job_log.json`
```

#### Step 4: 워커 인스트럭션 (예시)

**agents/workers/classifier.md**:
```markdown
# 고객 리뷰 분류기

## 목적
고객 리뷰를 제품/배송/CS 카테고리로 분류

## 역할
고객 경험 분석 전문가

## 입력
```json
[
  {"review_id": "R001", "text": "배송이 너무 느렸어요"},
  {"review_id": "R002", "text": "제품 품질이 좋아요"}
]
```

## 처리 방법
1. 각 리뷰의 핵심 키워드 파악
2. 카테고리별 관련성 평가
3. 가장 적합한 카테고리 선택

## 출력
```json
[
  {
    "review_id": "R001",
    "category": "delivery",
    "confidence": 0.92
  },
  {
    "review_id": "R002",
    "category": "product",
    "confidence": 0.95
  }
]
```

## 제약 조건
- confidence < 0.7이면 category = "mixed"
- 하나의 리뷰는 하나의 카테고리만
```

#### Step 5: 출력 스키마

**schemas/review-report.schema.json**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Weekly Review Report",
  "type": "object",
  "properties": {
    "report_period": {
      "type": "string",
      "description": "보고 기간 (예: 2024-W40)"
    },
    "total_reviews": {
      "type": "integer",
      "minimum": 0
    },
    "summary_by_department": {
      "type": "object",
      "properties": {
        "product": {
          "$ref": "#/definitions/department_summary"
        },
        "delivery": {
          "$ref": "#/definitions/department_summary"
        },
        "cs": {
          "$ref": "#/definitions/department_summary"
        }
      },
      "required": ["product", "delivery", "cs"]
    }
  },
  "required": ["report_period", "total_reviews", "summary_by_department"],
  "definitions": {
    "department_summary": {
      "type": "object",
      "properties": {
        "total_reviews": {"type": "integer"},
        "sentiment_ratio": {
          "type": "object",
          "properties": {
            "positive": {"type": "number"},
            "negative": {"type": "number"},
            "neutral": {"type": "number"}
          }
        },
        "top_keywords": {
          "type": "array",
          "items": {"type": "string"},
          "maxItems": 10
        },
        "recommendations": {
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["total_reviews", "sentiment_ratio", "top_keywords"]
    }
  }
}
```

### 5.2 실행 흐름

```
[일요일 23:00]
  ↓
[메타 에이전트]
  - workflow.yaml 읽기
  - review-analysis-architect 호출
  ↓
[아키텍트]
  - job_abc123 디렉토리 생성: /jobs/2024-10-03/job_abc123/
  - _job_log.json 초기화 (status: pending)
  ↓
[Step 1: classify]
  - classifier 워커 호출
  - 입력: customer_reviews_db (last 7 days)
  - 출력: classified_reviews.json
  - 검증: 최소 1개 리뷰 확인
  - _job_log.json 업데이트
  ↓
[Step 2: analyze_sentiment]
  - sentiment-analyzer 워커 호출
  - 입력: classified_reviews.json
  - 출력: sentiment_analysis.json
  ↓
[Step 3: extract_keywords]
  - keyword-extractor 워커 호출
  - 출력: keywords.json
  ↓
[Step 4: generate_report]
  - report-generator 워커 호출
  - 3개 파일 통합
  - 출력: weekly_report.json
  - 스키마 검증: review-report.schema.json
  ↓
[Step 5: human_approval]
  - 제품 매니저, CS 매니저에게 이메일 발송
  - 승인 대기 (최대 24시간)
  - _job_log.json 상태: paused
  ↓
[승인 후]
  ↓
[Step 6: distribute]
  - email-sender 워커 호출
  - 경영진에게 보고서 전송
  ↓
[아키텍트]
  - _job_log.json 최종 업데이트 (status: completed)
  - 메타 에이전트에 완료 보고
```

## 6. 설계 체크리스트

### 워크플로우 설계
- [ ] 목적이 명확한가?
- [ ] 모든 단계가 YAML로 정의되었는가?
- [ ] 단계 간 데이터 흐름이 명확한가?
- [ ] 검증 조건이 정의되었는가?
- [ ] 실패 처리 전략이 있는가?

### 계층 구조
- [ ] 메타/아키텍트/워커 역할이 명확히 분리되었는가?
- [ ] 각 계층의 책임이 명확한가?
- [ ] 계층 간 통신 프로토콜이 정의되었는가?

### 산출물 관리
- [ ] 표준 디렉토리 구조를 따르는가?
- [ ] 모든 산출물이 파일로 저장되는가?
- [ ] 메타데이터가 포함되어 있는가?
- [ ] 작업 로그가 기록되는가?

### 스키마
- [ ] 공통 스키마가 schemas/에 분리되었는가?
- [ ] JSON Schema로 검증 가능한가?
- [ ] 필수 필드가 명확히 정의되었는가?

### 확장성
- [ ] 새 워커 추가가 쉬운가?
- [ ] 워크플로우 수정이 용이한가?
- [ ] 재사용 가능한 구조인가?

## 7. 다음 단계

이 지식 베이스를 활용하여:

1. **메타 에이전트 구현**
   - 사용자 목표 해석
   - 적합한 아키텍트 선택/생성
   - 시스템 모니터링

2. **아키텍트 라이브러리 구축**
   - 범용 패턴별 아키텍트
   - 도메인 특화 아키텍트

3. **워커 라이브러리 구축**
   - 기본 워커 (분류, 추출, 변환 등)
   - 전문 워커 (조직 특화)

4. **평가 시스템**
   - 골든 데이터셋
   - 자동화된 테스트
   - 성능 벤치마크

5. **지속적 개선**
   - 워커 성능 모니터링
   - 워크플로우 최적화
   - 버전 관리
