# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업

## 구조
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
└── 00001-Q/
    └── phase-01/
        └── sprint-01/
            ├── story-01.md
            ├── tasks/     # Story별 고유
            └── workflows/ # Story별 고유
```

## 작업 순서
1. PROGRESS.md → "← 작업중" 찾기
2. 해당 파일 열고 Task 실행
3. 완료 시 PROGRESS.md 체크
4. Commit: [Q1-P1-S1-S2] 타입: 제목
5. 분기 완료 시 → ARCHIVE.md로 이동
