# 13.4 사고 산출물 표준화

13.3에서 `thinking_state.json`을 통해 사고 클러스터의 **진행 상태**를 추적하는 방법을 배웠습니다. 이제 **사고의 내용 자체**를 어떻게 기록할지 다룹니다. 즉, "어느 단계인가"가 아니라 "무엇을 생각했는가"를 표준화합니다.

---

## 13.4.1 JSON 기반 사고 기록: `thinking_record.json`

### 왜 사고 내용 표준화가 필요한가?

**문제: 비구조화된 사고 기록**
```yaml
비표준 사고 기록:
  /thinking_clusters/TC001_content/
    thinking/
      planning/
        notes.txt            # 자유 형식 텍스트
          "idea_A는 좋은데, idea_B는 별로..."
          "타겟은 30-40대 직장인"
          "경쟁사 X는 이렇게 했음"
      
      selection/
        decision.txt         # 구조 없는 결정
          "idea_B 선택함. 왜냐하면..."
  
  문제:
    - 사고 과정과 결과가 뒤섞여 있음
    - 프로그래밍으로 분석 불가 (텍스트만 있음)
    - "왜 이렇게 결정했는지" 추출하기 어려움
    - 일관된 형식이 없어 클러스터 간 비교 불가
```

**해결: JSON 기반 표준 스키마**
```yaml
표준화된 사고 기록:
  /thinking_clusters/TC001_content/
    thinking/
      planning/
        thinking_record.json:
          process:                      # ⭐ 사고 과정
            stage: "planning"
            started_at: "..."
            activities:
              - brainstorming
              - research
          
          output:                       # ⭐ 사고 결과
            ideas: [...]
            target: "30-40대 직장인"
            research_findings: "..."
  
  효과:
    - 과정(process)과 결과(output)가 명확히 구분
    - JSON으로 프로그래밍 처리 가능
    - 일관된 형식으로 자동 분석 가능
```

### `thinking_record.json` 기본 구조

```yaml
# thinking_record.json 표준 스키마
thinking_record_schema:
  # 메타데이터
  metadata:
    cluster_id: "TC001"
    stage: "planning"  # 어느 Stage의 기록인가
    version: "1.0"
    created_at: "2025-10-13T09:00:00Z"
    created_by: "AI + Human"
  
  # 사고 과정 (Process)
  process:
    description: "이 Stage에서 어떤 사고 활동을 했는가"
    activities: []       # 수행한 활동 목록
    duration_minutes: 30
    tools_used: []       # 사용한 도구/템플릿
    challenges: []       # 직면한 어려움
  
  # 사고 결과 (Output)
  output:
    type: "ideas | decision | plan | insight | artifact"
    content: {}          # Stage별로 다른 구조
    quality_score: 0.0   # 자체 평가 점수
    references: []       # 참조한 자료
  
  # 핵심 가치 평가 (report_kr.md 2층)
  core_values_alignment:
    practicality: 0.0    # 실용성 점수 (0-10)
    trust: 0.0           # 신뢰 점수 (0-10)
    innovation: 0.0      # 혁신 점수 (0-10)
    weighted_score: 0.0  # 가중 평균 점수
```

---

## 13.4.2 사고 과정 기록 (Process)

사고 **과정**은 "어떻게 생각했는가"를 기록합니다. 각 Stage마다 기록할 내용이 다릅니다.

### Stage별 Process 템플릿

