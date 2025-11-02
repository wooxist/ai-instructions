# Ch 16 실습 과제: 에이전트 설계

Part 4의 마지막 실습입니다! 이제 여러분이 직접 에이전트를 만들어볼 차례예요.

---

## 실습 개요

이 실습에서는 **3가지 난이도**의 에이전트를 단계별로 구현합니다:
- 🟢 **과제 1 (기본)**: 단일 에이전트 - 블로그 포스트 생성
- 🟡 **과제 2 (중급)**: 병렬 에이전트 팀 - 주간 리포트 생성
- 🔴 **과제 3 (고급)**: 계층적 에이전트 시스템 - 제품 기획

각 과제는 독립적으로 진행할 수 있지만, 순서대로 하는 것을 추천해요.

---

## 🟢 과제 1: 블로그 포스트 생성 에이전트 (기본)

### 목표
단일 에이전트를 구현하여 블로그 포스트를 자동 생성하는 시스템을 만듭니다.

### 시나리오
```
매주 기술 블로그 포스트를 작성해야 하는 개발자입니다.
주제만 주면 자동으로 초안을 작성하는 에이전트를 만들고 싶어요.

입력: "Python 비동기 프로그래밍 실전 가이드"
출력: 완성된 블로그 포스트 (마크다운)
```

### 요구사항

**1. 사고 클러스터 설계**
```yaml
사고 클러스터 ID: tc-blog-001
목표: 기술 블로그 포스트 작성
핵심 가치:
  - 정확성: 기술적으로 정확한 내용
  - 실용성: 바로 적용 가능한 예제
  - 가독성: 초보자도 이해할 수 있게

4 Stage:
  1. Planning: 포스트 구조 기획
  2. Reasoning: 각 섹션 내용 분석
  3. Experimenting: 초안 작성
  4. Reflecting: 품질 검토 및 개선
```

**2. 파일 시스템**
```
workspaces/blog-post-001/
├── thinking/
│   └── tc-blog-001/
│       ├── thinking_state.json
│       ├── planning/
│       │   └── thinking_record.json
│       ├── reasoning/
│       │   └── thinking_record.json
│       ├── experimenting/
│       │   └── thinking_record.json
│       └── reflecting/
│           └── thinking_record.json
├── outputs/
│   └── blog_post.md
├── meta/
│   ├── goal.json
│   └── constraints.json
└── checkpoints/
    └── blog-post-001.json
```

**3. 에이전트 구현**

기본 구조:
```yaml
BlogPostAgent:
  초기화:
    - task_id: 작업 식별자
    - topic: 블로그 주제
    - 필수_컴포넌트:
      * FileManager: 파일 관리
      * AgentStateMachine: Stage 관리
      * AgentLogger: 로깅
      * CheckpointManager: 체크포인트
  
  run(resume=True):
    목적: 에이전트 실행
    흐름: 16.3.2의 패턴 1 (상태 머신) 참조
  
  planning(context):
    목적: 블로그 구조 기획
    입력: topic, core_values
    출력: 제목, 개요, 섹션 구조
  
  reasoning(context):
    목적: 각 섹션 내용 분석
    입력: planning 결과
    출력: 섹션별 핵심 포인트
  
  experimenting(context):
    목적: 초안 작성
    입력: reasoning 결과
    출력: 블로그 포스트 초안
  
  reflecting(context):
    목적: 품질 검증 및 개선
    입력: experimenting 결과
    출력: 최종 블로그 포스트
```

**구현해야 할 것들**:
- [ ] `BlogPostAgent` 클래스
- [ ] 4개 Stage 메서드 (planning, reasoning, experimenting, reflecting)
- [ ] 상태 머신 통합
- [ ] 파일 자동 저장
- [ ] 체크포인트 및 재개
- [ ] 로깅

### 선택 기능

**Human-in-the-Loop** (선택):
```yaml
Experimenting_Stage_완료_후:
  1. 초안을 approval_gate에 제출
  2. 승인_요청:
     - approval_id: "{task_id}-draft"
     - context: draft 내용
     - explanation: "블로그 포스트 초안을 검토해주세요"
  
  3. 응답_처리:
     - is_approved = true: 다음 Stage로
     - is_approved = false: 피드백 반영하여 재작성
```

### 예상 소요 시간
- **설계**: 30분
- **구현**: 2-3시간
- **테스트**: 30분
- **총**: 3-4시간

