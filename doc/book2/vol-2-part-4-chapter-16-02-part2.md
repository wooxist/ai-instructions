# 16.2.3 계층적 에이전트 시스템 (14.3 기반) - 계속

```python
    async def _integrate_all_results(self):
        """모든 에이전트 결과를 통합"""
        
        prompt = f"""
당신은 전략 통합 전문가입니다.

목표: {self.goal}

각 에이전트 결과:

1. 시장 조사 (MarketResearchAgent):
{json.dumps(self.agent_results['market_research'], indent=2, ensure_ascii=False)}

2. 제품 포지셔닝 (PositioningAgent):
{json.dumps(self.agent_results['positioning'], indent=2, ensure_ascii=False)}

3. 마케팅 전략 (MarketingStrategyAgent):
{json.dumps(self.agent_results['marketing_strategy'], indent=2, ensure_ascii=False)}

4. 런칭 실행 계획 (LaunchPlanAgent):
{json.dumps(self.agent_results['launch_plan'], indent=2, ensure_ascii=False)}

이 4가지 결과를 통합하여 완전한 신제품 런칭 계획을 작성하세요.

통합 계획 구조:
1. Executive Summary (전체 요약)
2. Market Insights (시장 조사 핵심)
3. Product Positioning (포지셔닝 전략)
4. Marketing Strategy (마케팅 전략)
5. Launch Plan (실행 계획)
6. Success Metrics (성공 지표)
7. Risk Management (리스크 관리)
8. Timeline (전체 타임라인)

각 섹션은 서로 일관되어야 하며, 전체 목표를 달성하는 데 기여해야 합니다.
"""
        
        response = await call_ai(prompt, max_tokens=4000, temperature=0.3)
        integrated_plan = json.loads(response)
        
        return integrated_plan
    
    async def _final_validation(self, integrated_plan):
        """최종 통합 계획 검증"""
        
        prompt = f"""
당신은 런칭 전략 최종 검증자입니다.

목표: {self.goal}
핵심 가치: {json.dumps(self.core_values, ensure_ascii=False)}
제약조건: {json.dumps(self.constraints, ensure_ascii=False)}

통합 런칭 계획:
{json.dumps(integrated_plan, indent=2, ensure_ascii=False)}

최종 검증:
1. 완전성: 모든 필수 요소가 포함되었는가?
2. 일관성: 각 섹션이 서로 모순되지 않는가?
3. 실행 가능성: 현실적으로 실행 가능한가?
4. 성공 가능성: 목표 달성 가능성이 높은가?
5. 리스크 대비: 주요 리스크에 대한 대응책이 있는가?

응답 형식:
{{
  "passed": true/false,
  "overall_score": 0-10,
  "completeness": 0-10,
  "consistency": 0-10,
  "feasibility": 0-10,
  "success_likelihood": 0-10,
  "risk_preparedness": 0-10,
  "critical_issues": ["치명적 문제 (있다면)"],
  "recommendations": ["개선 권장 사항"],
  "approval_status": "approved" | "needs_revision" | "needs_human_review"
}}
"""
        
        response = await call_ai(prompt, temperature=0.2)
        validation = json.loads(response)
        
        return validation
    
    def _save_final_plan(self, integrated_plan):
        """최종 계획 저장"""
        
        # JSON 형식
        file_manager = FileManager(self.base_dir)
        file_manager.save_json('outputs/launch_plan.json', integrated_plan)
        
        # Markdown 형식 (사람이 읽기 좋게)
        markdown = self._format_plan_as_markdown(integrated_plan)
        file_manager.save_markdown('outputs/launch_plan.md', markdown)
        
        # 메타 조율 로그
        file_manager.save_json('meta/coordination.json', {
            'coordination_log': self.coordination_log,
            'validation_history': self.validation_history,
            'agent_results': self.agent_results
        })
    
    def _log_coordination(self, message):
        """조율 로그 기록"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.coordination_log.append(entry)
        print(f"[Meta] {message}")
    
    async def _request_human_intervention(self, agent_id, validation):
        """인간 개입 요청"""
        
        notification = {
            'type': 'human_intervention_required',
            'task_id': self.task_id,
            'agent_id': agent_id,
            'validation': validation,
            'context': self.agent_results,
            'message': f"{agent_id} 검증 실패 - 인간 검토 필요"
        }
        
        await self.config['notifier'].send(notification)
```

