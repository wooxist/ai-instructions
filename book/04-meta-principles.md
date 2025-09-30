# 4장. 인스트럭션 설계의 메타 원칙

**1부: 인스트럭션의 기초와 설계 원칙**

**목적:** 좋은 지시를 일관되게 만들고 유지·개선하기 위한 메타 원칙을 익힌다.

### 이 장에서 배우는 것
- 좋은 설계를 위한 상위 원칙(SSOT, SoC 등)을 먼저 학습하여 전체적인 관점을 잡는다.
- 각 원칙의 좋은/나쁜 예와 짧은 체크리스트
- 이 원칙들이 이후 장들(역할, 입/출력, 처리 방법)에 어떻게 적용되는지 이해한다.

범위 밖: 모델 학습 내부(RLHF, 파인튜닝 등)와 저수준 아키텍처는 다루지 않습니다. 필요 시 마지막 부분에서 참고 링크로 연결합니다.

## 4.1 구조적/조직적 원칙 (Framework & Organization)
설계의 “뼈대”를 정하는 원칙입니다. 한 번 정하면 모든 장과 템플릿이 이를 따릅니다.

### 4.1.1 SSOT (Single Source of Truth)[^1]
- 핵심 정의·템플릿·용어의 “공식 출처”를 1곳으로 고정합니다.
- 좋은 예: 지침·템플릿·용어집의 공식 출처를 `AGENTS.md`와 `book/index.md`에 두고, 본문에서는 요약만 싣고 상대 링크로 연결
- 나쁜 예: 동일 규칙이 여러 파일에 중복·불일치(수정 누락·충돌 발생)
- 체크: “이 정의의 원 출처는 어디인가?”를 본문에 명시(상대 링크)

### 4.1.2 SoC (Separation of Concerns)[^2]
- 하나의 소제목은 하나의 결과/목표만 다룹니다(겹침 최소화).
- 좋은 예: 형식 지정은 [6장](06-input-output.md)에서, 역할 정의는 [5장](05-agent-constraints.md)에서 각각 다루고 교차참조
- 나쁜 예: 한 소제목에 형식·컨텍스트·성공 기준을 모두 뒤섞어 기술
- 체크: 소제목별 “주제·목표·결과”가 1:1:1인지 확인

### 4.1.3 MECE (Mutually Exclusive, Collectively Exhaustive)[^3]
- 겹치지 않게 분류하되, 해당 범위를 빠짐없이 커버합니다.
- 좋은 예: 오류 유형을 입력(형식·데이터·정책) vs. 처리(재시도·요약·거절)로 나눠 중복 최소화
- 나쁜 예: 유사한 항목을 다른 이름으로 반복(“포맷 오류”/“형식 문제”)
- 체크: 분류표에 상호배타/전체포괄 표기(겹침 0, 빈칸 0)

### 4.1.4 Convention over Configuration[^4]
- 관례를 먼저 정하고, 꼭 필요할 때만 예외 설정을 허용합니다.
- 좋은 예: 기본 출력은 불릿 4–6개, 표는 마크다운 3열, JSON은 스키마 준수
- 나쁜 예: 매 과업마다 형식·길이를 처음부터 재협의(지연·불일치 발생)
- 체크: “기본 관례→예외 선언→검증” 순서가 문서에 보이는가

### 4.1.5 확장성(Scalability)[^5]
- 장·섹션·체크리스트가 개별 작업→프로젝트→조직 표준으로 자연스레 확장되게 설계합니다.
- 좋은 예: 장 공통 체크리스트를 리포지토리 전반의 PR 템플릿으로 재사용
- 나쁜 예: 특정 사례에만 맞춘 지침(다른 팀/과업에 이식 불가)
- 체크: “다른 팀이 그대로 가져가도 작동하는가?”

## 4.2 실행/작동 방식 원칙 (Execution & Process)
어떻게 일할지에 관한 루틴입니다. 좋은 결과는 좋은 루틴에서 나옵니다.

### 4.2.1 점진적 개선(Iterative Refinement)[^6]
- 초안을 빠르게 만들고, 피드백으로 짧은 주기의 개선을 반복합니다.
- 좋은 예: 개요→합의→본문→검사 스텝을 명시하고 각 단계 산출·성공 기준 포함
- 나쁜 예: 처음부터 완벽본 작성 시도(시간 과다·방향 빗나감)
- 체크: 단계별 산출물과 성공 기준이 문서에 존재하는가

### 4.2.2 자기 계획·검토(Auto-Planning & Review)[^7]
- 모델이 스스로 TODO/계획을 제안하고 진행 중 업데이트합니다.
- 좋은 예: “계획→수행→자체 리뷰→수정” 루프를 출력 형식에 내장
- 나쁜 예: 긴 작업을 단일 응답으로 시도(실패해도 복구 경로 없음)
- 체크: 계획/리뷰 로그가 남고, 다음 행동이 항상 제시되는가

### 4.2.3 자기 피드백 루프(Self-Feedback Loop)[^8]
- 산출물 기준으로 스스로 품질을 점검하고 보완합니다.
- 좋은 예: 체크리스트 통과율·누락 항목·수정사항을 보고 후 재생성
- 나쁜 예: 결과만 출력하고 자기 평가 없음
- 체크: “평가→수정”의 증거가 본문/로그에 남는가

### 4.2.4 산출물 중심(Output-Driven)[^9]
- 과정보다 출력 요건(형식·성공 기준·수용 조건)을 우선합니다.
- 좋은 예: “필수 필드 100%, 불릿 4–6개, 길이 N자” 등 검증 가능한 요구 명시
- 나쁜 예: “충분히 자세히” 같은 모호 표현 중심
- 체크: 기계/사람이 검증 가능한 출력 사양이 있는가