### 체크리스트

**설계 단계**:
- [ ] 사고 클러스터 설계 완료
- [ ] 파일 구조 정의
- [ ] Stage별 입출력 정의

**구현 단계**:
- [ ] BaseAgent 또는 템플릿 복사
- [ ] 4개 Stage 구현
- [ ] 상태 머신 통합
- [ ] FileManager로 파일 저장
- [ ] CheckpointManager로 체크포인트

**테스트 단계**:
- [ ] 정상 실행 (끝까지 완료)
- [ ] 중간 실패 → 재개 테스트
- [ ] 출력 파일 확인 (blog_post.md)
- [ ] thinking_state.json 업데이트 확인

### 성공 기준
```yaml
기능:
  ✓ 주제를 입력하면 블로그 포스트 생성
  ✓ 4 Stage 모두 정상 실행
  ✓ 중간 실패 시 재개 가능
  ✓ 모든 파일이 올바른 위치에 저장

품질:
  ✓ 생성된 포스트가 읽을 만한 수준
  ✓ 기술적으로 정확함
  ✓ 실행 가능한 예제 포함

시간:
  ✓ 전체 실행 시간 5분 이내
```

### 힌트

**힌트 1: 프롬프트 설계**
```yaml
Planning_Stage_프롬프트:
  역할: "당신은 기술 블로그 작가입니다"
  
  입력:
    - 주제: {topic}
  
  요청:
    - 제목 (매력적이고 SEO 친화적)
    - 개요 (3-5줄)
    - 주요 섹션 (5-7개)
    - 각 섹션의 핵심 내용
  
  응답_형식: JSON
    title: "..."
    overview: "..."
    sections:
      - name: "..."
        content: "..."
```

**힌트 2: 재시도 추가**
```yaml
call_ai_메서드:
  목적: API 호출 with 재시도
  
  구현_개념:
    - 16.3.2 패턴 3 (재시도 로직) 참조
    - RetryConfig 사용
    - max_retries: 3
    - exponential_backoff: true
```

**힌트 3: 진행 상황 출력**
```yaml
update_state_메서드:
  목적: 진행 상황 표시
  
  구현:
    - state_machine.get_progress() 호출
    - progress_percent 계산
    - 화면에 출력: "[75%] reasoning 진행 중..."
```

### 참고 자료
- 16.2.1: 단일 에이전트 설계
- 16.3.2: 핵심 구현 패턴
- 16.4.1: 설계 체크리스트

---

## 🟡 과제 2: 주간 리포트 생성 시스템 (중급)

### 목표
병렬 에이전트 팀을 구현하여 주간 업무 리포트를 자동 생성합니다.

### 시나리오
```
매주 금요일마다 주간 리포트를 작성해야 합니다.
- GitHub 활동 수집
- Slack 메시지 분석
- 주요 성과 요약

이 작업을 3개 에이전트가 협업하여 처리하도록 만들고 싶어요.
```

### 요구사항

**1. 에이전트 팀 구성**
```yaml
팀 이름: WeeklyReportTeam
목표: 주간 업무 리포트 생성

에이전트 3개:
  1. DataCollectionAgent
     - GitHub 활동 수집
     - Slack 메시지 수집
     - 캘린더 이벤트 수집
  
  2. AnalysisAgent
     - 활동 패턴 분석
     - 주요 성과 추출
     - 시간 사용 분석
  
  3. ReportAgent
     - 리포트 작성
     - 차트 생성
     - 최종 포맷팅

의존성:
  - AnalysisAgent는 DataCollectionAgent 완료 필요
  - ReportAgent는 AnalysisAgent 완료 필요
```

**2. 파일 시스템**
```
workspaces/weekly-report-001/
├── thinking/
│   ├── tc-data-collection/
│   │   └── ... (4 Stage)
│   ├── tc-analysis/
│   │   └── ... (4 Stage)
│   └── tc-report/
│       └── ... (4 Stage)
├── outputs/
│   ├── data_collection.json
│   ├── analysis.json
│   └── weekly_report.md
├── meta/
│   ├── goal.json
│   ├── dependencies.json  # 새로 추가
│   └── team_structure.json
└── checkpoints/
    ├── data-collection.json
    ├── analysis.json
    └── report.json
```

**3. 조율자 구현**

