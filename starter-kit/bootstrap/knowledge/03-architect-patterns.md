# 아키텍트 에이전트 패턴

> 이 문서는 워크플로우를 설계하고 워커 에이전트를 관리하는 아키텍트 에이전트의 설계 패턴을 제공합니다.

## 1. 아키텍트의 정의와 역할

### 1.1 핵심 정의

**아키텍트 에이전트**는 복잡한 목표를 달성하기 위해:
- 작업 계획을 수립하고 (Work Breakdown)
- 워커들에게 작업을 분배하며
- 전체 프로세스를 감독하는 **프로젝트 매니저** 역할

### 1.2 메타 에이전트 vs 아키텍트 vs 워커

```
[메타 에이전트]
  ↓ "신규 기능 출시" 같은 전략적 목표 받음
  ↓ 적합한 아키텍트 선택/생성
  
[아키텍트 에이전트]  
  ↓ 목표를 구체적 태스크로 분해
  ↓ 각 태스크에 워커 할당
  ↓ 워커들의 산출물 검증
  ↓ 최종 결과 통합
  
[워커 에이전트들]
  ↓ 개별 태스크 실행
  ↓ 산출물 생성
```

**차이점**:
- **메타 에이전트**: 시스템 총괄, 여러 아키텍트 관리
- **아키텍트**: 하나의 프로젝트/워크플로우 관리, 여러 워커 감독
- **워커**: 단일 작업 실행

### 1.3 아키텍트의 핵심 책임

1. **Work Breakdown (작업 분해)**
   - 큰 목표를 구체적인 태스크로 나눔
   - MECE 원칙 적용 (중복 없이, 빠짐없이)

2. **워커 선택 및 할당**
   - 각 태스크에 가장 적합한 워커 선택
   - 필요시 새 워커 요청 (메타 에이전트에게)

3. **산출물 검증**
   - 각 워커의 결과물 평가
   - 성공/실패 판단

4. **예외 처리**
   - 실패 시 재시도 또는 재할당
   - 복구 불가능 시 메타 에이전트에 에스컬레이션

5. **최종 통합**
   - 모든 워커의 산출물을 종합
   - 상위 계층에 보고

## 2. 아키텍트 설계 패턴

### 2.1 기본 파이프라인 패턴

**특징**: 순차적 작업 흐름, 각 단계의 출력이 다음 단계의 입력

**적용 상황**:
- 데이터 처리 파이프라인
- 콘텐츠 생성 워크플로우
- 문서 변환 작업

**구조**:
```yaml
architect: content-pipeline-architect

workflow:
  - step: research
    agent: researcher-worker
    output: research_data.json
    
  - step: draft
    agent: writer-worker
    input: research_data.json
    output: draft.md
    
  - step: review
    agent: reviewer-worker
    input: draft.md
    output: final_report.md
```

**아키텍트 인스트럭션 예시**:
```markdown
# 콘텐츠 파이프라인 아키텍트

## 목적
리서치 → 초안 작성 → 검수의 순차적 프로세스 관리

## 책임
1. 각 단계 완료 시 산출물 파일 존재 확인
2. 다음 단계에 올바른 입력 전달
3. 검수 단계에서 rejection 시 초안 작성 단계로 되돌림 (최대 2회)

## 워크플로우
```yaml
steps:
  - name: research
    agent: researcher-worker
    inputs: {topic: "{{user_topic}}"}
    outputs: {file: "research_data.json"}
    validation:
      - file_exists: "research_data.json"
      - min_sources: 3
    
  - name: draft
    agent: writer-worker
    inputs: {research: "research_data.json"}
    outputs: {file: "draft.md"}
    validation:
      - file_exists: "draft.md"
      - word_count: {min: 800, max: 1200}
    
  - name: review
    agent: reviewer-worker
    inputs: {draft: "draft.md"}
    outputs: {file: "final_report.md", decision: "approve|revise"}
    on_revise:
      - retry: step.draft
      - max_attempts: 2
