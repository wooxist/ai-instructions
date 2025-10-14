# 16.4 에이전트 설계 체크리스트 및 요약

이제 지금까지 배운 모든 것을 정리하고, 실전에서 에이전트를 설계할 때 사용할 수 있는 체크리스트를 만들어볼게요.

---

## 16.4.1 설계 체크리스트

에이전트를 만들기 전에 다음 체크리스트를 따라가 보세요. 각 단계를 차근차근 확인하면 실패 확률을 크게 줄일 수 있어요.

### Phase 1: 필요성 평가

먼저 정말로 에이전트가 필요한지부터 확인해야 해요.

**질문들**:

**Q1. 이 작업은 충분히 반복되나요?**
- [ ] 월 10회 이상 반복되는 작업인가?
- [ ] 앞으로도 계속 필요한 작업인가?
- [ ] 일회성 작업이 아닌가?

**판단 기준**: 
- 월 10회 이상 → 에이전트 고려 ✅
- 월 5-9회 → 반자동화 고려 (일부만 에이전트)
- 월 5회 미만 → 수동 유지 (에이전트 불필요)

**예시**:
```yaml
Good 사례:
  - 매주 블로그 포스트 작성 (월 4-5회)
  - 매일 데이터 리포트 생성 (월 20-25회)
  - 분기별 전략 기획 (분기 1회 = 월 0.3회) → 수동 유지

판단:
  - 블로그 포스트: 에이전트 구현 가치 있음
  - 데이터 리포트: 에이전트 필수
  - 전략 기획: 수동 유지 (반복 빈도 낮음)
```

**Q2. 프로세스가 명확히 정의되어 있나요?**
- [ ] 각 단계가 명확한가?
- [ ] 입력과 출력이 정의되어 있는가?
- [ ] 성공 기준이 명확한가?

**판단 기준**: 
- 사고 클러스터로 이미 정의했다면 ✅
- 프로세스가 모호하면 먼저 수동으로 여러 번 해보기

**Q3. 핵심 가치와 제약조건이 명확한가?**
- [ ] 핵심 가치를 3-5개로 정의했는가?
- [ ] 예산, 일정 등 제약조건이 명확한가?
- [ ] 품질 기준이 정의되어 있는가?

**Q4. Human-in-the-Loop 지점을 정의할 수 있나요?**
- [ ] 어디서 인간의 판단이 필요한가?
- [ ] 어떤 결과는 반드시 검토가 필요한가?
- [ ] 예산/리스크 임계값이 있는가?

**판단**: 모든 질문에 ✅ 표시가 되었다면 Phase 2로 진행하세요.

### Phase 2: 범위 결정

이제 에이전트가 무엇을 할지 정확히 정의해야 해요.

**Q5. 어느 Stage를 자동화할 것인가?**

사고 클러스터의 4 Stage 중에서 선택하세요:

| Stage | 자동화 난이도 | 자동화 추천 |
|-------|-------------|-----------|
| **Planning** | ⭐⭐ 쉬움 | ✅ 추천 (구조화된 작업) |
| **Reasoning** | ⭐⭐⭐ 보통 | ✅ 추천 (논리적 분석) |
| **Experimenting** | ⭐⭐⭐⭐ 어려움 | ⚠️ 주의 (창의성 필요) |
| **Reflecting** | ⭐⭐⭐ 보통 | ✅ 추천 (평가 기준 명확) |

**선택 가이드**:
```yaml
초기 단계:
  - Planning + Reasoning만 자동화
  - Experimenting은 수동 (인간의 창의성)
  - Reflecting은 반자동 (AI 초안 + 인간 검토)

성숙 단계:
  - Planning + Reasoning + Reflecting 자동화
  - Experimenting도 자동화 시도
  - Human-in-the-Loop로 품질 보장

완전 자동화:
  - 모든 Stage 자동화
  - 최종 결과만 Human-in-the-Loop
  - 높은 반복성과 명확한 기준 필요
```