```yaml
WeeklyReportTeam:
  초기화:
    - task_id: 작업 식별자
    - week_number: 주차 번호
    - agents: 3개 에이전트 딕셔너리
    - dependencies: 의존성 맵
  
  run():
    목적: 팀 실행
    흐름:
      1. 실행 순서 결정 (위상 정렬)
      2. 순서대로 에이전트 실행
      3. 각 에이전트 결과를 파일로 저장
      4. 다음 에이전트가 파일 읽어서 사용
  
  _get_execution_order():
    목적: 의존성 기반 실행 순서 결정
    방법: 위상 정렬 (Topological Sort)
    결과: ["data_collection", "analysis", "report"]
```

**구현해야 할 것들**:
- [ ] 3개 에이전트 클래스
- [ ] 팀 조율자 (WeeklyReportTeam)
- [ ] 의존성 관리 (dependencies.json)
- [ ] 실행 순서 자동 결정
- [ ] 파일 기반 통신
- [ ] 전체 진행 상황 추적

### 예상 소요 시간
- **설계**: 1시간
- **구현**: 4-5시간
- **테스트**: 1시간
- **총**: 6-7시간

### 체크리스트

**설계 단계**:
- [ ] 3개 에이전트 역할 정의
- [ ] 의존성 맵 작성
- [ ] 에이전트 간 데이터 전달 방식 정의

**구현 단계**:
- [ ] 3개 에이전트 구현
- [ ] 팀 조율자 구현
- [ ] 의존성 자동 해결
- [ ] 파일 기반 통신 구현

**테스트 단계**:
- [ ] 순차 실행 확인
- [ ] 의존성 오류 처리 테스트
- [ ] 중간 에이전트 실패 시나리오
- [ ] 최종 리포트 품질 확인

### 성공 기준
```yaml
기능:
  ✓ 3개 에이전트가 순차적으로 실행
  ✓ 의존성이 자동으로 해결됨
  ✓ 에이전트 간 데이터 전달 정상
  ✓ 최종 리포트 생성 완료

협업:
  ✓ 각 에이전트가 독립적으로 동작
  ✓ 한 에이전트 실패 시 전체 중단
  ✓ 재시작 시 완료된 에이전트 건너뛰기

품질:
  ✓ 리포트가 유용한 정보 포함
  ✓ 데이터 수집이 완전함
  ✓ 분석이 의미 있음
```

### 힌트

**힌트 1: 의존성 해결 (위상 정렬)**
```yaml
_get_execution_order_개념:
  목적: 의존성을 고려한 실행 순서 결정
  
  알고리즘:
    1. 방문_집합 초기화 (visited = set)
    2. 순서_목록 초기화 (order = [])
    
    3. 각_에이전트_방문:
       - 이미 방문했으면 스킵
       - 방문 표시
       - 의존하는 에이전트 먼저 재귀 방문
       - 현재 에이전트를 order에 추가
    
    4. order 반환
  
  결과:
    - data_collection (의존성 없음)
    - analysis (data_collection 의존)
    - report (analysis 의존)
```

**힌트 2: 파일 기반 통신**
```yaml
에이전트_A_데이터_저장:
  - file_manager.save_json('outputs/data_collection.json', result)
  - 다음 에이전트가 사용할 데이터 저장

에이전트_B_데이터_읽기:
  - data = file_manager.load_json('outputs/data_collection.json')
  - 이전 에이전트 결과 로드
  - 자신의 처리 수행
```

**힌트 3: 팀 진행 상황**
```yaml
get_team_progress:
  목적: 팀 전체 진행 상황 확인
  
  계산:
    - completed = 완료된 에이전트 수
    - total = 전체 에이전트 수
    - progress_percent = (completed / total) × 100
  
  반환:
    completed_agents: 2
    total_agents: 3
    progress_percent: 66.7
```

### 참고 자료
- 16.2.2: 병렬 에이전트 팀 설계
- 16.2.4: 에이전트 간 통신 패턴
- 16.3.3: 오류 처리 및 복구

---

## 🔴 과제 3: 제품 기획 에이전트 시스템 (고급)

### 목표
계층적 에이전트 시스템을 구현하여 신제품 기획을 자동화합니다.

### 시나리오
```
새로운 SaaS 제품을 기획하고 있습니다.
시장 조사부터 포지셔닝, 가격 전략, Go-to-Market까지
전체 기획 과정을 에이전트 시스템이 담당하도록 만들고 싶어요.

입력: "개발자를 위한 AI 코드 리뷰 도구"
출력: 완전한 제품 기획서
```