### 실행 에이전트 구현

```python
# 1. MarketResearchAgent
class MarketResearchAgent(BaseAgent):
    """시장 조사 에이전트"""
    
    async def run(self, context):
        """시장 조사 실행"""
        
        # Stage 1: 시장 규모 분석
        market_size = await self._analyze_market_size(context)
        
        # Stage 2: 경쟁사 분석
        competitors = await self._analyze_competitors(context)
        
        # Stage 3: 고객 니즈 분석
        customer_needs = await self._analyze_customer_needs(context)
        
        # Stage 4: 트렌드 분석
        trends = await self._analyze_trends(context)
        
        # 결과 통합
        result = {
            'market_size': market_size,
            'competitors': competitors,
            'customer_needs': customer_needs,
            'trends': trends,
            'summary': await self._summarize_findings({
                'market_size': market_size,
                'competitors': competitors,
                'customer_needs': customer_needs,
                'trends': trends
            })
        }
        
        # 파일 저장
        self.file_manager.save_json('thinking/tc-m1/market_research.json', result)
        
        return result
    
    async def _analyze_market_size(self, context):
        """시장 규모 분석"""
        
        prompt = f"""
신제품 런칭을 위한 시장 규모 분석:

제품: {context['constraints'].get('product_type', 'SaaS 제품')}
타겟 시장: {context['constraints'].get('target_market', '북미')}

다음을 분석하세요:
1. TAM (Total Addressable Market)
2. SAM (Serviceable Available Market)
3. SOM (Serviceable Obtainable Market)
4. 시장 성장률 (연간)
5. 시장 성숙도

응답 형식: JSON
"""
        
        response = await self.call_ai(prompt)
        return json.loads(response)


# 2. PositioningAgent
class PositioningAgent(BaseAgent):
    """제품 포지셔닝 에이전트"""
    
    async def run(self, context):
        """포지셔닝 전략 수립"""
        
        # 시장 조사 결과 참조
        market_research = context['dependencies']['market_research']
        
        # Stage 1: 타겟 고객 정의
        target_customer = await self._define_target_customer(market_research)
        
        # Stage 2: 가치 제안 (Value Proposition)
        value_proposition = await self._create_value_proposition(
            target_customer, 
            market_research
        )
        
        # Stage 3: 차별화 전략
        differentiation = await self._define_differentiation(
            value_proposition,
            market_research['competitors']
        )
        
        # Stage 4: 포지셔닝 스테이트먼트
        positioning_statement = await self._create_positioning_statement(
            target_customer,
            value_proposition,
            differentiation
        )
        
        result = {
            'target_customer': target_customer,
            'value_proposition': value_proposition,
            'differentiation': differentiation,
            'positioning_statement': positioning_statement
        }
        
        self.file_manager.save_json('thinking/tc-m2/positioning.json', result)
        
        return result


# 3. MarketingStrategyAgent
class MarketingStrategyAgent(BaseAgent):
    """마케팅 전략 에이전트"""
    
    async def run(self, context):
        """마케팅 전략 수립"""
        
        # 의존성 참조
        market_research = context['dependencies']['market_research']
        positioning = context['dependencies']['positioning']
        
        # Stage 1: 마케팅 목표 설정
        marketing_goals = await self._set_marketing_goals(context['goal'])
        
        # Stage 2: 채널 전략
        channel_strategy = await self._define_channel_strategy(
            positioning['target_customer'],
            market_research['trends']
        )
        
        # Stage 3: 메시징 전략
        messaging = await self._create_messaging_strategy(
            positioning['value_proposition']
        )
        
        # Stage 4: 캠페인 계획
        campaigns = await self._plan_campaigns(
            channel_strategy,
            messaging,
            context['constraints']
        )
        
        result = {
            'marketing_goals': marketing_goals,
            'channel_strategy': channel_strategy,
            'messaging': messaging,
            'campaigns': campaigns,
            'budget_allocation': await self._allocate_budget(
                campaigns,
                context['constraints'].get('budget', 100000)
            )
        }
        
        self.file_manager.save_json('thinking/tc-m3/marketing_strategy.json', result)
        
        return result


# 4. LaunchPlanAgent
class LaunchPlanAgent(BaseAgent):
    """런칭 실행 계획 에이전트"""
    
    async def run(self, context):
        """런칭 실행 계획 수립"""
        
        # 의존성 참조
        positioning = context['dependencies']['positioning']
        marketing_strategy = context['dependencies']['marketing_strategy']
        
        # Stage 1: 런칭 단계 정의
        launch_phases = await self._define_launch_phases()
        
        # Stage 2: 타임라인 수립
        timeline = await self._create_timeline(
            launch_phases,
            context['constraints'].get('launch_date', 'Q4 2025')
        )
        
        # Stage 3: 책임 할당
        responsibilities = await self._assign_responsibilities(
            launch_phases,
            context['constraints'].get('team_structure', {})
        )
        
        # Stage 4: 성공 지표 정의
        success_metrics = await self._define_success_metrics(
            marketing_strategy['marketing_goals']
        )
        
        # Stage 5: 리스크 관리 계획
        risk_management = await self._create_risk_management_plan(
            launch_phases
        )
        
        result = {
            'launch_phases': launch_phases,
            'timeline': timeline,
            'responsibilities': responsibilities,
            'success_metrics': success_metrics,
            'risk_management': risk_management
        }
        
        self.file_manager.save_json('thinking/tc-m4/launch_plan.json', result)
        
        return result
```

