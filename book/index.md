# 📚 AI 인스트럭션 설계 가이드북

> **참고**: 이 가이드북은 인간과 AI의 협업으로 작성되었습니다. 가이드북의 내용을 실천하는 과정에서 AI를 활용하여 만들었습니다.

## [00장. 서문: AI에게 '제대로' 일 시키는 법](00-preface.md)

---
### Part 1: 프롬프트와 인스트럭션의 기초
* [1장. 프롬프트와 인스트럭션 이해하기](01-introduction.md)
  * [1.1 프롬프트란?](01-introduction.md#11-프롬프트란)
  * [1.2 프롬프트를 잘 사용하려면](01-introduction.md#12-프롬프트를-잘-사용하려면)
  * [1.3 프롬프트의 한계 및 인스트럭션의 필요성](01-introduction.md#13-프롬프트의-한계-및-인스트럭션의-필요성)
* [2장. 질문 설계하기](02-questions.md)
  * [2.1 폐쇄형 질문](02-questions.md#21-폐쇄형-질문-closed-ended)
  * [2.2 개방형 질문](02-questions.md#22-개방형-질문-open-ended)
  * [2.3 탐색형 질문](02-questions.md#23-탐색형-질문-exploratory)
  * [2.4 비교형 질문](02-questions.md#24-비교형-질문-comparative)
  * [2.5 맥락 의존형 질문](02-questions.md#25-맥락-의존형-질문-context-dependent)
  * [2.6 메타 질문](02-questions.md#26-메타-질문-meta-questions)
* [3장. 좋은 인스트럭션](03-good-instructions.md)
  * [3.1 인스트럭션: 일회성 프롬프트를 넘어서](03-good-instructions.md#31-인스트럭션-일회성-프롬프트를-넘어서)
  * [3.7 표준 인스트럭션 템플릿: 8가지 핵심 구성 요소](03-good-instructions.md#37-표준-인스트럭션-템플릿-8가지-핵심-구성-요소)

---
### Part 2: 인스트럭션 시스템 설계와 평가
* [4장. 인스트럭션 설계의 메타 원칙](04-meta-principles.md)
  * [4.1 구조적 원칙](04-meta-principles.md#41-구조적-원칙-설계의-뼈대-세우기)
  * [4.2 실행 원칙](04-meta-principles.md#42-실행-원칙-ai와-함께-일하는-방식-정의하기)
  * [4.3 검증 및 책임 원칙](04-meta-principles.md#43-검증-및-책임-원칙-신뢰와-안전성-확보하기)
* [5장. 역할(Agent)과 제약(Constraint) 설계](05-agent-constraints.md)
  * [5.1 왜 '에이전트'를 설계해야 하는가?](05-agent-constraints.md#51-왜-에이전트를-설계해야-하는가)
  * [5.2 해결 원칙과 방법론](05-agent-constraints.md#52-해결-원칙과-방법론-단일-책임을-갖는-에이전트로-분할하라)
* [6장. 입력과 출력 설계](06-input-output.md)
  * [6.1 왜 입력과 출력 설계가 중요한가?](06-input-output.md#61-왜-입력과-출력-설계가-중요한가)
* [7장. 기본 워크플로우 패턴과 처리](07-process-workflow.md)
  * [7.1 파이프라인(Pipeline) 패턴](07-process-workflow.md#71-파이프라인pipeline-패턴)
  * [7.2 생성-검증(Generate-and-Verify) 패턴](07-process-workflow.md#72-생성-검증generate-and-verify-패턴)
  * [7.3 라우팅 패턴](07-process-workflow.md#73-라우팅-패턴)
* [8장. 성능 최적화: 품질, 비용, 속도의 균형 맞추기](08-performance.md)
* [9장. 인스트럭션의 평가와 검증](09-productivity.md)
* [10장. 고급 협업 아키텍처와 시스템 설계](10-advanced-collaboration-architectures.md)
  * [10.3 계층적 협업 아키텍처: 시스템의 시작과 동적 실행](10-advanced-collaboration-architectures.md#103-계층적-협업-아키텍처-시스템의-시작과-동적-실행)
  * [10.6 시스템 거버넌스: 태초의 메타 에이전트와 시스템의 시작](10-advanced-collaboration-architectures.md#106-시스템-거버넌스-태초의-메타-에이전트와-시스템의-시작)
* [11장. 상황별 설계 패턴 예제]
    * [11장 1부: 단일 에이전트 설계](11-1-single-agent.md)
    * [11장 2부: 단위 조직 설계](11-2-unit-organization.md)
    * [11장 3부: 복합 조직 설계](11-3-complex-organization.md)

---
### Part 3: 인스트럭션 시스템의 확장과 운영
* [12장. 도구(Tools)와 플러그인 활용](12-tools.md)
* [13장. 도메인 특화 언어(DSL) 설계 (작성 중)](13-workflow-as-code.md)
* [14장. 살아있는 시스템: 인스트럭션의 진화와 관리](14-evolution.md)

## [15장. 결론: AI 시대의 새로운 일잘법](15-conclusion.md)