```

## 실패 처리
- 각 단계 실패 시: 최대 3회 재시도
- 검수 거부 시: draft 단계로 되돌림
- 2회 연속 거부 시: 메타 에이전트에 에스컬레이션
```

### 2.2 생성-검증 패턴

**특징**: 생성 워커와 검증 워커를 쌍으로 묶어 품질 보장

**적용 상황**:
- 코드 생성 + 리뷰
- 문서 작성 + 팩트 체크
- 이미지 생성 + 품질 검증

**구조**:
```yaml
architect: generate-verify-architect

workflow:
  - step: generate
    agent: code-generator
    output: generated_code.py
    
  - step: verify
    agent: code-reviewer
    input: generated_code.py
    output: review_result.json
    
  - step: decision
    type: conditional
    if: "review_result.decision == 'approve'"
    then: finalize
    else: regenerate (loop back to generate)
```

**아키텍트 인스트럭션 예시**:
```markdown
# 코드 생성-검증 아키텍트

## 목적
코드 생성과 품질 검증을 반복하여 고품질 코드 산출

## 피드백 루프 전략
```yaml
loop:
  max_iterations: 3
  steps:
    - generate:
        agent: code-generator
        output: code.py
        
    - verify:
        agent: code-reviewer
        input: code.py
        output: review.json
        
    - decide:
        if: review.json.score >= 80
        then: accept
        else: provide_feedback_and_regenerate
```

## 종료 조건
1. 검증 점수 >= 80
2. 최대 반복 3회 도달
3. 사용자 수동 승인
```

### 2.3 병렬 실행 패턴

**특징**: 독립적인 작업들을 동시에 실행하여 시간 절약

**적용 상황**:
- 여러 언어로 동시 번역
- 다수의 독립적인 데이터 소스 조회
- 여러 형식으로 동시 변환

**구조**:
```yaml
architect: parallel-execution-architect

workflow:
  - step: parallel_tasks
    type: parallel
    tasks:
      - {agent: translator-ko, input: source.txt, output: ko.txt}
      - {agent: translator-ja, input: source.txt, output: ja.txt}
      - {agent: translator-zh, input: source.txt, output: zh.txt}
    
  - step: aggregate
    agent: aggregator
    inputs: [ko.txt, ja.txt, zh.txt]
    output: translations.json
```

**아키텍트 인스트럭션 예시**:
```markdown
# 병렬 번역 아키텍트

## 목적
원문을 여러 언어로 동시 번역하여 시간 단축

## 워크플로우
```yaml
step1_parallel:
  type: parallel
  wait_for_all: true
  tasks:
    - {agent: translator-ko, ...}
    - {agent: translator-ja, ...}
    - {agent: translator-zh, ...}
  timeout: 300  # 5분
  
step2_aggregate:
  agent: result-aggregator
  condition: all_tasks_completed
```

## 예외 처리
- 하나의 태스크 실패 시: 해당 태스크만 재시도
- 전체 타임아웃 시: 성공한 결과만 취합하고 실패 목록 보고
```

### 2.4 조건부 라우팅 패턴

**특징**: 중간 결과에 따라 다음 경로를 동적으로 결정

**적용 상황**:
- 우선순위에 따른 처리 분기
- 콘텐츠 유형별 다른 처리
- 승인/거부에 따른 다른 액션

**구조**:
```yaml
architect: conditional-routing-architect

workflow:
  - step: classify
    agent: classifier
    output: classification.json
    
  - step: route
    type: conditional
    based_on: classification.json.category
    routes:
      urgent: urgent-handler
      normal: normal-handler
      low: low-priority-handler
```

