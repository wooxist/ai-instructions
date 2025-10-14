# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업
- **AI 우선 명확성**: 모든 지침은 사람이 아닌 AI의 명확한 해석을 최우선으로 한다.

---

## Story → Workflow → Task

**Story**: 목표, 배경, 기대효과, Workflow 참조만  
**Workflow**: Task 목록 + 흐름 + 완료 기준  
**Task**: 목표 + 실행 방법 + 도구 + 체크리스트 + 산출물 (단위 작업, 더 이상 나누지 않음)

---

## 구조 규칙

```
1 Quarter = 3 Phase (각 1개월)
1 Phase = 4 Sprint (각 1주)  
1 Sprint = 최대 5 Story (각 1일)
1 Story = 1 Workflow = N Tasks
```

**핵심**: Task는 재사용 가능하도록 독립적 작성. Workflow는 Task들을 조합.

---

## 디렉토리

```
.ai-workspace/
├── PROGRESS.md              # 현재 작업 위치 (Story + Task)
├── GUIDE.md                 # 이 파일 (작업 가이드)
├── COMMIT-RULES.md          # 커밋 메시지 규칙
├── ARCHIVE.md               # 완료된 작업 기록
├── library/                 # 재사용 가능한 템플릿 모음
│   ├── workflows/           # 재사용 Workflow 모음
│   │   └── templates/       # Workflow 템플릿
│   └── tasks/               # 재사용 Task 모음
│       └── templates/       # Task 템플릿
├── 00001-Q/                 # Quarter 1 (3개월)
│   ├── index.md             # Quarter 계획
│   └── phase-01/            # Phase 1 (1개월)
│       ├── index.md         # Phase 계획
│       └── sprint-01/       # Sprint 1 (1주)
│           ├── index.md     # Sprint 계획
│           ├── story-01.md  # Story (목표)
│           ├── workflows/   # Story별 Workflow
│           │   └── workflow-01.md
│           └── tasks/       # Story별 Task
│               ├── task-01.md
│               └── task-02.md
├── 00002-Q/                 # Quarter 2
└── 00003-Q/                 # Quarter 3
```

---

## 작업 순서

1. PROGRESS.md → 현재 위치 확인
2. Story → 목표 이해
3. Workflow → Task 흐름 파악
4. Task 실행
5. PROGRESS.md 업데이트
6. COMMIT-RULES.md 참고하여 Commit

---

## Quarter 관리

- 여러 Quarter 미리 생성 가능
- 각 Quarter/index.md에 간단한 계획만
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성