**Q6. 인간 개입이 필요한 지점은 어디인가?**

다음 시나리오에서 인간 개입을 고려하세요:

**시나리오 1: 높은 비용**
```python
# 예시: 마케팅 캠페인 실행
if estimated_cost > 10000:  # $10k 초과
    approval_required = True
```

**시나리오 2: 되돌리기 어려움**
```python
# 예시: 대외 발표 자료
if audience == "external" and impact == "high":
    approval_required = True
```

**시나리오 3: 불확실성 높음**
```python
# 예시: AI 품질 점수
if quality_score < 0.8:  # 80점 미만
    human_review_required = True
```

**체크리스트**:
- [ ] 비용 임계값 정의 (예: $1,000 초과 시 승인)
- [ ] 리스크 임계값 정의 (예: 외부 공개 시 승인)
- [ ] 품질 임계값 정의 (예: 80점 미만 시 검토)

**Q7. 실패 시나리오를 정의했나요?**

에이전트가 실패할 수 있는 상황을 미리 생각해보세요:

**실패 시나리오 예시**:
```yaml
시나리오 1: API 호출 실패
  - 원인: 네트워크 오류, 레이트 리밋
  - 대응: 3회 재시도, 실패 시 알림

시나리오 2: 품질 기준 미달
  - 원인: AI 출력이 기준 미달
  - 대응: 다른 프롬프트로 재시도, 인간 검토

시나리오 3: 의존성 데이터 없음
  - 원인: 이전 에이전트 실패
  - 대응: 작업 중단, 의존성 확인 알림

시나리오 4: 예산 초과
  - 원인: API 호출 과다
  - 대응: 작업 일시 중단, 예산 승인 요청
```

**판단**: 모든 질문에 답했다면 Phase 3으로 진행하세요.

### Phase 3: 아키텍처 선택

이제 에이전트의 구조를 결정해야 해요.

**Q8. 어떤 패턴이 적합한가?**

| 패턴 | 특징 | 적합한 경우 |
|------|------|-----------|
| **단일 에이전트** | - 1개 에이전트<br>- 순차 실행<br>- 간단한 구조 | - Stage가 5개 이하<br>- 의존성 없음<br>- 한 명이 할 수 있는 작업 |
| **병렬 에이전트** | - 여러 에이전트<br>- 순차/병렬 혼합<br>- 의존성 관리 | - Stage가 6-10개<br>- 일부 병렬 가능<br>- 여러 역할 필요 |
| **계층적 에이전트** | - 메타 조율자<br>- 검증 루프<br>- 복잡한 조율 | - Stage가 10개 이상<br>- 일관성 중요<br>- 전략적 작업 |

**선택 가이드**:
```
작업 복잡도 평가:
  ├─ 간단 (1-5 Stage) → 단일 에이전트
  ├─ 중간 (6-10 Stage) → 병렬 에이전트
  └─ 복잡 (10+ Stage) → 계층적 에이전트

의존성 평가:
  ├─ 의존성 없음 → 단일 에이전트
  ├─ 순차 의존성 → 병렬 에이전트
  └─ 복잡한 의존성 + 일관성 중요 → 계층적 에이전트
```

**Q9. 몇 개의 에이전트가 필요한가?**

**판단 기준**:
```python
# 간단한 공식
num_agents = len(distinct_roles)

# 예시
콘텐츠 생성:
  - 역할: 작가 1명
  - 에이전트: 1개 (ContentAgent)

데이터 분석:
  - 역할: 수집가, 분석가, 통찰가
  - 에이전트: 3개 (각 역할당 1개)

신제품 런칭:
  - 역할: 조사원, 전략가, 마케터, 기획자
  - 에이전트: 4개 + 1개 조율자
```

**Q10. 에이전트 간 통신 방법은?**

