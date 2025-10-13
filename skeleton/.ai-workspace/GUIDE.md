# 가이드

## 핵심 원칙
- **SSOT**: 체크박스는 PROGRESS.md에만
- **SoC**: 각 파일은 하나의 역할만
- **MECE**: 구조는 중복/누락 없이
- **점진적**: 한 Story씩만 작업

## 구조 규칙
```
1 Quarter = 3 Phase (각 1개월)
1 Phase = 4 Sprint (각 1주)  
1 Sprint = 최대 5 Story (각 1일)

Quarter (3개월)
├── Phase-01 (1개월)
│   ├── Sprint-01 (1주)
│   ├── Sprint-02 (1주)
│   ├── Sprint-03 (1주)
│   └── Sprint-04 (1주)
├── Phase-02 (1개월)
│   └── [4개 Sprint]
└── Phase-03 (1개월)
    └── [4개 Sprint]
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
4. Commit: [Q#-P#-S#-S#] 타입: 제목
5. 분기 완료 시 → ARCHIVE.md로 이동
