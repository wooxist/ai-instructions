# AI 협업 프로젝트 템플릿

이 템플릿은 AI와 함께 작업하는 모든 프로젝트의 기반이 됩니다.

## 🎯 핵심 개념

### 3-레이어 구조

```
ROADMAP (전략 레이어)
   ↓ 분해
TODO (실행 레이어)
   ↑ 즉흥 추가
   ↓ 실제 작업
Session (기록 레이어)
```

**ROADMAP**: 프로젝트의 큰 그림 (몇 주~몇 달)
**TODO**: 이번 주에 할 구체적 작업들 (계획 + 즉흥)
**Session**: 오늘 실제로 한 것 (시간 순 기록)

---

## 🚀 빠른 시작 (3단계면 끝!)

### Step 1: 복사
```bash
cp -r .project_template/skeleton/* your-new-project/
cd your-new-project
```

### Step 2: 초기화
```bash
chmod +x setup.sh
./setup.sh
# → 프로젝트명 입력
# → 자동으로 첫 세션 생성
# → 준비 완료!
```

### Step 3: AI와 작업 시작
```
사용자: "세션 시작"
AI: [자동으로 작업 제안]
```

**끝!** 더 이상 아무것도 필요 없습니다. 😊

---

## 📁 skeleton 디렉토리 구조

```
skeleton/                    # 이것만 복사하면 됩니다!
│
├── .session/               # 세션 일기
│   └── .gitkeep
│
├── .work/                  # 작업 관리
│   ├── ROADMAP.md         # 로드맵 (템플릿 포함)
│   ├── TODO.md            # TODO (템플릿 포함)
│   └── tasks/             # 복잡한 작업 폴더
│       └── .gitkeep
│
├── .instructions.md        # AI 협업 지침 (완성)
├── README.md              # 프로젝트 README (완성)
└── setup.sh               # 자동 설정 스크립트
```

---

## ✨ setup.sh가 해주는 것

실행하면 자동으로:
- ✅ 프로젝트명 입력받기
- ✅ 오늘 날짜로 첫 세션 파일 생성
- ✅ ROADMAP/TODO에 프로젝트명 채우기
- ✅ 모든 YYYY-MM-DD를 오늘 날짜로 치환
- ✅ 준비 완료 메시지 출력

**3분이면 프로젝트 시작 가능!**

---

## 🎨 실제 예시 보기

`example_project/` 디렉토리에 실제 동작 예시가 있습니다:

```bash
cd example_project
cat .work/ROADMAP.md        # 웹 앱 Phase 1-4 계획
cat .work/TODO.md           # 실제 작업 항목
cat .session/2025-10-06.md  # 첫 세션 기록
```

---

## 📖 상세 가이드

### 필수 문서
- [structure.md](structure.md) - 디렉토리 구조 설명
- [workflows/integration.md](workflows/integration.md) - ROADMAP-TODO-Session 연동 방법
- [workflows/maintenance.md](workflows/maintenance.md) - 커지는 파일 정리/아카이브 운영

### skeleton 내부 파일들
- `.instructions.md` - AI가 읽는 협업 규칙
- `.work/ROADMAP.md` - Phase 계획 템플릿
- `.work/TODO.md` - 작업 목록 템플릿
- `README.md` - 프로젝트 설명 템플릿

---

## 🔄 일반적인 하루

**아침 (09:00)**
```
사용자: "이어서"

AI:
1. 어제 세션 읽기
2. "어제 XXX 했네요"
3. 오늘 세션 생성
4. TODO 확인 후 작업 제안
```

**작업 중 (11:00)**
```
사용자: "버그 발견했어. 고쳐줘"

AI:
1. 버그 수정
2. TODO에 즉흥 작업 추가
3. 세션 파일 자동 업데이트
```

**저녁 (18:00)**
```
사용자: "오늘은 여기까지"

AI:
1. 세션 종료 시각 기록
2. "다음에 할 것" 정리
3. TODO 동기화
```

