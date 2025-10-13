# 가이드

## 작업 순서
1. PROGRESS.md → "← 작업중" 찾기
2. 해당 파일 열고 Task 실행
3. 완료 시 PROGRESS.md 체크
4. Commit: [Q1-P1-S1-S2] 타입: 제목

## 구조
```
.ai-workspace/
├── PROGRESS.md         # 진행상황
├── GUIDE.md           # 이 파일
├── COMMIT-RULES.md    # 커밋 규칙
├── library/           # 재사용 가능
│   ├── tasks/
│   └── workflows/
└── 00001-Q/
    └── phase-01/
        └── sprint-01/
            ├── story-01.md
            ├── tasks/     # Story별 고유
            └── workflows/ # Story별 고유
```

## 원칙
- 체크박스: PROGRESS.md만
- 작업: 한 Story씩만
