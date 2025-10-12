## 12.4 병렬 사고 처리

계층적 사고 클러스터의 가장 큰 이점은 **여러 사고 프로세스를 동시에 실행**할 수 있다는 것입니다. 이 섹션에서는 병렬 사고 처리의 조건과 방법을 다룹니다.

### 12.4.1 병렬 처리의 조건

**언제 병렬 실행이 가능한가?**

```yaml
병렬_처리_기본_조건:
  조건_1_독립성:
    정의: "각 사고 클러스터가 다른 클러스터의 결과를 기다리지 않고 시작 가능"
    예시:
      good: "마케팅, 콘텐츠, 디자인이 동시에 시작"
      bad: "실행이 전략 완료를 기다려야 함"
    검증:
      - "의존성 그래프에서 연결된 간선이 없는가?"
      - "필수 입력 데이터가 없는가?"
  
  조건_2_리소스_가용성:
    정의: "각 클러스터가 필요한 리소스가 충분한가"
    고려_사항:
      - "인적 리소스 (팀 규모)"
      - "컴퓨팅 리소스 (AI API 호출 한도)"
      - "예산 (외부 서비스 비용)"
    부족시:
      - "우선순위 기반 배분 (12.2.2)"
      - "순차 실행으로 전환"
  
  조건_3_목표_충돌_없음:
    정의: "두 클러스터가 상충되는 방향으로 사고하지 않는가"
    예시:
      conflict: "마케팅은 '고급', 영업은 '대중' 추구"
      resolution: "충돌 해결 후 병렬 실행 (12.3.4)"
    검증:
      - "report_kr.md의 목표 충돌 유형 분석"
      - "핵심 가치 기반 사전 조정"
```

**병렬화 가능성 평가 매트릭스**:

```python
# 병렬 처리 가능성 평가

def evaluate_parallelizability(thinking_clusters, dependencies, resources):
    """
    사고 클러스터들이 병렬 실행 가능한지 평가합니다.
    
    Parameters:
    - thinking_clusters: 사고 클러스터 리스트
    - dependencies: 클러스터 간 의존성 그래프
    - resources: 가용 리소스
    
    Returns:
    - 병렬화 가능성 평가 결과
    """
    
    results = {
        'is_parallelizable': True,
        'parallel_groups': [],
        'sequential_stages': [],
        'blockers': [],
        'recommendations': []
    }
    
    # 조건 1: 의존성 분석
    independent_clusters = []
    dependent_clusters = []
    
    for cluster in thinking_clusters:
        cluster_name = cluster['name']
        deps = dependencies.get(cluster_name, [])
        
        if len(deps) == 0:
            independent_clusters.append(cluster_name)
        else:
            dependent_clusters.append({
                'cluster': cluster_name,
                'depends_on': deps
            })
    
    if len(independent_clusters) > 0:
        results['parallel_groups'].append({
            'stage': 1,
            'clusters': independent_clusters,
            'can_start': 'immediately'
        })
    else:
        results['is_parallelizable'] = False
        results['blockers'].append('모든 클러스터가 의존성을 가짐 - 병렬화 불가능')
    
    # 조건 2: 리소스 제약 확인
    total_resource_need = {}
    for cluster in thinking_clusters:
        for resource, amount in cluster.get('resource_needs', {}).items():
            total_resource_need[resource] = total_resource_need.get(resource, 0) + amount
    
    for resource, needed in total_resource_need.items():
        available = resources.get(resource, 0)
        if needed > available:
            results['blockers'].append(
                f"{resource} 부족: {needed} 필요, {available} 가용"
            )
            results['recommendations'].append(
                f"{resource} 추가 확보 또는 순차 실행 고려"
            )
    
    # 조건 3: 목표 충돌 검사
    for i, cluster_a in enumerate(thinking_clusters):
        for cluster_b in thinking_clusters[i+1:]:
            if has_goal_conflict(cluster_a, cluster_b):
                results['blockers'].append(
                    f"{cluster_a['name']} 과 {cluster_b['name']} 간 목표 충돌"
                )
                results['recommendations'].append(
                    f"충돌 해결 후 병렬 실행 (12.3.4 참조)"
                )
    
    # 최종 평가
    if len(results['blockers']) > 0:
        results['is_parallelizable'] = False
        results['summary'] = f"{len(results['blockers']}}개 블로커 발견 - 병렬화 지연됨"
    else:
        efficiency_gain = len(independent_clusters) / len(thinking_clusters) * 100
        results['summary'] = f"{len(independent_clusters)}개 클러스터 병렬 가능 ({efficiency_gain:.0f}% 효율 향상)"
    
    return results

def has_goal_conflict(cluster_a, cluster_b):
    """
    두 클러스터 간 목표 충돌 여부를 간단히 판단
    """
    # 간단한 예시: primary_value가 상충되는지 확인
    conflicting_pairs = [
        ('premium', 'budget'),
        ('growth', 'stability'),
        ('innovation', 'reliability')
    ]
    
    value_a = cluster_a.get('primary_value', '').lower()
    value_b = cluster_b.get('primary_value', '').lower()
    
    for pair in conflicting_pairs:
        if (value_a in pair[0] and value_b in pair[1]) or \
           (value_a in pair[1] and value_b in pair[0]):
            return True
    
    return False

# 사용 예시
clusters = [
    {'name': 'marketing_thinking', 'primary_value': 'brand_excellence', 'resource_needs': {'designers': 1}},
    {'name': 'content_thinking', 'primary_value': 'customer_satisfaction', 'resource_needs': {'designers': 1}},
    {'name': 'design_thinking', 'primary_value': 'innovation', 'resource_needs': {'designers': 2}}
]

dependencies = {
    'marketing_thinking': [],  # 독립적
    'content_thinking': [],     # 독립적
    'design_thinking': []       # 독립적
}

resources = {'designers': 3}  # 총 3명 가용

result = evaluate_parallelizability(clusters, dependencies, resources)
print(f"Parallelizable: {result['is_parallelizable']}")
print(f"Summary: {result['summary']}")

if result['blockers']:
    print(f"\nBlockers:")
    for blocker in result['blockers']:
        print(f"  - {blocker}")

if result['recommendations']:
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")

# 출력:
# Parallelizable: False
# Summary: 1개 블로커 발견 - 병렬화 지연됨
# Blockers:
#   - designers 부족: 4 필요, 3 가용
# Recommendations:
#   - designers 추가 확보 또는 순차 실행 고려
```

