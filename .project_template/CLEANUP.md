# .project_template 정비 지침

> **✅ Phase 1 완료!** skeleton 정리 완료 (2025-10-06)
> **✅ Phase 2 완료!** .project_template 자체 정비 완료 (2025-10-06)

---

## 📋 현재 상황

`.project_template/skeleton`에 불필요한 파일들이 추가되어 있습니다.
- **원인**: skeleton은 "빈 골격"이어야 하는데, 완성된 템플릿 파일들이 포함됨
- **문제**: skeleton ≠ 산출물. skeleton은 AI 컨텍스트 한계 극복을 위한 메타 구조일 뿐

---

## 🎯 정리 목표

### skeleton의 역할
```
skeleton = AI의 외부 메모리 시스템 골격
         ≠ 프로젝트 산출물
```

**skeleton에 포함되어야 할 것:**
- 빈 폴더 구조 (`.session/`, `.work/`)
- AI 협업 규칙 (`.instructions.md`)
- 초기화 스크립트 (`setup.sh`)
- 최소한의 템플릿 (`_template.md`)

**skeleton에서 제외되어야 할 것:**
- 상세한 가이드 문서 (README.md들)
- 완성된 템플릿 구조 (template-task/ 폴더 전체)
- 미리 채워진 ROADMAP.md, TODO.md

---

## ✅ Step 1: skeleton 정리 ✅ **완료!**

### 1-1. 이동된 파일들

**모든 파일이 `.trash/skeleton-cleanup-2025-10-06/`로 이동됨:**
```
.trash/skeleton-cleanup-2025-10-06/
├── session-README.md
├── session-template-session.md
├── work-ROADMAP.md
├── work-TODO.md
├── tasks-README.md
└── template-task/
    ├── README.md
    ├── context.md
    ├── plan.md
    └── artifacts/
        └── README.md
```

### 1-2. 정리 후 구조 ✅ **검증 완료!**

```
skeleton/
├── .instructions.md       ← AI 협업 규칙
├── README.md             ← 프로젝트 소개 템플릿
├── setup.sh              ← 초기화 스크립트
│
├── .session/
│   ├── .gitkeep          ← 빈 폴더 유지
│   └── _template.md      ← 세션 템플릿
│
└── .work/
    ├── .gitkeep          ← ✅ 추가됨
    └── tasks/
        ├── .gitkeep
        └── _template/    ← 복잡한 작업 템플릿
            ├── context.md
            └── plan.md
```

---

## 🔄 Step 2: root 프로젝트 구조 변경

### 2-1. 현재 root 프로젝트 상태 파악

```bash
cd /Users/woogis/Workspace/repo/ai-instructions

# 현재 구조 확인
ls -la

# 체크 포인트:
# - .session/ 폴더 있는지?
# - .work/ 폴더 있는지?
# - .instructions.md 있는지?
```

### 2-2. .project_template 적용 여부 판단

**Case A: 아직 적용 안 됨**
```bash
# skeleton을 현재 위치에 적용
cd /Users/woogis/Workspace/repo/ai-instructions

cp -r .project_template/skeleton/.session ./
cp -r .project_template/skeleton/.work ./
cp .project_template/skeleton/.instructions.md ./

# setup.sh 실행
cd .project_template/skeleton
./setup.sh
# → 프로젝트명 입력: "ai-instructions"
```

**Case B: 이미 일부 적용됨**
```bash
# 기존 구조 확인 후 수동 정리
# (다음 세션에서 AI와 함께 판단)
```

### 2-3. 기존 파일들과의 통합

**통합 원칙:**
1. **ROADMAP.md**: 루트의 `ROADMAP.md`와 `.work/ROADMAP.md` 역할 분리
   - 루트 ROADMAP.md: 전체 프로젝트 전략 (book, templates, agents 등 전체)
   - .work/ROADMAP.md: 현재 작업 중인 Phase들

2. **TODO 관리**: 
   - `.cache/todo/` 폴더가 있다면 → `.work/`로 통합 검토
   - 또는 역할 분리: .cache는 분석/컨텍스트, .work는 실행

3. **세션 기록**:
   - 새로 생성되는 `.session/` 폴더 사용
   - 과거 작업 기록은 별도 아카이브

---

## 📝 Step 3: .instructions.md 커스터마이징

### 3-1. 프로젝트 특성 섹션 작성