### 4.2.5 의도 확인 루프(Intent Clarification Loop)[^10]
- 목표·범위·우선순위가 명확해질 때까지 짧게 질의응답합니다.
- 좋은 예: “목표/대상/제약/형식” 4문으로 확인 후 본 작업 착수([6장](06-input-output.md) 참조)
- 나쁜 예: 모호한 요구를 그대로 수용해 재작업 유발
- 체크: 착수 전 합의된 목표·범위가 기록되었는가

## 4.3 검토/검증 원칙 (Validation & Review)
품질을 ‘만드는’ 동시에 ‘증명’하는 장치입니다.

### 4.3.1 비판적 검토(Critical Review)
- 사실·일반화 문장에 근거를 연결하거나 톤을 완화합니다.
- 좋은 예: “출처 없음” 문장은 단정 대신 추정·제한 표현으로 전환
- 나쁜 예: 강한 단정·숫자 제시 후 근거 부재
- 체크: 근거 링크 또는 톤 완화 규칙이 적용되었는가

### 4.3.2 오류 대응(Error Handling)
- 불완전/오류 출력에 대한 재시도·요약·거절 전략을 사전에 정의합니다.
- 좋은 예: JSON 유효성 실패→자동 재생성, 정책 위반 가능→요약/거절
- 나쁜 예: 실패 상황에서 같은 시도 반복
- 체크: 실패 시 대체 경로(플로우차트/규칙)가 문서화되었는가

### 4.3.3 투명성·추적 가능성(Transparency & Traceability)[^11]
- 결정·출처·근거·버전을 남겨 재현성과 책임소재를 확보합니다.
- 좋은 예: 교차참조는 상대 경로, 상태/버전은 장 하단 표기(본서 규칙 준수)
- 나쁜 예: 외부 링크·개인 메모 의존(사라지면 재현 불가)
- 체크: “왜 이렇게 썼는지”를 파일만으로 재구성 가능한가

## 4.4 책임/가치 원칙 (Governance & Ethics)
실무에서 반드시 필요한 안전선입니다.

### 4.4.1 윤리 경계(Ethical Boundaries)
- 개인정보·저작권·민감 주제는 최소 수집·필요 목적 내 처리·명시적 거절 원칙을 둡니다.
- 좋은 예: 민감 데이터는 가명화·요약만 허용, 법률 자문은 일반 원칙+전문가 상담 권고
- 나쁜 예: 출처 불명 데이터 재사용, 규제 해석 단정
- 체크: 민감 주제 처리·거절 문구가 템플릿에 포함되었는가

### 4.4.2 Human-in-the-Loop[^12]
- 중요한 의사결정·출시·대외 커뮤니케이션에는 사람 검토·승인을 끼워 넣습니다.
- 좋은 예: “모델 제안→사람 검토→승인/수정→배포” 게이트 명시
- 나쁜 예: 자동 생성물의 즉시 대외 노출
- 체크: 위험도에 따른 리뷰 단계가 운영 문서에 반영되었는가

---

## 참고 자료

---

## 참고 자료

- Fowler, M. (2002). Patterns of enterprise application architecture. Addison-Wesley Professional.
- Martin, R. C. (2009). Clean code: A handbook of agile software craftsmanship. Pearson Education.
- Evans, E. (2004). Domain-driven design: Tackling complexity in the heart of software. Addison-Wesley Professional.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design patterns: Elements of reusable object-oriented software. Pearson Education.
- Rasmusson, J. (2010). The agile samurai: How agile masters deliver great software. Pragmatic Bookshelf.
- McKinsey & Company. (2018). The MECE Principle: A Guide to Clear Thinking.
- Google. (2023). Machine Learning Glossary. https://developers.google.com/machine-learning/glossary
- IEEE. (2023). Ethically Aligned Design: A Vision for Prioritizing Human Well-being with Autonomous and Intelligent Systems.
 

---

[^1]: Single Source of Truth: 한 조직/프로젝트에서 공식적으로 인정한 단일한 지식·정의·템플릿의 원천.
[^2]: Separation of Concerns: 기능·역할을 분리해 변경 영향과 결합도를 줄이는 원칙.
[^3]: Mutually Exclusive, Collectively Exhaustive: 겹치지 않되 전체를 빠짐없이 포괄하는 분류 원칙.
[^4]: Convention over Configuration: 관례를 우선하고, 필요할 때만 설정으로 예외를 선언하는 접근(예: Ruby on Rails의 철학).
[^5]: Scalability: 요소·프로세스·규칙이 규모·복잡도 증가에도 성능·유지보수성을 유지하도록 설계하는 성질.
[^6]: Iterative Refinement: 초안→피드백→개선의 짧은 주기를 반복해 품질을 끌어올리는 방식.
[^7]: Auto-Planning: 모델이 스스로 할 일 목록과 순서를 제안·갱신하는 기법(계획 로그 포함).
[^8]: Feedback Loop: 산출물 기반의 자기 점검→수정 반복 루프.
[^9]: Output-Driven: 중간 과정보다 출력 요건(형식·성공 기준)을 우선하는 접근.
[^10]: Clarification Loop: 목적·범위를 질문으로 명확히 한 뒤 작업에 착수하는 절차.
[^11]: Traceability: 결정·출처·근거·버전을 남겨 재현 가능성을 보장하는 특성.
[^12]: Human-in-the-Loop: 중요한 의사결정 단계에 사람의 검토·승인을 포함시키는 운영 원칙.

**상태:** v1-draft  
**작성 시작일:** 2025-09-27
