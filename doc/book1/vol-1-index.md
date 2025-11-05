<!--
AI 에이전트 작업 지침:
이 파일을 수정할 때, 각 장의 서브챕터 목록을 절대 삭제하지 마십시오.
목차는 항상 서브챕터를 포함한 상세 목차여야 합니다.
-->
# 📚 AI 인스트럭션 설계 가이드북 (1권)

## 📘 출판 정보

- **버전**: v1.0 (2025년 1월)
- **대상 독자**: 개인 사용자, 소규모 팀, AI 협업 입문자~중급자
- **학습 범위**: 프롬프트 기초부터 단일 에이전트 설계까지
- **예상 학습 시간**: 15-20시간 (실습 포함)

> **참고**: 이 가이드북은 인간과 AI의 협업으로 작성되었습니다. 가이드북의 내용을 실천하는 과정에서 AI를 활용하여 만들었습니다.

---

## 🎯 1권에서 배우는 것

이 책은 **개인 또는 소규모 팀**에서 **단일 AI 에이전트**를 효과적으로 설계하고 활용하는 방법을 다룹니다.

### 핵심 역량
1. **효과적인 프롬프트 작성**: AI와 명확하게 소통하는 방법
2. **구조화된 인스트럭션 설계**: 재사용 가능한 AI 작업 명세서 작성
3. **단일 에이전트 구축**: 특정 업무를 전담하는 AI 에이전트 설계
4. **워크플로우 최적화**: 파이프라인, 생성-검증, 라우팅 패턴 활용
5. **성능 평가와 개선**: 품질, 비용, 속도의 균형 맞추기

---

## 📖 난이도 가이드

이 가이드북은 단계적 학습을 위해 각 장에 난이도를 표시했습니다:

- **★☆☆ (입문)**: 프롬프트 작성, AI 초보자 대상, 기본 개념 이해
- **★★☆ (중급)**: 인스트럭션 설계, 실무 활용, 단일 에이전트 구축

**1권 학습 목표**: 개인 또는 소규모 팀에서 단일 에이전트를 설계하고 효과적으로 활용하는 방법

**추천 학습 경로**:
- **AI를 처음 접하는 분**: Part 1부터 순서대로
- **실무 경험이 있는 분**: Part 2부터 시작 가능
- **실전 패턴만 빠르게 보려는 분**: Part 4 먼저 확인 후 필요시 이전 장 참고

---

## 📚 목차

## [00장. 서문: AI에게 '제대로' 일 시키는 법](vol-1-part-0-preface.md)

---
### Part 1: 프롬프트와 인스트럭션의 기초

**난이도**: ★☆☆~★★☆ | **학습 목표**: AI와의 기본 대화부터 구조화된 인스트럭션까지

