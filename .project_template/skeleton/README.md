# [프로젝트명]

[프로젝트 한 줄 설명]

## 🎯 프로젝트 목표

[이 프로젝트의 최종 목표를 작성하세요]

## 📁 프로젝트 구조

```
your-project/
├── ROADMAP.md        # 프로젝트 로드맵 (root)
├── .session/          # 작업 세션 일기
├── .work/            # 작업 관리
│   ├── TODO.md       # 할 일 목록
│   └── tasks/        # 복잡한 작업들
├── .instructions.md  # AI 협업 지침
└── [프로젝트 파일들]
```

## 🚀 시작하기 (2가지 방법)

### 방법 1: 자동 설정 (setup.sh 사용)

```bash
# skeleton 복사 후 setup.sh 실행
chmod +x setup.sh
./setup.sh
# → 프로젝트명 입력하면 자동 설정 완료!
```

### 방법 2: 수동 설정 (setup.sh 없이)

```bash
# 1. skeleton 폴더 복사
cp -r .project_template/skeleton/* .
cp -r .project_template/skeleton/.* . 2>/dev/null || true

# 2. 템플릿 파일들 수정
# - [프로젝트명] → 실제 프로젝트명으로 변경
# - YYYY-MM-DD → 오늘 날짜로 변경

# 3. 첫 세션 생성
cp .session/_template.md .session/$(date +%Y-%m-%d).md
```

**둘 다 똑같이 작동합니다!**

### 2. AI와 첫 세션 시작

```
사용자: "세션 시작"
AI: [자동으로 오늘 날짜 세션 파일 생성 및 작업 시작]
```

## 📚 참고 문서

- [ROADMAP](ROADMAP.md) - 프로젝트 전체 로드맵
- [TODO](.work/TODO.md) - 현재 할 일
- [워크플로우 가이드](../.project_template/workflows/integration.md)

## 🤝 AI 협업

이 프로젝트는 AI와의 체계적인 협업을 위해 설계되었습니다.

- **세션 관리**: 매일의 작업을 `.session/` 에 기록
- **작업 추적**: `.work/TODO.md` 로 할 일 관리
- **전략 계획**: `.work/ROADMAP.md` 로 전체 로드맵 관리

자세한 내용은 [.instructions.md](.instructions.md)를 참고하세요.
