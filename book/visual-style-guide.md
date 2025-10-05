# 시각 자료 스타일 가이드 (Mermaid)

본 가이드는 가이드북 전반의 Mermaid 다이어그램을 일관된 스타일로 작성하기 위한 규칙을 제공합니다.

## 기본 테마 초기화 스니펫

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

## 도형과 의미 매핑

- 개념/원칙: 직사각형 `id[Text]`
- 결정(분기): 마름모 `id{Question}`
- 에이전트(역할): 둥근 사각형 `id(Text)`
- 산출물/문서: 서브루틴 `id[[Artifact]]`
- 데이터/저장소/로그: 실린더 `id[(Data)]`
- 사람(Human-in-the-Loop): 원형 `id((Human))`

## 공통 클래스 정의 (선택)

아래 클래스를 필요 시 다이어그램에 포함해 시맨틱 강조를統一합니다.

```mermaid
%% 클래스 예시 (다이어그램 내부에 포함)
classDef principle fill:#1f77b4,stroke:#1f77b4,color:#ffffff;
classDef decision fill:#ffffff,stroke:#495057,stroke-width:2px,color:#212529;
classDef agent fill:#6f42c1,stroke:#6f42c1,color:#ffffff;
classDef artifact fill:#17a2b8,stroke:#17a2b8,color:#ffffff;
classDef data fill:#2ca02c,stroke:#2ca02c,color:#ffffff;
classDef human fill:#e83e8c,stroke:#e83e8c,color:#ffffff;
```

## 레이아웃 규칙

- 흐름 방향: 기본 `LR`(좌→우), 복잡한 경우 `TD` 사용
- 서브그래프: 팀/조직/모듈 경계를 표현할 때 사용, 제목은 역할 기준
- 라벨: 동사+목적어 5–7단어 이내, 핵심만 기입
- 간선: 의미 있는 곳에만 라벨(예/아니오, 승인/반려 등)

## 작성 팁

- 다이어그램마다 1가지 메시지에 집중합니다(“한 장에 한 메시지”).
- 산출물을 명시하고(파일·JSON 등), 다음 단계 입력과 연결합니다.
- 검증/승인 게이트는 `human_in_the_loop` 노드로 강조합니다.