### 12.4.2 독립성 검증 방법

**의존성 그래프 분석**:

```yaml
의존성_분석:
  단계_1_그래프_구축:
    nodes: "모든 사고 클러스터"
    edges: "의존 관계 (A → B: B가 A에 의존)"
    
    example:
      "마케팅 → 콘텐츠": "콘텐츠가 마케팅의 페르소나 필요"
      "마케팅 → 디자인": "디자인이 마케팅의 포지셔닝 필요"
      "디자인 → 없음": "디자인은 독립적"
  
  단계_2_계층_분류:
    level_0: "의존성이 없는 클러스터 (in-degree = 0)"
    level_1: "level_0에만 의존하는 클러스터"
    level_2: "level_0 또는 level_1에 의존하는 클러스터"
    
    example:
      level_0: ["마케팅"]
      level_1: ["콘텐츠", "디자인"]  # 병렬 가능
      level_2: ["실행"]
  
  단계_3_병렬_그룹_생성:
    rule: "같은 level의 클러스터들은 병렬 실행 가능"
    output:
      batch_1: [level_0]
      batch_2: [level_1]  # 병렬
      batch_3: [level_2]
```

**위상 정렬 (Topological Sort) 구현**:

```python
# 위상 정렬로 병렬 그룹 생성

def generate_parallel_batches(thinking_clusters, dependencies):
    """
    의존성 그래프를 기반으로 병렬 실행 가능한 배치를 생성합니다.
    
    Returns:
    - 병렬 배치 리스트 (batch 단위로 병렬 가능)
    """
    from collections import deque
    
    # 진입 차수 계산 (in-degree)
    in_degree = {cluster['name']: 0 for cluster in thinking_clusters}
    
    for cluster_name, deps in dependencies.items():
        for dep in deps:
            if dep in in_degree:
                in_degree[cluster_name] += 1
    
    # 진입 차수 0인 노드로 시작 (level 0)
    queue = deque([name for name, degree in in_degree.items() if degree == 0])
    batches = []
    processed = set()
    
    while queue:
        # 현재 단계에서 병렬 가능한 클러스터들
        current_batch = []
        batch_size = len(queue)
        
        for _ in range(batch_size):
            cluster_name = queue.popleft()
            current_batch.append(cluster_name)
            processed.add(cluster_name)
            
            # 이 클러스터에 의존하는 노드들의 진입 차수 감소
            for other_cluster, deps in dependencies.items():
                if cluster_name in deps and other_cluster not in processed:
                    in_degree[other_cluster] -= 1
                    if in_degree[other_cluster] == 0:
                        queue.append(other_cluster)
        
        batches.append(current_batch)
    
    # 순환 의존성 확인
    if len(processed) < len(thinking_clusters):
        unprocessed = [c['name'] for c in thinking_clusters if c['name'] not in processed]
        raise ValueError(f"순환 의존성 발견: {unprocessed}")
    
    return batches

# 사용 예시
clusters = [
    {'name': 'strategy_thinking'},
    {'name': 'marketing_thinking'},
    {'name': 'content_thinking'},
    {'name': 'design_thinking'},
    {'name': 'execution_thinking'}
]

dependencies = {
    'strategy_thinking': [],
    'marketing_thinking': ['strategy_thinking'],
    'content_thinking': ['marketing_thinking'],
    'design_thinking': ['marketing_thinking'],
    'execution_thinking': ['content_thinking', 'design_thinking']
}

try:
    batches = generate_parallel_batches(clusters, dependencies)
    
    print(f"Total batches: {len(batches)}")
    print(f"\nExecution plan:")
    
    total_time = 0
    for i, batch in enumerate(batches, 1):
        print(f"\nBatch {i} (parallel):")
        for cluster in batch:
            print(f"  - {cluster}")
        
        # 가정: 각 클러스터 1주 소요
        batch_time = 1  # week
        total_time += batch_time
        print(f"  Time: {batch_time} week(s)")
    
    print(f"\nTotal time: {total_time} weeks")
    print(f"Time saved vs sequential: {len(clusters) - total_time} weeks ({(len(clusters) - total_time) / len(clusters) * 100:.0f}%)")

except ValueError as e:
    print(f"❌ 오류: {e}")

# 출력:
# Total batches: 4
# 
# Execution plan:
# 
# Batch 1 (parallel):
#   - strategy_thinking
#   Time: 1 week(s)
# 
# Batch 2 (parallel):
#   - marketing_thinking
#   Time: 1 week(s)
# 
# Batch 3 (parallel):
#   - content_thinking
#   - design_thinking
#   Time: 1 week(s)
# 
# Batch 4 (parallel):
#   - execution_thinking
#   Time: 1 week(s)
# 
# Total time: 4 weeks
# Time saved vs sequential: 1 weeks (20%)
```

