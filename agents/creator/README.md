# Creator Agent 사용 가이드

## 개요
- 목적: 요구 분석 → 템플릿 선택 → 인스트럭션 초안 생성
- 기준: WRITER, glossary, 8가지 구성 요소

## 실행 흐름
1) instruction-intake → 2) intent-clarification → 3) template-selection → 4) constraints-synthesis → 5) io-schema-synthesis → 6) template-fill

## 입력/출력
- 입력: agents/creator/agent.md의 입력 스키마 참조
- 출력: Markdown 인스트럭션 + 성공 기준 체크리스트(JSON)

## 팁
- 산출물 중심(Output-Driven), Human-in-the-Loop 등 핵심 용어는 glossary 링크를 포함하세요.
