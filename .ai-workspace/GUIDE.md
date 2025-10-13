# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업
- **AI 우선 명확성**: 모든 지침은 사람이 아닌 AI의 명확한 해석을 최우선으로 한다.

## 작업 구성 요소
모든 작업은 **Story → Workflow → Task** 계층 구조를 따릅니다.
- **Story (목표):** 해결할 문제나 요구사항을 정의합니다. (What/Why)
- **Workflow (프로세스):** Story를 완수하기 위해 필요한 **Task들의 순서와 흐름**을 설계합니다. (How-To Plan)
- **Task (단위 작업):** Workflow의 각 단계를 구성하는 **실행 가능한 최소 단위**입니다. (How-To-Do)

## 구조 규칙
```
1 Quarter = 3 Phase (각 1개월)
1 Phase = 4 Sprint (각 1주)  
1 Sprint = 최대 5 Story (각 1일)
```

## 디렉토리 구조
```
.ai-workspace/
├── PROGRESS.md         # 현재 진행만
├── ARCHIVE.md         # 완료된 분기
├── GUIDE.md           # 이 파일
├── COMMIT-RULES.md    # 커밋 규칙
├── library/           # 재사용 가능
│   ├── tasks/
│   │   └── templates/
│   └── workflows/
│       └── templates/
├── 00001-Q/           # 현재 Quarter
│   ├── index.md       # 간단한 계획
│   └── phase-01/
│       └── sprint-01/
│           ├── story-01.md
│           ├── tasks/     # Story별 고유
│           └── workflows/ # Story별 고유
└── 00002-Q/           # 다음 Quarter (계획)
    └── index.md       # 간단한 계획만
```

## 작업 순서
1. PROGRESS.md → "← 작업중" 찾기
2. 해당 파일 열고 Task 실행
3. 완료 시 PROGRESS.md 체크
4. Commit: [Q#-P#-S#-S#] 타입: 제목
5. 분기 완료 시 → ARCHIVE.md로 이동

## Quarter 관리
- 여러 Quarter 미리 생성 가능
- 각 Quarter/index.md에 간단한 계획만
- 진행률은 PROGRESS.md에서만 관리
- Quarter 시작 시 Phase/Sprint/Story 구조 생성
