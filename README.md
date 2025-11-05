# AI 인스트럭션 설계 가이드북

> AI와의 효과적인 협업을 위한 체계적인 인스트럭션 설계 방법론

## 📖 프로젝트 소개

이 프로젝트는 개인 또는 소규모 팀에서 단일 AI 에이전트를 효과적으로 설계하고 활용하는 방법론을 정립하고, 이를 가이드북 형태로 제공합니다. 프롬프트 기초부터 체계적인 인스트럭션 설계, 그리고 여러 에이전트를 협업시키는 워크플로우 구축까지, AI를 믿을 수 있는 업무 파트너로 만드는 실용적인 방법을 다룹니다.

**프로젝트 목표**
- 코딩 없이 AI를 활용하는 체계적인 방법론 제시
- 일반 사용자가 바로 적용 가능한 실용적 가이드 작성
- 프롬프트부터 구조화된 인스트럭션 설계까지 단계적 학습 제공

---

## 📚 콘텐츠 구성

### Part 1: 프롬프트와 인스트럭션의 기초 (1-3장) ✅ 완성

AI와 명확하게 소통하기 위한 기본기를 다룹니다. 좋은 질문을 설계하는 방법부터, 재사용 가능한 지시서인 '인스트럭션'을 만드는 4가지 핵심 원칙과 8가지 구성 요소를 제공합니다.

### Part 2: 설계 원칙과 구성 요소 (4-8장) 🚧 작업 중

'문제 → 전략 → 전술'의 흐름에 따라 체계적인 인스트럭션 시스템을 설계하는 방법을 다룹니다.

- **문제 (4장)**: AI 협업 시 발생하는 현실적인 제약들
- **전략 (5장)**: 제약을 극복하기 위한 시스템 설계 원칙
- **전술 (6-8장)**: 입출력 설계, 에이전트 설계, 워크플로우 설계

---

## 🚀 가이드북 읽기

- **[서문: AI에게 '제대로' 일 시키는 법](doc/book1/vol-1-part-0-preface.md)**
- **[1권 전체 목차 바로가기](doc/book1/vol-1-index.md)**

### Part 1 목차

* [1장. 좋은 프롬프트의 원칙](doc/book1/vol-1-part-1-chapter-01.md) **★☆☆**
* [2장. 질문 설계하기](doc/book1/vol-1-part-1-chapter-02.md) **★☆☆**
* [3장. 효과적인 지시 작성의 기본 원칙](doc/book1/vol-1-part-1-chapter-03.md) **★★☆**

---

## 🔧 프로젝트 템플릿 사용하기

이 프로젝트의 작업 관리 시스템을 다른 프로젝트에도 적용할 수 있습니다.

### 템플릿 폴더 복사하기

```bash
# project-template 폴더를 새 프로젝트에 복사
cp -r project-template/. /path/to/new-project/

# 또는 특정 부분만 복사
cp -r project-template/.ai-workspace /path/to/new-project/
cp project-template/.instructions.md /path/to/new-project/
```

### 템플릿에 포함된 내용

**작업 관리 시스템** (`.ai-workspace/`)
- `GUIDE.md` - 작업 가이드 및 원칙
- `PROGRESS.md` - 현재 작업 위치 추적
- `ROADMAP.md` - 전체 분기 계획
- `ARCHIVE.md` - 완료된 분기 기록
- `COMMIT-RULES.md` - 커밋 메시지 규칙
- `library/` - 재사용 가능한 Workflow/Task 템플릿

**Quarter 템플릿** (`00001-Q/`, `00002-Q/`)
- Phase/Sprint/Story 구조 예시
- 각 레벨의 index.md 템플릿

**프로젝트 설정**
- `.instructions.md` - AI 작업 지침 템플릿
- `.github/` - GitHub Copilot 설정 (선택사항)

### 사용 시 수정 필요 사항

1. **`.instructions.md`** - 프로젝트에 맞게 작업 규칙 수정
2. **`ROADMAP.md`** - 실제 Quarter 계획으로 교체
3. **Quarter 디렉토리** - 필요에 따라 구조 조정

자세한 사용 방법은 `project-template/.ai-workspace/GUIDE.md`를 참조하세요.
