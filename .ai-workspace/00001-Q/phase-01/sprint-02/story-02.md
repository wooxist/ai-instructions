# Story 02: 2권 통합 목차 생성 및 메인 목차 업데이트

**목표:** 2권의 전체 구조를 명확히 하는 통합 목차를 생성하고, 메인 목차에 2권 섹션을 추가하여 독자가 전체 가이드북을 쉽게 탐색할 수 있도록 합니다.

**배경:**
- 현재 2권(`doc/book2/`)에는 28개의 파일이 있지만 통합 목차가 없음
- `doc/index.md`는 1권만 포함하고 있어 2권 접근이 어려움
- 2권의 Part 구조(Part 0, 4, 5)가 불명확함

**기대 효과:**
- 독자가 2권의 전체 구조를 한눈에 파악 가능
- 1권과 2권의 연결 관계 명확화
- 학습 경로 가이드 제공

---

## Workflow

이 Story는 **Workflow 01**을 따릅니다:

📋 **[Workflow 01: 2권 목차 생성 및 통합](workflows/workflow-01.md)**

**흐름**: 분석 → 생성 → 통합 → 검증

---

## Tasks

Workflow 01에 정의된 Task 목록:

### ✅ Task 01: 2권 파일 분석 (완료)
- **파일:** `tasks/task-01-analyze.md`
- **산출물:** 파일 맵핑 테이블 (`task-01-result.md`)

### 🔄 Task 02: 2권 통합 목차 생성 (현재)
- **파일:** `tasks/task-02-create-index.md`
- **산출물:** `doc/book2/vol-2-index.md`

### ⏳ Task 03: 메인 목차 업데이트
- **파일:** `tasks/task-03-update-main.md`
- **산출물:** 업데이트된 `doc/index.md`

### ⏳ Task 04: 검증 및 정리
- **파일:** `tasks/task-04-verify.md`
- **산출물:** 검증 완료 체크리스트

---

## 완료 기준

- [ ] `doc/book2/vol-2-index.md` 파일이 생성됨
- [ ] 2권의 모든 챕터가 목차에 포함됨
- [ ] `doc/index.md`에 2권 섹션이 추가됨
- [ ] 모든 내부 링크가 정상 작동함
- [ ] AI 사고 생태계 다이어그램이 포함됨
- [ ] 학습 경로 가이드가 명확함

---

## 참고 자료

- `workflows/workflow-01.md`: 전체 프로세스 설계
- `doc/book2/vol-2-part-0-preface.md`: 2권 서문
- `doc/book2/vol-2-part-4-intro.md`: Part 4 도입부
- `doc/book2/vol-2-part-5-intro.md`: Part 5 도입부
- `doc/index.md`: 1권 목차 (참고용)