### 12.4.3 동기화 지점 설계

병렬로 실행되는 사고 클러스터들의 결과를 **언제, 어떻게 통합할 것인가**가 중요합니다.

**합류 지점 (Join Points)**:

```yaml
join_points:
  정의: "여러 병렬 클러스터의 결과가 모이는 지점"
  
  유형_1_모두_완료_대기:
    description: "모든 병렬 클러스터가 완료될 때까지 대기"
    use_case: "필수 의존성"
    example:
      clusters: ["콘텐츠", "디자인"]
      join_action: "두 결과를 통합하여 최종 캐페인 완성"
      condition: "content.status == 'complete' AND design.status == 'complete'"
  
  유형_2_조기_통합:
    description: "클러스터가 완료되는 대로 순차적으로 통합"
    use_case: "선택적 의존성"
    example:
      scenario: "콘텐츠가 먼저 완료되면 일부 공개 가능"
      benefit: "빠른 피드백 및 반복 가능"
  
  유형_3_부분_통합:
    description: "특정 부분만 통합하고 나머지는 계속 병렬 실행"
    use_case: "점진적 통합"
    example:
      scenario: "마케팅의 타겟 페르소나만 먼저 공유"
      benefit: "나머지 작업 지연 없이 진행"
```

**동기화 지점 구현**:

