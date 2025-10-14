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
```python
# 간단한 단일 에이전트
# 특수한 요구사항 (예: 극도로 최적화된 성능 필요)
# 기존 시스템과의 긴밀한 통합 필요

# 예시: ContentAgent를 API 직접 호출로 구현
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

class SimpleContentAgent:
    def __init__(self, task_id, goal, core_values):
        self.task_id = task_id
        self.goal = goal
        self.core_values = core_values
        self.memory = {}
    
    async def run(self):
        # Planning
        planning_result = await self._call_api(
            self._create_planning_prompt()
        )
        self.memory['planning'] = planning_result
        
        # Reasoning
        reasoning_result = await self._call_api(
            self._create_reasoning_prompt(planning_result)
        )
        self.memory['reasoning'] = reasoning_result
        
        # Experimenting
        experimenting_result = await self._call_api(
            self._create_experimenting_prompt(reasoning_result)
        )
        self.memory['experimenting'] = experimenting_result
        
        # Reflecting
        final_result = await self._call_api(
            self._create_reflecting_prompt(experimenting_result)
        )
        
        return final_result
    
    async def _call_api(self, prompt, max_retries=3):
        """API 호출 with 재시도"""
        for attempt in range(max_retries):
            try:
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
    
    def _create_planning_prompt(self):
        return f"""
당신은 콘텐츠 기획 전문가입니다.

목표: {self.goal}
핵심 가치: {self.core_values}

1단계: 콘텐츠 구조 기획
이 목표를 달성하기 위한 콘텐츠 구조를 설계하세요.
"""
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

#### LangChain Agents 예시

```python
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_anthropic import ChatAnthropic
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate

# LLM 설정
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.3
)

# Tool 정의
def analyze_market(query: str) -> str:
    """시장 분석 tool"""
    # 실제 분석 로직
    return "시장 분석 결과..."

def create_strategy(query: str) -> str:
    """전략 수립 tool"""
    # 실제 전략 수립 로직
    return "전략 수립 결과..."

tools = [
    Tool(
        name="MarketAnalysis",
        func=analyze_market,
        description="시장을 분석합니다"
    ),
    Tool(
        name="StrategyCreation",
        func=create_strategy,
        description="전략을 수립합니다"
    )
]

# Agent 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 마케팅 전략 에이전트입니다."),
    ("human", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 실행
result = agent_executor.invoke({
    "input": "신제품 런칭 전략을 수립해주세요"
})
```

#### AutoGen 예시

```python
import autogen

config_list = [
    {
        "model": "claude-sonnet-4-20250514",
        "api_key": "your-api-key",
        "api_type": "anthropic"
    }
]

# Assistant Agent
assistant = autogen.AssistantAgent(
    name="MarketingAssistant",
    llm_config={"config_list": config_list},
    system_message="""당신은 마케팅 전문가입니다.
    시장 분석과 전략 수립을 도와주세요."""
)

# User Proxy Agent (사용자 대리)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "workspace"}
)

# 대화 시작
user_proxy.initiate_chat(
    assistant,
    message="신제품 런칭 전략을 수립해주세요"
)
```

#### CrewAI 예시

```python
from crewai import Agent, Task, Crew, Process

# Agent 정의
researcher = Agent(
    role='시장 조사원',
    goal='시장 트렌드와 경쟁사를 분석합니다',
    backstory='10년 경력의 시장 분석 전문가',
    verbose=True
)

strategist = Agent(
    role='전략 기획자',
    goal='시장 조사 결과를 바탕으로 전략을 수립합니다',
    backstory='마케팅 전략 전문가',
    verbose=True
)

# Task 정의
research_task = Task(
    description='신제품 시장을 조사하세요',
    agent=researcher
)

strategy_task = Task(
    description='시장 조사 결과를 바탕으로 런칭 전략을 수립하세요',
    agent=strategist
)

# Crew 구성
crew = Crew(
    agents=[researcher, strategist],
    tasks=[research_task, strategy_task],
    process=Process.sequential
)

# 실행
result = crew.kickoff()
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

#### OpenAI Assistants API 예시

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Assistant 생성
assistant = client.beta.assistants.create(
    name="Marketing Strategist",
    instructions="""당신은 마케팅 전략 전문가입니다.
    시장 분석을 바탕으로 실행 가능한 전략을 수립하세요.""",
    model="gpt-4-turbo",
    tools=[{"type": "code_interpreter"}]
)

# Thread 생성
thread = client.beta.threads.create()

# Message 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="신제품 런칭 전략을 수립해주세요"
)

# Run 실행
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# 완료 대기
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    time.sleep(1)

# 결과 가져오기
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

for message in messages.data:
    print(f"{message.role}: {message.content[0].text.value}")
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