**아키텍트 인스트럭션 예시**:
```markdown
# 티켓 라우팅 아키텍트

## 목적
고객 지원 티켓을 우선순위에 따라 적절한 처리 경로로 분배

## 라우팅 규칙
```yaml
step1_classify:
  agent: ticket-classifier
  output: classified.json  # {priority: "urgent|normal|low"}

step2_route:
  type: router
  input: classified.json.priority
  routes:
    urgent:
      - notify_human_immediately
      - agent: urgent-responder
        sla: 30_minutes
    normal:
      - agent: standard-responder
        sla: 4_hours
    low:
      - agent: batch-processor
        scheduled: daily
```
```

## 3. 워커 평가 전략

### 3.1 직접 평가 (Direct Evaluation)

아키텍트가 스스로 검증 - 간단하고 명확한 기준에 적합

**사용 사례**:
- 파일 존재 확인
- JSON 스키마 검증
- 필드 존재 여부
- 단어 수 체크

**예시**:
```markdown
## 산출물 검증 (직접 평가)

각 워커 작업 후 다음을 확인:

1. 파일 존재
   ```python
   assert os.path.exists(output_file), "산출물 파일 없음"
   ```

2. JSON 형식
   ```python
   with open(output_file) as f:
       data = json.load(f)  # 파싱 에러 시 실패
   ```

3. 필수 필드
   ```python
   required = ["summary", "categories", "priority"]
   assert all(k in data for k in required), "필수 필드 누락"
   ```

4. 값 범위
   ```python
   assert 1 <= data["priority"] <= 5, "priority 범위 초과"
   ```

검증 실패 시:
- 워커에 재실행 요청 (최대 3회)
- 3회 실패 시 메타 에이전트에 에스컬레이션
```

### 3.2 평가자 위임 (Evaluator Delegation)

별도의 평가 전문 워커에게 검증 위임 - 복잡하고 주관적인 기준에 적합

**사용 사례**:
- 코드 품질 평가
- 글의 논리성 검사
- 디자인 일관성 확인
- 창의성 평가

**구조**:
```yaml
workflow:
  - step: generate_code
    agent: code-generator
    output: code.py
    
  - step: evaluate_code
    agent: code-quality-evaluator  # 평가 전문 워커
    inputs:
      - code: code.py
      - criteria: quality_criteria.json
    output: evaluation.json
    
  - step: decide
    based_on: evaluation.json.score
    if: score >= 80
    then: approve
    else: regenerate_with_feedback
```

**평가 워커 인스트럭션 예시**:
```markdown
# 코드 품질 평가 워커

## 역할
숙련된 시니어 개발자

## 입력
- code: 평가할 코드 파일
- criteria: 평가 기준 정의

## 평가 차원
1. 가독성 (0-100)
   - 변수명 명확성
   - 주석 적절성
   - 함수 분리

2. 성능 (0-100)
   - 시간 복잡도
   - 공간 복잡도
   - 비효율적 패턴 없음

3. 안전성 (0-100)
   - 예외 처리
   - 입력 검증
   - 보안 취약점 없음

## 출력
```json
{
  "scores": {
    "readability": 85,
    "performance": 70,
    "safety": 90
  },
  "overall": 81.7,  // 평균
  "feedback": "변수명은 우수하나, 루프 최적화 필요",
  "decision": "approve|revise"
}
```

## 판단 기준
- overall >= 80: approve
- 60-79: revise (피드백 제공)
- < 60: reject
```

**아키텍트의 평가 위임 로직**:
```markdown
## 워커 평가 (평가자 위임)

복잡한 품질 평가는 평가 전문 워커에게 위임:

```yaml
step3_evaluate:
  agent: quality-evaluator
  inputs:
    - artifact: "{{previous_step_output}}"
    - rubric: "evaluation_rubric.json"
  outputs:
    - evaluation: "eval_result.json"

step4_decide:
  type: conditional
  based_on: "eval_result.json.decision"
  routes:
    approve:
      - finalize_and_report
    revise:
      - send_feedback_to_generator: "eval_result.json.feedback"
      - retry: step2_generate
      - max_attempts: 2
    reject:
      - escalate_to_meta_agent: "품질 기준 미달"