```python
# 합류 지점 (Join Point) 관리

class JoinPoint:
    """병렬 사고 클러스터들의 합류 지점"""
    
    def __init__(self, name, required_clusters, join_strategy='wait_all'):
        """
        Parameters:
        - name: 합류 지점 이름
        - required_clusters: 대기할 클러스터 리스트
        - join_strategy: 'wait_all' | 'first_complete' | 'threshold'
        """
        self.name = name
        self.required_clusters = required_clusters
        self.join_strategy = join_strategy
        self.completed_clusters = set()
        self.results = {}
    
    def report_completion(self, cluster_name, result):
        """
        클러스터가 완료를 보고합니다.
        """
        if cluster_name in self.required_clusters:
            self.completed_clusters.add(cluster_name)
            self.results[cluster_name] = result
            print(f"{cluster_name} completed at join point '{self.name}'")
            
            # 합류 조건 확인
            if self.is_ready_to_proceed():
                return self.merge_results()
        
        return None
    
    def is_ready_to_proceed(self):
        """합류 지점을 진행할 준비가 되었는지 확인"""
        if self.join_strategy == 'wait_all':
            return self.completed_clusters == set(self.required_clusters)
        
        elif self.join_strategy == 'first_complete':
            return len(self.completed_clusters) > 0
        
        elif self.join_strategy == 'threshold':
            threshold = int(len(self.required_clusters) * 0.7)  # 70%
            return len(self.completed_clusters) >= threshold
    
    def merge_results(self):
        """클러스터 결과를 통합합니다"""
        print(f"\nJoin point '{self.name}' activated:")
        print(f"  Completed: {', '.join(self.completed_clusters)}")
        
        # 결과 통합
        merged_result = {
            'join_point': self.name,
            'strategy': self.join_strategy,
            'completed_clusters': list(self.completed_clusters),
            'results': self.results,
            'merged_output': {}
        }
        
        # 간단한 통합 로직
        for cluster_name, result in self.results.items():
            for key, value in result.items():
                if key not in merged_result['merged_output']:
                    merged_result['merged_output'][key] = []
                merged_result['merged_output'][key].append({
                    'from': cluster_name,
                    'data': value
                })
        
        return merged_result

# 사용 예시
join_point = JoinPoint(
    name='campaign_integration',
    required_clusters=['content_thinking', 'design_thinking'],
    join_strategy='wait_all'
)

# 콘텐츠 클러스터 완료
result_1 = join_point.report_completion(
    cluster_name='content_thinking',
    result={
        'content_assets': ['blog_post_1', 'blog_post_2', 'social_posts'],
        'message_house': 'Innovation in AI'
    }
)
print(f"Ready to proceed: {join_point.is_ready_to_proceed()}\n")

# 디자인 클러스터 완료 (합류 지점 활성화)
result_2 = join_point.report_completion(
    cluster_name='design_thinking',
    result={
        'visual_system': 'modern_minimalist',
        'design_assets': ['logo', 'banner', 'social_templates']
    }
)

if result_2:
    print(f"\nMerged output:")
    for key, values in result_2['merged_output'].items():
        print(f"  {key}:")
        for item in values:
            print(f"    - {item['from']}: {item['data']}")

# 출력:
# content_thinking completed at join point 'campaign_integration'
# Ready to proceed: False
# 
# design_thinking completed at join point 'campaign_integration'
# 
# Join point 'campaign_integration' activated:
#   Completed: content_thinking, design_thinking
# 
# Merged output:
#   content_assets:
#     - content_thinking: ['blog_post_1', 'blog_post_2', 'social_posts']
#   message_house:
#     - content_thinking: Innovation in AI
#   visual_system:
#     - design_thinking: modern_minimalist
#   design_assets:
#     - design_thinking: ['logo', 'banner', 'social_templates']
```

### 12.4.4 리소스 배분 전략

병렬 실행 시 제한된 리소스를 어떻게 효율적으로 분배할 것인가?

**동적 리소스 배분**:

```yaml
리소스_배분_전략:
  전략_1_고정_배분:
    description: "각 클러스터에 사전에 리소스 할당"
    장점: "간단한 관리, 예측 가능한 성능"
    단점: "비효율적 사용 (한 클러스터가 놀면 낭비)"
    적합: "리소스 추분한 경우"
  
  전략_2_동적_배분:
    description: "클러스터가 필요한 때 요청하여 배분"
    장점: "효율적 사용, 병목 제거"
    단점: "복잡한 관리, 충돌 가능성"
    적합: "리소스 제한적인 경우"
  
  전략_3_우선순위_기반:
    description: "핵심 가치 우선순위로 리소스 배분"
    장점: "전략적 일관성, 명확한 근거"
    단점: "하위 클러스터 지연 가능성"
    적합: "모든 경우 (특히 충돌 시)"
```

**동적 리소스 풀 관리**:

