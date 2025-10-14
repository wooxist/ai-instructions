# 16.3 에이전트 구현 가이드 (Part 2)

## 16.3.2 핵심 구현 패턴 (계속)

### 패턴 3: 재시도 로직 (Retry Logic)

**왜 필요한가요?**  
AI API 호출은 네트워크 문제나 레이트 리밋으로 실패할 수 있어요. 자동 재시도 로직을 추가하면 안정성이 크게 향상됩니다.

**구현**:
```python
import asyncio
from typing import Callable, TypeVar, Optional
from functools import wraps

T = TypeVar('T')

class RetryConfig:
    """재시도 설정"""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_backoff: bool = True,
        retry_on_exceptions: tuple = (Exception,)
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_backoff = exponential_backoff
        self.retry_on_exceptions = retry_on_exceptions

async def with_retry(
    func: Callable[..., T],
    *args,
    config: Optional[RetryConfig] = None,
    **kwargs
) -> T:
    """함수를 재시도 로직과 함께 실행"""
    if config is None:
        config = RetryConfig()
    
    last_exception = None
    
    for attempt in range(config.max_retries):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        
        except config.retry_on_exceptions as e:
            last_exception = e
            
            if attempt == config.max_retries - 1:
                raise
            
            # 대기 시간 계산
            if config.exponential_backoff:
                delay = min(
                    config.base_delay * (2 ** attempt),
                    config.max_delay
                )
            else:
                delay = config.base_delay
            
            print(f"⚠️  시도 {attempt + 1}/{config.max_retries} 실패. "
                  f"{delay:.1f}초 후 재시도... (오류: {str(e)[:50]})")
            
            await asyncio.sleep(delay)
    
    raise last_exception


# Decorator로도 사용 가능
def retry(config: Optional[RetryConfig] = None):
    """재시도 decorator"""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await with_retry(func, *args, config=config, **kwargs)
        return wrapper
    
    return decorator


# 사용 예시
@retry(RetryConfig(max_retries=3))
async def call_api(prompt: str) -> str:
    """API 호출 (실패 가능)"""
    # ... API 호출 로직
    pass

result = await call_api("안녕하세요")
```

**고급 활용**:
```python
# API 호출용 특화 재시도 설정
API_RETRY_CONFIG = RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=30.0,
    exponential_backoff=True,
    retry_on_exceptions=(
        ConnectionError,
        TimeoutError,
    )
)

# BaseAgent에서 사용
class BaseAgent:
    def __init__(self):
        self.api_retry_config = API_RETRY_CONFIG
    
    async def call_ai(self, prompt: str) -> str:
        """AI 호출 (자동 재시도)"""
        return await with_retry(
            self._raw_api_call,
            prompt,
            config=self.api_retry_config
        )
```

### 패턴 4: Human-in-the-Loop

**왜 필요한가요?**  
에이전트가 중요한 결정을 내려야 할 때, 사람의 승인을 받는 것이 안전해요. 특히 비용이 많이 드는 작업이나 되돌리기 어려운 작업에서는 필수입니다.

**구현**:
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum

