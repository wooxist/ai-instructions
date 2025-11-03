# AI 인스트럭션 설계 가이드북# AI 인스트럭션 설계 가이드북<!--



> 이 프로젝트의 목적은 AI와 협업 잘하기입니다.AI 지침:



---> 이 프로젝트의 목적은 AI와 협업 잘하기입니다.1. 이 파일은 프로젝트 소개 문서입니다



## 📖 1권: 단일 에이전트 설계2. 프로젝트 목표와 구조 설명만 포함하세요



이 가이드북은 개인 또는 소규모 팀에서 단일 AI 에이전트를 효과적으로 설계하고 활용하는 방법을 다룹니다. ## 📖 1권: 단일 에이전트 설계3. 작업 규칙이나 진행 상황은 .ai-workspace/ 디렉토리 파일들을 참조하세요



프롬프트 기초부터 체계적인 인스트럭션 설계, 그리고 여러 에이전트를 협업시키는 워크플로우 구축까지, AI를 믿을 수 있는 업무 파트너로 만드는 실용적인 방법론을 제시합니다.-->



👉 **[1권 전체 목차 및 내용 바로가기](doc/book1/vol-1-index.md)**이 가이드북은 개인 또는 소규모 팀에서 단일 AI 에이전트를 효과적으로 설계하고 활용하는 방법을 다룹니다. 프롬프트 기초부터 체계적인 인스트럭션 설계, 그리고 여러 에이전트를 협업시키는 워크플로우 구축까지, AI를 믿을 수 있는 업무 파트너로 만드는 실용적인 방법론을 제시합니다.


# AI 인스트럭션 설계 가이드북

- **[1권 전체 목차 바로가기](doc/book1/vol-1-index.md)**

> AI와의 효과적인 협업을 위한 체계적인 인스트럭션 설계 방법론

### Part 1: 프롬프트와 인스트럭션의 기초 (1-3장)

AI와 명확하게 소통하기 위한 기본기를 다집니다. 좋은 질문을 설계하는 방법부터, 재사용 가능한 지시서인 '인스트럭션'을 만드는 4가지 핵심 원칙과 9가지 구성 요소를 배웁니다.## 📖 이 책에 대하여



### Part 2: 설계 원칙과 구성 요소 (4-8장)이 프로젝트는 AI와의 협업을 위한 체계적인 인스트럭션 설계 방법론을 정립하고, 이를 가이드북 형태로 제공하는 것을 목표로 합니다.

'문제 → 전략 → 전술'의 흐름에 따라 체계적인 인스트럭션 시스템을 설계합니다.

- **문제 (4장)**: AI 협업 시 발생하는 현실적인 제약들을 이해합니다.- **대상 독자**: 개인 사용자, 소규모 팀, AI 협업 입문자~중급자

- **전략 (5장)**: 제약을 극복하기 위한 핵심 전략으로 '시스템 설계 원칙'을 배웁니다.- **학습 목표**: 개인 또는 소규모 팀에서 단일 AI 에이전트를 효과적으로 설계하고 활용하는 방법을 배웁니다.

- **전술 (6-8장)**: 전략을 구현하기 위한 구체적인 기술인 '입출력 설계', '에이전트 설계', '워크플로우 설계'를 익힙니다.- **주요 내용**: 프롬프트 기초부터 구조화된 인스트럭션 설계, 워크플로우 최적화까지 다룹니다.



---## � 1권 목차 (Part 1: 프롬프트와 인스트럭션의 기초)



## 🚀 프로젝트 시작하기 (기여자용)현재 **Part 1: 프롬프트와 인스트럭션의 기초**가 완성되었습니다.



### AI 작업자용- **[전체 목차 바로가기](doc/book1/vol-1-index.md)**



1. **작업 전**: `.instructions.md` 읽기 (프로젝트 규칙)### [00장. 서문: AI에게 '제대로' 일 시키는 법](doc/book1/vol-1-part-0-preface.md)

2. **작업 방식**: `.ai-workspace/GUIDE.md` 참조 (일하는 방식)

