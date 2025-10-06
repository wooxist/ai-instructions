# 디렉토리 구조 상세 설명

이 문서는 AI 협업 프로젝트의 표준 디렉토리 구조를 설명합니다.

---

## 📁 전체 구조

```
your-project/
│
├── .session/                      # 세션 관리 (일기)
│   ├── 2025-10-06.md             # 오늘 세션
│   ├── 2025-10-05.md             # 어제 세션
│   ├── 2025-10-04.md             # 그저께 세션
│   └── _template.md              # 세션 템플릿
│
├── .work/                         # 작업 관리
│   │
│   ├── ROADMAP.md                # 프로젝트 로드맵
│   ├── TODO.md                   # 할 일 목록
│   │
│   ├── tasks/                    # 복잡한 작업 폴더
│   │   ├── task-001-feature-x/
│   │   │   ├── context.md       # 배경, 목표
│   │   │   ├── plan.md          # 상세 계획
│   │   │   └── artifacts/       # 산출물
│   │   │
│   │   └── task-002-bug-fix/
│   │       └── ...
│   │
│   └── [작업 폴더들...]
│
├── .instructions.md              # AI 협업 지침 (SSOT)
│
├── README.md                     # 프로젝트 소개
│
└── [프로젝트 파일들]             # 실제 코드, 문서 등
    ├── src/
    ├── docs/
    └── ...
```

---

## 📂 각 디렉토리 설명

### `.session/` - 세션 일기

**목적**: 시간 순으로 실제 작업 기록

**파일 명명 규칙**: `YYYY-MM-DD.md`

**내용**:
- 오늘 한 것 (체크리스트)
- 다음에 할 것
- 중요 결정사항
- 발견한 문제/아이디어
- 관련 TODO 링크

**특징**:
- 하루 1파일
- 삭제하지 않음 (히스토리 보존)
- _template.md는 새 세션 생성용 템플릿

**사용 예시**:
```bash
# 새 세션 시작
cp .session/_template.md .session/2025-10-06.md

# 최신 세션 확인 (AI가 자동으로 수행)
ls -t .session/*.md | head -1
```

---

### `.work/` - 작업 관리

**목적**: 할 일 관리 및 프로젝트 계획

#### `ROADMAP.md`
- 프로젝트 전체 로드맵
- Phase 1, 2, 3... 큰 그림
- 몇 주~몇 달 단위
- 변경 빈도: 낮음

#### `TODO.md`
- 이번 주 할 일 목록
- ROADMAP에서 분해된 작업
- 즉흥적으로 발견한 작업
- 변경 빈도: 매일

#### `tasks/` 디렉토리
복잡한 작업(> 2시간)은 별도 폴더로 관리

**언제 사용?**
- 작업이 여러 세션에 걸침
- 상세 계획 필요
- 여러 파일 산출물
- 독립적인 컨텍스트 필요

**폴더 구조**:
```
task-XXX-작업명/
├── context.md           # 왜 필요한지, 배경
├── plan.md             # 어떻게 할지, 단계
└── artifacts/          # 산출물
    ├── design.md
    ├── code/
    └── tests/
```

**명명 규칙**:
- `task-001-jwt-implementation`
- `task-042-database-migration`
- 번호 3자리 + 짧은 설명

---

### `.instructions.md` - AI 협업 지침

**목적**: AI가 반드시 읽어야 할 프로젝트 룰

**내용**:
- 세션 관리 규칙
- TODO 관리 규칙
- 작업 프로세스
- 문서 동기화 규칙
- 프로젝트별 커스텀 룰

**SSOT**: 모든 AI 행동의 단일 진실 공급원

**특징**:
- 프로젝트마다 커스터마이징
- AI가 가장 먼저 읽는 파일
- 사용자가 직접 편집 가능

---

## 🔄 파일 라이프사이클

### 세션 파일
```
생성 (아침) → 업데이트 (실시간) → 종료 (저녁) → 보존 (영구)
```

### TODO 항목
```
추가 (계획 or 즉흥) → 진행 (세션에서) → 완료 (체크) → 아카이브
```

### Task 폴더
```
생성 (복잡한 작업 시작) → 작업 (여러 세션) → 완료 → 정리 or 보존
```

---

## 📊 용량 관리

### 예상 용량
```
세션: 1일 = 1-5KB
     1년 = 365-1800KB (약 2MB)

TODO: 항상 < 100KB

Tasks: 작업당 1-10MB
       10개 작업 = 10-100MB
```

### 정리 주기
- **세션**: 절대 삭제 안 함 (압축은 가능)
- **TODO**: 주간 단위로 완료 항목 아카이브
- **Tasks**: 완료 후 6개월~1년 보존, 이후 압축

---

## 🎨 커스터마이징

### 프로젝트 타입별 구조

**책 집필 프로젝트**:
```
.work/
├── chapters/           # 챕터별 관리
│   ├── ch01/
│   └── ch02/
└── reviews/           # 리뷰 작업
```

**소프트웨어 개발**:
```
.work/
├── features/          # 기능별
├── bugs/             # 버그별
└── releases/         # 릴리스별
```

**연구 프로젝트**:
```
.work/
├── experiments/       # 실험별
├── papers/           # 논문별
└── data/             # 데이터셋
```

---

## 🚀 초기 세팅

### 1. 템플릿 복사
```bash
cp -r .project_template/structure/* your-project/
```

### 2. 디렉토리 생성
```bash
mkdir -p .session
mkdir -p .work/tasks
```

### 3. 파일 복사
```bash
cp .project_template/skeleton/.session/_template.md .session/
cp .project_template/tasks/TODO.template.md .work/TODO.md
cp .project_template/docs/ROADMAP.template.md .work/ROADMAP.md
```

### 4. 초기 파일 작성
```bash
# 첫 세션 생성
cp .session/_template.md .session/$(date +%Y-%m-%d).md
```

---

## 📝 모범 사례

### ✅ 좋은 예
```
✓ 세션 파일은 매일 새로 생성
✓ TODO는 완료 시 체크 + 세션 링크
✓ 복잡한 작업은 task 폴더로
✓ ROADMAP은 분기별 업데이트
```

### ❌ 나쁜 예
```
✗ 세션 파일을 덮어쓰기
✗ TODO 없이 바로 작업
✗ 모든 작업을 task 폴더로 (과도한 구조화)
✗ ROADMAP을 매일 수정
```

---

## 🔍 트러블슈팅

### Q: 세션 파일이 너무 많아요
**A**: 월별 폴더로 정리
```
.session/
├── 2025-10/
│   ├── 2025-10-01.md
│   └── ...
└── 2025-09/
```

### Q: TODO가 너무 길어요
**A**: 완료 항목을 별도 파일로
```
.work/
├── TODO.md           # 현재 작업만
└── archive/
    └── TODO-2025-Q3.md
```

### Q: task 폴더가 너무 많아요
**A**: 완료된 것은 아카이브로
```
.work/
├── tasks/           # 진행 중
└── tasks-archive/   # 완료된 것
```

---

이 구조를 따르면 어떤 규모의 프로젝트도 체계적으로 관리할 수 있습니다.
