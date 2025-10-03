[# Include moved from expert-book/index.md]
# 📚 AI 인스트럭션 고급서 — Power User Edition

> 이 개정판은 ‘설명’보다 ‘구동’을 우선합니다. VS Code, 터미널, 스크립트, 워크플로우를 통해 AI를 실무 자동화로 연결하는 방법을 다룹니다.

## Part 1. 실전 기초: 질문에서 자동화까지
- [01. 프롬프트와 인스트럭션: 자동화를 위한 관점 전환](01-introduction.md)
- [02. 질문 설계: 유형을 자동화 객체로 다루기](02-questions.md)
- [03. 좋은 인스트럭션: 재현성과 예측 가능성 설계](03-good-instructions.md)

## Part 2. 시스템 설계와 워크플로우
- [04. 인스트럭션 메타 원칙: 운영 환경에서의 원칙 적용](04-meta-principles.md)
- [05. 에이전트와 제약: 책임경계와 실패 안전장치](05-agent-constraints.md)
- [06. 입력/출력 계약: 스키마, 검증, 구조화 출력](06-input-output.md)
- [07. 워크플로우 패턴: 파이프라인/생성-검증/라우팅 실전화](07-process-workflow.md)
- [08. 성능 최적화: 비용·속도·품질 트레이드오프](08-performance.md)
- [09. 생산성 확장: 편집기·매크로·캐시·템플릿](09-productivity.md)

## Part 3. 협업 아키텍처와 운영
- [10. 고급 협업 아키텍처: 아키텍트-워커·비평가·라우터](10-advanced-collaboration-architectures.md)
- [11-1. 단일 에이전트 패턴: 고도화된 사용 패턴 모음](11-1-single-agent-patterns.md)
- [11-2. 조직 표준: 보안·컴플라이언스·비밀·로그 정책](11-2-organizational-standards.md)
- [12. 도구 통합: CLI/VS Code/로컬 LLM/관측성](12-tools.md)
- [13. Workflow as Code: just/Make/CI와 재현성](13-workflow-as-code.md)
- [14. 진화: 평가·회귀·지속개선 루프 설계](14-evolution.md)
- [15. 마무리: 자동화 문해력과 인간의 역할](15-conclusion.md)

부록
- 실행에 필요한 공통 전제: Python 3.10+, VS Code, jq/yq, curl, just 또는 make, 선택적 로컬 LLM(ollama) 및 클라우드 CLI(openai/anthropic)
- 예제는 모두 로컬에서 재현 가능하도록 설계되었습니다. 네트워크/자격증명이 필요한 경우, 명시적으로 주석 처리합니다.

