# 16.3 에이전트 구현 가이드 (Part 2)

## 16.3.2 핵심 구현 패턴 (계속)

### 패턴 3: 재시도 로직 (Retry Logic)

**왜 필요한가요?**  
AI API 호출은 네트워크 문제나 레이트 리밋으로 실패할 수 있어요. 자동 재시도 로직을 추가하면 안정성이 크게 향상됩니다.

**구현 개념**:
```yaml
재시도_설정:
  RetryConfig:
    목적: 재시도 동작 설정
    
    속성:
      max_retries: 최대 재시도 횟수 (기본: 3)
      base_delay: 기본 대기 시간 (초, 기본: 1.0)
      max_delay: 최대 대기 시간 (초, 기본: 60.0)
      exponential_backoff: 지수 백오프 사용 여부 (기본: true)
      retry_on_exceptions: 재시도할 예외 타입들
    
    예시:
      max_retries: 3
      base_delay: 1.0
      max_delay: 60.0
      exponential_backoff: true
      retry_on_exceptions: [ConnectionError, TimeoutError]

재시도_로직:
  with_retry:
    목적: 함수를 재시도 로직으로 감싸서 실행
    
    동작_흐름:
      1. 함수 실행 시도
      2. 성공하면 결과 반환
      3. 실패하면:
         - 재시도 가능한 예외인가? → 아니면 즉시 예외 발생
         - 최대 재시도 도달? → 예이면 예외 발생
         - 대기 시간 계산:
           * 지수_백오프 = base_delay × 2^attempt
           * max_delay를 초과하지 않도록 제한
         - 대기 후 다시 시도 (1단계로)
    
    대기_시간_예시:
      시도_1: 1.0초
      시도_2: 2.0초
      시도_3: 4.0초
      시도_4: 8.0초
      시도_5: 16.0초

  retry_decorator:
    목적: 함수에 재시도 로직을 decorator로 적용
    
    사용_방법:
      - 함수 정의 시 @retry(config) 추가
      - 함수 호출 시 자동으로 재시도 로직 적용

API_호출_특화_설정:
  API_RETRY_CONFIG:
    max_retries: 5
    base_delay: 1.0
    max_delay: 30.0
    exponential_backoff: true
    retry_on_exceptions:
      - ConnectionError
      - TimeoutError
      - RateLimitError
  
  적용_사례:
    - BaseAgent의 call_ai 메서드
    - 모든 API 호출에 자동 적용
    - 일시적 오류에 강건하게 대응

장점:
  - 일시적 네트워크 문제 자동 해결
  - 레이트 리밋 자동 대응
  - 안정성 대폭 향상
  - 수동 재시도 불필요
```

### 패턴 4: Human-in-the-Loop

**왜 필요한가요?**  
에이전트가 중요한 결정을 내려야 할 때, 사람의 승인을 받는 것이 안전해요. 특히 비용이 많이 드는 작업이나 되돌리기 어려운 작업에서는 필수입니다.

