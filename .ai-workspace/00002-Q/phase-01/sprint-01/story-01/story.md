# Story 1: Book1 전체 코드 제거

## 목표
Book1의 13개 마크다운 파일에서 프로그래밍 언어 코드를 제거하여 일반 독자의 접근성을 높입니다.

## 배경
- **독자 프로필**: 코딩 경험이 없거나 기초적인 일반 회사원, 분야 전문가
- **문제점**: Python, JavaScript 등 프로그래밍 코드는 독자의 이해를 방해함
- **해결책**: 실제 프로그래밍 코드는 제거하되, YAML/JSON(설정), Mermaid(다이어그램)는 유지

## 기대효과
- 비개발자 독자도 Book1 내용을 쉽게 이해할 수 있음
- 책의 핵심 메시지(AI 인스트럭션 설계)에 집중 가능

## Workflow

### Task 1: 파일 검토 및 수정 계획 (Review & Plan)
- **담당**: AI + Human
- **방법**: 
  1. AI가 13개 파일을 모두 읽고 프로그래밍 코드 블록 식별
  2. 각 파일별로 제거 대상과 수정 방안 제시
  3. Human이 검토 및 승인
- **완료 기준**: 13개 파일 전체의 수정 계획 승인 완료

### Task 2: 파일 수정 실행 (Execute)
- **담당**: AI
- **방법**: 승인된 계획에 따라 파일 수정
- **완료 기준**: 13개 파일 모두 수정 완료

### Task 3: 최종 확인 (Verify)
- **담당**: Human
- **방법**: 수정 결과 검토
- **완료 기준**: 최종 승인

## 대상 파일 목록 (13개)

1. vol-1-index.md
2. vol-1-part-0-preface.md
3. vol-1-part-1-chapter-01.md
4. vol-1-part-1-chapter-02.md
5. vol-1-part-1-chapter-03.md
6. vol-1-part-1-complete.md
7. vol-1-part-2-chapter-04.md
8. vol-1-part-2-chapter-05.md
9. vol-1-part-2-chapter-06.md
10. vol-1-part-3-chapter-07.md
11. vol-1-part-3-chapter-08.md
12. vol-1-part-3-chapter-09.md
13. vol-1-part-4-chapter-10.md

## 제약 조건
- **유지**: ```yaml, ```json, ```markdown, ```mermaid, ```text
- **제거**: ```python, ```javascript, ```js, ```java, ```cpp 등 모든 프로그래밍 언어 코드
- **원칙**: 코드 제거 시 문맥의 흐름이 자연스럽게 유지되어야 함
