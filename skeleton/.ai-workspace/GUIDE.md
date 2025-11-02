<!--
AI 지침:
1. 이 파일은 작업 가이드입니다
2. 내용을 수정할 때 전체 구조와 섹션을 유지하세요
3. 핵심 원칙과 Story-Workflow-Task 구조는 변경하지 마세요
-->

# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업
- **AI 우선 명확성**: 모든 지침은 사람이 아닌 AI의 명확한 해석을 최우선으로 한다.

---

## 구조 개요

```
Quarter (3개월) → Phase (1개월) → Sprint (1주) → Story (1일) → Workflow → Task
```

**실행 단위:**
- **Story**: 목표, 배경, 기대효과, Workflow 참조
- **Workflow**: Task 목록 + 흐름 + 완료 기준 (library에서 재사용 가능)
- **Task**: 실행 방법 + 산출물 (Workflow 내 설명으로 충분, 별도 파일 선택적)

---

## 일하는 방식

### 작업하기 (Executing)

**1단계: 어디서부터?**
→ `PROGRESS.md` 확인
- 현재 Story 경로
- 현재 Task 이름

**2단계: 무엇을?**
→ `Story/story.md` 읽기
- 목표: 무엇을 달성할 것인가
- 배경: 왜 필요한가
- 기대효과: 무엇이 개선되는가

**3단계: 어떻게?**
→ `Workflow` 확인
- Task 흐름과 순서
- 각 Task의 입출력
- 완료 기준

→ `Task` 실행
- Workflow 내 Task 설명 참조
- 실행 방법 따라 작업
- 산출물 생성

**4단계: 마무리**
1. PROGRESS.md 업데이트 (다음 Task로)
2. COMMIT-RULES.md 참고하여 Commit

---

### 계획하기 (Planning)

**하향식 분해 (Top-Down):**

**1단계: Quarter 목표 정의** → `ROADMAP.md`
- 3개월 동안 달성할 최종 목표
- 간략하고 명확하게 작성

**2단계: Phase 목표 분해** → `Quarter/index.md`
- Quarter 목표를 3개의 Phase로 분해
- 각 Phase는 1개월 단위

**3단계: Sprint 목표 구체화** → `Phase/index.md`
- Phase 목표를 4개의 Sprint로 구체화
- 각 Sprint는 1주 단위

**4단계: Story 도출** → `Sprint/index.md`
- Sprint 목표를 달성하기 위한 Story 나열
- 권장 5개 이하, 실제 작업량에 맞게 조정 가능

**5단계: Story 디렉토리 생성** → `Sprint/story-XX/`
- Story 디렉토리 생성
- `story.md` 파일 생성 (목표, 배경, Workflow)
- 필요시 `tasks/` 디렉토리 생성

**6단계: Workflow 설계** → `story.md` 내
- Task 흐름, 입출력, 의존성, 완료 기준 정의
- 기본적으로 story.md 내에 Workflow 포함
- 재사용 가능한 Workflow는 `library/workflows/`에

**7단계: Task 정의**
- **기본**: `story.md` 내 Workflow에 Task 설명 포함
- **선택적**: Task가 복잡한 경우만 `story-XX/tasks/`에 별도 파일

---

### 계획 조정하기 (Adjusting)

**Story 단위 조정** (가장 유연)
- Story 추가/삭제/재배치 가능
- Sprint 목표 범위 내에서 자유롭게 조정

**Sprint/Phase 조정** (목표 유지)
- 목표는 그대로 두되 Story 재배치로 대응
- 불가피한 경우만 목표 수정

**Quarter 목표 변경** (전체 재검토)
- Phase/Sprint/Story 전체 영향도 검토
- ROADMAP.md 업데이트 필수

---

## 파일 구조 최적화

### Workflow 재사용 원칙
- **반복되는 프로세스**: `library/workflows/`에 생성
- **Story 전용 프로세스**: `Story/workflows/`에 생성
- **참조 방식**: Story에서 상대 경로로 Workflow 참조

### Task 파일 생성 기준
- **생성 불필요**: Workflow 내 설명으로 충분한 경우 (대부분)
- **생성 권장**: 
  - Task가 매우 복잡하여 별도 문서가 필요한 경우
  - 여러 Workflow에서 재사용되는 경우
  - 상세한 체크리스트나 도구 설명이 필요한 경우

### Story 디렉토리 구조
```
sprint-01/
├── index.md              # Sprint 계획
├── story-01/             # Story 디렉토리
│   ├── story.md          # Story 정의 (목표, 배경, Workflow)
│   └── (tasks/)          # 이 Story의 Task 파일 (선택적)
├── story-02/             # Story 디렉토리
│   ├── story.md          # Story 정의
│   └── (tasks/)          # 이 Story의 Task 파일 (선택적)
└── (workflows/)          # Sprint 공통 Workflow (선택적)
```

**핵심 원칙**:
- **Story는 디렉토리**, 내부에 `story.md` 필수
- Task는 대부분 `story.md` 내 Workflow에 포함
- 복잡한 Task만 해당 Story의 `tasks/` 디렉토리에 별도 파일
- Sprint 공통 Workflow는 Sprint 레벨의 `workflows/`에
- **Story 간 Task 파일이 섞이지 않음** (각 Story의 tasks/ 분리)

---

## 필요할 때만 참조

### ROADMAP.md
- **용도**: 전체 분기 계획 조망
- **언제**: Quarter 전체 계획 확인할 때

### ARCHIVE.md
- **용도**: 완료된 Quarter 기록
- **언제**: Quarter 완료 시 기록

### COMMIT-RULES.md
- **용도**: 커밋 메시지 형식
- **언제**: 커밋 직전에만 참조
- **형식**: `[Q#-P#-S#-S#-T#] 타입: 제목`

### library/
- **용도**: 재사용 가능한 Workflow/Task 모음
- **언제**: 
  - 비슷한 작업이 반복될 때
  - 다른 Story에서 같은 Workflow가 필요할 때
  - Story 작성 시 재사용 Workflow 참조할 때

---

## 디렉토리 구조 (참고)

```
.ai-workspace/
├── PROGRESS.md              # 현재 작업 위치
├── GUIDE.md                 # 이 파일
├── ROADMAP.md               # 전체 분기 계획
├── COMMIT-RULES.md          # 커밋 규칙
├── ARCHIVE.md               # 완료 기록
├── library/                 # 재사용 템플릿
│   ├── workflows/           # 공통 Workflow
│   └── tasks/               # 공통 Task (선택적)
└── 00001-Q/                 # Quarter 1
    ├── index.md             # Quarter 계획
    └── phase-01/            # Phase 1
        ├── index.md         # Phase 계획
        └── sprint-01/       # Sprint 1
            ├── index.md     # Sprint 계획
            ├── story-01/    # Story 디렉토리
            │   ├── story.md # Story 정의
            │   └── tasks/   # Story 전용 Task (선택적)
            ├── story-02/    # Story 디렉토리
            │   ├── story.md # Story 정의
            │   └── tasks/   # Story 전용 Task (선택적)
            └── workflows/   # Sprint 공통 (선택적)
```

---

## Quarter 관리

- 여러 Quarter 미리 생성 가능
- ROADMAP.md에 전체 분기 계획 나열
- 각 Quarter/index.md에 상세 계획
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성
