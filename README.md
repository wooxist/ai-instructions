# AI 인스트럭션 설계 가이드북 (개정판)

## 📌 프로젝트 개요
이 프로젝트는 AI와 협업할 때 필요한 **인스트럭션 설계 원칙**과 **실무 적용 방법**을 정리한 가이드북입니다.  
단순 프롬프트를 넘어, **재현성·협업성·생산성**을 보장하는 "인스트럭션 세트"를 구축하고,  
이를 개인/조직 환경에서 활용할 수 있도록 합니다.

## 🎯 목적
- **인스트럭션 설계하기**: 재현성·협업성·생산성을 보장하는 체계적인 인스트럭션 작성 방법 습득
- **인스트럭션 평가하기**: 기존 인스트럭션의 품질을 평가하고 개선점을 도출하는 방법 제공
- **조직 환경(기업/팀 단위)**: 주니어도 바로 투입 가능하고, 팀이 공유할 수 있는 표준 인스트럭션 구축
- **개인 환경(1인 개발자/스타트업)**: 다양한 전문 영역을 AI와 함께 커버하며, 하나의 서비스/제품을 직접 운영할 수 있도록 지원

## 📚 가이드북 구조
가이드북은 아래 5개 Part로 구성됩니다:

### Part 1: 프롬프트와 인스트럭션의 기초 (1–3장)
- 프롬프트와 인스트럭션의 기본 개념, 좋은 질문/인스트럭션의 원칙

### Part 2: 설계 원칙과 구성 요소 (4–6장)
- 메타 원칙(SSOT/SoC/MECE 등), 역할(에이전트), 입력·출력 설계

### Part 3: 워크플로우, 성능과 평가 (7–9장)
- 기본 워크플로우 패턴, 성능 최적화, 평가·검증

### Part 4: 아키텍처와 설계 패턴 (10–11장)
- 계층적 협업 아키텍처, 상황별 설계 패턴(단일/단위/복합 조직)

### Part 5: 시스템 확장과 운영 (12–15장)
- 도구·플러그인, DSL, 진화·거버넌스, 결론