```yaml
# Stage 1: Planning (기획 사고)
planning_process:
  stage: "planning"
  thinking_type: "발산적 사고 (Divergent Thinking)"
  
  activities:
    - name: "목표 분석"
      description: "4층 목표를 구체적 질문으로 분해"
      duration_minutes: 10
    
    - name: "브레인스토밍"
      description: "아이디어 10개 이상 생성"
      duration_minutes: 15
      method: "자유 연상 + 경쟁사 분석"
    
    - name: "타겟 리서치"
      description: "타겟 페르소나 정의"
      duration_minutes: 5
  
  tools_used:
    - "/shared/templates/brainstorming_guide.md"
    - "/shared/templates/target_analysis_template.json"
  
  challenges:
    - "타겟 데이터 부족 → 가정 기반으로 진행"
  
  key_decisions:
    - "타겟: 30-40대 직장인으로 설정 (업무 효율성 관심 높음)"

# Stage 2: Reasoning (추론 사고)
reasoning_process:
  stage: "reasoning"
  thinking_type: "수렴적 사고 (Convergent Thinking)"
  
  activities:
    - name: "핵심 가치 평가"
      description: "각 아이디어를 실용성/신뢰/혁신 기준으로 평가"
      duration_minutes: 15
      method: "10점 척도 평가 + 근거 작성"
    
    - name: "대안 비교"
      description: "상위 3개 아이디어 심층 비교"
      duration_minutes: 10
    
    - name: "최종 선정"
      description: "idea_B 선정 + 근거 문서화"
      duration_minutes: 5
  
  tools_used:
    - "/shared/libraries/evaluation_utils.py"
    - "/shared/configs/core_values.yaml"
  
  evaluation_criteria:
    - name: "실용성"
      weight: 0.4
      definition: "측정 가능한 가치 제공"
    - name: "신뢰"
      weight: 0.3
      definition: "사실 기반, 출처 명시"
    - name: "혁신"
      weight: 0.3
      definition: "새로운 관점 제시"
  
  key_decisions:
    - "idea_B 선정 (가중 점수 7.7점, 실용성 8점으로 가장 높음)"
    - "idea_C는 백업 (혁신 9점으로 높지만 실용성 6점)"

# Stage 3: Experimenting (실험 사고)
experimenting_process:
  stage: "experimenting"
  thinking_type: "생성적 사고 (Generative Thinking)"
  
  activities:
    - name: "초안 작성"
      description: "idea_B를 1,000단어 원고로 구체화"
      duration_minutes: 20
      iterations: 2  # draft_v1, draft_v2
    
    - name: "메시지 하우스 적용"
      description: "핵심 메시지 → 근거 3개 → 증거"
      duration_minutes: 10
  
  tools_used:
    - "/shared/templates/message_house_template.json"
  
  experiments:
    - hypothesis: "draft_v1의 톤앤매너로 충분할까?"
      result: "실패 (톤앤매너 점수 5점)"
      learning: "더 친근한 톤 필요 → draft_v2 작성"
  
  key_decisions:
    - "draft_v2에서 '~입니다' 대신 '~해요' 체 사용"
    - "통계 수치(30% 향상)를 도입부에 배치"

# Stage 4: Reflecting (성찰 사고)
reflecting_process:
  stage: "reflecting"
  thinking_type: "비판적 사고 (Critical Thinking)"
  
  activities:
    - name: "품질 체크리스트 검증"
      description: "10개 기준 체크"
      duration_minutes: 10
      passed: 10
      failed: 0
    
    - name: "사실 확인"
      description: "통계 출처 검증"
      duration_minutes: 5
    
    - name: "최종 승인"
      description: "인간 검토 + 승인"
      duration_minutes: 5
  
  tools_used:
    - "/shared/templates/quality_checklist_template.json"
  
  quality_checks:
    - criterion: "톤앤매너 일관성"
      score: 9
      passed: true
    - criterion: "사실 확인 (출처 명시)"
      score: 10
      passed: true
    - criterion: "메시지 명확성"
      score: 9
      passed: true
  
  key_decisions:
    - "승인 완료 → outputs/final.md 이동"
    - "30% 수치 출처: McKinsey 2024 보고서 (각주 추가)"
```

---

## 13.4.3 사고 결과물 기록 (Output)

사고 **결과물**은 "무엇을 생각해냈는가"를 기록합니다. Output 타입은 4가지입니다.

### Output 타입 정의

