# 16.3 에이전트 구현 가이드 (Part 1)

이제 실제로 에이전트를 구현하는 방법을 알아볼게요. 16.2에서 본 세 가지 패턴을 어떻게 코드로 만들 수 있는지 단계별로 살펴보겠습니다.

---

## 16.3.1 구현 옵션 비교

에이전트를 구현하는 방법은 크게 세 가지예요. 각각의 장단점을 이해하고 상황에 맞는 선택을 하는 것이 중요합니다.

### Option 1: API 직접 호출

**개념**: Anthropic API나 OpenAI API를 직접 호출하여 모든 로직을 직접 구현하는 방식이에요.

**장점**:
- ✅ 완전한 제어권: 모든 로직을 원하는 대로 구현 가능
- ✅ 불필요한 의존성 없음: 외부 라이브러리 불필요
- ✅ 최적화 가능: 성능과 비용을 직접 최적화

**단점**:
- ❌ 개발 시간 많이 소요: 모든 것을 직접 구현해야 함
- ❌ 반복 코드 많음: 상태 관리, 재시도 로직 등 매번 구현
- ❌ 유지보수 부담: 버그 수정, 기능 추가 모두 직접

**적합한 경우**:
- 간단한 단일 에이전트
- 특수한 요구사항 (예: 극도로 최적화된 성능 필요)
- 기존 시스템과의 긴밀한 통합 필요

**구현 구조**:
```yaml
SimpleContentAgent:
  초기화:
    - task_id: 작업 식별자
    - goal: 목표
    - core_values: 핵심 가치
    - memory: 빈 딕셔너리 (단계별 결과 저장)
  
  실행_흐름:
    1. Planning:
       - 프롬프트 생성 (목표, 핵심 가치 포함)
       - API 호출
       - 결과를 memory['planning']에 저장
    
    2. Reasoning:
       - Planning 결과를 포함한 프롬프트 생성
       - API 호출
       - 결과를 memory['reasoning']에 저장
    
    3. Experimenting:
       - Reasoning 결과를 포함한 프롬프트 생성
       - API 호출
       - 결과를 memory['experimenting']에 저장
    
    4. Reflecting:
       - Experimenting 결과를 포함한 프롬프트 생성
       - API 호출
       - 최종 결과 반환
  
  API_호출_로직:
    재시도_메커니즘:
      - 최대 3회 재시도
      - 실패 시 지수 백오프 (2^attempt 초)
      - 마지막 시도 실패 시 예외 발생
    
    호출_파라미터:
      - model: "claude-sonnet-4-20250514"
      - max_tokens: 4000
      - messages: [{"role": "user", "content": prompt}]
  
  프롬프트_구조:
    Planning_프롬프트:
      - 역할: "콘텐츠 기획 전문가"
      - 목표: goal 값
      - 핵심_가치: core_values 값
      - 요청: "콘텐츠 구조 설계"
```

**평가**: 간단한 에이전트라면 좋지만, 복잡해질수록 직접 관리하는 것이 부담스러워요.

### Option 2: 에이전트 프레임워크 사용

**개념**: LangChain, AutoGen, CrewAI 같은 에이전트 프레임워크를 활용하는 방식이에요.

**장점**:
- ✅ 빠른 개발: 공통 패턴이 이미 구현되어 있음
- ✅ 검증된 코드: 많은 사용자가 테스트한 안정적 코드
- ✅ 커뮤니티 지원: 문서, 예제, 커뮤니티 지원 풍부

**단점**:
- ❌ 프레임워크 학습 필요: 각 프레임워크의 철학과 API 학습
- ❌ 제약사항 존재: 프레임워크가 지원하는 패턴으로 제한됨
- ❌ 의존성 증가: 프레임워크 버전 업데이트에 영향받음

#### LangChain Agents 개념

```yaml
LangChain_구조:
  핵심_개념:
    - LLM: 언어 모델 (Claude, GPT 등)
    - Tools: 에이전트가 사용할 수 있는 도구들
    - Agent: LLM과 Tools를 연결
    - AgentExecutor: Agent 실행 관리
  
  구성_요소:
    LLM_설정:
      - model: "claude-sonnet-4-20250514"
      - temperature: 0.3
    
    Tools_정의:
      - name: 도구 이름
      - func: 실제 실행 함수
      - description: 도구 설명 (LLM이 선택 시 참고)
    
    Agent_생성:
      - prompt: 시스템 메시지 + 입력 템플릿
      - llm: 사용할 언어 모델
      - tools: 사용 가능한 도구 목록
    
    실행:
      - AgentExecutor가 Agent와 Tools 조율
      - LLM이 어떤 Tool을 사용할지 결정
      - Tool 실행 결과를 LLM에 다시 전달
      - 최종 답변 생성

  사용_예시_흐름:
    1. "신제품 런칭 전략 수립" 요청
    2. LLM이 "먼저 시장 분석이 필요" 판단
    3. MarketAnalysis Tool 호출
    4. 결과를 받아 "이제 전략 수립" 판단
    5. StrategyCreation Tool 호출
    6. 최종 전략 반환
```