`.instructions.md` 파일의 "프로젝트별 규칙" 섹션을 채우기:

```markdown
## 🎯 프로젝트별 규칙

### 이 프로젝트 특성
- **타입**: 책 집필 + 템플릿 개발
- **주요 디렉토리**: 
  - `/book`: 책 콘텐츠
  - `/templates`: 재사용 가능한 템플릿들
  - `/agents`: 에이전트 설계 문서
  - `.project_template`: 메타 구조
- **목표**: AI 협업 가이드북 작성 및 템플릿 시스템 구축

### 작업 시 주의사항
- book/ 디렉토리 작업 시 WRITER.md 규칙 준수
- 템플릿 수정 시 backward compatibility 고려
- 용어는 glossary.md 기준 사용
```

### 3-2. 기존 작업 흐름과의 통합

```markdown
## 🔄 기존 프로젝트 파일과의 관계

### book/ 디렉토리
- `book/ROADMAP.md`: book 콘텐츠 중장기 계획
- `book/TODO.md`: book 작업 목록
- → 이것들은 **유지**. .work/는 **전체 프로젝트** 작업 관리용

### .cache/ 디렉토리
- 분석 자료, 컨텍스트 보관
- → 이것도 **유지**. 용도가 다름
```

---

## 🚀 실행 체크리스트

### ✅ Phase 1: Skeleton 정리 (완료!)
- [x] setup.sh 수정 완료
- [x] CLEANUP.md 작성 완료
- [x] 파일들 .trash로 이동 완료
- [x] .gitkeep 파일 추가 완료
- [x] 정리 후 구조 검증 완료

### ✅ Phase 2: .project_template 자체 정비 (완료!)
- [x] structure.md 업데이트 - 현재 구조와 일치
- [x] setup.sh 개선 - OS 호환성, 템플릿 찾기 강화
- [x] skeleton/README.md 경로 문제 해결
- [x] .project_template/README.md 버전 이력 업데이트
- [x] 템플릿 파일들 점검 완료

### Phase 3: Root 프로젝트 적용 (다음 세션)
- [ ] 현재 root 구조 분석
- [ ] .project_template 적용 여부 판단
- [ ] 기존 파일들과 통합 전략 수립
- [ ] .instructions.md 커스터마이징
- [ ] 첫 세션 생성 테스트

### Phase 4: 검증 (다음 세션)
- [ ] AI가 .session 파일 읽고 컨텍스트 복원하는지 테스트
- [ ] ROADMAP → TODO → Session 흐름 작동 확인
- [ ] 새 창 열어도 작업 이어지는지 확인

---

## 📌 중요 원칙 (다시 한 번!)

1. **.project_template = AI 메모리 시스템**
   - 프로젝트 산출물과는 무관
   - 컨텍스트 윈도우 한계 극복용

2. **skeleton = 빈 골격**
   - 상세 가이드 ❌
   - 빈 폴더 + 최소 템플릿 ✅

3. **setup.sh가 템플릿 복사**
   - skeleton에는 포함 안 함
   - docs/, sessions/, tasks/ 에서 가져옴

4. **실제 작업은 project root에서**
   - src/, docs/, book/ 등
   - .session/, .work/는 메타 정보만

---

## 🔗 참고 문서

- `.project_template/README.md`: 전체 시스템 설명
- `.project_template/structure.md`: 디렉토리 구조 상세
- `.project_template/workflows/integration.md`: ROADMAP-TODO-Session 연동

---

## 📋 다음 세션 시작 지침

**다음 세션을 시작할 때:**

1. **이 문서 읽기**
   ```
   사용자: ".project_template/CLEANUP.md 읽어줘"
   ```

2. **Phase 1 완료 확인**
   - ✅ skeleton 구조가 깔끔한지 확인
   - ✅ .trash에 파일들이 있는지 확인

3. **Phase 2 시작**
   ```
   사용자: "이제 root 프로젝트에 .project_template을 적용할 거야"
   AI: [CLEANUP.md의 Step 2 참조하여 진행]
   ```

---

**작성일:** 2025-10-06  
**Phase 1 완료:** 2025-10-06  
**Phase 2 완료:** 2025-10-06  
**작성자:** Claude (Sonnet 4.5)  
**목적:** .project_template 정비 및 root 프로젝트 구조 변경 가이드
