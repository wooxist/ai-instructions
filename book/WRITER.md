# WRITER Guide

본 문서는 책 집필과 유지보수 과정에서 합의된 작성 규칙(SSOT)을 정리합니다. 모든 변경은 아래 규칙을 준수해 주세요.

## 1) 구조와 파트 구성
- 파트는 5개로 유지합니다.
  - Part 1: 1–3장 (기초)
  - Part 2: 4–6장 (설계 원칙·구성 요소)
  - Part 3: 7–9장 (워크플로우·성능·평가)
  - Part 4: 10–11장 (아키텍처·설계 패턴)
  - Part 5: 12–15장 (확장·운영)
- 각 장 상단의 Part 라벨과 `book/index.md` 목차의 파트 섹션을 동기화합니다.

## 2) 목차와 교차 링크
- `book/index.md`는 “상세 목차(서브챕터 포함)”를 유지합니다. 서브챕터 목록은 삭제하지 않습니다.
- 내부 링크는 실제 존재하는 파일·섹션으로만 연결합니다. 장·파일명이 변경되면 교차 링크를 즉시 갱신합니다.
- 11장 사례 맵은 `11-1-single-agent.md` 상단에 유지하고, `index.md`에서 해당 섹션으로 앵커 링크를 제공합니다.

## 3) 다이어그램 스타일 (Mermaid)
- 모든 다이어그램은 `%%{init: ...}%%` 스니펫으로 초기화합니다. 기본 스니펫:
  ```mermaid
  %%{init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#1f77b4',
      'primaryTextColor': '#ffffff',
      'primaryBorderColor': '#1f77b4',
      'lineColor': '#6c757d',
      'background': 'transparent',
      'edgeLabelBackground': '#2ca02c'
    }
  }}%%
  ```
- 도형 의미 매핑: 결정=마름모, 에이전트=둥근 사각형, 산출물=서브루틴, 데이터=실린더, Human=원형.
- 공통 클래스는 필요 시 다이어그램 내에 정의합니다(예: `principle`, `decision`, `agent` 등).
- “한 다이어그램=한 메시지” 원칙. 산출물과 다음 입력의 연결을 명시합니다.
- 자세한 기준과 예시는 본 문서의 "부록 A) 시각 자료 스타일 가이드 (Mermaid)"를 참조합니다. 해당 부록이 SSOT이며, `book/visual-style-guide.md`는 부록으로의 안내 역할만 합니다.

## 4) 체크리스트와 실습
- 각 장 말미에 “실습 체크리스트” 섹션을 포함합니다.
  - 형식: “이 장을 완료하셨다면…” + “실습 과제” 1–2개.
- 부록 `book/practice-guide.md`에 장별 심화 과제를 유지합니다.

## 5) SSOT 동기화
- `book/` 업데이트 시 다음을 반드시 점검합니다.
  - `book/index.md`(목차), `README.md`(파트 구조), `ai-knowledge/meta-agent-design/book-summary.md`(요약) 동기화

## 6) TODO 운영
- `book/TODO.md`의 체크박스 상태, 진행률 표, 작업 이력을 업데이트합니다.
- 새로 합의된 규칙은 본 `WRITER.md`에 즉시 반영합니다.

---

## 부록 A) 시각 자료 스타일 가이드 (Mermaid)
본 부록은 가이드북 전반의 Mermaid 다이어그램을 일관된 스타일로 작성하기 위한 SSOT입니다. `book/visual-style-guide.md`는 본 부록으로의 안내(미러) 문서입니다.

### 기본 테마 초기화 스니펫
모든 다이어그램 상단에 아래 스니펫을 붙여 일관된 색상·선 스타일을 적용합니다.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1f77b4',
    'lineColor': '#6c757d',
    'noteBkgColor': '#f8f9fa',
    'noteTextColor': '#212529',
    'background': 'transparent',
    'edgeLabelBackground': '#2ca02c'
  }
}}%%
```

### 도형과 의미 매핑
- 개념/원칙: 직사각형 `id[Text]`
- 결정(분기): 마름모 `id{Question}`
- 에이전트(역할): 둥근 사각형 `id(Text)`
- 산출물/문서: 서브루틴 `id[[Artifact]]`
- 데이터/저장소/로그: 실린더 `id[(Data)]`
- 사람(Human-in-the-Loop): 원형 `id((Human))`

### 공통 클래스 정의 (선택)
필요 시 아래 클래스를 다이어그램에 포함해 시맨틱 강조를 통일합니다.

```mermaid
%% 클래스 예시 (다이어그램 내부에 포함)
classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
```

### 레이아웃 규칙
- 흐름 방향: 기본 `LR`(좌→우), 복잡한 경우 `TD` 사용
- 서브그래프: 팀/조직/모듈 경계를 표현할 때 사용(제목은 역할 기준)
- 라벨: 동사+목적어 5–7단어 이내, 핵심만 기입
- 간선: 의미 있는 곳에만 라벨(예/아니오, 승인/반려 등)

### 작성 팁
- 다이어그램마다 1가지 메시지에 집중합니다(“한 장에 한 메시지”).
- 산출물을 명시하고(파일·JSON 등), 다음 단계 입력과 연결합니다.
- 검증/승인 게이트는 `human_in_the_loop` 노드로 강조합니다.