#### AutoGen 개념

```yaml
AutoGen_구조:
  핵심_개념:
    - Multi-Agent 대화
    - 각 에이전트가 서로 대화하며 문제 해결
    - Human-in-the-Loop 자연스럽게 통합
  
  주요_에이전트_타입:
    AssistantAgent:
      - 역할: AI 어시스턴트
      - 특징: LLM 기반 응답 생성
      - 사용: 분석, 기획, 전략 수립
    
    UserProxyAgent:
      - 역할: 사용자 대리
      - 특징: 코드 실행, 사용자 입력 처리
      - 사용: 실행 검증, 승인 요청
  
  대화_흐름:
    1. UserProxy가 AssistantAgent에 요청
    2. Assistant가 응답 생성
    3. UserProxy가 검증 (자동 또는 인간)
    4. 필요시 추가 대화 반복
    5. 목표 달성 시 종료

  사용_예시_흐름:
    설정:
      - MarketingAssistant: 마케팅 전문가 역할
      - UserProxy: 사용자 대리 (자동 모드)
    
    대화:
      1. UserProxy: "신제품 런칭 전략 수립"
      2. Assistant: "먼저 시장 조사가 필요합니다..."
      3. UserProxy: "진행하세요"
      4. Assistant: "분석 결과... 이제 전략은..."
      5. 완료
```

#### CrewAI 개념

```yaml
CrewAI_구조:
  핵심_개념:
    - Role 기반 에이전트
    - Task 중심 워크플로우
    - Sequential/Parallel 프로세스
  
  구성_요소:
    Agent:
      - role: 역할 (예: 시장 조사원)
      - goal: 목표
      - backstory: 배경 스토리 (페르소나)
      - verbose: 로깅 여부
    
    Task:
      - description: 작업 설명
      - agent: 담당 에이전트
      - expected_output: 기대 결과 (선택)
    
    Crew:
      - agents: 에이전트 목록
      - tasks: 작업 목록
      - process: Sequential 또는 Parallel
  
  실행_흐름:
    Sequential_프로세스:
      1. Task 1 → Agent A 실행
      2. Task 1 완료
      3. Task 2 → Agent B 실행 (Task 1 결과 참조)
      4. Task 2 완료
      5. 전체 완료
    
    Parallel_프로세스:
      1. Task 1, 2, 3 동시 실행
      2. 모두 완료 대기
      3. 결과 통합

  사용_예시_흐름:
    설정:
      - researcher: 시장 조사원 (10년 경력)
      - strategist: 전략 기획자 (마케팅 전문가)
    
    Tasks:
      - research_task: 시장 조사
      - strategy_task: 전략 수립
    
    실행:
      1. researcher가 시장 조사 수행
      2. strategist가 조사 결과로 전략 수립
      3. 최종 전략 반환
```

**프레임워크 선택 가이드**:
| 프레임워크 | 특징 | 적합한 경우 |
|-----------|------|------------|
| **LangChain** | - Tool 중심<br>- 복잡한 체인 구성<br>- RAG 통합 쉬움 | - 데이터 기반 애플리케이션<br>- 다양한 Tool 통합 필요<br>- 검색-증강 생성 |
| **AutoGen** | - Multi-Agent 대화<br>- 코드 실행<br>- Human-in-the-Loop | - 협업 에이전트<br>- 코드 생성/실행<br>- 대화형 작업 |
| **CrewAI** | - Role 기반<br>- 프로세스 중심<br>- 간단한 API | - 역할이 명확한 팀<br>- 순차/병렬 프로세스<br>- 빠른 프로토타입 |

### Option 3: 클라우드 서비스 활용

**개념**: OpenAI Assistants API나 Anthropic Claude API의 고수준 기능을 사용하는 방식이에요.

**장점**:
- ✅ 관리 불필요: 인프라, 확장, 모니터링 모두 서비스에서 처리
- ✅ 빠른 시작: 복잡한 설정 없이 바로 사용 가능
- ✅ 지속적 개선: 서비스 제공자가 계속 업데이트

