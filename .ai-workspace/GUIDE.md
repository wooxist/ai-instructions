# Skeleton 사용 가이드

> **이 파일은 Skeleton 사용법입니다** (모든 프로젝트 공통)  
> 개별 프로젝트 규칙 → `.instructions.md`

---

## ⚡ 빠른 참조

### 읽을 파일 (순서대로)
1. `.instructions.md` ← 프로젝트 규칙
2. `PROGRESS.md` ← 현재 Story
3. Story 파일 ← 오늘 작업

### 작업 흐름
```
읽기 → 실행 → 체크 → Commit
```

### 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 파일별 역할 분리
- **MECE**: 중복 없음, 누락 없음
- **점진적**: 한 Story씩만

---

## 📁 구조

```
.ai-workspace/
├── PROGRESS.md          ← 유일한 체크박스 (SSOT)
├── GUIDE.md            ← 이 파일
├── COMMIT-RULES.md     ← Commit 형식
├── library/            ← 재활용
│   ├── tasks/
│   └── workflows/
├── 00001-Q/            ← 1분기
│   ├── index.md
│   ├── phases/phase-01.md
│   ├── sprints/phase-01/sprint-01.md
│   └── stories/phase-01/sprint-01/story-01.md
└── 00002-Q/            ← 2분기
```

---

## 🎯 계층 (MECE)

```
Quarter (3개월)
  ↓
Phase (1개월, 3개/분기)
  ↓
Sprint (1주, 4-5개/Phase)
  ↓
Story (1일, 최대 5개/Sprint)
  ↓
Task (단위 작업)
```

---

## 🔄 작업 절차

### 1-3: 읽기
```
1. .instructions.md 읽기
2. PROGRESS.md 읽기 → 현재 Story 확인
3. Story 파일 읽기 → Task 확인
```

### 4-6: 실행
```
4. library/ 확인 (재활용 가능한 것)
5. Task 실행 (Workflow 따라)
6. 산출물 생성 (src/ or doc/)
```

### 7-8: 완료
```
7. PROGRESS.md 체크박스 ☑
8. Git commit [Q#-P#-S#-S#] 타입: 제목
```

---

## 📝 핵심 가치의 적용

### SSOT (Single Source of Truth)
- ✅ PROGRESS.md에만 체크박스 존재
- ❌ 다른 파일에 중복된 정보 금지

### SoC (Separation of Concerns)
- `.instructions.md` → 프로젝트 규칙만
- `GUIDE.md` → Skeleton 사용법만
- `COMMIT-RULES.md` → Commit 규칙만
- 각각 독립적으로 관리

### MECE (Mutually Exclusive, Collectively Exhaustive)
- Quarter → Phase → Sprint → Story → Task
- 모든 작업 = Story에 포함
- 중복 없고, 누락 없이

### 점진적/단계적 계획 처리
- **한 번에 한 Story만 작업**
- Story → Task → Workflow 순서대로
- 완료 후 다음 단계

---

## 📚 Library

### Task
- 사용: `library/tasks/task-*.md`
- 템플릿: `library/tasks/templates/task-template.md`

### Workflow
- 사용: `library/workflows/workflow-*.md`
- 템플릿: `library/workflows/templates/workflow-template.md`

---

## ⚠️ 금지

- ❌ PROGRESS.md 외 다른 곳에 체크박스
- ❌ 여러 Story 동시 작업
- ❌ Story 완료 전 다음 Story 시작
- ❌ GUIDE.md 수정 (개별 규칙은 .instructions.md에)

---

## 📁 파일명

| 타입 | 형식 | 예시 |
|------|------|------|
| Quarter | `00001-Q/` | 00001-Q |
| Phase | `phase-01.md` | phase-01 |
| Sprint | `sprint-01.md` | sprint-01 |
| Story | `story-01.md` | story-01 |
| Task | `task-[이름].md` | task-read |
| Workflow | `workflow-[이름].md` | workflow-api |

---

## 🚀 시작

```
1. .instructions.md 확인 (프로젝트 규칙)
2. PROGRESS.md 확인 (현재 위치)
3. Story 읽기
4. 작업 시작!
```