### 사용 예시

```python
async def main():
    # 설정
    config = {
        'goal': 'Q4 신제품 런칭 성공 (목표 매출 $1M)',
        'core_values': [
            {'name': '고객 중심', 'description': '고객 가치를 최우선으로'},
            {'name': '혁신', 'description': '차별화된 솔루션 제공'},
            {'name': '품질', 'description': '높은 품질 기준 유지'}
        ],
        'constraints': {
            'budget': 500000,
            'launch_date': '2025-10-01',
            'team_size': 15,
            'product_type': 'AI 생산성 도구'
        },
        'dependencies': {
            'market_research': {
                'depends_on': [],
                'outputs': ['thinking/tc-m1/market_research.json']
            },
            'positioning': {
                'depends_on': ['market_research'],
                'requires': ['thinking/tc-m1/market_research.json'],
                'outputs': ['thinking/tc-m2/positioning.json']
            },
            'marketing_strategy': {
                'depends_on': ['market_research', 'positioning'],
                'requires': [
                    'thinking/tc-m1/market_research.json',
                    'thinking/tc-m2/positioning.json'
                ],
                'outputs': ['thinking/tc-m3/marketing_strategy.json']
            },
            'launch_plan': {
                'depends_on': ['positioning', 'marketing_strategy'],
                'requires': [
                    'thinking/tc-m2/positioning.json',
                    'thinking/tc-m3/marketing_strategy.json'
                ],
                'outputs': ['thinking/tc-m4/launch_plan.json']
            }
        },
        'market_config': {...},
        'positioning_config': {...},
        'marketing_config': {...},
        'launch_config': {...},
        'notifier': SlackNotifier(channel='#launch-review')
    }
    
    # 시스템 생성 및 실행
    system = LaunchAgentSystem(task_id='launch-q4-2025', config=config)
    
    try:
        result = await system.run()
        
        print("\n✅ 런칭 계획 완료!")
        print(f"상태: {result['status']}")
        print(f"검증 점수: {result['validation']['overall_score']}/10")
        print(f"결과 파일: {result['output_files']}")
        
    except ValidationFailure as e:
        print(f"\n❌ 검증 실패: {e}")
    except DependencyError as e:
        print(f"\n❌ 의존성 오류: {e}")


# 실행
asyncio.run(main())
```

### 계층적 에이전트 패턴 요약

**핵심 특징**:
1. **메타 조율자**: 전체 일관성 유지, 각 에이전트 결과 검증
2. **실행 에이전트**: 독립적 실행, 자신의 영역만 책임
3. **컨텍스트 전달**: 의존하는 에이전트의 결과를 컨텍스트로 전달
4. **검증 루프**: 각 에이전트 완료 후 메타 조율자가 검증
5. **재작업 메커니즘**: 검증 실패 시 피드백과 함께 재실행
6. **최종 통합**: 모든 결과를 하나의 완전한 계획으로 통합