```
```

## 4. 작업 상태 관리

### 4.1 작업 로그 (_job_log.json)

모든 아키텍트는 작업 진행 상황을 표준 로그 파일에 기록:

```json
{
  "job_id": "job_abc123",
  "workflow_template": "content-generation",
  "status": "running",  // pending|running|completed|failed|paused
  "created_at": "2025-10-03T09:00:00Z",
  "last_updated_at": "2025-10-03T10:05:12Z",
  "current_step": "step2_draft",
  "history": [
    {
      "task_id": "task-01-research",
      "agent_name": "researcher-v2",
      "status": "success",
      "started_at": "2025-10-03T09:00:00Z",
      "completed_at": "2025-10-03T09:05:00Z",
      "output_file": "research_data.json"
    },
    {
      "task_id": "task-02-draft",
      "agent_name": "writer-v3",
      "status": "running",
      "started_at": "2025-10-03T10:00:00Z"
    }
  ],
  "errors": []
}
```

**작업 상태 설명**:
- `pending`: 생성되었으나 아직 시작 안 됨
- `running`: 하나 이상의 태스크 진행 중
- `completed`: 모든 태스크 성공 완료
- `failed`: 태스크 실패로 워크플로우 중단
- `paused`: 사용자 개입 필요 (예: Human-in-the-Loop)

### 4.2 아키텍트의 모니터링 책임

```markdown
## 작업 상태 모니터링

아키텍트는 주기적으로 작업 상태를 점검:

1. 각 워커 완료 시:
   ```python
   update_job_log({
     "current_step": next_step,
     "history": append_task_record(task_result),
     "last_updated_at": now()
   })
   ```

2. 실패 감지 시:
   ```python
   if task_failed:
     update_job_log({
       "status": "failed",
       "errors": append_error(error_details)
     })
     escalate_to_meta_agent()
   ```

3. 완료 시:
   ```python
   update_job_log({
     "status": "completed",
     "final_output": output_file_path
   })
   report_to_meta_agent()
   ```
```

## 5. 아키텍트 인스트럭션 템플릿

```markdown
# [아키텍트 이름]

## 1. 목적
[복잡한 목표 한 문장]

## 2. 역할
프로젝트 매니저 / 워크플로우 오케스트레이터

## 3. 관리 대상 워커
- worker1: [역할과 책임]
- worker2: [역할과 책임]
- worker3: [역할과 책임]

## 4. 워크플로우 정의
```yaml
workflow_name: [이름]
trigger: [실행 조건]

steps:
  - step: [단계명]
    type: sequential|parallel|conditional
    agent: [워커명]
    inputs:
      - param1: [값 또는 이전 단계 산출물]
    outputs:
      - file: [출력 파일명]
    validation:
      - [검증 조건1]
      - [검증 조건2]
    on_failure:
      - action: retry|skip|escalate
      - max_attempts: 3
```

## 5. 평가 전략
### 직접 평가
- [간단한 검증 조건들]

### 평가자 위임
```yaml
evaluator: [평가 워커명]
criteria: [평가 기준 파일]
threshold: [승인 기준]
```

## 6. 예외 처리
### 워커 실패
- 재시도: [최대 횟수]
- 대체 워커: [있다면]
- 에스컬레이션: [조건]

### 타임아웃
- 각 단계: [제한 시간]
- 전체 워크플로우: [제한 시간]

## 7. 로깅
작업 디렉토리: `/jobs/YYYY-MM-DD/job_{{job_id}}/`
로그 파일: `_job_log.json`

기록 내용:
- 각 워커 실행 기록
- 성공/실패 상태
- 산출물 파일 경로
- 에러 메시지

## 8. 최종 보고
워크플로우 완료 시 메타 에이전트에 보고:
```json
{
  "job_id": "...",
  "status": "completed|failed",
  "duration": "...",
  "final_output": "...",
  "summary": "..."
}
```
```