| 통신 방법 | 장점 | 단점 | 추천 |
|----------|------|------|------|
| **파일 기반** | 간단, 디버깅 쉬움 | 실시간 어려움 | ✅ 대부분 |
| **공유 상태** | 빠름 | 동시성 문제 | 특수 경우만 |
| **메시지 큐** | 확장성 | 인프라 필요 | 대규모만 |
| **이벤트 기반** | 느슨한 결합 | 디버깅 어려움 | 특수 경우만 |

**추천**: 대부분의 경우 **파일 기반**을 선택하세요. 간단하고 안정적이며 디버깅이 쉬워요.

### Phase 4: 구현 방법

마지막으로 구현 방식을 결정해야 해요.

**Q11. 어떤 구현 옵션을 선택할 것인가?**

16.3.1에서 본 3가지 옵션을 다시 떠올려보세요:

```
결정 트리:
  
  "빠른 프로토타입 필요?"
    ├─ Yes → Option 3 (클라우드) 또는 Option 2 (프레임워크)
    └─ No → 다음 질문
  
  "최적화와 제어가 중요?"
    ├─ Yes → Option 1 (API 직접)
    └─ No → Option 2 (프레임워크)
  
  "팀 규모는?"
    ├─ 1-2명 → Option 1 (API 직접)
    └─ 3명+ → Option 2 (프레임워크)
```

**Q12. 상태 추적을 어떻게 구현할 것인가?**

**필수 파일**:
```yaml
파일 구조:
  thinking/
    tc-{cluster_id}/
      thinking_state.json  # 필수: 전체 진행 상태
      planning/
        thinking_record.json  # 필수: Stage별 기록
      reasoning/
        thinking_record.json
      # ... 기타 Stage들

구현 방법:
  - FileManager 사용 (16.3.2 참조)
  - 각 Stage 완료 시 자동 저장
  - 실패 시 마지막 체크포인트부터 재개
```

**Q13. 파일 시스템과 어떻게 통합할 것인가?**

**통합 체크리스트**:
- [ ] FileManager 클래스 구현 (16.3.2 참조)
- [ ] thinking_record 자동 저장
- [ ] thinking_state 자동 업데이트
- [ ] 출력 파일 정리 (outputs/ 디렉토리)

---

## 16.4.2 자주 하는 실수

실전에서 자주 발생하는 실수들과 해결 방법을 정리했어요.

### 실수 1: 과도한 자동화

**증상**:
- 인간 개입 없이 모든 것을 자동화
- "한 번 시작하면 끝까지 자동으로!"

**문제**:
- 품질 저하: AI가 잘못된 방향으로 가도 모름
- 예상치 못한 결과: 검토 없이 최종 결과 생성
- 비용 폭탄: 무한 루프나 과다 API 호출

**실제 사례**:
```yaml
잘못된 예:
  - 마케팅 이메일을 자동 생성하고 즉시 발송
  - 결과: 부적절한 내용으로 고객 불만 발생

올바른 예:
  - 이메일 초안 자동 생성
  - 마케터가 검토 및 승인
  - 승인 후 발송
```

**해결책**:
```python
# Human-in-the-Loop 추가
class EmailAgent:
    async def run(self):
        # 초안 생성
        draft = await self.generate_draft()
        
        # 승인 요청
        approval = await self.approval_gate.require_approval(
            approval_id=f"email-{self.task_id}",
            context={'draft': draft},
            explanation="이메일 초안을 검토해주세요."
        )
        
        if not approval.is_approved:
            raise ApprovalDenied("이메일 발송 거부됨")
        
        # 발송
        await self.send_email(draft)
```

**원칙**:
> **"되돌리기 어려운 작업은 반드시 Human-in-the-Loop"**

### 실수 2: 오류 처리 부족

**증상**:
- API 실패 시 에이전트가 그냥 중단
- 재시도 없음
- 에러 메시지만 출력

**문제**:
- 재개 불가능: 처음부터 다시 시작해야 함
- 작업 손실: 이미 완료한 Stage도 다시 실행
- 비용 낭비: 같은 작업 반복

