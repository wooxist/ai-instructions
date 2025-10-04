# 에이전트 설계 방법론

> 이 문서는 메타 에이전트가 새로운 아키텍트 및 워커 에이전트를 설계할 때 따라야 할 구체적인 방법론을 제공합니다.

## 1. 에이전트 범위 결정

### 1.1 물리적 제약: 컨텍스트 윈도우

**토큰 예산 개념**:
```
총 컨텍스트 윈도우 = 인스트럭션 + 입력 데이터 + 출력 데이터
```

**경험 법칙**:
1. **인스트럭션 비율**: 전체 컨텍스트의 20-30% 이하로 유지
2. **분리 기준**: `[인스트럭션 길이] + [평균 입력 데이터] > [컨텍스트의 70%]` → 에이전트 분리 고려
3. **최소 기능 인스트럭션**: 작동하는 가장 짧은 버전으로 시작, 필요시 점진적 확장

**예시**:
```markdown
# 나쁜 예: 하나의 거대 에이전트 (15,000 토큰 인스트럭션)
- 고객 분류, 감성 분석, 보고서 생성을 모두 담당
- 컨텍스트 윈도우 포화 위험

# 좋은 예: 3개의 작은 에이전트
1. 분류 에이전트 (3,000 토큰)
2. 분석 에이전트 (3,000 토큰)
3. 보고 에이전트 (3,000 토큰)
```

### 1.2 설계 원칙: 단일 책임 (SRP)

에이전트 분리 여부는 다음 3가지 관점으로 판단:

#### 전문성 (Expertise)
**질문**: 서로 다른 전문 지식을 요구하는가?

**예시**:
```yaml
# 분리 필요
- UI 디자인 에이전트  # 디자인 전문성
- DB 스키마 에이전트  # 데이터베이스 전문성

# 통합 가능
- 버튼 생성 에이전트
- 텍스트 필드 생성 에이전트
→ 통합: UI 위젯 에이전트 (하나의 목적: UI 컴포넌트 생성)
```

#### 재사용성 (Reusability)
**질문**: 다른 워크플로우에서도 재사용될 수 있는가?

**예시**:
```markdown
# 독립 에이전트로 만들 가치가 있음
- 코드 리뷰 에이전트: 모든 코드 생성 작업에 재사용
- PDF 파싱 에이전트: 다양한 문서 분석 작업에 재사용

# 특정 워크플로우에만 사용
- 주간 보고서 서론 작성: 재사용성 낮음
```

#### 응집도 (Cohesion)
**질문**: 하나의 목적을 위해 긴밀하게 묶여 있는가?

**예시**:
```markdown
# 높은 응집도 (하나의 에이전트)
- 이메일 형식 검증
- 이메일 내용 생성  
- 이메일 서명 추가
→ 모두 "이메일 생성"이라는 단일 목적

# 낮은 응집도 (분리 필요)
- 이메일 생성
- SQL 쿼리 실행
→ 서로 관련 없는 작업
```

## 2. AI의 한계 극복 전략

### 2.1 할루시네이션 방지

#### 방법 1: 근거 기반 책임 부여
```markdown
## 역할
데이터 분석가

## 제약 조건 (할루시네이션 방지)
1. 제공된 데이터셋 외의 정보는 절대 사용하지 말 것
2. 모든 수치는 반드시 출처 데이터의 행/컬럼을 명시할 것
3. 추측이 필요하면 "데이터 부족으로 판단 불가"라고 명시할 것
```

#### 방법 2: 지식 출처 한정 (SSOT)
```yaml
agents:
  - name: research-agent
    knowledge_sources:
      - corpus_id: "company_docs_v2.3"  # 허용된 문서만
      - database: "customer_db"
    constraints:
      - "외부 인터넷 검색 금지"
      - "모든 인용은 corpus_id와 페이지 번호 포함"
```

#### 방법 3: 검증 에이전트 분리
```yaml
workflow:
  - step: generate_content
    agent: content-writer
  - step: verify_facts
    agent: fact-checker  # 생성된 내용 검증 전담
    inputs:
      - original_sources: "..."
      - generated_content: "step1_output"
```

### 2.2 비일관성 문제 해결

#### 방법 1: 페르소나 구체화
```markdown
# 나쁜 예
## 역할
변호사

# 좋은 예
## 역할
20년차 기업 법무팀 변호사
- 법률 용어를 정확히 사용하되
- 고객에게는 중학생도 이해할 수 있는 평이한 언어로 설명
- 단정적 조언 대신 "~할 가능성이 있습니다" 형태로 표현
```

#### 방법 2: 구조화된 출력 강제
```json
{
  "output_schema": {
    "type": "object",
    "properties": {
      "decision": {
        "type": "string",
        "enum": ["approve", "reject", "revision_needed"]
      },
      "reasoning": {"type": "string"},
      "confidence": {
        "type": "number",
        "minimum": 0,
        "maximum": 100
      }
    },
    "required": ["decision", "reasoning"]
  }
}
```

