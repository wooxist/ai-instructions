<!--
AI 지침:
1. 이 파일은 프로젝트 소개 문서입니다
2. 프로젝트 목표와 구조 설명만 포함하세요
3. 작업 규칙이나 진행 상황은 .ai-workspace/ 디렉토리 파일들을 참조하세요
-->

# AI Instructions

> AI 인스트럭션 설계 가이드북 프로젝트

## 🎯 프로젝트 목표
AI와의 효과적인 협업을 위한 체계적인 인스트럭션 설계 방법론을 정립하고, 이를 가이드북으로 문서화하여 배포

## 📦 주요 산출물
1. **가이드북** (`doc/book*/`): AI 인스트럭션 설계 방법론 문서
2. **템플릿** (`skeleton/`): 재사용 가능한 프로젝트 구조 템플릿

## 📁 디렉토리 구조

```
ai-instructions/
├── .instructions.md        # AI 에이전트 작업 지침 엔트리 포인트
├── doc/
│   ├── book1/              # 1권: 기본편
│   └── book2/              # 2권: 조직편
├── skeleton/               # 프로젝트 템플릿
│   └── .ai-workspace/      # 작업 관리 구조
└── .ai-workspace/          # 이 프로젝트의 작업 진행 관리
    ├── PROGRESS.md         # 현재 작업 위치
    ├── GUIDE.md            # 작업 가이드
    ├── ROADMAP.md          # 분기 계획
    ├── COMMIT-RULES.md     # 커밋 규칙
    └── ARCHIVE.md          # 완료 기록
```

## 🚀 시작하기

### AI 작업자용

1. **작업 전**: `.instructions.md` 읽기 (프로젝트 규칙)
2. **작업 방식**: `.ai-workspace/GUIDE.md` 참조 (일하는 방식)
3. **현재 위치**: `.ai-workspace/PROGRESS.md` 확인
4. **커밋 시**: `.ai-workspace/COMMIT-RULES.md` 참조

### 사람 작업자용

- **전체 계획**: `.ai-workspace/ROADMAP.md`
- **현재 진행**: `.ai-workspace/PROGRESS.md`
- **완료 기록**: `.ai-workspace/ARCHIVE.md`

### 가이드북 읽기

- **1권**: `doc/index.md`
- **2권**: `doc/book2/vol-2-index.md`

### 프로젝트 템플릿 사용

- `skeleton/` 디렉토리를 새 프로젝트에 복사
- `.ai-workspace/GUIDE.md`에서 작업 방식 확인