```yaml
# Output Type 1: Ideas (아이디어 목록)
output_type_ideas:
  type: "ideas"
  use_case: "Planning Stage에서 브레인스토밍 결과"
  
  structure:
    ideas:
      - id: "idea_A"
        title: "..."
        description: "..."
        initial_score: 0.0
      - id: "idea_B"
        title: "..."
  
  example:
    type: "ideas"
    ideas:
      - id: "idea_A"
        title: "AI로 시간 절약"
        description: "반복 작업을 AI에게 위임하여 시간 절약"
        tags: ["productivity", "automation"]
        initial_score: 7.5
      
      - id: "idea_B"
        title: "AI로 생산성 30% 향상"
        description: "McKinsey 2024 보고서 인용, 구체적 수치"
        tags: ["productivity", "data-driven"]
        initial_score: 8.2

# Output Type 2: Decision (의사결정)
output_type_decision:
  type: "decision"
  use_case: "Reasoning Stage에서 최종 선택"
  
  structure:
    selected: "idea_id"
    rationale: "왜 이것을 선택했는가"
    alternatives: []
    confidence: 0.0-1.0
  
  example:
    type: "decision"
    selected: "idea_B"
    rationale:
      summary: "실용성과 신뢰 점수가 가장 높음"
      details:
        - "실용성 8점: 구체적 수치(30%)로 측정 가능"
        - "신뢰 7점: McKinsey 출처 명시"
        - "혁신 8점: 데이터 기반 접근"
    
    core_values_scores:
      practicality: 8
      trust: 7
      innovation: 8
      weighted_score: 7.7
    
    alternatives:
      - id: "idea_A"
        score: 6.8
        reason: "실용성 7점이지만 측정 지표 부족"
      - id: "idea_C"
        score: 7.2
        reason: "혁신 9점으로 높지만 실용성 6점"
    
    confidence: 0.85
    risks:
      - "McKinsey 보고서가 B2B에 특화됨 (일반 직장인과 차이 있을 수 있음)"

# Output Type 3: Plan (실행 계획)
output_type_plan:
  type: "plan"
  use_case: "Experimenting Stage에서 작성 계획"
  
  structure:
    steps: []
    timeline: "..."
    resources: []
  
  example:
    type: "plan"
    goal: "1,000단어 원고 작성"
    steps:
      - step: 1
        action: "도입부 작성 (100단어)"
        duration_minutes: 5
      - step: 2
        action: "본론 작성 (700단어, 3개 섹션)"
        duration_minutes: 20
      - step: 3
        action: "결론 작성 (200단어)"
        duration_minutes: 5
    
    timeline:
      start: "2025-10-13T10:00:00Z"
      end: "2025-10-13T10:30:00Z"
    
    resources:
      - "/shared/templates/message_house_template.json"
      - "/thinking/selection/selected.json"

# Output Type 4: Insight (인사이트)
output_type_insight:
  type: "insight"
  use_case: "Reflecting Stage에서 발견한 학습"
  
  structure:
    findings: []
    implications: []
    next_steps: []
  
  example:
    type: "insight"
    findings:
      - "draft_v1의 톤이 너무 형식적 (점수 5점)"
      - "구체적 수치(30%)가 독자의 관심을 끎"
      - "메시지 하우스 적용 후 구조가 명확해짐"
    
    implications:
      - stage: "planning"
        learning: "타겟 분석 시 톤앤매너 미리 정의 필요"
      
      - stage: "reasoning"
        learning: "실용성 기준에 '측정 가능 지표' 명시 효과적"
      
      - stage: "experimenting"
        learning: "초안은 2개 버전으로 충분 (v3 불필요)"
    
    next_steps:
      - "타겟 분석 템플릿에 '선호 톤앤매너' 항목 추가"
      - "핵심 가치 정의 업데이트 (실용성 = 측정 가능)"
```

---

## 13.4.4 품질 지표 및 메타데이터

사고 산출물의 **품질**을 측정하고, **핵심 가치와의 정렬**을 평가합니다.

### 품질 지표 (Quality Metrics)