## 3. 입출력 설계

### 3.1 출력 우선 설계 (Output-Driven)

**원칙**: 원하는 출력을 먼저 정의한 후, 필요한 입력을 역산

**예시**: 번역 에이전트

**Step 1: 출력 정의**
```json
{
  "original_text": "...",
  "translated_text": "...",
  "style": "formal|casual|poetic",
  "explanation": "번역 스타일 선택 이유"
}
```

**Step 2: 필요 입력 역산**
```markdown
## 입력
- source_text: 번역할 원문
- target_language: 목표 언어
- style_preference: formal|casual|poetic
- context: 번역 목적 (비즈니스 문서, SNS 게시물 등)
```

### 3.2 구조화된 출력 기법

#### 기법 1: JSON Schema
```markdown
## 출력 형식
아래 스키마를 준수하는 JSON만 출력할 것

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "summary": {
      "type": "string",
      "maxLength": 500
    },
    "categories": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["bug", "feature", "question"]
      },
      "minItems": 1
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5
    }
  },
  "required": ["summary", "categories", "priority"]
}
```

#### 기법 2: Few-Shot 예시
```markdown
## 출력 예시

입력: "앱이 자꾸 꺼져요"
출력:
{
  "summary": "앱 강제 종료 이슈",
  "categories": ["bug"],
  "priority": 5
}

입력: "다크모드 지원 언제 되나요?"
출력:
{
  "summary": "다크모드 기능 요청",
  "categories": ["feature"],
  "priority": 3
}

이제 주어진 입력을 동일한 형식으로 처리하세요.
```

#### 기법 3: 평가 기준 명시
```markdown
## 평가 기준
이 요약문의 품질은 다음 기준으로 평가됩니다:
1. 핵심 내용 포함 여부 (필수)
2. 300단어 미만 (필수)
3. 중학생도 이해 가능한 언어 사용 (필수)
4. 불필요한 기술 용어 없음

출력 전 위 기준을 스스로 체크하세요.
```

### 3.3 입력 설계

#### 체계적 컨텍스트 제공
```markdown
## 컨텍스트 (구조화)

### 최종 목표
고객 만족도 향상을 위한 개선 방안 도출

### 대상 독자
- 1차: 제품팀 리더 (기술적 배경 있음)
- 2차: 경영진 (비기술적, 의사결정 중심)

### 제약 사항
- 예산: 월 5백만원 이하
- 기간: 3개월 내 실행 가능한 방안
- 기술 스택: 현재 Python/React 기반 유지

### 참고 자료
- customer_feedback_2024Q4.csv
- product_roadmap_2025.md
```

#### 데이터 전처리
```markdown
## 입력 데이터 전처리 규칙
1. CSV 파일: 
   - 컬럼명 공백 제거
   - 빈 행 삭제
   - 날짜 형식 통일 (YYYY-MM-DD)

2. 텍스트:
   - HTML 태그 제거
   - 특수문자 정규화
```

## 4. 동적 명세 기법: 의도 확인 루프

모호한 요청을 받았을 때 실행 전 명세를 구체화하는 전략:

```markdown
## 처리 방법
1. 입력 검증: 다음 정보가 모두 있는지 확인
   - 대상 독자
   - 분량
   - 톤앤매너

2. 불충분 시 질문 생성:
   "번역을 진행하기 전에 확인이 필요합니다:
   - 대상 독자: 누구를 위한 번역인가요? (일반인/전문가)
   - 톤앤매너: 어떤 분위기를 원하시나요? (격식/캐주얼/전문적)
   - 분량: 원문 길이를 유지해야 하나요, 요약도 가능한가요?"

3. 응답 받은 후 작업 수행
```

## 5. 에이전트 설계 템플릿

### 5.1 워커 에이전트 템플릿

```markdown
# [에이전트 이름] (예: CSV 데이터 추출기)

## 1. 목적
[한 문장 목표]

## 2. 역할
[전문가 페르소나]

## 3. 입력
### 필수
- param1: [설명, 타입, 예시]
- param2: [설명, 타입, 예시]

### 선택
- param3: [설명, 기본값]

## 4. 처리 방법
1. [단계 1]
2. [단계 2]
3. [단계 3]

## 5. 출력
### 형식
[JSON Schema 또는 구조 설명]

### 예시
```json
{
  "field1": "value1",
  "field2": 123
}
```

## 6. 제약 조건
### 필수
- [지켜야 할 규칙 1]
- [지켜야 할 규칙 2]

### 금지
- [하지 말아야 할 것 1]
- [하지 말아야 할 것 2]

## 7. 평가 기준
- [ ] [기준 1]
- [ ] [기준 2]
- [ ] [기준 3]

## 8. 기초 지식
[항상 참고할 원칙이나 배경지식]
```