## 📂 프로젝트 구조
```plaintext
ai-instructions/
├── README.md                    # 프로젝트 개요 (본 파일)
├── ROADMAP.md                   # 프로젝트 통합 로드맵 (중장기 계획)
├── .instructions.md             # AI 에이전트 협업 가이드 (SSOT)
│
├── .cache/                      # 작업 관리 및 캐싱
│   └── todo/
│       ├── TODO.md              # 실행 가능한 작업 목록 (단기)
│       ├── current-phase.md     # 현재 Phase 상세 정보
│       ├── changelog.md         # 작업 변경 이력
│       ├── status.json          # 작업 상태 추적 (자동 생성)
│       ├── analysis/            # 분석 자료 저장
│       │   └── *.md
│       ├── planning/            # 계획 자료 저장
│       │   └── *.md
│       ├── context/             # 작업별 컨텍스트
│       │   └── *.md
│       └── templates/           # 작업 템플릿
│           ├── task-template.md
│           ├── analysis-template.md
│           └── planning-template.md
│
├── agents/                      # 에이전트 정의 (Phase 4-5 완료)
│   ├── creator/
│   │   ├── agent.md            # Creator Agent 정의
│   │   └── prompts/            # 생성용 프롬프트 템플릿
│   └── evaluator/
│       ├── agent.md            # Evaluator Agent 정의
│       └── prompts/            # 평가용 프롬프트 템플릿
│
├── templates/                   # 인스트럭션 작성 템플릿 (Phase 3 완료)
│   ├── simple-task.md          # 단순 작업용
│   ├── medium-complexity.md    # 중간 복잡도
│   └── complex-workflow.md     # 복잡한 워크플로우
│
├── examples/                    # 실제 사용 예시 (Phase 3 완료)
│   ├── good/                   # 좋은 지침 예시
│   └── improved/               # 개선된 지침 예시
│
└── book/                        # 가이드북 콘텐츠 (Phase 1 완료)
    ├── ROADMAP.md              # root ROADMAP 리다이렉트
    ├── WRITER.md               # 집필 가이드 (상세)
    ├── index.md                # 전체 목차
    ├── glossary.md             # 용어집
    ├── practice-guide.md       # 실습 과제 모음
    ├── visual-style-guide.md   # 시각 자료 스타일 가이드
    │
    ├── 00-preface.md           # 서문
    ├── 01-introduction.md      # 1장: 프롬프트와 인스트럭션 이해하기
    ├── 02-questions.md         # 2장: 질문 설계하기
    ├── 03-good-instructions.md # 3장: 좋은 인스트럭션
    ├── 04-meta-principles.md   # 4장: 인스트럭션 설계의 메타 원칙
    ├── 05-agent-constraints.md # 5장: 역할(Agent)과 제약(Constraint) 설계
    ├── 06-input-output.md      # 6장: 입력과 출력 설계
    ├── 07-process-workflow.md  # 7장: 기본 워크플로우 패턴과 처리
    ├── 08-performance.md       # 8장: 성능 최적화
    ├── 09-productivity.md      # 9장: 인스트럭션의 평가와 검증
    ├── 10-advanced-collaboration-architectures.md # 10장: 고급 협업 아키텍처
    ├── 11-1-single-agent.md    # 11장 1부: 단일 에이전트 설계
    ├── 11-2-unit-organization.md # 11장 2부: 단위 조직 설계
    ├── 11-3-complex-organization.md # 11장 3부: 복합 조직 설계
    ├── 12-tools.md             # 12장: 도구(Tools)와 플러그인 활용
    ├── 13-workflow-as-code.md  # 13장: 도메인 특화 언어(DSL) 설계
    ├── 14-evolution.md         # 14장: 살아있는 시스템 - 인스트럭션의 진화와 관리
    └── 15-conclusion.md        # 15장: 결론 - AI 시대의 새로운 일잘법
```

## 🚀 현재 상태 (2025년 10월 6일)

- ✅ **Phase 1 완료**: 가이드북 초판 (15개 장)
- ✅ **Phase 3 완료**: 프로젝트 구조 확장
- ✅ **Phase 4-5 완료**: Creator & Evaluator 에이전트 개발
- 🔄 **Phase 2 진행 중**: 학습 경험 개선 (2025년 10-12월)

**다음 마일스톤**: Phase 2.1 (학습 곡선 완화) - 2025년 11월 목표

## 📖 내용 참조
- 가이드북 전체 내용은 [book/](book/) 디렉토리에 있습니다
- 전체 목차와 내용 요약은 [book/index.md](book/index.md)에서 확인하실 수 있습니다
- 프로젝트 로드맵은 [ROADMAP.md](ROADMAP.md)에서 확인하실 수 있습니다

## 🤝 AI 협업 방식

이 프로젝트는 **점진적 캐싱(Progressive Caching)** 방식으로 AI와 협업합니다:

1. **작업 컨텍스트 유지**: 각 작업의 진행 상황을 `.cache/todo/context/`에 저장
2. **상태 추적**: `status.json`으로 모든 작업 상태를 추적
3. **변경 이력 관리**: `changelog.md`로 모든 변경 사항 기록
4. **템플릿 활용**: 일관된 작업 문서 생성

자세한 내용은 [.instructions.md](.instructions.md)를 참조하세요.

## 💬 토론 및 문의
이 프로젝트에 대한 질문, 제안 또는 토론은 언제든지 환영합니다.  
궁금한 점이나 논의하고 싶은 주제가 있으시면 언제든지 연락해 주세요.

📧 이메일: iam@daewook.me

## 📄 라이센스
이 프로젝트는 MIT 라이센스로 제공됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
