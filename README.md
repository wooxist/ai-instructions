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

### 1장. 인스트럭션 이해하기 — [바로가기](book/chapters/01-introduction/index.md)
- 1.1 인스트럭션과 프롬프트의 차이  
 - 1.1 프롬프트와 인스트럭션: 정의와 관계  
- 1.2 인스트럭션 설계의 필요성  
- 1.3 실제 활용 사례  

### 2장. 인스트럭션 라이프 사이클 — [바로가기](book/chapters/02-lifecycle/index.md)
- 2.1 목적 정의  
- 2.2 초안 작성  
- 2.3 테스트 실행  
- 2.4 평가  
- 2.5 수정 & 최적화  
- 2.6 재사용 & 축적  
- 2.7 피드백 루프  

### 3장. 좋은 지시(명령)의 원칙 — [바로가기](book/chapters/03-good-instructions/index.md)
- 3.1 명확성 (Clear)  
- 3.2 구체성 (Specific)  
- 3.3 단계성 (Step-wise)  
- 3.4 제약 조건과 한계 설정  
- 3.5 실패하는 지시의 특징  

### 4장. 질문 설계하기 — [바로가기](book/chapters/04-questions/index.md)
- 4.1 폐쇄형 질문 (Closed-ended)  
- 4.2 개방형 질문 (Open-ended)  
- 4.3 탐색형 질문 (Exploratory)  
- 4.4 비교형 질문 (Comparative)  
- 4.5 맥락 의존형 질문 (Context-dependent)  
- 4.6 메타 질문 (Meta-questions)  

### 5장. 기본 정보 채워넣기 — [바로가기](book/chapters/05-context/index.md)
- 5.1 컨텍스트(Context) 제공하기  
- 5.2 출력 형식 지정 (표, JSON, Markdown 등)  
- 5.3 Few-shot / Zero-shot 예시 활용  

### 6장. Agent 설계와 Persona 정의 — [바로가기](book/chapters/06-agent-persona/index.md)
- 6.1 Persona 기반 설계의 필요성  
- 6.2 역할(Role) 구체화 방법  
- 6.3 경계 지점 설정하기 (Boundary Conditions)  
- 6.4 멀티에이전트 협업 설계  

### 7장. 실무 활용하기 — [바로가기](book/chapters/07-practical/index.md)
- 7.1 조직형 실무 사례 (분업형 환경)  
- 7.2 개인형 실무 사례 (1인 개발자/스타트업)  
- 7.3 실습: 조직 vs 개인 시나리오 비교  

### 8장. 도움이 되는 도구 — [바로가기](book/chapters/08-tools/index.md)
- 8.1 Prompt 관리 도구 (Notion, Obsidian, GitHub)  
- 8.2 RAG/Agent 프레임워크 (LangChain, LlamaIndex)  
- 8.3 성능 평가 및 추적 도구 (PromptLayer, W&B 등)  

### 9장. 퍼포먼스에 영향을 미치는 요인 — [바로가기](book/chapters/09-performance/index.md)
- 9.1 인스트럭션 품질 (명확성, 구체성, 길이)  
- 9.2 모델 특성 (버전, Temperature, Top-p 등)  
- 9.3 컨텍스트 크기와 데이터 최신성  
- 9.4 사용자 피드백 루프  

### 10장. 생산성 측정 & 명령어 검증 — [바로가기](book/chapters/10-productivity/index.md)
- 10.1 성능 지표 (정확도, 간결성, 재현율, 만족도)  
- 10.2 A/B 테스트 및 비교 실험  
- 10.3 검증과 개선 사이클  
- 10.4 정형화된 업무 vs 비정형적 업무의 인스트럭션 설계  

### 11장. 환경 변화와 인스트럭션의 진화 — [바로가기](book/chapters/11-evolution/index.md)
- 11.1 1인 → 조직 확장: 팀 단위 인스트럭션 표준화  
- 11.2 조직 → 업무 통합: 멀티직무 인스트럭션 설계  
- 11.3 경계 조건 재설정  
- 11.4 개인 지시 → 팀 자산으로 발전  

### 12장. MCP(Model Context Protocol)와 인스트럭션의 미래 — [바로가기](book/chapters/12-mcp-future/index.md)
- 12.1 MCP란 무엇인가  
- 12.2 멀티에이전트·도구 연결에서의 필요성  
- 12.3 인스트럭션 전달·관리에서 MCP의 역할  
- 12.4 실무 적용 시나리오  
- 12.5 향후 전망  

### 자료/세트 바로가기
- 인스트럭션 세트: [book/instruction-sets/](book/instruction-sets/) — [summary.md](book/instruction-sets/summary.md), [qa.md](book/instruction-sets/qa.md), [agent.md](book/instruction-sets/agent.md)
- 참고 자료: [book/resources/](book/resources/) — [references.md](book/resources/references.md), [notes.md](book/resources/notes.md)

---

## 📂 프로젝트 구조

```plaintext
ai-instruction-guide/
├── README.md                        # 프로젝트 개요 + 목차
│
└── book/                            # 모든 원고와 자료 관리
    ├── chapters/                    # 각 장별 원고
    │   ├── 01-introduction/
    │   │   └── index.md             # 1장: 인스트럭션 이해하기
    │   ├── 02-lifecycle/
    │   │   └── index.md             # 2장: 인스트럭션 라이프 사이클
    │   ├── 03-good-instructions/
    │   │   └── index.md             # 3장: 좋은 지시(명령)의 원칙
    │   ├── 04-questions/
    │   │   └── index.md             # 4장: 질문 설계하기
    │   ├── 05-context/
    │   │   └── index.md             # 5장: 기본 정보 채워넣기
    │   ├── 06-agent-persona/
    │   │   └── index.md             # 6장: Agent 설계와 Persona 정의
    │   ├── 07-practical/
    │   │   └── index.md             # 7장: 실무 활용하기
    │   ├── 08-tools/
    │   │   └── index.md             # 8장: 도움이 되는 도구
    │   ├── 09-performance/
    │   │   └── index.md             # 9장: 퍼포먼스 요인
    │   ├── 10-productivity/
    │   │   └── index.md             # 10장: 생산성 측정 & 검증
    │   ├── 11-evolution/
    │   │   └── index.md             # 11장: 환경 변화와 인스트럭션 진화
    │   └── 12-mcp-future/
    │       └── index.md             # 12장: MCP와 미래
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

 