class ApprovalStatus(Enum):
    """승인 상태"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMEOUT = "timeout"

class ApprovalResponse:
    """승인 응답"""
    
    def __init__(
        self,
        status: ApprovalStatus,
        feedback: Optional[str] = None,
        modifications: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.feedback = feedback
        self.modifications = modifications or {}
    
    @property
    def is_approved(self) -> bool:
        return self.status == ApprovalStatus.APPROVED


class Notifier(ABC):
    """알림 발송 인터페이스"""
    
    @abstractmethod
    async def send(self, message: Dict[str, Any]):
        pass


class SlackNotifier(Notifier):
    """Slack 알림"""
    
    def __init__(self, webhook_url: str, channel: str):
        self.webhook_url = webhook_url
        self.channel = channel
    
    async def send(self, message: Dict[str, Any]):
        print(f"[Slack #{self.channel}] {message}")


class ApprovalGate:
    """Human-in-the-Loop 승인 게이트"""
    
    def __init__(
        self,
        notifier: Notifier,
        timeout_seconds: int = 3600
    ):
        self.notifier = notifier
        self.timeout_seconds = timeout_seconds
        self.pending_approvals: Dict[str, ApprovalResponse] = {}
    
    async def require_approval(
        self,
        approval_id: str,
        context: Dict[str, Any],
        explanation: str = ""
    ) -> ApprovalResponse:
        """승인 요청"""
        
        message = {
            'type': 'approval_request',
            'approval_id': approval_id,
            'explanation': explanation,
            'context': context,
            'timeout': f"{self.timeout_seconds // 60}분"
        }
        
        await self.notifier.send(message)
        
        # 승인 대기
        start_time = asyncio.get_event_loop().time()
        
        while True:
            if approval_id in self.pending_approvals:
                response = self.pending_approvals.pop(approval_id)
                return response
            
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > self.timeout_seconds:
                return ApprovalResponse(
                    status=ApprovalStatus.TIMEOUT,
                    feedback="승인 타임아웃"
                )
            
            await asyncio.sleep(1)
    
    def submit_approval(
        self,
        approval_id: str,
        approved: bool,
        feedback: Optional[str] = None
    ):
        """승인 응답 제출"""
        status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        
        response = ApprovalResponse(
            status=status,
            feedback=feedback
        )
        
        self.pending_approvals[approval_id] = response
        print(f"✓ 승인 응답 제출: {approval_id} -> {status.value}")


# 사용 예시
async def main():
    notifier = SlackNotifier(
        webhook_url="https://hooks.slack.com/...",
        channel="approvals"
    )
    
    approval_gate = ApprovalGate(
        notifier=notifier,
        timeout_seconds=1800
    )
    
    context = {
        'task': 'Launch marketing campaign',
        'estimated_cost': '$50,000'
    }
    
    response = await approval_gate.require_approval(
        approval_id='campaign-launch-2025-q4',
        context=context,
        explanation='Q4 마케팅 캠페인 승인이 필요합니다.'
    )
    
    if response.is_approved:
        print("✅ 승인됨!")
        await launch_campaign(context)
    else:
        print("❌ 거부됨")
```

---

## 16.3.3 오류 처리 및 복구

에이전트가 실패했을 때 어떻게 대응하느냐가 시스템의 신뢰성을 결정해요.

### 체크포인트 및 재개 (Checkpoint & Resume)

**왜 필요한가요?**  
에이전트가 긴 작업을 수행 중 실패하면, 처음부터 다시 시작하는 것은 비효율적이에요. 체크포인트를 저장하고 실패 지점부터 재개하면 시간과 비용을 절약할 수 있습니다.

**구현**:
```python
import json
from pathlib import Path
from typing import Optional, Any, Dict
from datetime import datetime

class Checkpoint:
    """체크포인트 데이터"""
    
    def __init__(
        self,
        stage_name: str,
        stage_index: int,
        result: Any,
        timestamp: str
    ):
        self.stage_name = stage_name
        self.stage_index = stage_index
        self.result = result
        self.timestamp = timestamp
    
    def to_dict(self) -> Dict:
        return {
            'stage_name': self.stage_name,
            'stage_index': self.stage_index,
            'result': self.result,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Checkpoint':
        return cls(
            stage_name=data['stage_name'],
            stage_index=data['stage_index'],
            result=data['result'],
            timestamp=data['timestamp']
        )


class CheckpointManager:
    """체크포인트 관리"""
    
    def __init__(self, base_dir: str, task_id: str):
        self.base_dir = Path(base_dir)
        self.task_id = task_id
        self.checkpoint_file = self.base_dir / f"checkpoints/{task_id}.json"
        
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        stage_name: str,
        stage_index: int,
        result: Any
    ):
        """체크포인트 저장"""
        checkpoint = Checkpoint(
            stage_name=stage_name,
            stage_index=stage_index,
            result=result,
            timestamp=datetime.now().isoformat()
        )
        
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"💾 체크포인트 저장: {stage_name} (#{stage_index})")
    
    def load_checkpoint(self) -> Optional[Checkpoint]:
        """체크포인트 로드"""
        if not self.checkpoint_file.exists():
            return None
        
        with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        checkpoint = Checkpoint.from_dict(data)
        print(f"📂 체크포인트 로드: {checkpoint.stage_name} (#{checkpoint.stage_index})")
        
        return checkpoint
    
    def clear_checkpoint(self):
        """체크포인트 삭제"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