**구현 개념**:
```yaml
승인_상태:
  ApprovalStatus:
    - PENDING: 승인 대기 중
    - APPROVED: 승인됨
    - REJECTED: 거부됨
    - TIMEOUT: 승인 시간 초과

승인_응답:
  ApprovalResponse:
    속성:
      - status: 승인 상태 (ApprovalStatus)
      - feedback: 피드백 메시지 (선택)
      - modifications: 수정 사항 (선택)
    
    is_approved:
      - status가 APPROVED이면 true
      - 그 외는 false

알림_시스템:
  Notifier_인터페이스:
    목적: 알림 발송 추상화
    메서드: send(message)
  
  구현_예시:
    SlackNotifier:
      - webhook_url: Slack 웹훅 URL
      - channel: 알림 채널
      - 메시지를 Slack으로 전송
    
    EmailNotifier:
      - recipient: 수신자 이메일
      - smtp_config: SMTP 설정
      - 메시지를 이메일로 전송

승인_게이트:
  ApprovalGate:
    목적: Human-in-the-Loop 승인 프로세스 관리
    
    초기화:
      - notifier: 알림 발송자
      - timeout_seconds: 승인 타임아웃 (기본: 3600초 = 1시간)
      - pending_approvals: 대기 중인 승인 목록
    
    require_approval(approval_id, context, explanation):
      동작_흐름:
        1. 알림_발송:
           - type: "approval_request"
           - approval_id: 승인 식별자
           - explanation: 설명 메시지
           - context: 승인 컨텍스트
           - timeout: 타임아웃 시간
        
        2. 승인_대기:
           - 주기적으로 pending_approvals 확인
           - approval_id에 대한 응답이 있는가?
             * 있으면 → 응답 반환
             * 없으면 → 계속 대기
           - 타임아웃 초과 시:
             * TIMEOUT 응답 반환
        
        3. 응답_반환:
           - ApprovalResponse 객체
           - 호출자는 is_approved로 승인 여부 확인
    
    submit_approval(approval_id, approved, feedback):
      동작:
        - 외부에서 승인 응답 제출
        - approved=true이면 APPROVED
        - approved=false이면 REJECTED
        - pending_approvals에 저장
        - require_approval이 응답 발견

사용_시나리오:
  마케팅_캠페인_런칭:
    1. 에이전트가 캠페인 계획 수립
    2. 예상_비용: $50,000
    3. approval_gate.require_approval() 호출
    4. Slack으로 승인 요청 알림
    5. 담당자가 검토
    6. approval_gate.submit_approval() 호출
    7. 승인되면 캠페인 실행
    8. 거부되면 작업 중단

적용_사례:
  - 고비용 작업 (광고 캠페인, 대규모 이메일 발송)
  - 되돌리기 어려운 작업 (데이터 삭제, 공개 발표)
  - 법적/윤리적 검토 필요 작업
  - 브랜드 이미지 관련 작업

장점:
  - 중요한 결정에 인간 개입
  - 위험 감소
  - 책임 소재 명확
  - 타임아웃으로 무한 대기 방지
```

---

## 16.3.3 오류 처리 및 복구

에이전트가 실패했을 때 어떻게 대응하느냐가 시스템의 신뢰성을 결정해요.

### 체크포인트 및 재개 (Checkpoint & Resume)

**왜 필요한가요?**  
에이전트가 긴 작업을 수행 중 실패하면, 처음부터 다시 시작하는 것은 비효율적이에요. 체크포인트를 저장하고 실패 지점부터 재개하면 시간과 비용을 절약할 수 있습니다.

**구현 개념**:
```yaml
체크포인트_데이터:
  Checkpoint:
    목적: 특정 시점의 상태 저장
    
    속성:
      - stage_name: Stage 이름
      - stage_index: Stage 인덱스
      - result: 실행 결과
      - timestamp: 저장 시간
    
    직렬화:
      - to_dict(): 딕셔너리로 변환
      - from_dict(): 딕셔너리에서 복원

체크포인트_관리자:
  CheckpointManager:
    목적: 체크포인트 저장/로드 관리
    
    초기화:
      - base_dir: 기본 디렉토리
      - task_id: 작업 식별자
      - checkpoint_file: {base_dir}/checkpoints/{task_id}.json
      - 디렉토리 자동 생성
    
    save_checkpoint(stage_name, stage_index, result):
      동작:
        1. Checkpoint 객체 생성
        2. 현재 시간 기록
        3. JSON 파일로 저장
        4. 저장 확인 메시지 출력
    
    load_checkpoint():
      동작:
        1. checkpoint_file 존재 확인
        2. 없으면 None 반환
        3. 있으면 JSON 로드
        4. Checkpoint 객체로 변환
        5. 로드 확인 메시지 출력
    
    clear_checkpoint():
      동작:
        - checkpoint_file 삭제
        - 작업 완료 후 호출

BaseAgent_통합:
  run(resume=True):
    동작_흐름:
      1. 시작_준비:
         - start_stage_index = 0
         - previous_results = {}
      
      2. 체크포인트_확인 (resume=True인 경우):
         - checkpoint = load_checkpoint()
         - checkpoint가 있으면:
           * start_stage_index = checkpoint.stage_index + 1
           * previous_results = checkpoint.result
           * "재개 중..." 메시지
      
      3. Stage_실행_루프:
         - start_stage_index부터 끝까지:
           * Stage 실행
           * 성공 시:
             - 체크포인트 저장
             - previous_results에 추가
           * 실패 시:
             - 오류 메시지
             - "resume=True로 재실행하면 이 지점부터 계속" 안내
             - 예외 발생
      
      4. 완료_처리:
         - 체크포인트 삭제
         - 최종 결과 반환

실제_사용_예시:
  첫_번째_실행:
    - agent.run() 호출
    - Planning 완료 → 체크포인트 저장
    - Reasoning 완료 → 체크포인트 저장
    - Experimenting 중 실패 → 예외 발생
  
  재실행:
    - agent.run(resume=True) 호출
    - 체크포인트 로드: "Reasoning 완료됨"
    - Experimenting부터 재개
    - Reflecting 완료
    - 전체 완료 → 체크포인트 삭제

장점:
  - 시간 절약 (완료된 단계 스킵)
  - 비용 절약 (API 재호출 불필요)
  - 안정성 향상 (언제든 재개 가능)
  - 디버깅 용이 (실패 지점 명확)
```

