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

**1단계: 현재 위치 파악**
→ `PROGRESS.md` 확인
- Story: `.ai-workspace/00002-Q/phase-01/sprint-01/story-03/`
- Task: `Task 2: 문서 작성`

**2단계: Story 목표 확인**
→ `story-03/story.md` 읽기
- 목표: 무엇을 달성해야 하는가?
- 배경: 왜 이 작업이 필요한가?
- 기대효과: 어떤 개선이 기대되는가?

**3단계: Task 실행**
→ `story.md`의 Workflow 섹션에서 Task 설명 확인
```markdown
### Task 2: 문서 작성
분석 결과를 바탕으로 개선된 문서를 작성합니다.
- 입력: 분석 보고서
- 출력: 개선된 문서
- 완료 기준: 모든 개선 사항 반영
```

→ Task 실행
- 설명대로 작업 수행
- 산출물 생성

**4단계: 마무리**
1. PROGRESS.md 업데이트
   - Task 완료: `Task 3`로 업데이트
   - Story 완료: 다음 Story 경로로 업데이트
2. COMMIT-RULES.md 참고하여 커밋
   - 형식: `[Q2-P1-S1-S3-T2] feat: 문서 개선 완료`

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
- Story 디렉토리 생성 (번호는 01부터 순차적으로)
- `story.md` 파일 생성
  - 목표: 이 Story로 달성할 것
  - 배경: 왜 이 작업이 필요한가
  - Workflow: Task 목록과 각 Task 설명 (대부분 여기서 끝)
- `tasks/` 디렉토리는 매우 복잡한 경우만 생성

**6단계: Workflow 설계** → `story.md` 내
- Task 흐름, 입출력, 의존성, 완료 기준 정의
- 기본적으로 story.md 내에 Workflow 포함
- 재사용 가능한 Workflow는 `library/workflows/`에

**7단계: Task 정의**
- **기본 (99%)**: `story.md` 내 Workflow 섹션에 모든 Task 설명 포함
  ```markdown
  ## Workflow
  
  ### Task 1: 분석
  현재 상태를 분석하고 문제점을 파악합니다.
  - 입력: 기존 문서
  - 출력: 분석 보고서
  
  ### Task 2: 개선
  분석 결과를 바탕으로 개선안을 작성합니다.
  ...
  ```
- **예외 (1%)**: 매우 복잡한 Task만 `story-XX/tasks/task-XX.md`로 분리

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

**99% 경우 - Task 파일 불필요**:
- Workflow 내 Task 설명(1-3문단)으로 충분
- 입력/출력이 명확한 단순 작업
- 한 Story에서만 사용되는 Task

**1% 경우 - Task 파일 생성**:
- 10단계 이상의 복잡한 절차
- 여러 Workflow에서 재사용
- 별도의 상세 기술 문서 필요
- 복잡한 도구 사용법 설명 필요

### Story 디렉토리 구조
```
sprint-01/
├── index.md              # Sprint 계획
├── story-01/             # Story 디렉토리 (필수)
│   ├── story.md          # Story 정의 (목표, 배경, Workflow 포함)
│   └── tasks/            # 복잡한 Task 파일 (선택적, 대부분 불필요)
├── story-02/             # Story 디렉토리 (필수)
│   ├── story.md          # Story 정의
│   └── tasks/            # 복잡한 Task 파일 (선택적)
└── workflows/            # Sprint 공통 Workflow (선택적, 재사용 시)
```

**핵심 원칙**:
- **Story는 반드시 디렉토리로 생성**, 내부에 `story.md` 필수
- **Task 설명은 기본적으로 `story.md` 내 Workflow 섹션에 포함**
- 매우 복잡한 Task만 해당 Story의 `tasks/` 디렉토리에 별도 파일로 생성
- Sprint 전체에서 재사용되는 Workflow는 Sprint 레벨의 `workflows/`에 생성
- 여러 Sprint에서 재사용되는 Workflow는 `library/workflows/`에 생성
- **각 Story는 독립된 디렉토리** - Task 파일이 Story 간 섞이지 않음

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
├── PROGRESS.md              # 현재 작업 위치 (필수 확인)
├── GUIDE.md                 # 작업 가이드 (지금 읽고 있는 파일)
├── ROADMAP.md               # 전체 Quarter 계획 목록
├── COMMIT-RULES.md          # 커밋 메시지 규칙
├── ARCHIVE.md               # 완료된 Quarter 기록
├── library/                 # 재사용 가능한 코드
│   ├── workflows/           # 여러 Sprint에서 재사용하는 Workflow
│   └── tasks/               # 여러 Sprint에서 재사용하는 Task (드물게 사용)
└── 00002-Q/                 # Quarter 2 (현재 진행 중)
    ├── index.md             # Quarter 2 목표와 Phase 분해
    └── phase-01/            # Phase 1 (1개월)
        ├── index.md         # Phase 1 목표와 Sprint 나열
        └── sprint-01/       # Sprint 1 (1주)
            ├── index.md     # Sprint 1 목표와 Story 목록
            ├── story-01/    # Story 1 (1일 작업)
            │   └── story.md # 목표 + 배경 + Workflow (대부분 Task는 여기에)
            ├── story-02/    # Story 2 (1일 작업)
            │   ├── story.md # 목표 + 배경 + Workflow
            │   └── tasks/   # 복잡한 Task만 (드물게 필요)
            └── workflows/   # Sprint 내 여러 Story에서 공유 (선택적)
```

---

## Quarter 관리

- 여러 Quarter 미리 생성 가능
- ROADMAP.md에 전체 분기 계획 나열
- 각 Quarter/index.md에 상세 계획
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성
