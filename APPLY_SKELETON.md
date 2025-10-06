# 🚀 Skeleton 구조 적용 지침

이 문서는 `.project_template/skeleton` 구조를 현재 프로젝트 root에 적용하는 지침입니다.

## 📋 적용 전 확인사항

현재 위치: `/Users/woogis/Workspace/repo/ai-instructions/`

**이미 있는 파일들:**
- `ROADMAP.md` - 전체 프로젝트 로드맵 (유지)
- 기타 프로젝트 파일들 (book/, templates/, agents/ 등)

**새로 생성할 구조:**
- `.session/` - 작업 일기 폴더
- `.work/` - 작업 관리 폴더
- `.instructions.md` - AI 협업 지침

## 🔧 작업 순서

### 1단계: 기존 파일 백업 (필요시)

```bash
# 기존 파일이 있다면 백업
[ -f ".instructions.md" ] && cp .instructions.md .instructions-backup.md
[ -f "TODO.md" ] && cp TODO.md TODO-backup.md
```

### 2단계: 필수 디렉토리 생성

```bash
# 세션 관리 폴더
mkdir -p .session

# 작업 관리 폴더
mkdir -p .work/tasks/_template
```

### 3단계: skeleton에서 파일 복사

```bash
# AI 협업 지침
cp .project_template/skeleton/.instructions.md ./

# 세션 템플릿
cp .project_template/skeleton/.session/_template.md .session/

# TODO 파일
cp .project_template/skeleton/.work/TODO.md .work/

# 복잡한 작업 템플릿
cp .project_template/skeleton/.work/tasks/_template/context.md .work/tasks/_template/
cp .project_template/skeleton/.work/tasks/_template/plan.md .work/tasks/_template/
```

### 4단계: 첫 세션 파일 생성

```bash
# 오늘 날짜로 세션 파일 생성
TODAY=$(date +%Y-%m-%d)
cp .session/_template.md .session/${TODAY}.md

# 세션 파일 초기화 (수동 편집)
# - YYYY-MM-DD를 오늘 날짜로 변경
# - HH:MM를 현재 시간으로 변경
# - 타입을 "프로젝트 구조 정비"로 설정
```

### 5단계: .instructions.md 커스터마이징

`.instructions.md` 파일을 열어 "프로젝트별 규칙" 섹션을 다음으로 수정:

```markdown
## 🎯 프로젝트별 규칙

### 이 프로젝트 특성
- **타입**: 책 집필 + 템플릿 개발 + 에이전트 설계
- **주요 디렉토리**: 
  - `/book`: AI 협업 가이드북 콘텐츠
  - `/templates`: 재사용 가능한 템플릿들
  - `/agents`: 에이전트 설계 문서
  - `/.project_template`: 메타 프로젝트 구조
- **목표**: AI 협업 가이드북 작성 및 템플릿 시스템 구축

### 작업 시 주의사항
- ROADMAP.md는 root에 있음 (전체 프로젝트 계획)
- TODO.md는 .work/에 있음 (현재 할 일)
- book/ 디렉토리 작업 시 WRITER.md 규칙 준수
- 템플릿 수정 시 backward compatibility 고려
- 용어는 glossary.md 기준 사용
```

### 6단계: TODO.md 초기화

`.work/TODO.md` 파일을 열어 현재 작업으로 업데이트:

```markdown
# TODO

**프로젝트**: ai-instructions
**마지막 업데이트**: 2025-10-06

---

## 🎯 이번 주 우선순위 (Top 3)

1. [ ] book 챕터 5-6 작성
2. [ ] .project_template Phase 3 진행
3. [ ] example_project 검증

---

## 📋 ROADMAP 연계 작업 (../ROADMAP.md 참고)

### Phase 2.3 - 템플릿 시스템 완성
- [x] skeleton 구조 정비 (Phase 1-2 완료)
- [x] root 프로젝트 적용
- [ ] example_project 테스트
- [ ] 문서화 완성

---

## ⚡ 즉흥 / 긴급 작업

- [ ] [작업 중 발견한 것들 추가]

---

## ✅ 완료된 작업

### 2025-10-06
- [x] .project_template Phase 1-2 완료 - [세션](../.session/2025-10-06.md)
- [x] skeleton 구조 root 적용 - [세션](../.session/2025-10-06.md)
```

## ✅ 최종 검증 체크리스트

작업 완료 후 다음 항목들을 확인:

- [ ] **폴더 구조 확인**
  ```bash
  ls -la .session/
  ls -la .work/
  ls -la .work/tasks/_template/
  ```

- [ ] **파일 존재 확인**
  - [ ] `.instructions.md` 존재 및 커스터마이징
  - [ ] `.session/2025-10-06.md` 존재
  - [ ] `.work/TODO.md` 존재
  - [ ] `ROADMAP.md`는 root에 그대로 유지

- [ ] **AI 테스트**
  - [ ] "세션 시작"이라고 말했을 때 AI가 반응
  - [ ] AI가 `.instructions.md` 내용 인지
  - [ ] AI가 오늘 세션 파일 확인
  - [ ] AI가 TODO와 ROADMAP 참조

## 📌 중요 참고사항

### 파일 위치
- **ROADMAP.md**: root에 위치 (이동하지 않음!)
- **TODO.md**: `.work/` 폴더 안에 위치
- **.session/**: git에 포함 (팀 협업 시 공유)

### 일상 사용 패턴
```
아침: "세션 시작" → AI가 어제 작업 이어받음
작업 중: "TODO 업데이트" → AI가 .work/TODO.md 수정
저녁: "오늘 마무리" → AI가 세션 종료 기록
```

### 작업 완료 후 효과
- 새 창에서도 "세션 시작"만 하면 자동으로 작업 연결
- 더 이상 "컨텍스트 설정" 요청 불필요
- 모든 작업이 체계적으로 기록되고 추적됨

## 🎯 다음 단계

1. **이 지침대로 작업 실행**
2. **테스트**: "세션 시작"으로 AI 반응 확인
3. **일상 사용 시작**: 매일 세션으로 작업 관리

---

**작성일**: 2025-10-06  
**목적**: skeleton 구조를 root 프로젝트에 적용  
**결과**: AI가 작업을 자동으로 이어받을 수 있는 구조 완성
