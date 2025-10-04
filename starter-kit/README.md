# AI 에이전트 시스템 스타터 키트 (Starter Kit)

이 디렉토리는 여러분의 AI 에이전트 시스템을 구축하기 위한 **시작점(Starter Kit)**입니다.

이 폴더를 **당신의 프로젝트에 그대로 복사**하여, `system.yaml`을 수정하고 에이전트들을 순서대로 실행하는 것만으로 새로운 AI 에이전트 시스템의 뼈대를 빠르고 일관되게 구축할 수 있습니다.

## 최종 구조 (Directory Structure)
```
starter-kit/
├── bootstrap/
│   ├── knowledge/             # 에이전트 설계를 위한 핵심 지식 베이스
│   ├── bootstrap_agent.md     # '태초의 메타 에이전트' (내용 채우기)
│   ├── governance_agent.md    # '거버넌스 에이전트' (시스템 감사)
│   └── scaffolding_agent.md   # '스캐폴딩 에이전트' (뼈대 생성)
├── system.yaml                # 시스템 전체 설계도
└── README.md                  # 본 문서 (사용 가이드)
```

## 시스템 시작을 위한 4단계 워크플로우

1.  **1단계 (인간): 설정**
    *   `starter-kit/system.yaml` 파일을 열어, 당신이 만들고 싶은 시스템의 `domains`(부서)과 `entrypoints`(주요 프로젝트)를 정의합니다.

2.  **2단계 (AI): 뼈대 생성**
    *   `starter-kit/bootstrap/scaffolding_agent.md`를 실행합니다.
    *   이 에이전트는 `system.yaml`을 읽고, `ai-agents/engineering/architects`와 같이 필요한 모든 디렉토리 구조를 자동으로 생성합니다.

3.  **3단계 (AI): 초기화**
    *   `starter-kit/bootstrap/bootstrap_agent.md`를 실행합니다.
    *   이 에이전트는 `system.yaml`과 `knowledge/`를 참조하여, 생성된 폴더 구조 안에 `meta.md`와 같은 초기 에이전트 파일들을 생성하여 내용을 채웁니다.

4.  **4단계 (AI): 검증**
    *   `starter-kit/bootstrap/governance_agent.md`를 실행합니다.
    *   이 에이전트는 최종적으로 생성된 모든 파일과 폴더가 `system.yaml`에 정의된 대로 완벽하게 구성되었는지 검증하고 보고서를 제출합니다.