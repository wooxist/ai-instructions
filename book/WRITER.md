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
- 자세한 기준과 예시는 `book/visual-style-guide.md` 참조.

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
본 부록은 다이어그램 작성 규칙의 핵심 요약입니다. SSOT는 `book/visual-style-guide.md`이며, 상세 규칙과 예시는 해당 문서를 우선합니다.

- 초기화 스니펫(반드시 포함):
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
- 도형과 의미: 개념/원칙=직사각형, 결정=마름모, 에이전트=둥근 사각형, 산출물=서브루틴, 데이터=실린더, Human=원형.
- 레이아웃: 기본 흐름 `LR`, 필요 시 `TD`. 서브그래프는 팀/모듈 경계에 사용.
- 라벨: 간선 라벨은 의미 있을 때만, 간결하게. 연결 라벨·화살표의 배경은 자동으로 녹색(edgeLabelBackground) 적용.
- 클래스 예시(선택): `principle`, `decision`, `agent`, `artifact`, `data`, `human` 등 공통 정의를 필요 시 다이어그램 내에 포함.
- 품질 원칙: 한 다이어그램=한 메시지, 산출물 명시 및 다음 단계 입력과 연결.

자세한 규칙과 예시는: `book/visual-style-guide.md`