* [1장. 좋은 프롬프트의 원칙](vol-1-part-1-chapter-01.md) **★☆☆**
  * [1.1 프롬프트란?](vol-1-part-1-chapter-01.md#11-프롬프트란)
  * [1.2 프롬프트를 잘 사용하려면](vol-1-part-1-chapter-01.md#12-프롬프트를-잘-사용하려면)
  * [1.3 프롬프트 사용 방식의 차이](vol-1-part-1-chapter-01.md#13-프롬프트-사용-방식의-차이)
* [2장. 질문 설계하기](vol-1-part-1-chapter-02.md) **★☆☆**
  * [2.1 폐쇄형 질문](vol-1-part-1-chapter-02.md#21-폐쇄형-질문-closed-ended)
  * [2.2 개방형 질문](vol-1-part-1-chapter-02.md#22-개방형-질문-open-ended)
  * [2.3 탐색형 질문](vol-1-part-1-chapter-02.md#23-탐색형-질문-exploratory)
  * [2.4 비교형 질문](vol-1-part-1-chapter-02.md#24-비교형-질문-comparative)
  * [2.5 맥락 의존형 질문](vol-1-part-1-chapter-02.md#25-맥락-의존형-질문-context-dependent)
  * [2.6 메타 질문](vol-1-part-1-chapter-02.md#26-메타-질문-meta-questions)
  * [실습 체크리스트](vol-1-part-1-chapter-02.md#실습-체크리스트)
* [3장: 프롬프트를 시스템으로 만들기](vol-1-part-1-chapter-03.md) **★★☆**
  * [3.1 문제: 왜 채팅창의 프롬프트만으로는 부족한가?](vol-1-part-1-chapter-03.md#31-문제-왜-채팅창의-프롬프트만으로는-부족한가)
  * [3.2 해결책: 프롬프트를 '시스템'으로 만들기](vol-1-part-1-chapter-03.md#32-해결책-프롬프트를-시스템으로-만들기)
  * [3.3 방법론: 시스템을 만드는 9가지 구성 요소](vol-1-part-1-chapter-03.md#33-방법론-시스템을-만드는-9가지-구성-요소)

---
### Part 2: 설계 원칙과 구성 요소

**난이도**: ★★☆ | **학습 목표**: 인스트럭션 설계 원칙과 에이전트 구조화 방법 습득

* [4장. AI 협업의 4가지 제약 조건과 해결 원칙](vol-1-part-2-chapter-04.md) **★★☆**
  * [4.1 AI 협업의 4가지 제약 조건](vol-1-part-2-chapter-04.md#41-ai-협업의-4가지-제약-조건)
    * [4.1.1 제약 1: Context Window 한계와 Lost in the Middle](vol-1-part-2-chapter-04.md#411-제약-1-context-window-한계와-lost-in-the-middle)
    * [4.1.2 제약 2: 할루시네이션 (Hallucination)](vol-1-part-2-chapter-04.md#412-제약-2-할루시네이션-hallucination)
    * [4.1.3 제약 3: 비일관성 (Inconsistency)](vol-1-part-2-chapter-04.md#413-제약-3-비일관성-inconsistency)
    * [4.1.4 제약 4: 유지보수 어려움 (Maintenance Difficulty)](vol-1-part-2-chapter-04.md#414-제약-4-유지보수-어려움-maintenance-difficulty)
  * [4.2 제약을 기회로: 체계적인 업무 자동화](vol-1-part-2-chapter-04.md#42-제약을-기회로-체계적인-업무-자동화)
    * [4.2.1 업무를 작은 단위로 나누기](vol-1-part-2-chapter-04.md#421-업무를-작은-단위로-나누기)
    * [4.2.2 표준화된 프로세스 구축](vol-1-part-2-chapter-04.md#422-표준화된-프로세스-구축)
    * [4.2.3 명확한 책임 분배](vol-1-part-2-chapter-04.md#423-명확한-책임-분배)
  * [실습 체크리스트](vol-1-part-2-chapter-04.md#실습-체크리스트)
* [5장. 인스트럭션 시스템 설계 원칙](vol-1-part-2-chapter-05.md) **★★☆**
  * [5.1 구조적 원칙](vol-1-part-2-chapter-05.md#51-구조적-원칙-설계의-뼈대-세우기)
  * [5.2 실행 원칙](vol-1-part-2-chapter-05.md#52-실행-원칙-ai와-함께-일하는-방식-정의하기)
  * [5.3 검증 및 책임 원칙](vol-1-part-2-chapter-05.md#53-검증-및-책임-원칙-신뢰와-안전성-확보하기)
  * [5.4 시스템 설계 원칙 요약표](vol-1-part-2-chapter-05.md#54-시스템-설계-원칙-요약표)
  * [5.5 상황별 원칙 적용 가이드](vol-1-part-2-chapter-05.md#55-상황별-원칙-적용-가이드)
  * [실습 체크리스트](vol-1-part-2-chapter-05.md#실습-체크리스트)
* [6장. 입력과 출력 설계](vol-1-part-2-chapter-06.md) **★★☆**
  * [6.1 왜 입력과 출력 설계가 중요한가?](vol-1-part-2-chapter-06.md#61-왜-입력과-출력-설계가-중요한가)
  * [6.2 무엇을 설계해야 하는가?](vol-1-part-2-chapter-06.md#62-무엇을-설계해야-하는가-입력과-출력의-명세화)
  * [6.3 어떻게 설계하는가?](vol-1-part-2-chapter-06.md#63-어떻게-설계하는가-결과물-중심-접근법과-구체적-기법)
  * [실습 체크리스트](vol-1-part-2-chapter-06.md#실습-체크리스트)
* [7장. 단일 에이전트 설계](vol-1-part-2-chapter-07.md) **★★☆**
  * [7.1 에이전트란 무엇인가?](vol-1-part-2-chapter-07.md#71-에이전트란-무엇인가)
  * [7.2 에이전트의 핵심 구성 요소: 정체성, 지식, 도구](vol-1-part-2-chapter-07.md#72-에이전트의-핵심-구성-요소-정체성-지식-도구)
  * [7.3 정체성(Identity) 부여하기](vol-1-part-2-chapter-07.md#73-정체성identity-부여하기)
  * [7.4 지식(Knowledge) 제공하기](vol-1-part-2-chapter-07.md#74-지식knowledge-제공하기)
  * [7.5 도구(Tools) 활용하기](vol-1-part-2-chapter-07.md#75-도구tools-활용하기)
  * [7.6 에이전트 설계 템플릿](vol-1-part-2-chapter-07.md#76-에이전트-설계-템플릿)
  * [실습 체크리스트](vol-1-part-2-chapter-07.md#실습-체크리스트)
* [8장. 워크플로우 설계: 에이전트 협업 시스템 구축](vol-1-part-2-chapter-08.md) **★★☆**
  * [8.1 파이프라인(Pipeline) 패턴](vol-1-part-2-chapter-08.md#81-파이프라인pipeline-패턴)
  * [8.2 생성-검증(Generate-and-Verify) 패턴](vol-1-part-2-chapter-08.md#82-생성-검증generate-and-verify-패턴)
  * [8.3 라우팅 패턴](vol-1-part-2-chapter-08.md#83-라우팅-패턴)
  * [8.4 워크플로우 정의 (`workflow.yaml`)](vol-1-part-2-chapter-08.md#84-워크플로우-정의-workflowyaml)
  * [실습 체크리스트](vol-1-part-2-chapter-08.md#실습-체크리스트)

---

## 📚 부록 및 참고 자료

### 1권 전용 부록
* [실습 과제 모음](practice-guide.md) - 1권 전체 실습 체크리스트
* [용어집](glossary.md) - 1권에서 사용된 주요 용어 정리

### 추가 학습 자료
* [GitHub Repository](https://github.com/wooxist/ai-instructions) - 예제 코드 및 템플릿
* [커뮤니티 포럼](https://community.example.com) - 질문과 경험 공유 (계획 중)
* [공식 블로그](https://blog.example.com) - 최신 사례 및 업데이트 (계획 중)

---

## 💬 피드백 및 문의

**이메일**: iam@daewook.me
**GitHub Issues**: [https://github.com/wooxist/ai-instructions/issues](https://github.com/wooxist/ai-instructions/issues)

---

**© 2025 AI Instruction Design Guide | Version 1.0 | 1권 완결판**