## 6. 실전 예시

### 사례: 주간 콘텐츠 생성 아키텍트

```markdown
# 주간 블로그 포스트 생성 아키텍트

## 목적
리서치 → 초안 작성 → 검수 → 발행 파이프라인 관리

## 관리 대상 워커
- research-worker: 주제 조사 및 자료 수집
- writer-worker: 블로그 초안 작성
- reviewer-worker: 문법/사실 검증
- publisher-worker: 최종 포맷팅 및 발행

## 워크플로우
```yaml
workflow_name: weekly-blog-generation
trigger: weekly (Sunday 10:00)

steps:
  - step: research
    agent: research-worker
    inputs:
      - topic: "{{user_topic}}"
      - sources: ["news", "papers", "industry_reports"]
    outputs:
      - file: "research_notes.json"
    validation:
      - min_sources: 5
      - relevance_score: ">= 0.8"
    timeout: 1800  # 30분
    
  - step: draft
    agent: writer-worker
    inputs:
      - research: "research_notes.json"
      - style_guide: "blog_style.md"
    outputs:
      - file: "draft.md"
    validation:
      - word_count: {min: 800, max: 1500}
      - readability_score: ">= 60"
    timeout: 3600  # 1시간
    
  - step: review
    agent: reviewer-worker
    inputs:
      - draft: "draft.md"
      - original_research: "research_notes.json"
    outputs:
      - file: "review_result.json"
      - corrected_draft: "draft_v2.md"
    validation:
      - grammar_errors: "== 0"
      - fact_accuracy: ">= 95%"
    
  - step: decision
    type: conditional
    based_on: "review_result.json.decision"
    routes:
      approved:
        - step: publish
      revision_needed:
        - step: revise_draft
        - retry: step.draft
        - max_attempts: 2
      rejected:
        - escalate: "품질 기준 미달"
    
  - step: publish
    agent: publisher-worker
    inputs:
      - final_draft: "draft_v2.md"
    outputs:
      - published_url: "url.txt"
```

## 평가 전략
- 리서치: 직접 평가 (소스 개수, 관련성 점수)
- 초안: 평가자 위임 (reviewer-worker)
- 검수: 직접 평가 (에러 개수, 정확도)

## 예외 처리
- 리서치 실패: 3회 재시도 후 에스컬레이션
- 초안 2회 거부: 사람 개입 요청 (Human-in-the-Loop)
- 발행 실패: 메타 에이전트에 즉시 보고

## 로깅
모든 단계를 `/jobs/2025-10-03/job_blog_001/_job_log.json`에 기록
```

## 7. 체크리스트

아키텍트 설계 시:

### 기본 구조
- [ ] 목적이 명확한가?
- [ ] 관리할 워커들이 정의되었는가?
- [ ] 워크플로우가 YAML로 명시되었는가?

### 워커 관리
- [ ] 각 워커의 역할이 MECE인가? (중복 없이, 빠짐없이)
- [ ] 워커 간 데이터 전달이 명확한가?
- [ ] 각 워커의 산출물 검증 방법이 있는가?

### 평가 전략
- [ ] 직접 평가 vs 평가자 위임이 적절히 선택되었는가?
- [ ] 평가 기준이 명확하고 측정 가능한가?
- [ ] 승인/거부 후 액션이 정의되었는가?

### 예외 처리
- [ ] 재시도 로직이 있는가?
- [ ] 최대 재시도 횟수가 설정되었는가?
- [ ] 에스컬레이션 조건이 명확한가?

### 로깅
- [ ] 모든 워커 실행이 기록되는가?
- [ ] 작업 상태가 실시간 반영되는가?
- [ ] 에러 정보가 충분히 기록되는가?
