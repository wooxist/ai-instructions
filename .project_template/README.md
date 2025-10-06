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

## 📁 디렉토리 구조

```
your-project/
├── .session/                 # 세션 일기
│   ├── 2025-10-06.md
│   ├── 2025-10-05.md
│   └── active.md            # 현재 활성 세션
│
├── .work/                    # 작업 관리
│   ├── TODO.md              # 할 일 목록
│   ├── ROADMAP.md           # 프로젝트 로드맵
│   ├── tasks/               # 개별 작업 폴더
│   │   ├── task-001/
│   │   │   ├── context.md
│   │   │   └── artifacts/
│   │   └── task-002/
│   └── templates/           # 작업 템플릿
│
├── .instructions.md          # AI 협업 지침 (SSOT)
└── README.md                # 프로젝트 설명
```

---

## 🚀 빠른 시작

### 1. 새 프로젝트 시작

```bash
# 템플릿 복사
cp -r .project_template/structure/* your-project/

# 초기 세팅
cd your-project
./setup.sh  # (템플릿에 포함)
```

### 2. 첫 세션 시작

AI와 대화 시작:
```
사용자: "세션 시작"
AI: [자동으로 .session/YYYY-MM-DD.md 생성]
```

### 3. 작업 추가

**ROADMAP에서 분해:**
```markdown
# .work/ROADMAP.md
- Phase 1: 기초 설계
  → TODO: [ ] 요구사항 분석
  → TODO: [ ] 프로토타입 작성
```

**즉흥 작업:**
```markdown
# .work/TODO.md
- [ ] 버그 수정 (issue #42)
- [ ] 문서 오타 수정
```

---

## 📖 상세 가이드

- [디렉토리 구조 설명](structure.md)
- [세션 워크플로우](workflows/session-workflow.md)
- [작업 관리 워크플로우](workflows/task-workflow.md)
- [ROADMAP-TODO-Session 연동](workflows/integration.md)

---

## 🎨 사용 예시

### 일반적인 하루

**아침 (09:00)**
```
사용자: "이어서"
AI: 
  1. .session/active.md 읽기
  2. "어제 Phase 1 작업했네요"
  3. .session/2025-10-06.md 생성
  4. "오늘은 프로토타입 작성부터 하시겠어요?"
```

**작업 중 (11:00)**
```
사용자: "이 파일 버그 있네. 고쳐줘"
AI:
  1. 버그 수정
  2. .work/TODO.md에 "✓ 버그 수정" 추가
  3. .session/2025-10-06.md 업데이트
```

**저녁 (18:00)**
```
사용자: "오늘은 여기까지"
AI:
  1. .session/2025-10-06.md 종료 시각 기록
  2. "다음 세션에서 할 것" 정리
  3. .work/TODO.md 동기화
```

---

## 🔧 커스터마이징

### 프로젝트 타입별

**책 집필:**
```
.work/
├── chapters/          # 챕터별 작업
└── review/           # 리뷰 작업
```

**소프트웨어 개발:**
```
.work/
├── features/         # 기능별 작업
└── bugs/            # 버그 수정
```

**연구:**
```
.work/
├── experiments/      # 실험별 작업
└── papers/          # 논문 작성
```

---

## 📝 원칙

### 1. SSOT (Single Source of Truth)
- 세션: 시간 순 기록의 SSOT
- TODO: 할 일 목록의 SSOT
- ROADMAP: 전략의 SSOT

### 2. 점진적 캐싱
- 모든 컨텍스트는 파일로 저장
- AI가 언제든 재개 가능
- 채팅창 닫혀도 OK

### 3. 유연성
- 계획된 작업 + 즉흥 작업 모두 수용
- 프로젝트마다 커스터마이징 가능

---

## 🤝 기여

이 템플릿은 계속 발전합니다. 개선 아이디어가 있다면:
1. 실제 프로젝트에서 테스트
2. 피드백 수집
3. 템플릿 업데이트

---

## 📚 버전

- v1.0.0 (2025-10-06): 초기 템플릿 설계