### 로깅 및 디버깅

**구현 개념**:
```yaml
에이전트_로거:
  AgentLogger:
    목적: 에이전트 전용 로깅 시스템
    
    초기화:
      - task_id: 작업 식별자
      - log_file: 로그 파일 경로 (선택)
      - logger 생성 (logging.getLogger)
      - 로그 레벨: DEBUG
    
    핸들러_설정:
      Console_Handler:
        - 레벨: INFO
        - 출력: 표준 출력
        - 형식: [시간] [이름] [레벨] 메시지
      
      File_Handler (log_file 지정 시):
        - 레벨: DEBUG
        - 출력: 파일
        - 형식: [시간] [이름] [레벨] 메시지
        - 인코딩: UTF-8
    
    주요_메서드:
      stage_start(stage_name):
        - 메시지: "🚀 {stage_name} 시작"
        - 레벨: INFO
      
      stage_complete(stage_name, duration_seconds):
        - 메시지: "✅ {stage_name} 완료 ({duration}초)"
        - 레벨: INFO
      
      stage_failed(stage_name, error):
        - 메시지: "❌ {stage_name} 실패: {error}"
        - 레벨: ERROR
      
      api_call(prompt_preview, tokens):
        - 메시지: "🔵 API 호출: {prompt[:50]}... (토큰: {tokens})"
        - 레벨: DEBUG
      
      human_approval_required(approval_id):
        - 메시지: "⏸️  승인 대기: {approval_id}"
        - 레벨: WARNING
      
      human_approval_received(approval_id, approved):
        - 메시지: "✓ 승인 응답: {approval_id} -> 승인/거부"
        - 레벨: INFO

로그_활용:
  개발_단계:
    - Console에서 실시간 확인
    - 문제 발생 시 즉시 파악
  
  운영_단계:
    - 파일에 모든 로그 기록
    - 문제 발생 시 로그 분석
    - 성능 모니터링
  
  디버깅:
    - DEBUG 레벨로 상세 정보
    - API 호출 내용 확인
    - Stage별 소요 시간 분석

로그_예시:
  "[2025-11-02 10:30:15] [agent.content-001] [INFO] 🚀 planning 시작"
  "[2025-11-02 10:30:18] [agent.content-001] [DEBUG] 🔵 API 호출: 당신은 콘텐츠 기획 전문가입니다... (토큰: 1500)"
  "[2025-11-02 10:30:30] [agent.content-001] [INFO] ✅ planning 완료 (15.3초)"
  "[2025-11-02 10:30:31] [agent.content-001] [WARNING] ⏸️  승인 대기: idea-selection-001"
```

### 알림 및 모니터링