**적용 시나리오**:
- 복잡한 전략 수립 (신제품 런칭, 조직 재편)
- 여러 팀/부서 협력 필요한 프로젝트
- 전체 일관성이 중요한 경우
- 중간 검증이 필수인 경우

**메타 조율자의 역할**:
```yaml
조율 역할:
  - 실행 순서 결정
  - 컨텍스트 준비 (의존성 데이터)
  - 에이전트 실행 트리거

검증 역할:
  - 목표 부합성 확인
  - 핵심 가치 정렬 확인
  - 이전 결과와의 일관성 확인
  - 필요 시 재작업 지시

통합 역할:
  - 모든 결과 통합
  - 최종 검증
  - 완전한 계획 산출
```

**vs 병렬 에이전트 (16.2.2)**:
| 특성 | 병렬 에이전트 | 계층적 에이전트 |
|------|--------------|----------------|
| **조율자** | 단순 의존성 관리 | 메타 조율자 (검증 + 통합) |
| **검증** | 없음 (자동 진행) | 각 단계마다 검증 |
| **일관성** | 개별 에이전트 책임 | 메타 조율자 책임 |
| **재작업** | 없음 | 피드백 기반 재작업 |
| **통합** | 최종 에이전트가 통합 | 메타 조율자가 통합 |
| **복잡도** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 16.2.4 에이전트 간 통신 패턴

여러 에이전트가 협업할 때 필요한 통신 패턴들을 정리합니다.

### 패턴 1: 파일 기반 통신 (File-Based)

**개념**: 에이전트가 파일 시스템을 통해 데이터를 주고받습니다.

**장점**:
- 간단하고 직관적
- 디버깅 용이 (파일 내용 직접 확인)
- 재현성 높음 (파일로 모든 것이 기록됨)

**단점**:
- 실시간 통신 어려움
- 파일 I/O 오버헤드

**구현**:
```python
# Agent A: 데이터 생성
class AgentA:
    async def run(self):
        result = await self.process()
        
        # 파일로 저장
        self.file_manager.save_json('outputs/data.json', result)
        
        return result

# Agent B: 데이터 읽기
class AgentB:
    async def run(self):
        # Agent A의 출력 파일 읽기
        data = self.file_manager.load_json('outputs/data.json')
        
        # 처리
        result = await self.process(data)
        
        return result
```

**적용**: 16.2.2 병렬 에이전트, 16.2.3 계층적 에이전트

### 패턴 2: 메시지 큐 (Message Queue)

**개념**: 에이전트가 메시지 큐를 통해 비동기 통신합니다.

**장점**:
- 비동기 처리
- 확장성 높음
- 장애 복구 용이

**단점**:
- 인프라 필요 (Redis, RabbitMQ 등)
- 복잡도 증가

**구현**:
```python
import asyncio
from aioredis import Redis

class MessageQueue:
    def __init__(self, redis_url):
        self.redis = Redis.from_url(redis_url)
    
    async def publish(self, channel, message):
        """메시지 발행"""
        await self.redis.publish(channel, json.dumps(message))
    
    async def subscribe(self, channel, handler):
        """메시지 구독"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                await handler(data)

# Agent A: 메시지 발행
class AgentA:
    def __init__(self, message_queue):
        self.mq = message_queue
    
    async def run(self):
        result = await self.process()
        
        # 메시지 발행
        await self.mq.publish('agent_a_completed', {
            'agent': 'agent_a',
            'status': 'completed',
            'result': result
        })
        
        return result

# Agent B: 메시지 구독
class AgentB:
    def __init__(self, message_queue):
        self.mq = message_queue
        self.agent_a_result = None
    
    async def run(self):
        # Agent A 완료 대기
        await self.mq.subscribe('agent_a_completed', self._handle_agent_a)
        
        # Agent A 결과가 올 때까지 대기
        while self.agent_a_result is None:
            await asyncio.sleep(0.1)
        
        # 처리
        result = await self.process(self.agent_a_result)
        
        return result
    
    async def _handle_agent_a(self, message):
        """Agent A 완료 처리"""
        self.agent_a_result = message['result']
```

### 패턴 3: 공유 상태 (Shared State)

**개념**: 에이전트가 공유 상태 객체를 통해 데이터를 주고받습니다.

**장점**:
- 빠른 접근
- 실시간 동기화

