# AI 지침 스타터 킷 (AI Instructions Starter Kit)

이 스타터 킷은 `ai-instructions`의 설계 철학에 따라 새로운 AI 에이전트 시스템을 구축하기 위한 템플릿입니다.

## 🚀 빠른 시작 (Quick Start)

1.  **프로젝트 생성 및 파일 복사:**
    -   새로운 프로젝트를 위한 디렉토리를 만듭니다. (예: `my-ai-project`)
    -   이 `starter-kit` 디렉토리의 모든 내용(`bootstrap/`, `system.yaml`, `README.md`)을 새 프로젝트 디렉토리 안으로 복사합니다.

2.  **시스템 초기화 워크플로우 실행:**
    -   (AI 실행 환경에서) `bootstrap/workflow.yaml` 워크플로우를 실행합니다.
    -   워크플로우가 시작되면, 에이전트들이 질문을 할 것입니다. 대화형 지시에 따라 시스템의 초기 설계를 완료하십시오.

## ⚙️ 초기화 워크플로우 상세

`bootstrap/workflow.yaml`은 다음 두 전문가 에이전트를 순서대로 실행하여 시스템을 구축합니다.

1.  **1단계: 시스템 아키텍트 (`governance_agent`)**
    -   **역할:** 시스템의 전체 청사진을 설계합니다.
    -   **프로세스:** `governance_agent`가 먼저 실행되어, 당신과의 대화를 통해 시스템의 청사진인 `system.yaml` 파일을 완성합니다. 이 과정에서 시스템의 이름, 필요한 도메인(부서), 주요 프로젝트 등을 결정하게 됩니다.

2.  **2단계: 수석 엔지니어 (`bootstrap_agent`)**
    -   **역할:** 설계된 청사진에 따라 실제 초기 조직을 건설합니다.
    -   **프로세스:** `governance_agent`가 `system.yaml`을 완성하면, `bootstrap_agent`가 실행됩니다. `bootstrap_agent`는 완성된 `system.yaml`을 읽고, 그에 명시된 초기 메타 에이전트들을 당신의 검토와 승인을 거쳐 실제로 생성합니다.

초기화가 완료되면, 당신의 프로젝트는 `system.yaml`이라는 헌법과 각 도메인을 책임지는 메타 에이전트들을 갖춘 완전한 시스템으로 거듭납니다.

## 🌱 시스템 확장 및 변경 (System Expansion & Changes)

> **중요:** 시스템의 구조(예: 새로운 도메인 추가, 기존 도메인 제거)를 변경하고 싶을 때는, 파일을 직접 수정하는 대신 **반드시 `governance_agent`를 다시 실행**하십시오.
>
> `governance_agent`는 `system.yaml`을 안전하게 수정하고 시스템의 일관성을 유지하는 유일한 공식 창구입니다.

---
**버전:** 1.0.0