**구현 개념**:
```yaml
알림_관리자:
  AlertManager:
    목적: 다양한 이벤트에 대한 알림 발송
    
    초기화:
      - notifiers: 알림 발송자 목록 (Slack, Email 등)
    
    alert_failure(task_id, stage_name, error):
      목적: 실패 알림
      
      메시지_내용:
        - type: "agent_failure"
        - task_id: 작업 ID
        - stage: 실패한 Stage
        - error: 오류 메시지
        - timestamp: 발생 시간
      
      발송:
        - 모든 notifiers에게 전송
        - 즉시 확인 필요
    
    alert_completion(task_id, duration_seconds):
      목적: 완료 알림
      
      메시지_내용:
        - type: "agent_completion"
        - task_id: 작업 ID
        - duration: 소요 시간
        - timestamp: 완료 시간
      
      발송:
        - 모든 notifiers에게 전송
        - 성공 확인
    
    alert_cost_warning(task_id, current_cost, budget):
      목적: 비용 경고
      
      조건:
        - current_cost > budget × 0.8
        - 예산의 80% 초과 시 경고
      
      메시지_내용:
        - type: "cost_warning"
        - task_id: 작업 ID
        - current_cost: 현재 비용
        - budget: 예산
        - percent: 사용률 (%)
      
      발송:
        - 모든 notifiers에게 전송
        - 예산 초과 방지

알림_전략:
  중요도별_채널:
    CRITICAL (실패):
      - Slack #alerts
      - Email (팀 전체)
      - SMS (담당자)
    
    WARNING (비용 경고):
      - Slack #monitoring
      - Email (담당자)
    
    INFO (완료):
      - Slack #status
      - Email (선택)

모니터링_대시보드:
  실시간_지표:
    - 실행 중인 에이전트 수
    - 평균 완료 시간
    - 실패율
    - 총 비용
  
  알림_히스토리:
    - 최근 24시간 알림
    - 실패 원인 분석
    - 비용 추이
```

---

## 16.3.4 성능 최적화

에이전트를 실전에서 사용하려면 성능과 비용 최적화가 필수예요.

### API 호출 최소화

**1. 결과 캐싱**:
```yaml
응답_캐시:
  ResponseCache:
    목적: API 응답 캐싱으로 중복 호출 방지
    
    초기화:
      - cache_dir: 캐시 저장 디렉토리
      - 디렉토리 자동 생성
    
    _get_cache_key(prompt, model):
      목적: 캐시 키 생성
      방법:
        - "{model}:{prompt}" 문자열 생성
        - MD5 해시로 변환
        - 파일명으로 사용
    
    get(prompt, model):
      동작:
        1. 캐시 키 생성
        2. 캐시 파일 존재 확인
        3. 있으면:
           - 파일 읽기
           - response 반환
           - "캐시 히트" 메시지
        4. 없으면 None 반환
    
    set(prompt, model, response):
      동작:
        1. 캐시 키 생성
        2. 캐시 파일 경로 생성
        3. 데이터 저장:
           - prompt
           - model
           - response
           - timestamp

BaseAgent_통합:
  call_ai(prompt):
    동작_흐름:
      1. 캐시_확인 (enable_cache=True인 경우):
         - cache.get(prompt, model)
         - 있으면 즉시 반환 (API 호출 스킵)
      
      2. API_호출:
         - 캐시 미스 시에만 호출
         - 실제 API 요청
      
      3. 캐시_저장:
         - cache.set(prompt, model, response)
         - 다음 호출 시 재사용

효과:
  - 동일 프롬프트 재사용 시 API 호출 0
  - 비용 절감 (캐시 히트 시 무료)
  - 응답 속도 향상 (네트워크 지연 없음)
  - 디버깅 용이 (응답 재현 가능)

주의사항:
  - 캐시 만료 시간 설정 고려
  - 민감한 데이터는 캐싱 비활성화
  - 디스크 용량 관리
```