# BaseAgent에 통합
class BaseAgent:
    def __init__(self, task_id: str, base_dir: str):
        self.task_id = task_id
        self.checkpoint_manager = CheckpointManager(base_dir, task_id)
    
    async def run(self, resume: bool = True):
        """에이전트 실행"""
        start_stage_index = 0
        previous_results = {}
        
        # 체크포인트 확인
        if resume:
            checkpoint = self.checkpoint_manager.load_checkpoint()
            
            if checkpoint:
                start_stage_index = checkpoint.stage_index + 1
                previous_results = checkpoint.result
                print(f"🔄 {checkpoint.stage_name} 이후부터 재개...")
        
        # Stage 실행
        context = {'previous_results': previous_results}
        
        for i in range(start_stage_index, len(self.stages)):
            stage = self.stages[i]
            
            try:
                result = await stage.handler(context)
                
                # 체크포인트 저장
                self.checkpoint_manager.save_checkpoint(
                    stage_name=stage.name,
                    stage_index=i,
                    result=result
                )
                
                context['previous_results'][stage.name] = result
                
            except Exception as e:
                print(f"❌ {stage.name} 실패: {e}")
                print(f"💡 resume=True로 재실행하면 이 지점부터 계속됩니다.")
                raise
        
        # 완료 후 체크포인트 삭제
        self.checkpoint_manager.clear_checkpoint()
        
        return context['previous_results']
```

### 로깅 및 디버깅

**구현**:
```python
import logging
from datetime import datetime

class AgentLogger:
    """에이전트 전용 로거"""
    
    def __init__(self, task_id: str, log_file: str = None):
        self.task_id = task_id
        self.logger = logging.getLogger(f"agent.{task_id}")
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def stage_start(self, stage_name: str):
        """Stage 시작"""
        self.logger.info(f"🚀 {stage_name} 시작")
    
    def stage_complete(self, stage_name: str, duration_seconds: float):
        """Stage 완료"""
        self.logger.info(f"✅ {stage_name} 완료 ({duration_seconds:.1f}초)")
    
    def stage_failed(self, stage_name: str, error: Exception):
        """Stage 실패"""
        self.logger.error(f"❌ {stage_name} 실패: {error}")
    
    def api_call(self, prompt_preview: str, tokens: int):
        """API 호출"""
        self.logger.debug(f"🔵 API 호출: {prompt_preview[:50]}... (토큰: {tokens})")
    
    def human_approval_required(self, approval_id: str):
        """승인 요청"""
        self.logger.warning(f"⏸️  승인 대기: {approval_id}")
    
    def human_approval_received(self, approval_id: str, approved: bool):
        """승인 응답"""
        status = "승인" if approved else "거부"
        self.logger.info(f"✓ 승인 응답: {approval_id} -> {status}")


# 사용 예시
logger = AgentLogger(
    task_id='content-gen-001',
    log_file='logs/content-gen-001.log'
)

logger.stage_start('planning')
# ... 작업 수행
logger.stage_complete('planning', 15.3)
```

### 알림 및 모니터링

**구현**:
```python
class AlertManager:
    """알림 관리자"""
    
    def __init__(self, notifiers: List[Notifier]):
        self.notifiers = notifiers
    
    async def alert_failure(
        self,
        task_id: str,
        stage_name: str,
        error: Exception
    ):
        """실패 알림"""
        message = {
            'type': 'agent_failure',
            'task_id': task_id,
            'stage': stage_name,
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        }
        
        for notifier in self.notifiers:
            await notifier.send(message)
    
    async def alert_completion(
        self,
        task_id: str,
        duration_seconds: float
    ):
        """완료 알림"""
        message = {
            'type': 'agent_completion',
            'task_id': task_id,
            'duration': f"{duration_seconds:.1f}초",
            'timestamp': datetime.now().isoformat()
        }
        
        for notifier in self.notifiers:
            await notifier.send(message)
    
    async def alert_cost_warning(
        self,
        task_id: str,
        current_cost: float,
        budget: float
    ):
        """비용 경고"""
        if current_cost > budget * 0.8:
            message = {
                'type': 'cost_warning',
                'task_id': task_id,
                'current_cost': current_cost,
                'budget': budget,
                'percent': (current_cost / budget) * 100
            }
            
            for notifier in self.notifiers:
                await notifier.send(message)


