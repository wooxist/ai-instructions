# AI 에이전트 시스템 스타터 키트 (Starter Kit)

이 디렉토리는 여러분의 AI 에이전트 시스템을 구축하기 위한 **시작점(Starter Kit)**입니다.

이 폴더를 **당신의 프로젝트에 그대로 복사**하여, `system.yaml`을 수정하는 것만으로 새로운 AI 에이전트 시스템을 빠르고 일관되게 구축할 수 있습니다. 이 모듈은 시스템 전체를 **초기화(initialize)**하고 **통제(govern)**하는 핵심 구성요소를 담고 있습니다.

## 최종 구조 (Directory Structure)
```
starter-kit/
├── bootstrap/
│   ├── knowledge/             # 1. 에이전트 설계를 위한 핵심 지식 베이스
│   │   ├── 01-core-principles.md
│   │   └── ...
│   ├── bootstrap_agent.md     # 2. '태초의 메타 에이전트' (다른 메타 생성)
│   ├── governance_agent.md    # 3. '거버넌스 에이전트' (시스템 감사)
│   └── system.yaml            # 4. 시스템 전체 설계도
└── README.md              # 5. 본 문서 (사용 가이드)
```

## 핵심 구성 요소 (Core Components)

모든 핵심 구현 파일은 `starter-kit/bootstrap/` 디렉토리 내에 위치합니다.

1.  **`bootstrap/knowledge/` (지식 베이스):**
    *   **역할:** '태초의 메타 에이전트'가 다른 에이전트를 생성할 때 참조하는 핵심 원칙과 설계 방법론의 요약본입니다.

2.  **`bootstrap/bootstrap_agent.md` (태초의 메타 에이전트):**
    *   **역할:** 시스템의 유일한 시작점(Entrypoint)입니다.
    *   **책임:** `system.yaml` 파일을 읽고, `knowledge/`의 지식을 바탕으로 그 안에 정의된 모든 '도메인 메타 에이전트'들을 생성하는 임무를 수행합니다.

3.  **`bootstrap/governance_agent.md` (거버넌스 에이전트):**
    *   **역할:** 시스템의 구조적 무결성을 검증하는 '감사관(Auditor)'입니다.
    *   **책임:** `system.yaml` 설계도와 실제 파일 시스템의 구조를 비교하여, 규칙 위반이나 불일치가 없는지 검증하고 보고합니다.

4.  **`bootstrap/system.yaml` (시스템 설계도):**
    *   **역할:** 시스템 전체의 구조, 도메인, 규칙 등을 정의하는 중앙 메타데이터 파일(Manifest)입니다.
    *   **책임:** `bootstrap_agent`가 무엇을 생성해야 하는지, `governance_agent`가 무엇을 검증해야 하는지에 대한 기준을 제공합니다.

## 시스템 시작 및 운영 흐름 (Bootstrap & Governance Flow)

1.  **설정 (Setup):** 인간 설계자가 `starter-kit/bootstrap/system.yaml` 파일에 만들고 싶은 AI 조직의 전체 구조를 정의합니다.

2.  **초기화 (Initialization):** `starter-kit/bootstrap/bootstrap_agent.md`를 단 한 번 실행합니다. 이 에이전트는 `system.yaml`을 읽어 필요한 모든 '도메인 메타 에이전트'들을 `ai-agents/` 디렉토리 아래에 생성합니다.

3.  **검증 (Validation):** `starter-kit/bootstrap/governance_agent.md`를 실행하여, 초기화된 시스템이 `system.yaml`에 정의된 대로 정확하게 구성되었는지 검증합니다.