```python
# 동적 리소스 풀 관리

class ResourcePool:
    """병렬 사고 클러스터를 위한 리소스 풀"""
    
    def __init__(self, resources):
        """
        Parameters:
        - resources: {resource_name: available_amount}
        """
        self.total_resources = resources.copy()
        self.available_resources = resources.copy()
        self.allocations = {}  # {cluster_name: {resource: amount}}
        self.waitlist = []  # 대기 중인 요청
    
    def request_resources(self, cluster_name, resource_request, priority=0):
        """
        리소스를 요청합니다.
        
        Parameters:
        - cluster_name: 요청 클러스터
        - resource_request: {resource_name: requested_amount}
        - priority: 우선순위 (낮을수록 높음)
        
        Returns:
        - True if allocated, False if waitlisted
        """
        
        # 요청된 모든 리소스가 가용한지 확인
        can_allocate = all(
            self.available_resources.get(resource, 0) >= amount
            for resource, amount in resource_request.items()
        )
        
        if can_allocate:
            # 리소스 할당
            for resource, amount in resource_request.items():
                self.available_resources[resource] -= amount
            
            self.allocations[cluster_name] = resource_request
            print(f"✓ {cluster_name}: Resources allocated")
            for resource, amount in resource_request.items():
                print(f"    {resource}: {amount}")
            return True
        
        else:
            # 대기 목록에 추가
            self.waitlist.append({
                'cluster': cluster_name,
                'request': resource_request,
                'priority': priority
            })
            self.waitlist.sort(key=lambda x: x['priority'])
            
            print(f"❌ {cluster_name}: Insufficient resources, waitlisted (priority {priority})")
            return False
    
    def release_resources(self, cluster_name):
        """
        클러스터가 완료되면 리소스 반환
        """
        if cluster_name in self.allocations:
            allocation = self.allocations.pop(cluster_name)
            
            for resource, amount in allocation.items():
                self.available_resources[resource] += amount
            
            print(f"\n{cluster_name} released resources:")
            for resource, amount in allocation.items():
                print(f"  {resource}: {amount}")
            
            # 대기 목록 처리
            self._process_waitlist()
    
    def _process_waitlist(self):
        """대기 중인 요청 처리"""
        processed = []
        
        for i, wait_item in enumerate(self.waitlist):
            can_allocate = all(
                self.available_resources.get(resource, 0) >= amount
                for resource, amount in wait_item['request'].items()
            )
            
            if can_allocate:
                # 할당 가능
                for resource, amount in wait_item['request'].items():
                    self.available_resources[resource] -= amount
                
                self.allocations[wait_item['cluster']] = wait_item['request']
                print(f"\n✓ {wait_item['cluster']} (waitlist): Resources now allocated")
                processed.append(i)
        
        # 처리된 항목 제거 (역순으로 제거하여 인덱스 문제 방지)
        for i in reversed(processed):
            self.waitlist.pop(i)
    
    def get_status(self):
        """현재 리소스 상태 반환"""
        return {
            'total': self.total_resources,
            'available': self.available_resources,
            'allocated': self.allocations,
            'waitlist_count': len(self.waitlist)
        }

# 사용 예시
pool = ResourcePool({
    'designers': 2,
    'api_credits': 1000
})

# 3개 클러스터가 동시에 리소스 요청
pool.request_resources('marketing_thinking', {'designers': 1, 'api_credits': 300}, priority=0)
pool.request_resources('content_thinking', {'designers': 1, 'api_credits': 400}, priority=1)
pool.request_resources('design_thinking', {'designers': 1, 'api_credits': 300}, priority=2)  # 대기

# 마케팅 완료
pool.release_resources('marketing_thinking')

# 상태 확인
status = pool.get_status()
print(f"\nCurrent status:")
print(f"  Available: {status['available']}")
print(f"  Waitlist: {status['waitlist_count']} clusters")

# 출력:
# ✓ marketing_thinking: Resources allocated
#     designers: 1
#     api_credits: 300
# ✓ content_thinking: Resources allocated
#     designers: 1
#     api_credits: 400
# ❌ design_thinking: Insufficient resources, waitlisted (priority 2)
# 
# marketing_thinking released resources:
#   designers: 1
#   api_credits: 300
# 
# ✓ design_thinking (waitlist): Resources now allocated
# 
# Current status:
#   Available: {'designers': 0, 'api_credits': 300}
#   Waitlist: 0 clusters
```

---