```yaml
# 품질 지표 4가지
quality_metrics:
  # 1. 완전성 (Completeness)
  completeness:
    definition: "필요한 정보가 모두 포함되었는가?"
    scale: "0-10"
    thresholds:
      low: "< 5: 핵심 정보 누락"
      medium: "5-7: 기본 정보 포함"
      high: "> 7: 충분히 상세"
    
    evaluation_criteria:
      - "모든 필수 필드가 채워졌는가?"
      - "추가 설명 없이 이해 가능한가?"
      - "참조 자료가 명시되었는가?"
    
    example:
      ideas_output:
        completeness: 8
        reason: "10개 아이디어 모두 title + description + tags 포함"
  
  # 2. 일관성 (Coherence)
  coherence:
    definition: "논리가 일관적이고 모순이 없는가?"
    scale: "0-10"
    thresholds:
      low: "< 5: 모순 있음"
      medium: "5-7: 대체로 일관"
      high: "> 7: 완전히 일관"
    
    evaluation_criteria:
      - "선택 근거가 평가 기준과 일치하는가?"
      - "Stage 간 연결이 논리적인가?"
      - "주장과 증거가 부합하는가?"
    
    example:
      decision_output:
        coherence: 9
        reason: "idea_B 선정 근거(실용성 8점)가 평가 기준과 완벽히 일치"
  
  # 3. 실행 가능성 (Actionability)
  actionability:
    definition: "다음 단계로 바로 진행 가능한가?"
    scale: "0-10"
    thresholds:
      low: "< 5: 추가 정보 필요"
      medium: "5-7: 약간의 보완 필요"
      high: "> 7: 즉시 실행 가능"
    
    evaluation_criteria:
      - "구체적인 next_actions가 정의되었는가?"
      - "필요한 자원이 명시되었는가?"
      - "불확실성이 최소화되었는가?"
    
    example:
      plan_output:
        actionability: 9
        reason: "단계별 작업 + 소요 시간 + 필요 템플릿 모두 명시"
  
  # 4. 정렬성 (Alignment)
  alignment:
    definition: "핵심 가치(2층)와 얼마나 정렬되었는가?"
    scale: "0-10"
    calculation: "weighted_score (실용성 0.4 + 신뢰 0.3 + 혁신 0.3)"
    thresholds:
      low: "< 6: 가치와 불일치"
      medium: "6-8: 가치와 부분 일치"
      high: "> 8: 가치와 완전 일치"
    
    evaluation_criteria:
      - "실용성: 측정 가능한 가치를 제공하는가?"
      - "신뢰: 사실 기반이고 출처가 명확한가?"
      - "혁신: 새로운 관점을 제시하는가?"
    
    example:
      decision_output:
        alignment: 7.7
        breakdown:
          practicality: 8  # 30% 수치로 측정 가능
          trust: 7         # McKinsey 출처
          innovation: 8    # 데이터 기반 접근
        reason: "핵심 가치와 높은 정렬 (목표 6점 이상)"
```

### 메타데이터 구조

```yaml
# thinking_record.json 완전한 메타데이터
complete_metadata:
  # 기본 정보
  cluster_id: "TC001"
  cluster_name: "content_generation"
  stage: "reasoning"
  version: "1.0"
  
  # 작성자 정보
  created_by:
    human: "user@example.com"
    ai: "Claude Sonnet 4"
    collaboration_mode: "AI 초안 + 인간 검토"
  
  # 타임스탬프
  timestamps:
    created_at: "2025-10-13T09:30:00Z"
    updated_at: "2025-10-13T09:45:00Z"
    approved_at: "2025-10-13T09:50:00Z"
  
  # 연결 정보
  references:
    parent_goal: "/goals/q4_content_strategy.json"
    previous_stage: "/thinking/planning/thinking_record.json"
    next_stage: "/thinking/experimenting/thinking_record.json"
    related_clusters: ["TC010", "TC011"]
  
  # 품질 평가
  quality:
    completeness: 8
    coherence: 9
    actionability: 9
    alignment: 7.7
    overall_score: 8.4  # 평균
  
  # 상태
  status: "approved"
  approved_by: "user@example.com"
```

---

## 13.4.5 완전한 예시: 전체 사고 클러스터 기록

하나의 사고 클러스터(TC001)가 4개 Stage를 모두 거쳐 완성되는 전체 과정을 통합 예시로 보여드립니다.

### 통합 예시: TC001 콘텐츠 생성 클러스터

