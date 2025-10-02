# AI 인스트럭션 프로젝트 로드맵

## 📅 Phase 1: 가이드북 완성 (완료)

### Part 1: 프롬프트와 인스트럭션의 기초 (1-3장)
- [x] 1장: 프롬프트와 인스트럭션 이해하기 (v1-released)
- [x] 2장: 질문 설계하기 (v1-released)
- [x] 3장: 좋은 인스트럭션 (v1-released)

### Part 2: 인스트럭션 시스템 설계와 평가 (4-9장)
- [x] 4장: 인스트럭션 설계의 메타 원칙 (v1-released)
- [x] 5장: 역할(Agent)과 제약(Constraint) 설계 (v1-released)
- [x] 6장: 입력과 출력 설계 (v1-released)
- [x] 7장: 처리 방법과 워크플로우 설계 (v1-released)
- [x] 8장: 인스트럭션 시스템의 성능 최적화 (v1-released)
- [x] 9장: 인스트럭션의 평가와 검증 (v1-released)

### Part 3: 인스트럭션 시스템의 확장과 발전 (10-13장)
- [x] 10장: 상황별 인스트럭션 설계 패턴 예제 (v1-released)
- [x] 11장: 인스트럭션 시스템을 위한 도구와 프레임워크 (v1-released)
- [x] 12장: 살아있는 시스템: 인스트럭션의 진화와 관리 (v1-released)
- [x] 13장: 인스트럭션의 미래: 자율적인 에이전트 시스템을 향하여 (v1-released)

## 📅 Phase 2: 프로젝트 구조 확장

### 디렉토리 구조 설계 및 생성
```plaintext
ai-instructions/
├── book/                    # 가이드북 콘텐츠 (Phase 1)
├── agents/                  # 에이전트 정의 (Phase 2)
│   ├── creator/            # 지침 생성 에이전트
│   │   ├── agent.md        # 에이전트 역할 및 제약
│   │   └── prompts/        # 프롬프트 템플릿
│   └── evaluator/          # 지침 평가 에이전트
│       ├── agent.md
│       └── prompts/
├── templates/              # 지침 작성 템플릿 (Phase 2)
│   ├── simple-task.md
│   ├── medium-complexity.md
│   └── complex-workflow.md
└── examples/               # 실제 사용 예시 (Phase 2)
    ├── good/              # 좋은 지침 예시
    └── improved/          # 개선된 지침 예시
```

**작업 항목:**
- [ ] 에이전트 디렉토리 구조 설계 및 생성 (agents/creator, agents/evaluator)
- [ ] 지침 작성 템플릿 생성 (templates/ 디렉토리)
- [ ] 좋은 지침 예시 및 개선 사례 추가 (examples/ 디렉토리)

## 📅 Phase 3: 지침 생성 에이전트 개발

### Creator Agent 구현
**목적:** book/ 내용을 기반으로 효과적인 인스트럭션을 자동 생성

**기능:**
- [ ] 사용자 요구사항 분석 (복잡도 수준 판단)
- [ ] 적절한 템플릿 선택
- [ ] 원칙 기반 지침 초안 생성
- [ ] 역할(Agent) 및 제약(Constraint) 자동 설정
- [ ] 입력/출력 형식 정의
- [ ] 처리 방법 및 워크플로우 구성

**산출물:**
- [ ] `agents/creator/agent.md` - 에이전트 정의
- [ ] `agents/creator/prompts/` - 프롬프트 템플릿 세트
- [ ] 사용 가이드 및 예시

## 📅 Phase 4: 지침 평가 에이전트 개발

### Evaluator Agent 구현
**목적:** 기존 인스트럭션의 품질을 평가하고 개선 방향 제시

**기능:**
- [ ] 인스트럭션 구조 분석
- [ ] 원칙 준수 여부 검증
  - 명확성(Clarity)
  - 구체성(Specificity)
  - 목표 지향성(Goal-oriented)
  - 일관성(Consistency)
- [ ] 복잡도 수준 적합성 평가
- [ ] 개선점 도출 및 제안
- [ ] Before/After 비교 리포트 생성

**산출물:**
- [ ] `agents/evaluator/agent.md` - 에이전트 정의
- [ ] `agents/evaluator/prompts/` - 평가 프롬프트 세트
- [ ] 평가 기준 체크리스트
- [ ] 사용 가이드 및 예시

## 📅 Phase 5: 통합 및 검증

### 시스템 통합
- [ ] Creator ↔ Evaluator 연동 워크플로우
- [ ] 피드백 루프 구현 (생성 → 평가 → 개선)
- [ ] CLI 도구 개발 (선택사항)

### 검증 및 테스트
- [ ] 다양한 도메인에서 테스트
- [ ] 실제 사용 사례 수집
- [ ] 에이전트 성능 평가 및 개선

### 문서화
- [ ] 전체 시스템 사용 가이드
- [ ] 베스트 프랙티스 문서
- [ ] FAQ 및 트러블슈팅

## 📅 Phase 6: 커뮤니티 및 확장

### 오픈소스화
- [ ] 기여 가이드라인 작성
- [ ] 이슈 템플릿 및 PR 템플릿
- [ ] 코드 리뷰 프로세스 정립

### 확장 기능
- [ ] 도메인별 특화 템플릿 추가
- [ ] 다국어 지원
- [ ] MCP 통합 (13장 내용 기반)
- [ ] 웹 인터페이스 개발 (선택사항)

---

## 🎯 현재 상태
**Phase 1** 완료. **Phase 2** 진행 예정.

## 📝 업데이트 이력
- 2025-10-01: 로드맵 초안 작성