**구현**:
```python
from enum import Enum
from typing import Optional, List, Callable
from datetime import datetime

class StageStatus(Enum):
    """Stage 상태"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Stage:
    """개별 Stage"""
    
    def __init__(
        self,
        name: str,
        handler: Callable,
        description: str = ""
    ):
        self.name = name
        self.handler = handler
        self.description = description
        self.status = StageStatus.PENDING
        self.result = None
        self.error = None

class AgentStateMachine:
    """에이전트 상태 머신"""
    
    def __init__(self, stages: List[Stage]):
        self.stages = stages
        self.current_index = 0
        self.history = []
    
    def get_current_stage(self) -> Optional[Stage]:
        """현재 Stage 가져오기"""
        if self.current_index < len(self.stages):
            return self.stages[self.current_index]
        return None
    
    async def execute_current_stage(self, context: dict):
        """현재 Stage 실행"""
        stage = self.get_current_stage()
        if not stage:
            raise RuntimeError("No more stages")
        
        stage.status = StageStatus.IN_PROGRESS
        
        try:
            result = await stage.handler(context)
            stage.status = StageStatus.COMPLETED
            stage.result = result
            
            self.history.append({
                'stage': stage.name,
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            stage.status = StageStatus.FAILED
            stage.error = str(e)
            
            self.history.append({
                'stage': stage.name,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            
            raise
    
    def move_next(self) -> bool:
        """다음 Stage로 이동"""
        if self.current_index < len(self.stages) - 1:
            self.current_index += 1
            return True
        return False
    
    def get_progress(self) -> dict:
        """진행 상황"""
        completed = sum(
            1 for s in self.stages
            if s.status == StageStatus.COMPLETED
        )
        
        return {
            'total_stages': len(self.stages),
            'completed_stages': completed,
            'current_stage': self.get_current_stage().name if self.get_current_stage() else None,
            'progress_percent': (completed / len(self.stages)) * 100
        }


# 사용 예시
async def planning_handler(context):
    print("Planning...")
    return {"structure": "..."}

stages = [
    Stage("planning", planning_handler, "콘텐츠 구조 기획"),
    Stage("reasoning", reasoning_handler, "논리 전개 분석"),
    Stage("experimenting", experimenting_handler, "실험적 작성"),
    Stage("reflecting", reflecting_handler, "반성 및 개선")
]

state_machine = AgentStateMachine(stages)

context = {"goal": "...", "core_values": "..."}

while state_machine.get_current_stage():
    result = await state_machine.execute_current_stage(context)
    context['previous_result'] = result
    
    if not state_machine.move_next():
        break

progress = state_machine.get_progress()
print(f"진행률: {progress['progress_percent']}%")
```

### 패턴 2: 파일 I/O 자동화

**왜 필요한가요?**  
에이전트는 파일 시스템을 통해 입출력을 주고받아요. 디렉토리 생성, 파일 저장, JSON 직렬화 등 반복 작업을 자동화하면 코드가 간결해집니다.

**구현**:
```python
import json
from pathlib import Path
from typing import Any, Dict

class FileManager:
    """파일 관리 유틸리티"""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self._ensure_directory(self.base_dir)
    
    def _ensure_directory(self, path: Path):
        """디렉토리가 없으면 생성"""
        path.mkdir(parents=True, exist_ok=True)
    
    def get_path(self, relative_path: str) -> Path:
        """상대 경로를 절대 경로로 변환"""
        return self.base_dir / relative_path
    
    def save_json(self, relative_path: str, data: Any):
        """JSON 파일 저장"""
        file_path = self.get_path(relative_path)
        self._ensure_directory(file_path.parent)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 저장: {relative_path}")
    
    def load_json(self, relative_path: str) -> Any:
        """JSON 파일 로드"""
        file_path = self.get_path(relative_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"파일 없음: {relative_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_text(self, relative_path: str, text: str):
        """텍스트 파일 저장"""
        file_path = self.get_path(relative_path)
        self._ensure_directory(file_path.parent)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def load_text(self, relative_path: str) -> str:
        """텍스트 파일 로드"""
        file_path = self.get_path(relative_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # 사고 클러스터 전용 헬퍼
    def save_thinking_record(
        self,
        cluster_id: str,
        stage: str,
        record: Dict[str, Any]
    ):
        """thinking_record.json 저장"""
        path = f"thinking/{cluster_id}/{stage}/thinking_record.json"
        self.save_json(path, record)
    
    def load_thinking_record(
        self,
        cluster_id: str,
        stage: str
    ) -> Dict[str, Any]:
        """thinking_record.json 로드"""
        path = f"thinking/{cluster_id}/{stage}/thinking_record.json"
        return self.load_json(path)


# 사용 예시
file_manager = FileManager('./workspaces/task-123')

# JSON 저장
file_manager.save_json('outputs/result.json', {
    'title': '결과',
    'data': [1, 2, 3]
})

# thinking_record 저장
file_manager.save_thinking_record(
    cluster_id='tc-c1',
    stage='planning',
    record={'plan': '...', 'reasoning': '...'}
)
```

---

**(계속 Part 2로)**