```json
// /thinking_clusters/TC001_content_generation/thinking/planning/thinking_record.json
{
  "metadata": {
    "cluster_id": "TC001",
    "cluster_name": "content_generation",
    "stage": "planning",
    "version": "1.0",
    "created_by": {
      "human": "user@example.com",
      "ai": "Claude Sonnet 4",
      "collaboration_mode": "AI 브레인스토밍 + 인간 선별"
    },
    "timestamps": {
      "created_at": "2025-10-13T09:00:00Z",
      "completed_at": "2025-10-13T09:30:00Z"
    }
  },
  
  "process": {
    "stage": "planning",
    "thinking_type": "발산적 사고 (Divergent Thinking)",
    "activities": [
      {
        "name": "목표 분석",
        "description": "4층 목표를 구체적 질문으로 분해",
        "duration_minutes": 5
      },
      {
        "name": "브레인스토밍",
        "description": "아이디어 10개 생성",
        "duration_minutes": 20,
        "method": "자유 연상 + 경쟁사 분석"
      },
      {
        "name": "타겟 리서치",
        "description": "타겟 페르소나 정의",
        "duration_minutes": 5
      }
    ],
    "tools_used": [
      "/shared/templates/brainstorming_guide.md",
      "/shared/templates/target_analysis_template.json"
    ],
    "key_decisions": [
      "타겟: 30-40대 직장인 (업무 효율성 관심)"
    ]
  },
  
  "output": {
    "type": "ideas",
    "ideas": [
      {
        "id": "idea_A",
        "title": "AI로 시간 절약",
        "description": "반복 작업을 AI에게 위임하여 시간 절약",
        "tags": ["productivity", "automation"],
        "initial_score": 7.5
      },
      {
        "id": "idea_B",
        "title": "AI로 생산성 30% 향상",
        "description": "McKinsey 2024 보고서 인용, 구체적 수치",
        "tags": ["productivity", "data-driven"],
        "initial_score": 8.2
      },
      {
        "id": "idea_C",
        "title": "AI로 창의성 강화",
        "description": "브레인스토밍 파트너로 AI 활용",
        "tags": ["creativity", "innovation"],
        "initial_score": 7.8
      }
      // ... 총 10개 아이디어
    ],
    "target_analysis": {
      "persona": "30-40대 직장인",
      "pain_points": ["시간 부족", "반복 작업"],
      "interests": ["생산성", "측정 가능한 결과"]
    }
  },
  
  "quality": {
    "completeness": 9,
    "coherence": 8,
    "actionability": 8,
    "alignment": 7.8,
    "overall_score": 8.3
  },
  
  "next_actions": [
    "Stage 2 (Reasoning)로 전이",
    "10개 아이디어를 핵심 가치로 평가",
    "최종 1개 선정"
  ]
}

// /thinking_clusters/TC001_content_generation/thinking/reasoning/thinking_record.json
{
  "metadata": {
    "cluster_id": "TC001",
    "stage": "reasoning",
    "version": "1.0",
    "created_at": "2025-10-13T09:30:00Z",
    "completed_at": "2025-10-13T10:00:00Z",
    "references": {
      "previous_stage": "../planning/thinking_record.json"
    }
  },
  
  "process": {
    "stage": "reasoning",
    "thinking_type": "수렴적 사고 (Convergent Thinking)",
    "activities": [
      {
        "name": "핵심 가치 평가",
        "description": "각 아이디어를 실용성/신뢰/혁신 기준으로 평가",
        "duration_minutes": 20,
        "method": "10점 척도 + 근거 작성"
      },
      {
        "name": "최종 선정",
        "description": "idea_B 선정",
        "duration_minutes": 10
      }
    ],
    "tools_used": [
      "/shared/libraries/evaluation_utils.py",
      "/shared/configs/core_values.yaml"
    ],
    "evaluation_criteria": [
      {
        "name": "실용성",
        "weight": 0.4,
        "definition": "측정 가능한 가치 제공"
      },
      {
        "name": "신뢰",
        "weight": 0.3,
        "definition": "사실 기반, 출처 명시"
      },
      {
        "name": "혁신",
        "weight": 0.3,
        "definition": "새로운 관점 제시"
      }
    ],
    "key_decisions": [
      "idea_B 선정 (가중 점수 7.7점)",
      "idea_C는 백업 (혁신 9점으로 높지만 실용성 6점)"
    ]
  },
  
  "output": {
    "type": "decision",
    "selected": "idea_B",
    "rationale": {
      "summary": "실용성과 신뢰 점수가 가장 높음",
      "details": [
        "실용성 8점: 구체적 수치(30%)로 측정 가능",
        "신뢰 7점: McKinsey 출처 명시",
        "혁신 8점: 데이터 기반 접근"
      ]
    },
    "core_values_scores": {
      "practicality": 8,
      "trust": 7,
      "innovation": 8,
      "weighted_score": 7.7
    },
    "alternatives": [
      {
        "id": "idea_A",
        "score": 6.8,
        "reason": "실용성 7점이지만 측정 지표 부족"
      },
      {
        "id": "idea_C",
        "score": 7.2,
        "reason": "혁신 9점으로 높지만 실용성 6점"
      }
    ],
    "confidence": 0.85,
    "risks": [
      "McKinsey 보고서가 B2B에 특화됨"
    ]
  },
  
  "quality": {
    "completeness": 9,
    "coherence": 10,
    "actionability": 9,
    "alignment": 7.7,
    "overall_score": 8.9
  },
  
  "next_actions": [
    "Stage 3 (Experimenting)로 전이",
    "idea_B를 1,000단어 원고로 작성",
    "메시지 하우스 템플릿 적용"
  ]
}

// /thinking_clusters/TC001_content_generation/thinking/experimenting/thinking_record.json
{
  "metadata": {
    "cluster_id": "TC001",
    "stage": "experimenting",
    "version": "1.0",
    "created_at": "2025-10-13T10:00:00Z",
    "completed_at": "2025-10-13T10:45:00Z",
    "references": {
      "previous_stage": "../reasoning/thinking_record.json"
    }
  },
  
  "process": {
    "stage": "experimenting",
    "thinking_type": "생성적 사고 (Generative Thinking)",
    "activities": [
      {
        "name": "초안 작성",
        "description": "idea_B를 1,000단어 원고로 구체화",
        "duration_minutes": 30,
        "iterations": 2
      },
      {
        "name": "메시지 하우스 적용",
        "description": "핵심 메시지 → 근거 3개 → 증거",
        "duration_minutes": 15
      }
    ],
    "tools_used": [
      "/shared/templates/message_house_template.json"
    ],
    "experiments": [
      {
        "hypothesis": "draft_v1의 톤앤매너로 충분할까?",
        "result": "실패 (톤앤매너 점수 5점)",
        "learning": "더 친근한 톤 필요 → draft_v2 작성"
      }
    ],
    "key_decisions": [
      "draft_v2에서 '~입니다' 대신 '~해요' 체 사용",
      "통계 수치(30% 향상)를 도입부에 배치"
    ]
  },
  
  "output": {
    "type": "artifact",
    "artifacts": [
      {
        "file": "../../drafts/draft_v1.md",
        "version": "v1",
        "word_count": 1000,
        "quality_score": 7.0,
        "issues": ["톤앤매너 형식적"]
      },
      {
        "file": "../../drafts/draft_v2.md",
        "version": "v2",
        "word_count": 1020,
        "quality_score": 8.5,
        "improvements": ["친근한 톤", "구조 명확"]
      }
    ],
    "selected_version": "v2",
    "rationale": "v2가 타겟(30-40대 직장인)에게 더 어필"
  },
  
  "quality": {
    "completeness": 9,
    "coherence": 9,
    "actionability": 9,
    "alignment": 8.5,
    "overall_score": 8.9
  },
  
  "next_actions": [
    "Stage 4 (Reflecting)로 전이",
    "품질 체크리스트 검증",
    "사실 확인 (30% 수치 출처)"
  ]
}

// /thinking_clusters/TC001_content_generation/thinking/reflecting/thinking_record.json
{
  "metadata": {
    "cluster_id": "TC001",
    "stage": "reflecting",
    "version": "1.0",
    "created_at": "2025-10-13T10:45:00Z",
    "completed_at": "2025-10-13T11:30:00Z",
    "references": {
      "previous_stage": "../experimenting/thinking_record.json"
    }
  },
  
  "process": {
    "stage": "reflecting",
    "thinking_type": "비판적 사고 (Critical Thinking)",
    "activities": [
      {
        "name": "품질 체크리스트 검증",
        "description": "10개 기준 체크",
        "duration_minutes": 15,
        "passed": 10,
        "failed": 0
      },
      {
        "name": "사실 확인",
        "description": "통계 출처 검증",
        "duration_minutes": 10
      },
      {
        "name": "최종 승인",
        "description": "인간 검토 + 승인",
        "duration_minutes": 20
      }
    ],
    "tools_used": [
      "/shared/templates/quality_checklist_template.json"
    ],
    "quality_checks": [
      {
        "criterion": "톤앤매너 일관성",
        "score": 9,
        "passed": true
      },
      {
        "criterion": "사실 확인 (출처 명시)",
        "score": 10,
        "passed": true,
        "evidence": "McKinsey 2024 보고서 각주 추가"
      },
      {
        "criterion": "메시지 명확성",
        "score": 9,
        "passed": true
      }
    ],
    "key_decisions": [
      "승인 완료 → outputs/final.md 이동",
      "30% 수치 출처: McKinsey 2024 보고서 (각주 추가)"
    ]
  },
  
  "output": {
    "type": "insight",
    "findings": [
      "draft_v1의 톤이 너무 형식적 (점수 5점)",
      "구체적 수치(30%)가 독자의 관심을 끔",
      "메시지 하우스 적용 후 구조가 명확해짐"
    ],
    "implications": [
      {
        "stage": "planning",
        "learning": "타겟 분석 시 톤앤매너 미리 정의 필요"
      },
      {
        "stage": "reasoning",
        "learning": "실용성 기준에 '측정 가능 지표' 명시 효과적"
      },
      {
        "stage": "experimenting",
        "learning": "초안은 2개 버전으로 충분 (v3 불필요)"
      }
    ],
    "next_steps": [
      "타겟 분석 템플릿에 '선호 톤앤매너' 항목 추가",
      "핵심 가치 정의 업데이트 (실용성 = 측정 가능)"
    ],
    "final_output": {
      "file": "../../outputs/final.md",
      "approved": true,
      "approved_by": "user@example.com",
      "approved_at": "2025-10-13T11:30:00Z"
    }
  },
  
  "quality": {
    "completeness": 10,
    "coherence": 10,
    "actionability": 9,
    "alignment": 9.0,
    "overall_score": 9.5
  },
  
  "feedback_for_next_cluster": {
    "successful_practices": [
      "타겟 분석 템플릿 효과적",
      "핵심 가치 평가 시스템 정확 (실제 결과와 상관관계 높음)",
      "메시지 하우스 구조화 유용"
    ],
    "improvements": [
      "Planning에 톤앤매너 사전 정의 추가",
      "Experimenting에서 초안 개수 제한 (최대 2개)"
    ]
  },
  
  "status": "completed"
}
```

