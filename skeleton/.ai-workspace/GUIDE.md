# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업
- **AI 우선 명확성**: 모든 지침은 사람이 아닌 AI의 명확한 해석을 최우선으로 한다.

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
├── PROGRESS.md
├── ARCHIVE.md
├── GUIDE.md
├── COMMIT-RULES.md
├── library/
│   ├── workflows/templates/  # 재사용 Workflow
│   └── tasks/templates/      # 재사용 Task
├── 00001-Q/
│   └── phase-01/
│       └── sprint-01/
│           ├── story-01.md        # 목표
│           ├── workflows/
│           │   └── workflow-01.md # Task 흐름
│           └── tasks/
│               ├── task-01.md     # 실행 단위
│               ├── task-02.md
│               └── task-03.md
```

---

## 작업 순서

1. PROGRESS.md → 현재 위치 확인
2. Story → Workflow 확인
3. Workflow → Task 입출력 확인
4. Task 실행
5. PROGRESS.md 업데이트
6. Commit: `[Q#-P#-S#-S#-T#] 타입: 제목`

---

## Quarter 관리

- 여러 Quarter 미리 생성 가능
- 각 Quarter/index.md에 간단한 계획만
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성