**실제 사례**:
```yaml
잘못된 예:
  - 4시간 걸린 데이터 분석 작업
  - 마지막 Stage에서 API 타임아웃
  - 모든 것을 처음부터 다시 시작

올바른 예:
  - 각 Stage마다 체크포인트 저장
  - API 실패 시 자동 재시도 (3회)
  - 재시작 시 마지막 체크포인트부터 재개
```

**해결책**:
```python
# 1. 재시도 로직
@retry(RetryConfig(max_retries=3))
async def call_api(self, prompt: str) -> str:
    return await self._raw_api_call(prompt)

# 2. 체크포인트
async def run_stage(self, stage: Stage):
    result = await stage.handler()
    
    # 체크포인트 저장
    self.checkpoint_manager.save_checkpoint(
        stage_name=stage.name,
        stage_index=self.current_index,
        result=result
    )
    
    return result

# 3. 재개 로직
async def run(self, resume=True):
    if resume:
        checkpoint = self.checkpoint_manager.load_checkpoint()
        if checkpoint:
            # 체크포인트부터 시작
            self.current_index = checkpoint.stage_index + 1
```

**원칙**:
> **"모든 에이전트에 재시도 + 체크포인트 필수"**

### 실수 3: 상태 추적 미흡

**증상**:
- 에이전트가 지금 뭐 하는지 모름
- 진행률을 알 수 없음
- 디버깅이 매우 어려움

**문제**:
- 모니터링 불가: "이 에이전트 살아있나?"
- 디버깅 어려움: 어디서 문제가 생겼는지 모름
- 재개 불가: 어디까지 했는지 모름

**해결책**:
```python
# 1. 상세한 로깅
logger = AgentLogger(task_id='task-123')

logger.stage_start('planning')
# ... 작업
logger.stage_complete('planning', duration_seconds=15.3)

# 2. thinking_state.json 자동 업데이트
def update_state(self, stage: str, status: str):
    state = {
        'current_stage': stage,
        'status': status,
        'progress': f"{self.current_index + 1}/{len(self.stages)}",
        'updated_at': datetime.now().isoformat()
    }
    self.file_manager.save_json('thinking_state.json', state)

# 3. 진행 상황 API
def get_progress(self) -> dict:
    return {
        'current_stage': self.get_current_stage().name,
        'completed_stages': self.completed_count,
        'total_stages': len(self.stages),
        'progress_percent': (self.completed_count / len(self.stages)) * 100,
        'estimated_time_remaining': self.estimate_time_remaining()
    }
```

**원칙**:
> **"항상 thinking_state.json을 최신으로 유지"**

### 실수 4: 비용 무시

**증상**:
- API 호출 최적화 없이 구현
- 같은 프롬프트를 여러 번 호출
- 비용 추적 안 함

**문제**:
- 비용 급증: 예상보다 10배 비용
- 예산 초과: 월말에 청구서 보고 놀람
- 최적화 불가: 어디서 비용이 나가는지 모름

**실제 사례**:
```yaml
잘못된 예:
  - 매번 같은 프롬프트로 API 호출
  - 한 달 후: $5,000 청구서
  - 예상 비용: $500

올바른 예:
  - 응답 캐싱 구현
  - 한 달 비용: $800 (84% 절감)
```

**해결책**:
```python
# 1. 캐싱
cache = ResponseCache('./cache')

async def call_api(self, prompt: str) -> str:
    # 캐시 확인
    cached = cache.get(prompt, self.model)
    if cached:
        return cached
    
    # API 호출
    response = await self._raw_api_call(prompt)
    
    # 캐시 저장
    cache.set(prompt, self.model, response)
    
    return response

# 2. 비용 추적
cost_tracker = CostTracker()

async def call_api(self, prompt: str) -> str:
    response = await self._raw_api_call(prompt)
    
    # 비용 기록
    cost_tracker.track(
        input_tokens=len(prompt) // 4,
        output_tokens=len(response) // 4
    )
    
    # 예산 초과 경고
    if cost_tracker.get_total_cost() > self.budget * 0.8:
        await self.alert_manager.alert_cost_warning(
            task_id=self.task_id,
            current_cost=cost_tracker.get_total_cost(),
            budget=self.budget
        )
    
    return response

# 3. 비용 리포트
def get_cost_summary(self):
    return {
        'total_cost': cost_tracker.get_total_cost(),
        'budget': self.budget,
        'remaining': self.budget - cost_tracker.get_total_cost(),
        'utilization': (cost_tracker.get_total_cost() / self.budget) * 100
    }
```

