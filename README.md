# AI 인스트럭션 설계 가이드북
부제: 원칙 · 실무 · 성능 최적화

---

## 📌 프로젝트 개요
이 프로젝트는 AI와 협업할 때 필요한 **인스트럭션 설계 원칙**과 **실무 적용 방법**을 정리한 가이드북입니다.  
단순 프롬프트를 넘어, **재현성·협업성·생산성**을 보장하는 "인스트럭션 세트"를 구축하고,  
이를 개인/조직 환경에서 활용할 수 있도록 합니다.  

---

## 🎯 목적
- **조직 환경(기업/팀 단위)**:  
  주니어도 바로 투입 가능하고, 팀이 공유할 수 있는 표준 인스트럭션 구축.  
- **개인 환경(1인 개발자/스타트업)**:  
  다양한 전문 영역을 AI와 함께 커버하며, 하나의 서비스/제품을 직접 운영할 수 있도록 지원.  

---

## 📚 목차

- **1장. 프롬프트와 인스트럭션 이해하기** — [바로가기](book/01-introduction.md)  
  *목적: 프롬프트와 인스트럭션이 무엇인지, 그리고 왜 중요한지 기본 개념을 익힌다.*

- **2장. 인스트럭션 설계에 필요한 사전 지식** — [바로가기](book/02-meta-principles.md)  
  *목적: 좋은 지침을 만들기 위해 알아야 할 메타 원칙 15가지를 학습한다.*

- **3장. 좋은 지시(명령)의 원칙** — [바로가기](book/03-good-instructions.md)  
  *목적: 명령문 자체의 품질을 높이는 법을 배운다.*

- **4장. 질문 설계하기** — [바로가기](book/04-questions.md)  
  *목적: AI의 답변을 원하는 방향으로 이끌기 위해 질문을 잘 만드는 방법을 배운다.*

- **5장. 기본 정보 채워넣기** — [바로가기](book/05-context.md)  
  *목적: AI가 혼동하지 않도록 필수 정보를 제공하는 법을 익힌다.*

- **6장. Agent 설계와 Persona 정의** — [바로가기](book/06-agent-persona.md)  
  *목적: AI에게 특정 역할과 성격을 부여하여 전문성을 강화한다.*

- **7장. 실무 활용하기** — [바로가기](book/07-practical.md)  
  *목적: 개인과 조직 상황에서 AI 인스트럭션을 실제로 적용하는 방법을 배운다.*

- **8장. 도움이 되는 도구** — [바로가기](book/08-tools.md)  
  *목적: 인스트럭션 관리와 실무 지원에 활용할 수 있는 툴들을 소개한다.*

- **9장. 퍼포먼스에 영향을 미치는 요인** — [바로가기](book/09-performance.md)  
  *목적: 인스트럭션의 성능에 영향을 주는 요소들을 이해한다.*

- **10장. 생산성 측정 & 명령어 검증** — [바로가기](book/10-productivity.md)  
  *목적: 지침의 성능을 검증하고 개선하는 방법을 배운다.*

- **11장. 환경 변화와 인스트럭션의 진화** — [바로가기](book/11-evolution.md)  
  *목적: 조직 규모와 업무 방식의 변화에 맞춰 지침을 발전시키는 방법을 다룬다.*

- **12장. MCP(Model Context Protocol)와 인스트럭션의 미래** — [바로가기](book/12-mcp-future.md)  
  *목적: 인스트럭션 관리와 연결의 미래 기술을 이해한다.*

### 자료/세트 바로가기
- **전체 목차 및 개요** — [바로가기](book/index.md)
- **인스트럭션 세트** — [summary.md](book/instruction-sets/summary.md), [qa.md](book/instruction-sets/qa.md), [agent.md](book/instruction-sets/agent.md)
- **참고 자료** — [references.md](book/resources/references.md), [notes.md](book/resources/notes.md)

---

## 📂 프로젝트 구조

```plaintext
ai-instruction-guide/
├── README.md                        # 프로젝트 개요 + 목차
│
└── book/                            # 모든 원고와 자료 관리
    ├── 01-introduction.md           # 1장: 프롬프트와 인스트럭션 이해하기
    ├── 02-meta-principles.md        # 2장: 인스트럭션 설계에 필요한 사전 지식
    ├── 03-good-instructions.md      # 3장: 좋은 지시(명령)의 원칙
    ├── 04-questions.md              # 4장: 질문 설계하기
    ├── 05-context.md                # 5장: 기본 정보 채워넣기
    ├── 06-agent-persona.md          # 6장: Agent 설계와 Persona 정의
    ├── 07-practical.md              # 7장: 실무 활용하기
    ├── 08-tools.md                  # 8장: 도움이 되는 도구
    ├── 09-performance.md            # 9장: 퍼포먼스에 영향을 미치는 요인
    ├── 10-productivity.md           # 10장: 생산성 측정 & 명령어 검증
    ├── 11-evolution.md              # 11장: 환경 변화와 인스트럭션 진화
    ├── 12-mcp-future.md             # 12장: MCP와 인스트럭션의 미래
    ├── index.md                     # 전체 목차 및 개요
    │
    ├── instruction-sets/            # 실행 가능한 인스트럭션 세트
    │   ├── summary.md               # 요약 인스트럭션
    │   ├── qa.md                    # 질문 설계 인스트럭션
    │   ├── agent.md                 # Persona/Agent 인스트럭션
    │   └── ...
    │
    └── resources/                   # 참고 자료 및 노트
        ├── references.md
        └── notes.md
```

 