---

## 💡 핵심 원칙

### 1. 간단함
- skeleton만 복사
- setup.sh만 실행
- AI와 대화 시작

### 2. 자동화
- 세션 자동 생성
- TODO 자동 업데이트
- 컨텍스트 자동 저장

### 3. 유연성
- 계획된 작업 + 즉흥 작업
- 프로젝트별 커스터마이징
- 복잡도 기반 차등 관리

---

## 🎯 프로젝트 타입별 사용

### 소프트웨어 개발
```bash
cp -r .project_template/skeleton/* my-app/
cd my-app && ./setup.sh
# → Phase: 설계, 개발, 테스트, 배포
```

### 책 집필
```bash
cp -r .project_template/skeleton/* my-book/
cd my-book && ./setup.sh
# → Phase: 초고, 수정, 리뷰, 출판
```

### 데이터 분석
```bash
cp -r .project_template/skeleton/* my-analysis/
cd my-analysis && ./setup.sh
# → Phase: 수집, 전처리, 분석, 시각화
```

---

## 🚨 주의사항

### 필수 확인
- [ ] setup.sh 실행 전 프로젝트명 생각해두기
- [ ] setup.sh 실행 후 ROADMAP.md 커스터마이징
- [ ] .instructions.md "프로젝트별 규칙" 작성

### Git 사용 시
```bash
# .gitignore 권장
.session/*.md    # 개인 작업 일기
```

---

## 🧰 유지보수 도구(대형화 방지)

파일이 커지면 다음 스크립트를 프로젝트 루트에서 실행하세요.

```bash
# 완료된 TODO를 주간 아카이브로 이동
./.project_template/tools/rollover.sh todo

# 14일 지난 세션을 월별 폴더로 이동하고 INDEX 생성
./.project_template/tools/rollover.sh sessions --days 14

# ROADMAP Phase를 파일로 분리하고 색인 생성
./.project_template/tools/rollover.sh roadmap

# 간단한 크기 점검
./.project_template/tools/rollover.sh check
```

자세한 정책은 [workflows/maintenance.md](workflows/maintenance.md) 참고.

---

## 🤔 FAQ

### Q: skeleton만 있으면 되나요?
**A**: 네! skeleton 디렉토리만 복사하면 모든 준비 완료입니다.

### Q: 템플릿을 수정하고 싶은데요?
**A**: skeleton 안의 파일들을 직접 수정하세요. 다음 프로젝트부터 적용됩니다.

### Q: setup.sh 없이 수동으로 하려면?
**A**: 
1. 첫 세션 파일 직접 생성 (`.session/YYYY-MM-DD.md`)
2. ROADMAP/TODO에서 [프로젝트명]과 YYYY-MM-DD 수동 치환

### Q: AI가 세션을 안 읽으면?
**A**: ".instructions.md 확인해줘"라고 요청하세요.

---

## 📈 버전

- **v1.1.0** (2025-10-06): Skeleton 정비 완료 ✅
  - Phase 1 완료: 불필요한 파일들 `.trash/`로 이동
  - skeleton을 빈 골격으로 정리 (AI 컨텍스트 관리 최적화)
  - structure.md 현재 구조와 일치하도록 업데이트
  - setup.sh OS 호환성 개선 (macOS/Linux)
  - 템플릿 찾기 로직 강화

- **v1.0.0** (2025-10-06): 초기 릴리스
  - skeleton 구조 완성
  - setup.sh 자동화
  - example_project 예시 포함
  - 완전한 문서화

---

## 🎉 시작하기

```bash
# 지금 바로 시작해보세요!
cp -r .project_template/skeleton/* my-awesome-project/
cd my-awesome-project
chmod +x setup.sh
./setup.sh

# AI와 대화 시작
# "세션 시작" 입력
```

**3분이면 준비 완료!** 🚀

행복한 AI 협업 되세요! 🤝