# 사용
alert_manager = AlertManager([
    SlackNotifier(webhook_url="...", channel="alerts"),
    EmailNotifier(recipient="team@example.com")
])

await alert_manager.alert_failure(
    task_id='task-123',
    stage_name='reasoning',
    error=Exception("API timeout")
)
```

---

## 16.3.4 성능 최적화

에이전트를 실전에서 사용하려면 성능과 비용 최적화가 필수예요.

### API 호출 최소화

**1. 결과 캐싱**:
```python
import hashlib
from typing import Optional

class ResponseCache:
    """API 응답 캐시"""
    
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, prompt: str, model: str) -> str:
        """캐시 키 생성"""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str) -> Optional[str]:
        """캐시에서 가져오기"""
        key = self._get_cache_key(prompt, model)
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"💚 캐시 히트: {prompt[:30]}...")
                return data['response']
        
        return None
    
    def set(self, prompt: str, model: str, response: str):
        """캐시에 저장"""
        key = self._get_cache_key(prompt, model)
        cache_file = self.cache_dir / f"{key}.json"
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'prompt': prompt,
                'model': model,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)


# BaseAgent에서 사용
class BaseAgent:
    def __init__(self, enable_cache: bool = True):
        self.cache = ResponseCache('./cache') if enable_cache else None
    
    async def call_ai(self, prompt: str) -> str:
        # 캐시 확인
        if self.cache:
            cached = self.cache.get(prompt, "claude-sonnet-4-20250514")
            if cached:
                return cached
        
        # API 호출
        response = await self._raw_api_call(prompt)
        
        # 캐시 저장
        if self.cache:
            self.cache.set(prompt, "claude-sonnet-4-20250514", response)
        
        return response
```

**2. 배치 처리**:
```python
class BatchProcessor:
    """여러 요청을 배치로 처리"""
    
    def __init__(self, batch_size: int = 5):
        self.batch_size = batch_size
        self.queue = []
    
    async def add(self, prompt: str) -> str:
        """요청 추가"""
        self.queue.append(prompt)
        
        # 배치 크기에 도달하면 처리
        if len(self.queue) >= self.batch_size:
            return await self.flush()
    
    async def flush(self) -> List[str]:
        """대기 중인 모든 요청 처리"""
        if not self.queue:
            return []
        
        # 한 번에 처리
        results = await self._process_batch(self.queue)
        self.queue = []
        
        return results
    
    async def _process_batch(self, prompts: List[str]) -> List[str]:
        """배치 처리"""
        # 병렬 처리
        tasks = [self._call_api(p) for p in prompts]
        return await asyncio.gather(*tasks)
```

### 비용 추적

```python
class CostTracker:
    """API 비용 추적"""
    
    # 토큰당 비용 (예시)
    COST_PER_1K_INPUT_TOKENS = 0.003
    COST_PER_1K_OUTPUT_TOKENS = 0.015
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def track(self, input_tokens: int, output_tokens: int):
        """토큰 사용 기록"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
    
    def get_total_cost(self) -> float:
        """총 비용 계산"""
        input_cost = (self.total_input_tokens / 1000) * self.COST_PER_1K_INPUT_TOKENS
        output_cost = (self.total_output_tokens / 1000) * self.COST_PER_1K_OUTPUT_TOKENS
        
        return input_cost + output_cost
    
    def get_summary(self) -> Dict:
        """비용 요약"""
        return {
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_cost_usd': self.get_total_cost(),
            'average_cost_per_call': self.get_total_cost() / max(1, self.call_count)
        }


# BaseAgent에서 사용
class BaseAgent:
    def __init__(self):
        self.cost_tracker = CostTracker()
    
    async def call_ai(self, prompt: str) -> str:
        response = await self._raw_api_call(prompt)
        
        # 비용 추적
        input_tokens = len(prompt) // 4  # 대략 추정
        output_tokens = len(response) // 4
        self.cost_tracker.track(input_tokens, output_tokens)
        
        return response
    
    def get_cost_summary(self):
        return self.cost_tracker.get_summary()
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