**단점**:
- ❌ 제어 제한: 내부 로직을 직접 제어할 수 없음
- ❌ 비용: 서비스 요금 지불 필요
- ❌ 종속성: 서비스 변경/중단에 영향받음

#### OpenAI Assistants API 개념

```yaml
Assistants_API_구조:
  핵심_개념:
    - Assistant: 영구적인 AI 어시스턴트
    - Thread: 대화 스레드
    - Message: 대화 메시지
    - Run: 실행 단위
  
  구성_요소:
    Assistant_생성:
      - name: 어시스턴트 이름
      - instructions: 시스템 지침
      - model: 사용 모델
      - tools: 사용 도구 (code_interpreter 등)
    
    Thread_생성:
      - 독립적인 대화 공간
      - 여러 Message 포함
      - 컨텍스트 자동 관리
    
    Message_추가:
      - role: "user" 또는 "assistant"
      - content: 메시지 내용
    
    Run_실행:
      - Thread에서 Assistant 실행
      - 비동기 처리
      - 상태: queued → in_progress → completed
  
  실행_흐름:
    1. Assistant_생성:
       - 한 번 생성, 계속 재사용
       - 역할과 지침 설정
    
    2. Thread_생성:
       - 작업마다 새 Thread
       - 대화 컨텍스트 격리
    
    3. Message_추가:
       - 사용자 요청 추가
    
    4. Run_실행:
       - Assistant가 처리 시작
       - 비동기로 진행
    
    5. 완료_대기:
       - 상태 주기적 확인
       - completed 상태까지 대기
    
    6. 결과_가져오기:
       - Thread의 Message 목록 조회
       - Assistant의 응답 추출

  장점:
    - 상태 관리 자동화
    - 코드 실행 내장
    - 파일 업로드/다운로드 지원
    - 다중 대화 관리
```

### 구현 옵션 선택 기준

다음 결정 트리를 따라 자신에게 맞는 옵션을 선택하세요:

```
[에이전트 구현 필요]
    |
    ├─ 복잡도: 단순 (1-2 Stage)
    |   └─ 특수 요구사항 있나요?
    |       ├─ Yes → Option 1 (API 직접)
    |       └─ No → Option 3 (클라우드)
    |
    ├─ 복잡도: 중간 (3-5 Stage)
    |   └─ 프레임워크 경험 있나요?
    |       ├─ Yes → Option 2 (프레임워크)
    |       └─ No → 학습 시간 있나요?
    |           ├─ Yes → Option 2
    |           └─ No → Option 1
    |
    └─ 복잡도: 복잡 (6+ Stage)
        └─ 팀 규모는?
            ├─ 1-2명 → Option 1 (API 직접)
            └─ 3명+ → Option 2 (프레임워크)
```

**필자 추천**:
```yaml
초심자:
  - 먼저: Option 1 (API 직접) + 간단한 예제로 시작
  - 그 다음: Option 3 (클라우드) 탐색
  - 필요할 때: Option 2 (프레임워크) 학습

실무자:
  - 프로토타입: Option 3 (클라우드) 빠른 검증
  - 실제 구현: Option 1 (API 직접) 최적화
  - 대규모 시스템: Option 2 (프레임워크) 협업
```

---

## 16.3.2 핵심 구현 패턴

어떤 옵션을 선택하든, 다음의 핵심 패턴들은 반드시 알아두어야 해요. 이 패턴들을 재사용 가능한 유틸리티로 만들어두면 에이전트 구현이 훨씬 쉬워집니다.

### 패턴 1: 상태 머신 (State Machine)

**왜 필요한가요?**  
에이전트가 여러 Stage를 거치며 작업할 때, 현재 어느 단계에 있는지 추적하고 다음 단계로 안전하게 이동하는 메커니즘이 필요해요.

