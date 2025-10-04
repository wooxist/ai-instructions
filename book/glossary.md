# 용어집 (Glossary)

이 용어집은 책 전체에서 사용되는 핵심 개념들의 정의와 첫 등장 위치를 정리한 것입니다.

## 핵심 용어

### 프롬프트 (Prompt)
- **정의**: AI 모델에게 말을 거는 방식이자, 원하는 결과를 얻기 위한 일회성 지시문
- **첫 등장**: [1장 1.1절](01-introduction.md#11-프롬프트란)
- **관련 개념**: 인스트럭션, 지시

### 인스트럭션 (Instruction)
- **정의**: 반복 가능한 작업을 위해 표준화된 지시 체계. 프롬프트의 한계를 극복하기 위한 재사용 가능한 시스템
- **첫 등장**: [1장 1.3절](01-introduction.md#13-프롬프트의-한계-및-인스트럭션의-필요성)
- **관련 개념**: 프롬프트, 에이전트, 워크플로우

### 에이전트 (Agent)
- **정의**: 특정 역할, 책임, 제약 조건을 가진 독립적인 실행 단위. 명확하게 정의된 단일 책임을 수행하는 AI 전문가
- **첫 등장**: [5장 5.1절](05-agent-constraints.md#51-왜-에이전트를-설계해야-하는가)
- **관련 개념**: 역할(Role), 페르소나(Persona), 워커 에이전트

### 워크플로우 (Workflow)
- **정의**: 여러 에이전트가 작업을 수행하는 순서와 방식을 정의한 프로세스
- **첫 등장**: [7장](07-process-workflow.md)
- **관련 개념**: 파이프라인, 생성-검증, 라우팅

### 산출물 (Artifact)
- **정의**: 에이전트가 생성하는 결과물이자, 에이전트 간 협업을 위한 소통 매개체
- **첫 등장**: [6장](06-input-output.md)
- **심화**: [10장 10.2절](10-advanced-collaboration-architectures.md#102-협업의-전제-조건-산출물-인터페이스)
- **관련 개념**: 산출물 인터페이스, 입출력 명세

### 산출물 인터페이스 (Artifact Interface)
- **정의**: 에이전트 간의 명확한 소통 규약. 한 에이전트의 출력이 다른 에이전트의 입력이 되는 표준화된 형식
- **첫 등장**: [10장 10.2절](10-advanced-collaboration-architectures.md#102-협업의-전제-조건-산출물-인터페이스)
- **관련 개념**: 산출물, 입출력 설계, JSON Schema

---

## 설계 원칙

### SSOT (Single Source of Truth)
- **정의**: 핵심 정의·템플릿·지식을 단일 출처에서 관리하여 중복을 제거하는 원칙
- **첫 등장**: [4장 4.1절](04-meta-principles.md#41-구조적-원칙-설계의-뼈대-세우기)
- **적용**: 인스트럭션 중복 제거, 지식 출처 한정

### SoC (Separation of Concerns)
- **정의**: 각 부분이 하나의 책임만 갖도록 분리하여 결합도를 줄이는 원칙
- **첫 등장**: [4장 4.1절](04-meta-principles.md#41-구조적-원칙-설계의-뼈대-세우기)
- **적용**: 에이전트 역할 분리, 모듈화

### MECE (Mutually Exclusive, Collectively Exhaustive)
- **정의**: 중복 없이, 빠짐없이 구성하는 분류 원칙
- **첫 등장**: [4장 4.1절](04-meta-principles.md#41-구조적-원칙-설계의-뼈대-세우기)
- **적용**: 작업 분류, 에이전트 역할 분배

### 산출물 중심 (Output-Driven)
- **정의**: 중간 과정보다 최종 결과물의 요건을 먼저 명확히 정의하는 접근법
- **첫 등장**: [4장 4.2절](04-meta-principles.md#42-실행-원칙-ai와-함께-일하는-방식-정의하기)
- **적용**: 입출력 설계, 역방향 설계

### Human-in-the-Loop
- **정의**: 중요한 의사결정에 반드시 사람의 검토를 포함시키는 원칙
- **첫 등장**: [4장 4.3절](04-meta-principles.md#43-검증-및-책임-원칙-신뢰와-안전성-확보하기)
- **적용**: 승인 프로세스, 최종 검증

---

## 기술 용어

### 컨텍스트 윈도우 (Context Window)
- **정의**: AI 모델이 한 번에 처리하고 기억할 수 있는 최대 정보의 양 (토큰 단위)
- **첫 등장**: [1장 각주](01-introduction.md)
- **관련 개념**: 토큰, 할루시네이션

### 할루시네이션 (Hallucination)
- **정의**: AI가 사실이 아닌 정보를 그럴듯하게 생성하는 현상
- **첫 등장**: [5장 5.1절](05-agent-constraints.md#51-왜-에이전트를-설계해야-하는가)
- **해결책**: SSOT, 근거 기반 책임, 검증 에이전트

### RAG (Retrieval-Augmented Generation)
- **정의**: 외부 지식을 검색하여 답변 생성을 보강하는 기술
- **첫 등장**: [5장 각주](05-agent-constraints.md)
- **적용 사례**: [11.5 사내 Q&A 봇](11-2-organizational-standards.md#115-사례-5-조직-표준-표준전문)

### JSON Schema
- **정의**: JSON 데이터의 구조를 정의하고 검증하기 위한 표준 규격
- **첫 등장**: [6장 각주](06-input-output.md)
- **적용**: 구조화된 출력, 산출물 인터페이스

### Few-shot Learning
- **정의**: AI에게 몇 가지 예시만 제공하여 패턴을 학습시키는 방법
- **첫 등장**: [1장 각주](01-introduction.md)
- **적용**: 예시 기반 인스트럭션

---

## 아키텍처 패턴

### 파이프라인 (Pipeline) 패턴
- **정의**: 에이전트들이 순차적으로 작업을 처리하는 협업 모델
- **첫 등장**: [7장 7.1절](07-process-workflow.md#71-파이프라인pipeline-패턴)
- **사례**: 데이터 수집 → 정제 → 추출 → 보고서 생성

### 생성-검증 (Generate-and-Verify) 패턴
- **정의**: 한 에이전트가 결과물을 생성하면, 다른 에이전트가 검증하는 협업 모델
- **첫 등장**: [7장 7.2절](07-process-workflow.md#72-생성-검증generate-and-verify-패턴)
- **사례**: 작가 에이전트 + 편집자 에이전트

### 라우팅 (Routing) 패턴
- **정의**: 입력 내용이나 조건에 따라 다음 처리 경로를 결정하는 패턴
- **첫 등장**: [7장 7.3절](07-process-workflow.md#73-라우팅-패턴)
- **유형**: 분류 기반 라우팅, 조건부 라우팅

### 계층적 협업 아키텍처
- **정의**: '실행'과 '생성'의 역할이 분리된 동적인 에이전트 시스템 구조. **메타 에이전트**는 아키텍트의 요청에 따라 에이전트를 생성/관리하고, **아키텍트 에이전트**는 외부의 지시를 받아 프로젝트를 실행하며, **워커 에이전트**는 실무를 수행한다.
- **첫 등장**: [10장 10.3절](10-advanced-collaboration-architectures.md#103-계층적-협업-아키텍처-시스템의-시작과-동적-실행)
- **구성**: 메타 에이전트(생성/관리), 아키텍트 에이전트(실행/지휘), 워커 에이전트(수행)

### 재귀적 협업 구조 (Recursive Collaboration Architecture)
- **정의**: 에이전트 시스템이 `메타->아키텍트->워커` 구조를 반복하며 더 큰 조직을 형성하는 유연한 구조. 특정 스코프(Scope)를 가진 메타 에이전트가 더 큰 시스템의 아키텍트가 될 수 있다.
- **첫 등장**: [10장 10.3.5절](10-advanced-collaboration-architectures.md#1035-심화-실제-조직과-같은-재귀적-구조)
- **특징**: 유연성, 확장성, 스코프 기반 역할 정의

---

## 품질 및 성능

### 트레이드오프 (Trade-off)
- **정의**: 한 가치를 얻기 위해 다른 가치를 포기해야 하는 상충 관계
- **첫 등장**: [2장 각주](02-questions.md)
- **적용**: 품질-비용-속도의 균형 ([8장](08-performance.md))

### 성능의 삼각형
- **정의**: 품질(Quality), 자원(Resource), 대기 시간(Latency)의 상충 관계
- **첫 등장**: [8장 8.1절](08-performance.md#81-왜-성능-최적화가-필요한가)
- **관련 개념**: 트레이드오프, 최적화

### 멱등성 (Idempotency)
- **정의**: 같은 입력에 대해 항상 같은 출력이 나오는 성질
- **첫 등장**: [4장 4.2절](04-meta-principles.md#42-실행-원칙-ai와-함께-일하는-방식-정의하기)
- **중요성**: 재현 가능성, 신뢰성 보장

---

## 도구 및 표준

### MCP (Model Context Protocol)
- **정의**: AI 에이전트와 도구 간의 상호운용성을 위한 표준 프로토콜
- **첫 등장**: [12장 12.6절](12-tools.md#126-mcp-상호운용성을-위한-표준-프로토콜)
- **목적**: 도구 파편화 해결, 에코시스템 통합

### 도구 명세 (Tool Specification)
- **정의**: 에이전트가 도구를 사용하기 위한 '사용 설명서' (이름, 설명, 입출력 스키마)
- **첫 등장**: [12장 12.3절](12-tools.md#123-에이전트에게-도구를-부여하는-방법)
- **구성**: tool_name, description, input_schema, output_schema

---

## 조직 및 관리

### Instruction Decay
- **정의**: 시간이 지남에 따라 인스트럭션의 품질과 관련성이 저하되는 현상
- **첫 등장**: [14장 14.4절](14-evolution.md#144-인스트럭션의-부패와-유지보수-instruction-decay)
- **원인**: 환경 변화, 기술 진화, 문서 노후화
- **해결**: 지속적 모니터링, 버전 관리, 정기 업데이트

### 조직 표준 시스템
- **정의**: 개인이나 팀의 인스트럭션을 조직 전체가 공유하고 재사용하는 시스템
- **첫 등장**: [11장 2부](11-2-organizational-standards.md)
- **특징**: 다수 사용자 공유, 표준화된 템플릿, 버전 관리
- **사례**: 11.4 (회의록 요약), 11.5 (사내 Q&A), 11.6 (고객 리뷰 분석)

---

## 색인 (Index)

### ㄱ
- 간단/일상 → [4장 매트릭스](04-meta-principles.md#45-상황별-원칙-적용-가이드)
- 계층적 협업 → [10장 10.3절](#계층적-협업-아키텍처)
- 구조화된 출력 → [6장 6.3절](06-input-output.md#63-어떻게-설계하는가-결과물-중심-접근법과-구체적-기법)

### ㄷ
- 도구 (Tools) → [12장](#도구-명세-tool-specification)

### ㅁ
- 메타 에이전트 → [10장 10.3.4절](10-advanced-collaboration-architectures.md#1034-메타-에이전트-meta-agent-시스템-총괄-설계자)
- 멱등성 → [#멱등성-idempotency](#멱등성-idempotency)

### ㅂ
- 병렬 처리 → [8장 8.3절](08-performance.md#83-어떻게-최적화하는가-사용자를-위한-실용적인-트레이드오프-전략)

### ㅅ
- 산출물 → [#산출물-artifact](#산출물-artifact)
- 산출물 인터페이스 → [#산출물-인터페이스-artifact-interface](#산출물-인터페이스-artifact-interface)
- 산출물 중심 → [#산출물-중심-output-driven](#산출물-중심-output-driven)

### ㅇ
- 에이전트 → [#에이전트-agent](#에이전트-agent)
- 워크플로우 → [#워크플로우-workflow](#워크플로우-workflow)
- 원자성 → [4장 4.1절](04-meta-principles.md#41-구조적-원칙-설계의-뼈대-세우기)

### ㅈ
- 복합 조직 시스템 → [11장 2부](11-2-organizational-standards.md)

### ㅍ
- 파이프라인 → [#파이프라인-pipeline-패턴](#파이프라인-pipeline-패턴)
- 프롬프트 → [#프롬프트-prompt](#프롬프트-prompt)
- 피드백 루프 → [4장 4.2절](04-meta-principles.md#42-실행-원칙-ai와-함께-일하는-방식-정의하기)

### ㅎ
- 할루시네이션 → [#할루시네이션-hallucination](#할루시네이션-hallucination)

### A-Z
- Human-in-the-Loop → [#human-in-the-loop](#human-in-the-loop)
- JSON Schema → [#json-schema](#json-schema)
- MCP → [#mcp-model-context-protocol](#mcp-model-context-protocol)
- MECE → [#mece-mutually-exclusive-collectively-exhaustive](#mece-mutually-exclusive-collectively-exhaustive)
- RAG → [#rag-retrieval-augmented-generation](#rag-retrieval-augmented-generation)
- SoC → [#soc-separation-of-concerns](#soc-separation-of-concerns)
- SSOT → [#ssot-single-source-of-truth](#ssot-single-source-of-truth)