**원칙**:
> **"캐싱 + 비용 추적은 필수, 예산의 80% 도달 시 알림"**

---

## 16.4.3 Part 4 통합 요약

Part 4를 통해 우리는 AI 사고 생태계의 완성 단계를 배웠어요. 이제 전체를 정리해볼까요?

### Part 4에서 배운 내용

| 장 | 주제 | 핵심 개념 | 산출물 |
|----|------|----------|--------|
| **Ch 11** | 사고 클러스터 기본 | - 4 Stage<br>- 사고 조율자<br>- thinking_record | 단일 사고 클러스터 설계 |
| **Ch 12** | 계층적 사고 | - 메타 조율자<br>- 의존성 관리<br>- 사고 워커 | 복잡한 사고 체계 |
| **Ch 13** | 파일 시스템 | - 디렉토리 구조<br>- 상태 추적<br>- 파일 조직 | 실행 가능한 워크스페이스 |
| **Ch 14** | 실전 사례 | - 콘텐츠 생성<br>- 데이터 분석<br>- 신제품 런칭 | 3가지 완전한 사례 |
| **Ch 15** | 프롬프트 엔지니어링 | - Stage별 프롬프트<br>- 품질 향상<br>- 일관성 유지 | 효과적인 프롬프트 |
| **Ch 16** | 에이전트 설계 | - 자율 실행<br>- 에이전트 팀<br>- 자동화 | 실행 가능한 에이전트 |

### 사고 중심 조직의 여정

```
[설계 단계: Ch 11-12]
   목표: 사고 체계 설계
   산출: 사고 클러스터 구조
   
   ↓
   
[구현 단계: Ch 13]
   목표: 파일 시스템 구축
   산출: 워크스페이스
   
   ↓
   
[실전 단계: Ch 14]
   목표: 수동 실행 검증
   산출: 완성된 결과물
   
   ↓
   
[최적화 단계: Ch 15]
   목표: 프롬프트 개선
   산출: 고품질 출력
   
   ↓
   
[자동화 단계: Ch 16]
   목표: 에이전트 구현
   산출: 자율 실행 시스템
```

### 핵심 원칙 정리

**1. 사고가 먼저, 자동화는 나중에**
```
❌ 잘못된 순서:
   에이전트 만들기 → 무엇을 자동화할지 고민

✅ 올바른 순서:
   사고 클러스터 설계 → 수동 실행 → 검증 → 에이전트 구현
```

**2. 명확성이 품질을 결정**
```
명확한 것들:
  ✓ 목표 (Goal)
  ✓ 핵심 가치 (Core Values)
  ✓ 제약조건 (Constraints)
  ✓ 프로세스 (4 Stage)
  ✓ 성공 기준 (Success Criteria)

→ 높은 품질의 결과
```

**3. 파일 시스템이 기초**
```
모든 것은 파일로:
  - 사고 과정 (thinking_record.json)
  - 진행 상태 (thinking_state.json)
  - 최종 결과 (outputs/)
  - 메타데이터 (meta/)

→ 재현 가능, 디버깅 가능, 협업 가능
```

**4. Human-in-the-Loop는 선택이 아닌 필수**
```
자동화 수준:
  Level 1: 모든 Stage 수동
  Level 2: 일부 Stage 자동 + 검토
  Level 3: 대부분 자동 + 최종 승인
  Level 4: 완전 자동 + 예외만 알림

→ 대부분의 경우 Level 2-3이 최적
```

---

**(다음 페이지에 계속)**