3. **현재 위치**: `.ai-workspace/PROGRESS.md` 확인---

4. **커밋 시**: `.ai-workspace/COMMIT-RULES.md` 참조### Part 1: 프롬프트와 인스트럭션의 기초



### 사람 작업자용* [1장. 프롬프트와 인스트럭션 이해하기](doc/book1/vol-1-part-1-chapter-01.md) **★☆☆**

  * [1.1 프롬프트란?](doc/book1/vol-1-part-1-chapter-01.md#11-프롬프트란)

- **전체 계획**: `.ai-workspace/ROADMAP.md`  * [1.2 프롬프트를 잘 사용하려면](doc/book1/vol-1-part-1-chapter-01.md#12-프롬프트를-잘-사용하려면)

- **현재 진행**: `.ai-workspace/PROGRESS.md`  * [1.3 프롬프트의 한계 및 인스트럭션의 필요성](doc/book1/vol-1-part-1-chapter-01.md#13-프롬프트의-한계-및-인스트럭션의-필요성)

- **완료 기록**: `.ai-workspace/ARCHIVE.md`* [2장. 질문 설계하기](doc/book1/vol-1-part-1-chapter-02.md) **★☆☆**

  * [2.1 폐쇄형 질문](doc/book1/vol-1-part-1-chapter-02.md#21-폐쇄형-질문-closed-ended)
  * [2.2 개방형 질문](doc/book1/vol-1-part-1-chapter-02.md#22-개방형-질문-open-ended)
  * [2.3 탐색형 질문](doc/book1/vol-1-part-1-chapter-02.md#23-탐색형-질문-exploratory)
  * [2.4 비교형 질문](doc/book1/vol-1-part-1-chapter-02.md#24-비교형-질문-comparative)
  * [2.5 맥락 의존형 질문](doc/book1/vol-1-part-1-chapter-02.md#25-맥락-의존형-질문-context-dependent)
  * [2.6 메타 질문](doc/book1/vol-1-part-1-chapter-02.md#26-메타-질문-meta-questions)
* [3장. 효과적인 지시 작성의 기본 원칙](doc/book1/vol-1-part-1-chapter-03.md) **★★☆**
  * [3.1 인스트럭션: 일회성 프롬프트를 넘어서](doc/book1/vol-1-part-1-chapter-03.md#31-인스트럭션-일회성-프롬프트를-넘어서)
  * [3.2 명확성 (Clear)](doc/book1/vol-1-part-1-chapter-03.md#32-명확성-clear)
  * [3.3 구체성 (Specific)](doc/book1/vol-1-part-1-chapter-03.md#33-구체성-specific)
  * [3.4 단계성 (Step-wise)](doc/book1/vol-1-part-1-chapter-03.md#34-단계성-step-wise)
  * [3.5 제약 조건(Constraints)과 한계 설정](doc/book1/vol-1-part-1-chapter-03.md#35-제약-조건constraints과-한계-설정)
  * [3.6 실패하는 지시의 특징 (안티패턴)](doc/book1/vol-1-part-1-chapter-03.md#36-실패하는-지시의-특징-안티패턴)
  * [3.7 표준 인스트럭션 템플릿: 8가지 핵심 구성 요소](doc/book1/vol-1-part-1-chapter-03.md#37-표준-인스트럭션-템플릿-8가지-핵심-구성-요소)

---

## 🚀 프로젝트 시작하기

### AI 작업자용

1. **작업 전**: `.instructions.md` 읽기 (프로젝트 규칙)
2. **작업 방식**: `.ai-workspace/GUIDE.md` 참조 (일하는 방식)
3. **현재 위치**: `.ai-workspace/PROGRESS.md` 확인
4. **커밋 시**: `.ai-workspace/COMMIT-RULES.md` 참조

### 사람 작업자용

- **전체 계획**: `.ai-workspace/ROADMAP.md`
- **현재 진행**: `.ai-workspace/PROGRESS.md`
- **완료 기록**: `.ai-workspace/ARCHIVE.md`