### 요구사항

**1. 에이전트 시스템 구성**
```yaml
시스템 이름: ProductPlanningSystem
목표: 신제품 완전 기획

메타 조율자: MetaCoordinator
  역할:
    - 전체 일관성 검증
    - 각 에이전트 결과 승인
    - 최종 통합

실행 에이전트 4개:
  1. MarketResearchAgent
     - 시장 규모 분석
     - 경쟁사 분석
     - 고객 니즈 파악
  
  2. PositioningAgent
     - 타겟 고객 정의
     - 가치 제안 (Value Proposition)
     - 차별화 포인트
     (의존: MarketResearchAgent)
  
  3. PricingAgent
     - 가격 전략
     - 수익 모델
     - 경쟁력 분석
     (의존: MarketResearchAgent, PositioningAgent)
  
  4. GTMAgent (Go-to-Market)
     - 런칭 전략
     - 마케팅 채널
     - 실행 계획
     (의존: 모든 에이전트)
```

**2. 검증 루프**
```
각 에이전트 완료 후:
  1. MetaCoordinator가 결과 검증
  2. 핵심 가치 부합성 확인
  3. 이전 결과와 일관성 확인
  4. 통과하면 다음 에이전트
  5. 실패하면 피드백과 함께 재실행
```

**3. 파일 시스템**
```
workspaces/product-planning-001/
├── thinking/
│   ├── meta/
│   │   └── coordination_log.json
│   ├── tc-market-research/
│   ├── tc-positioning/
│   ├── tc-pricing/
│   └── tc-gtm/
├── outputs/
│   ├── market_research.json
│   ├── positioning.json
│   ├── pricing.json
│   ├── gtm_strategy.json
│   └── product_plan.md  # 최종 통합 기획서
├── meta/
│   ├── goal.json
│   ├── core_values.json
│   ├── dependencies.json
│   └── validation_history.json
└── checkpoints/
    └── ... (각 에이전트별)
```

**4. 메타 조율자 구현**

```yaml
MetaCoordinator:
  초기화:
    - task_id: 작업 식별자
    - product_idea: 제품 아이디어
    - core_values: 핵심 가치 목록
    - agents: 4개 실행 에이전트 딕셔너리
    - validation_history: 검증 이력
  
  run():
    목적: 시스템 실행
    흐름:
      1. 실행 순서 결정
      2. 각 에이전트 순차 실행:
         - 에이전트 실행
         - 결과 검증
         - 통과하면 다음, 실패하면 재실행
      3. 모든 결과 통합
      4. 최종 검증
      5. 기획서 생성
  
  _validate_result(agent_id, result):
    목적: 에이전트 결과 검증
    검증_항목:
      - 핵심 가치 부합성
      - 완전성
      - 실행 가능성
      - 이전 결과와 일관성
    반환:
      passed: true/false
      score: 0-10
      issues: []
      feedback: "..."
  
  _integrate_all_results():
    목적: 모든 결과 통합
    방법:
      - 4개 에이전트 결과 수집
      - AI로 통합 기획서 작성
      - 구조화된 문서 생성
```

**구현해야 할 것들**:
- [ ] MetaCoordinator 클래스
- [ ] 4개 실행 에이전트
- [ ] 검증 로직 (핵심 가치 부합성, 일관성)
- [ ] 재실행 메커니즘 (피드백 기반)
- [ ] 최종 통합 로직
- [ ] 전체 조율 로그

### 예상 소요 시간
- **설계**: 2시간
- **구현**: 8-10시간
- **테스트**: 2시간
- **총**: 12-14시간

### 체크리스트

**설계 단계**:
- [ ] 메타 조율자 역할 정의
- [ ] 4개 에이전트 역할 및 의존성
- [ ] 검증 기준 정의
- [ ] 재실행 시나리오 설계

**구현 단계**:
- [ ] MetaCoordinator 구현
- [ ] 4개 에이전트 구현
- [ ] 검증 로직 구현
- [ ] 재실행 메커니즘
- [ ] 최종 통합 로직

**테스트 단계**:
- [ ] 전체 시스템 정상 실행
- [ ] 검증 실패 → 재실행 테스트
- [ ] 최종 기획서 품질 확인
- [ ] 일관성 검증