---

## 요약

13.4에서는 사고 산출물을 표준화하는 방법을 배웠습니다:

**핵심 내용**:
1. **thinking_record.json**: 사고 과정(process)과 결과(output)를 명확히 분리
2. **Process 기록**: 각 Stage에서 "어떻게 생각했는가" (활동, 도구, 결정사항)
3. **Output 타입 4가지**: ideas, decision, plan, insight
4. **품질 지표**: 완전성, 일관성, 실행 가능성, 정렬성 (각 0-10점)
5. **완전한 예시**: TC001이 4개 Stage를 모두 거쳐 완성되는 전체 기록

**13장 전체 요약**:
- **13.1**: 5층(사고) → 6층(실행) → 파일 시스템 흐름
- **13.2**: 디렉토리 구조 설계 원칙 (격리/공유/명명/산출물)
- **13.3**: thinking_state.json으로 진행 상태 추적
- **13.4**: thinking_record.json으로 사고 내용 표준화

**다음 장**: 14장에서는 이 모든 개념을 통합하여 **실전 사례**를 다룹니다. 콘텐츠 생성, 데이터 분석, 복합 프로젝트 등 3개 사례를 통해 report_kr.md의 6계층 모델 전체(미션 → 핵심 가치 → 비전 → 목표 → 사고 클러스터 → 파일 시스템)가 실무에서 어떻게 작동하는지 보여줍니다.