**2. 배치 처리**:
```yaml
배치_프로세서:
  BatchProcessor:
    목적: 여러 요청을 모아서 효율적으로 처리
    
    초기화:
      - batch_size: 배치 크기 (기본: 5)
      - queue: 대기 중인 요청 목록
    
    add(prompt):
      동작:
        1. queue에 prompt 추가
        2. queue 크기 확인
        3. batch_size 도달 시:
           - flush() 호출
           - 배치 처리 실행
    
    flush():
      동작:
        1. queue가 비어있으면 즉시 반환
        2. 모든 요청을 한꺼번에 처리
        3. 병렬 처리 (asyncio.gather)
        4. queue 초기화
        5. 결과 목록 반환

효과:
  - 네트워크 오버헤드 감소
  - 처리 속도 향상
  - 자원 활용 효율화

사용_시나리오:
  - 여러 아이디어 동시 평가
  - 대량 문서 분석
  - 일괄 번역 작업
```

### 비용 추적

```yaml
비용_추적기:
  CostTracker:
    목적: API 비용 실시간 추적
    
    비용_설정:
      COST_PER_1K_INPUT_TOKENS: 0.003  # $0.003 per 1K input tokens
      COST_PER_1K_OUTPUT_TOKENS: 0.015  # $0.015 per 1K output tokens
    
    초기화:
      - total_input_tokens: 0
      - total_output_tokens: 0
      - call_count: 0
    
    track(input_tokens, output_tokens):
      동작:
        - 입력 토큰 누적
        - 출력 토큰 누적
        - 호출 횟수 증가
    
    get_total_cost():
      계산:
        - input_cost = (total_input_tokens / 1000) × COST_PER_1K_INPUT
        - output_cost = (total_output_tokens / 1000) × COST_PER_1K_OUTPUT
        - total_cost = input_cost + output_cost
    
    get_summary():
      반환:
        - total_input_tokens: 총 입력 토큰
        - total_output_tokens: 총 출력 토큰
        - total_cost_usd: 총 비용 (USD)
        - average_cost_per_call: 호출당 평균 비용

BaseAgent_통합:
  call_ai(prompt):
    동작:
      1. API 호출
      2. 토큰_계산:
         - input_tokens = len(prompt) / 4 (대략)
         - output_tokens = len(response) / 4 (대략)
      3. 비용_추적:
         - cost_tracker.track(input_tokens, output_tokens)
      4. 응답 반환
  
  get_cost_summary():
    - 현재까지의 비용 요약 반환
    - 로그에 기록
    - 예산 초과 확인

활용_방안:
  실시간_모니터링:
    - 작업 진행 중 비용 확인
    - 예산 초과 전 경고
    - 비용 효율성 분석
  
  최적화_기준:
    - 어떤 Stage가 비용이 많이 드는가?
    - 프롬프트 최적화 필요성
    - 캐싱 효과 측정

예산_관리:
  설정:
    - budget: 1000.0  # $1000
    - alert_threshold: 0.8  # 80%
  
  확인:
    - 매 API 호출 후 비용 체크
    - current_cost > budget × 0.8 시 경고
    - current_cost > budget 시 작업 중단
```

---

## 16.3.5 정리

이 섹션에서 우리는 에이전트 구현을 위한 핵심 패턴들을 배웠어요:

**구현 옵션**:
- Option 1: API 직접 호출 (완전한 제어)
- Option 2: 프레임워크 사용 (빠른 개발)
- Option 3: 클라우드 서비스 (관리 불필요)

**핵심 패턴**:
- 상태 머신: Stage 진행 관리
- 파일 I/O 자동화: 반복 작업 제거
- 재시도 로직: 안정성 향상
- Human-in-the-Loop: 중요 결정 승인

**오류 처리**:
- 체크포인트: 실패 지점부터 재개
- 로깅: 디버깅 및 추적
- 알림: 실패/완료 통지

**성능 최적화**:
- 캐싱: API 호출 감소
- 배치 처리: 효율적 처리
- 비용 추적: 예산 관리

다음 섹션(16.4)에서는 이 모든 것을 통합하여 실전 에이전트를 만들어볼 거예요!