**단점**:
- 동시성 문제 (락 필요)
- 재현성 낮음

**구현**:
```python
import asyncio
from typing import Dict, Any

class SharedState:
    """에이전트 간 공유 상태"""
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
    
    async def set(self, key: str, value: Any):
        """값 설정 (락 사용)"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        
        async with self._locks[key]:
            self._state[key] = value
    
    async def get(self, key: str, wait=True, timeout=60):
        """값 가져오기 (대기 가능)"""
        if key in self._state:
            return self._state[key]
        
        if not wait:
            return None
        
        # 값이 설정될 때까지 대기
        start_time = asyncio.get_event_loop().time()
        while key not in self._state:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for {key}")
            
            await asyncio.sleep(0.1)
        
        return self._state[key]

# 사용 예시
shared_state = SharedState()

class AgentA:
    async def run(self):
        result = await self.process()
        
        # 공유 상태에 저장
        await shared_state.set('agent_a_result', result)
        
        return result

class AgentB:
    async def run(self):
        # Agent A 결과 대기
        agent_a_result = await shared_state.get('agent_a_result', wait=True)
        
        # 처리
        result = await self.process(agent_a_result)
        
        return result
```

### 패턴 4: 이벤트 기반 (Event-Driven)

**개념**: 에이전트가 이벤트를 발행하고 구독합니다.

**장점**:
- 느슨한 결합
- 확장 용이

**단점**:
- 디버깅 어려움
- 순서 보장 필요 시 복잡

**구현**:
```python
from typing import Callable, List
import asyncio

class EventBus:
    """이벤트 버스"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        """이벤트 구독"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: Any):
        """이벤트 발행"""
        if event_type in self._handlers:
            # 모든 핸들러 호출
            await asyncio.gather(*[
                handler(data)
                for handler in self._handlers[event_type]
            ])

# 사용 예시
event_bus = EventBus()

class AgentA:
    def __init__(self, event_bus):
        self.event_bus = event_bus
    
    async def run(self):
        result = await self.process()
        
        # 이벤트 발행
        await self.event_bus.publish('agent_a_completed', {
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result

class AgentB:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.agent_a_result = None
        
        # 이벤트 구독
        self.event_bus.subscribe('agent_a_completed', self._on_agent_a_completed)
    
    async def _on_agent_a_completed(self, data):
        """Agent A 완료 이벤트 핸들러"""
        self.agent_a_result = data['result']
        print("Agent A 완료!")
    
    async def run(self):
        # Agent A 결과 대기
        while self.agent_a_result is None:
            await asyncio.sleep(0.1)
        
        # 처리
        result = await self.process(self.agent_a_result)
        
        return result
```

### 통신 패턴 선택 가이드

| 상황 | 추천 패턴 |
|------|----------|
| 간단한 순차 실행 | 파일 기반 |
| 복잡한 워크플로우, 높은 재현성 필요 | 파일 기반 |
| 대규모 분산 시스템 | 메시지 큐 |
| 빠른 데이터 공유 필요 | 공유 상태 |
| 느슨한 결합, 확장성 중요 | 이벤트 기반 |

**실전 권장**: 
- 16.2.1 (단일): 파일 기반
- 16.2.2 (병렬): 파일 기반 + 의존성 관리자
- 16.2.3 (계층적): 파일 기반 + 공유 상태 (메타 조율자와 실행 에이전트 간)

---

## 16.2.5 정리

16.2에서 우리는 3가지 에이전트 팀 패턴을 배웠습니다:

**16.2.1 단일 에이전트** (ContentAgent):
- 4 Stage를 순차 실행
- 상태 머신, 메모리, 파일 관리 통합
- Human-in-the-Loop 선택적 적용
- 품질 재시도 메커니즘

**16.2.2 병렬 에이전트 팀** (AnalysisAgentTeam):
- 3개 에이전트 순차 실행
- 의존성 자동 관리
- 파일 기반 통신
- 개별 에이전트 독립성

**16.2.3 계층적 에이전트 시스템** (LaunchAgentSystem):
- 메타 조율자 + 4개 실행 에이전트
- 각 단계 검증 및 재작업
- 최종 통합 및 검증
- 높은 일관성 유지

**다음 섹션 (16.3)**에서는 이러한 에이전트를 실제로 구현하는 방법을 다룹니다.
