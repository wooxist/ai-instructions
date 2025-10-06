# [프로젝트명]

[프로젝트 한 줄 설명]

## 🎯 프로젝트 목표

[이 프로젝트의 최종 목표를 작성하세요]

## 📁 프로젝트 구조

```
your-project/
├── .session/          # 작업 세션 일기
├── .work/            # 작업 관리
│   ├── ROADMAP.md    # 프로젝트 로드맵
│   ├── TODO.md       # 할 일 목록
│   └── tasks/        # 복잡한 작업들
├── .instructions.md  # AI 협업 지침
└── [프로젝트 파일들]
```

## 🚀 시작하기

### 1. 초기 설정

```bash
# 새 프로젝트 디렉토리에 skeleton 파일들을 복사한 후:
cp -r .project_template/skeleton/* .
cp -r .project_template/skeleton/.* . 2>/dev/null || true

# setup.sh 실행
./setup.sh
```

이 명령어는:
- 첫 세션 파일 생성
- ROADMAP/TODO 초기화
- 기본 구조 확인

### 2. AI와 첫 세션 시작

```
사용자: "세션 시작"
AI: [자동으로 오늘 날짜 세션 파일 생성 및 작업 시작]
```

## 📚 참고 문서

- [ROADMAP](.work/ROADMAP.md) - 프로젝트 전체 로드맵
- [TODO](.work/TODO.md) - 현재 할 일
- [워크플로우 가이드](../.project_template/workflows/integration.md)

## 🤝 AI 협업

이 프로젝트는 AI와의 체계적인 협업을 위해 설계되었습니다.

- **세션 관리**: 매일의 작업을 `.session/` 에 기록
- **작업 추적**: `.work/TODO.md` 로 할 일 관리
- **전략 계획**: `.work/ROADMAP.md` 로 전체 로드맵 관리

자세한 내용은 [.instructions.md](.instructions.md)를 참고하세요.