**구현 개념**:
```yaml
상태_머신_구조:
  StageStatus:
    목적: Stage의 상태를 나타내는 열거형
    값:
      - PENDING: 대기 중
      - IN_PROGRESS: 실행 중
      - COMPLETED: 완료
      - FAILED: 실패
  
  Stage:
    목적: 개별 Stage 정의
    속성:
      - name: Stage 이름
      - handler: 실행할 함수
      - description: 설명
      - status: 현재 상태 (StageStatus)
      - result: 실행 결과
      - error: 오류 메시지 (있는 경우)
  
  AgentStateMachine:
    목적: 여러 Stage의 실행 순서와 상태 관리
    
    속성:
      - stages: Stage 목록
      - current_index: 현재 Stage 인덱스
      - history: 실행 히스토리
    
    주요_메서드:
      get_current_stage():
        - 현재 Stage 반환
        - 모든 Stage 완료 시 None
      
      execute_current_stage(context):
        - 현재 Stage 실행
        - 상태를 IN_PROGRESS로 변경
        - handler 함수 호출
        - 성공 시: COMPLETED, 결과 저장
        - 실패 시: FAILED, 오류 저장
        - history에 기록
      
      move_next():
        - 다음 Stage로 이동
        - 가능하면 True, 불가능하면 False
      
      get_progress():
        - 진행 상황 반환
        - total_stages: 전체 Stage 수
        - completed_stages: 완료된 Stage 수
        - current_stage: 현재 Stage 이름
        - progress_percent: 진행률 (%)

사용_패턴:
  1. Stage_정의:
     - 각 Stage마다 handler 함수 정의
     - Stage 객체 생성 (name, handler, description)
  
  2. StateMachine_생성:
     - Stage 목록으로 AgentStateMachine 생성
  
  3. 실행_루프:
     - current_stage 있는 동안 반복:
       * execute_current_stage(context) 호출
       * 결과를 context에 추가
       * move_next() 호출
       * 이동 불가능하면 종료
  
  4. 진행_상황_확인:
     - get_progress()로 현재 진행률 확인
     - 사용자에게 피드백 제공

장점:
  - 명확한 상태 추적
  - 오류 처리 일관성
  - 재시작 가능 (체크포인트)
  - 진행 상황 가시성
```

### 패턴 2: 파일 I/O 자동화

**왜 필요한가요?**  
에이전트는 파일 시스템을 통해 입출력을 주고받아요. 디렉토리 생성, 파일 저장, JSON 직렬화 등 반복 작업을 자동화하면 코드가 간결해집니다.

**구현 개념**:
```yaml
파일_관리자_구조:
  FileManager:
    목적: 파일 I/O 작업 자동화
    
    초기화:
      - base_dir: 기본 디렉토리 경로
      - 디렉토리 자동 생성
    
    핵심_메서드:
      _ensure_directory(path):
        - 디렉토리가 없으면 생성
        - parents=True: 부모 디렉토리도 생성
        - exist_ok=True: 이미 존재해도 오류 없음
      
      get_path(relative_path):
        - 상대 경로를 절대 경로로 변환
        - base_dir 기준으로 결합
      
      save_json(relative_path, data):
        - JSON 파일로 저장
        - 디렉토리 자동 생성
        - UTF-8 인코딩
        - 들여쓰기 2칸
        - 저장 확인 메시지 출력
      
      load_json(relative_path):
        - JSON 파일 로드
        - 파일 없으면 FileNotFoundError
        - 파싱 후 반환
      
      save_text(relative_path, text):
        - 텍스트 파일로 저장
        - 디렉토리 자동 생성
        - UTF-8 인코딩
      
      load_text(relative_path):
        - 텍스트 파일 로드
        - 전체 내용 문자열로 반환
    
    사고_클러스터_전용_헬퍼:
      save_thinking_record(cluster_id, stage, record):
        - thinking_record.json 저장
        - 경로: thinking/{cluster_id}/{stage}/thinking_record.json
        - record를 JSON으로 저장
      
      load_thinking_record(cluster_id, stage):
        - thinking_record.json 로드
        - 경로: thinking/{cluster_id}/{stage}/thinking_record.json
        - JSON을 딕셔너리로 반환

사용_패턴:
  1. 초기화:
     - FileManager('./workspaces/task-123')
     - 작업 디렉토리 자동 생성
  
  2. JSON_저장:
     - save_json('outputs/result.json', data)
     - outputs/ 디렉토리 자동 생성
     - data를 JSON 형식으로 저장
  
  3. thinking_record_저장:
     - save_thinking_record('tc-c1', 'planning', record)
     - thinking/tc-c1/planning/ 자동 생성
     - thinking_record.json 저장
  
  4. 파일_로드:
     - load_json('outputs/result.json')
     - 파일 존재 확인
     - JSON 파싱 후 반환

디렉토리_구조_예시:
  workspaces/task-123/
  ├── thinking/
  │   ├── tc-c1/
  │   │   ├── planning/
  │   │   │   └── thinking_record.json
  │   │   ├── reasoning/
  │   │   │   └── thinking_record.json
  │   │   └── ...
  │   └── tc-c2/
  │       └── ...
  ├── outputs/
  │   ├── result.json
  │   └── report.md
  └── data/
      └── input.csv

장점:
  - 경로 관리 간소화
  - 오류 처리 일관성
  - 디렉토리 자동 생성
  - 인코딩 통일
  - 재사용성 높음
```

---

**(계속 Part 2로)**