### 성공 기준
```yaml
기능:
  ✓ 4개 에이전트가 순차 실행
  ✓ 각 단계마다 메타 검증
  ✓ 검증 실패 시 재실행
  ✓ 최종 통합 기획서 생성

품질:
  ✓ 모든 결과가 핵심 가치와 일치
  ✓ 에이전트 간 일관성 유지
  ✓ 실행 가능한 기획서

고급 기능:
  ✓ Human-in-the-Loop (선택)
  ✓ 비용 추적
  ✓ 성능 모니터링
```

### 힌트

**힌트 1: 검증 로직**
```yaml
_validate_result_개념:
  목적: 에이전트 결과 검증
  
  프롬프트_구조:
    역할: "제품 기획 검증 전문가"
    입력:
      - 핵심 가치
      - 에이전트 ID
      - 결과 데이터
    
    검증_항목:
      1. 핵심_가치_부합성: 결과가 핵심 가치와 일치하는가?
      2. 완전성: 필요한 모든 정보가 포함되었는가?
      3. 실행_가능성: 실제로 실행 가능한 계획인가?
    
    응답_형식: JSON
      passed: true/false
      score: 0-10
      issues: ["문제점들"]
      feedback: "개선 방향"
```

**힌트 2: 재실행 with 피드백**
```yaml
_run_agent_with_validation_개념:
  목적: 검증 포함 에이전트 실행
  
  흐름:
    max_attempts: 3
    
    for attempt in range(max_attempts):
      1. 에이전트_실행:
         - agents[agent_id].run(context)
      
      2. 결과_검증:
         - _validate_result(agent_id, result)
      
      3. 검증_통과:
         - validation['passed'] == true
         - 결과 반환
      
      4. 검증_실패:
         - context에 feedback 추가
         - 재시도 메시지 출력
         - 다음 attempt
    
    최종_실패:
      - ValidationFailed 예외 발생
```

**힌트 3: 최종 통합**
```yaml
_integrate_all_results_개념:
  목적: 모든 결과를 하나의 기획서로 통합
  
  프롬프트_구조:
    역할: "제품 기획 통합 전문가"
    
    입력:
      - 시장 조사 결과
      - 포지셔닝 결과
      - 가격 전략 결과
      - Go-to-Market 결과
    
    요청:
      "이 결과들을 통합하여 완전한 제품 기획서를 작성하세요"
    
    기획서_구조:
      1. Executive Summary
      2. Market Analysis
      3. Product Positioning
      4. Pricing Strategy
      5. Go-to-Market Plan
      6. Success Metrics
      7. Risks and Mitigation
  
  출력:
    - 구조화된 기획서 (마크다운)
    - product_plan.md 파일로 저장
```

### 참고 자료
- 16.2.3: 계층적 에이전트 시스템
- 16.3.3: 오류 처리 및 복구
- 16.4.1: 설계 체크리스트

---

## 제출 및 피드백

### 제출 방법
1. GitHub 저장소에 코드 푸시
2. `README.md`에 실행 방법 작성
3. 각 과제별로 `outputs/` 디렉토리의 결과 포함

### 자가 평가
```yaml
과제 1 (단일 에이전트):
  □ 4 Stage 모두 구현
  □ 파일 시스템 올바르게 구성
  □ 체크포인트 및 재개 동작
  □ 생성된 포스트 품질 만족

과제 2 (병렬 에이전트):
  □ 3개 에이전트 구현
  □ 의존성 자동 해결
  □ 에이전트 간 통신 정상
  □ 최종 리포트 유용성

과제 3 (계층적 에이전트):
  □ 메타 조율자 구현
  □ 4개 실행 에이전트 구현
  □ 검증 루프 동작
  □ 최종 기획서 완성도
```

### 다음 단계

**과제를 완료했다면**:
1. ✅ Part 4 완전 정복!
2. 🎯 Part 5 준비 (시스템 확장과 운영)
3. 🚀 실전 프로젝트에 적용

**더 학습하고 싶다면**:
- LangChain/AutoGen 프레임워크 학습
- 프로덕션 배포 학습
- 모니터링 및 로깅 심화

**커뮤니티**:
- GitHub에 프로젝트 공유
- Discord/Slack 커뮤니티 참여
- 다른 학습자와 경험 공유

---

축하합니다! Part 4 실습을 모두 완료했어요! 🎉
