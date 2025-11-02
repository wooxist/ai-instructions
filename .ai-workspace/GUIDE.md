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
Quarter (3개월) → Phase (1개월) → Sprint (1주) → Story (1일) → Workflow → Task (단위작업)
```

**작업 규모:**
- **Task**: 단위 작업 (시간~반나절)
- **Story**: 1일 작업 (여러 Task 포함)
- **Sprint**: 1주 작업 (5개 내외의 Story)
- **Phase**: 1개월 작업 (5개 내외의 Sprint)
- **Quarter**: 3개월 작업 (5개 내외의 Phase)

**실행 단위:**
- **Story**: 목표, 배경, 기대효과, Workflow 포함
- **Workflow**: Task 목록 + 흐름 + 완료 기준
- **Task**: 실행 방법 + 산출물

---

## 일하는 방식

### 작업하기 (Executing)

**1단계: 현재 위치 파악**
→ `PROGRESS.md` 확인
- Story 경로 확인 (예: `.ai-workspace/00002-Q/phase-01/sprint-01/story-01/`)
- 현재 Task 확인 (예: `Task 2: 문서 작성`)

**2단계: Story 목표 확인**
→ 해당 `story-XX/story.md` 읽기
- 목표: 무엇을 달성해야 하는가?
- 배경: 왜 이 작업이 필요한가?
- 기대효과: 어떤 개선이 기대되는가?

**3단계: Task 실행**
→ `story.md`의 Workflow 섹션에서 Task 파일 경로 확인
→ 해당 Task 파일 (`tasks/task-XX.md`) 열어서 상세 내용 확인
→ Task 파일의 지침대로 작업 수행
- 입력물 확인
- 실행 방법 따라 작업
- 산출물 생성
- 완료 기준 충족 확인

**4단계: 마무리**
1. PROGRESS.md 업데이트
   - Task 완료: 다음 Task 번호로 업데이트
   - Story 완료: 다음 Story 경로로 업데이트
2. COMMIT-RULES.md 참고하여 커밋
   - 형식: `[Q#-P#-S#-S#-T#] 타입: 제목`

---

### 계획하기 (Planning)

**하향식 분해 (Top-Down):**

**1단계: Quarter 목표 정의** → `ROADMAP.md`
- 3개월 동안 달성할 최종 목표
- 간략하고 명확하게 작성

**2단계: Phase 목표 분해** → `00XXX-Q/index.md`
- Quarter 목표를 5개 내외의 Phase로 분해 (보통 3-5개)
- 각 Phase는 1개월 단위

**3단계: Sprint 목표 구체화** → `phase-XX/index.md`
- Phase 목표를 5개 내외의 Sprint로 구체화 (보통 4-5개)
- 각 Sprint는 1주 단위

**4단계: Story 도출** → `sprint-XX/index.md`
- Sprint 목표를 달성하기 위한 Story 나열
- **5개 내외로 제한** (최대 7개 초과 금지)
- 각 Story는 1일 작업량으로 설계
- Story가 너무 많으면 Sprint를 분할 고려

**5단계: Story 작성** → `sprint-XX/story-XX/story.md`
- Story 디렉토리 생성 (번호는 01부터 순차적으로)
- `story.md` 파일 생성:
  - 목표: 이 Story로 달성할 것
  - 배경: 왜 이 작업이 필요한가
  - Workflow: Task 목록과 참조

**6단계: Workflow 설계**
- `story.md` 내 Workflow 섹션에 Task 목록과 흐름 정의
- **재사용 필요 시**:
  - Sprint 내 공유: `sprint-XX/workflows/`에 생성
  - 여러 Sprint 공유: `library/workflows/`에 생성

**7단계: Task 파일 생성**
- 각 Task는 별도 파일로 생성: `story-XX/tasks/task-XX.md`
- Task 번호는 01부터 순차적으로
- 각 Task는 단위 작업 (몇 시간~반나절)
- Story당 보통 3-5개의 Task
- `story.md`의 Workflow 섹션에서 Task 파일 참조
  ```markdown
  ## Workflow
  
  ### Task 1: 분석
  → `tasks/task-01.md`
  
  ### Task 2: 개선
  → `tasks/task-02.md`
  ```

- Task 파일 내용:
  ```markdown
  # Task 1: 분석
  
  ## 목적
  현재 상태를 분석하고 문제점을 파악합니다.
  
  ## 입력
  - 기존 문서
  
  ## 출력
  - 분석 보고서
  
  ## 실행 방법
  1. 문서 구조 분석
  2. 문제점 식별
  3. 개선 방안 도출
  
  ## 완료 기준
  - 모든 섹션 분석 완료
  - 문제점 목록 작성
  ```

---

### 계획 조정하기 (Adjusting)

**Story 단위 조정** (가장 유연)
- Story 추가/삭제/재배치 가능
- Sprint 목표 범위 내에서 조정
- **Sprint당 5개 내외 유지 필수**
- 초과 시 다음 Sprint로 이동 또는 Story 분할

**Sprint/Phase 조정** (목표 유지)
- 목표는 그대로 두되 Story 재배치로 대응
- 불가피한 경우만 목표 수정

**Quarter 목표 변경** (전체 재검토)
- Phase/Sprint/Story 전체 영향도 검토
- ROADMAP.md 업데이트 필수

---

## 파일 구조

### 표준 디렉토리 구조
```
.ai-workspace/
├── PROGRESS.md              # 현재 작업 위치 (필수 확인)
├── GUIDE.md                 # 작업 가이드 (이 파일)
├── ROADMAP.md               # 전체 Quarter 계획 목록
├── COMMIT-RULES.md          # 커밋 메시지 규칙
├── ARCHIVE.md               # 완료된 Quarter 기록
├── library/                 # 재사용 가능한 코드
│   ├── workflows/           # 여러 Sprint에서 재사용하는 Workflow
│   └── tasks/               # 여러 Sprint에서 재사용하는 Task (드물게 사용)
└── 00XXX-Q/                 # Quarter (예: 00002-Q)
    ├── index.md             # Quarter 목표와 Phase 분해
    └── phase-XX/            # Phase (예: phase-01)
        ├── index.md         # Phase 목표와 Sprint 나열
        └── sprint-XX/       # Sprint (예: sprint-01)
            ├── index.md     # Sprint 목표와 Story 목록
            ├── story-XX/    # Story 디렉토리 (필수)
            │   ├── story.md # Story 정의 (필수)
            │   └── tasks/   # Task 파일들 (필수)
            │       ├── task-01.md
            │       └── task-02.md
            └── workflows/   # Sprint 내 공유 Workflow (선택적)
```

### 파일 생성 원칙

**Story 파일 (필수)**
- 모든 Story는 디렉토리로 생성 (`story-XX/`)
- 각 Story 디렉토리에 `story.md` 필수
- 번호는 01부터 순차적으로

**Task 파일 (필수)**
- 모든 Task는 별도 파일로 생성: `story-XX/tasks/task-XX.md`
- 번호는 01부터 순차적으로
- `story.md`에서는 Task 파일 참조만

**Workflow 파일 (재사용 시)**
- Sprint 내 재사용: `sprint-XX/workflows/`
- 여러 Sprint 재사용: `library/workflows/`
- 기본은 `story.md` 내 포함

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

## Quarter 관리

- 여러 Quarter 미리 생성 가능
- ROADMAP.md에 전체 분기 계획 나열
- 각 Quarter/index.md에 상세 계획
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성

### 작업량 가이드라인
- **Quarter**: 5개 내외의 Phase (3-5개월 작업)
- **Phase**: 5개 내외의 Sprint (1개월 작업)
- **Sprint**: 5개 내외의 Story (1주 작업)
- **Story**: 3-5개의 Task (1일 작업)
- **Task**: 단위 작업 (시간~반나절)

⚠️ **주의**: Sprint에 Story를 무한정 추가 금지! 5개 내외 유지 필수