### 5.2 아키텍트 에이전트 템플릿

```markdown
# [아키텍트 이름] (예: 콘텐츠 생성 아키텍트)

## 1. 목적
[복잡한 워크플로우의 목표]

## 2. 역할
프로젝트 매니저 / 워크플로우 설계자

## 3. 책임
1. Work Breakdown: [작업 분해 방법]
2. 워커 할당: [적합한 워커 선택 기준]
3. 산출물 검증: [검증 방법]
4. 예외 처리: [실패 시 대응]

## 4. 관리 대상 워커
- worker1: [역할]
- worker2: [역할]
- worker3: [역할]

## 5. 워크플로우
```yaml
steps:
  - name: [단계명]
    agent: [워커명]
    inputs: [...]
    outputs: [...]
    validation: [검증 기준]
```

## 6. 검증 전략
### 직접 평가
- [파일 존재 확인]
- [형식 검증]

### 평가자 위임
```yaml
- name: verify_quality
  agent: evaluator-agent
  inputs:
    - generated_output: "step3_output"
  acceptance:
    - score >= 80
```

## 7. 실패 처리
- 재시도: 최대 [N]회
- 롤백: [조건]
- 에스컬레이션: [사람 개입 조건]

## 8. 로깅
모든 워커 작업을 `_job_log.json`에 기록:
```json
{
  "job_id": "...",
  "status": "running|completed|failed",
  "history": [
    {"task": "...", "agent": "...", "status": "...", "timestamp": "..."}
  ]
}
```
```

## 6. 실전 예시: 단계별 설계 과정

### 시나리오
"고객 리뷰를 분석하여 주간 보고서를 생성하는 에이전트가 필요하다"

### Step 1: 작업 분해 (Breakdown)
```
고객 리뷰 분석
├─ 1. 리뷰 분류 (제품/배송/CS)
├─ 2. 감성 분석 (긍정/부정/중립)
├─ 3. 핵심 키워드 추출
└─ 4. 보고서 생성
```

### Step 2: 에이전트 범위 결정
- 각 단계가 다른 전문성 필요 → 분리
- 컨텍스트 확인: 각 단계 3,000 토큰 이내 → OK

### Step 3: 워커 에이전트 설계

**워커 1: 리뷰 분류기**
```markdown
# 고객 리뷰 분류기

## 목적
고객 리뷰를 제품/배송/CS 카테고리로 분류

## 역할
데이터 분류 전문가

## 입력
- review_text: string

## 출력
```json
{
  "review_id": "R123",
  "category": "product|delivery|cs",
  "confidence": 0.95
}
```

## 제약
- confidence < 0.7이면 "uncertain" 반환
```

**워커 2, 3, 4**: (유사한 방식으로 설계)

### Step 4: 아키텍트 에이전트 설계

```markdown
# 고객 리뷰 분석 아키텍트

## 목적
주간 고객 리뷰 분석 보고서 생성

## 워크플로우
```yaml
steps:
  - name: classify
    agent: review-classifier
    inputs: {reviews: "input.csv"}
    outputs: {file: "classified.json"}
    
  - name: analyze_sentiment
    agent: sentiment-analyzer
    inputs: {reviews: "classified.json"}
    outputs: {file: "analyzed.json"}
    
  - name: extract_keywords
    agent: keyword-extractor
    inputs: {reviews: "analyzed.json"}
    outputs: {file: "keywords.json"}
    
  - name: generate_report
    agent: report-generator
    inputs:
      - classified: "classified.json"
      - analyzed: "analyzed.json"
      - keywords: "keywords.json"
    outputs: {file: "weekly_report.json"}
```

## 검증
각 단계 완료 시:
- 파일 존재 확인
- JSON 스키마 검증
- status = "success" 확인
```

## 7. 체크리스트

새 에이전트 설계 시 확인:

### 기본
- [ ] 8가지 구성 요소 모두 정의됨
- [ ] 입출력 형식이 명확함
- [ ] 제약 조건이 명시됨

### 컨텍스트 윈도우
- [ ] 인스트럭션이 전체의 20-30% 이하
- [ ] 평균 입력 데이터 고려 시 70% 초과하지 않음

### 단일 책임
- [ ] 하나의 명확한 전문성
- [ ] 다른 워크플로우에서 재사용 가능
- [ ] 높은 응집도

### 할루시네이션 방지
- [ ] 지식 출처 한정
- [ ] 근거 인용 요구
- [ ] 필요시 검증 에이전트 분리

### 출력 품질
- [ ] 구조화된 형식 (JSON Schema)
- [ ] Few-shot 예시 포함
- [ ] 평가 기준 명시
