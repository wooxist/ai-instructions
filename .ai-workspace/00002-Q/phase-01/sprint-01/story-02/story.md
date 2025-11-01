# Story 2: Book2 기본 파일 + Chapter 11 코드 제거

## 목표
Book2의 기본 파일 4개와 Chapter 11의 5개 파일, 총 9개 마크다운 파일에서 프로그래밍 언어 코드를 제거합니다.

## 배경
Book2는 더 심화된 내용을 다루지만, 여전히 주요 독자는 코딩 경험이 제한적인 사용자입니다. 특히 practice-guide와 terminology-guide는 전체 Book2의 기반이 되는 문서이므로 접근성이 중요합니다.

## 기대효과
- Book2의 기초 문서와 첫 챕터에서 프로그래밍 코드 장벽 제거
- 독자가 Book2에 더 쉽게 진입할 수 있음

## Workflow
(Story 1과 동일한 5단계 워크플로우)

### Task 1: 파일 검토 (Review) - Human
### Task 2: 개선 계획 수립 (Plan) - AI
### Task 3: 계획 승인 (Approve) - Human
### Task 4: 파일 수정 실행 (Execute) - AI
### Task 5: 최종 확인 (Verify) - Human

## 제약 조건
- **유지**: ```yaml, ```json, ```markdown, ```mermaid, ```text
- **제거**: 모든 프로그래밍 언어 코드

## 대상 파일 목록 (9개)

### 기본 파일 (4개)
1. practice-guide.md
2. terminology-guide.md
3. vol-2-index.md
4. vol-2-part-0-preface.md

### Chapter 11 (5개)
5. vol-2-part-4-chapter-11-00-intro.md
6. vol-2-part-4-chapter-11-01.md
7. vol-2-part-4-chapter-11-02.md
8. vol-2-part-4-chapter-11-03.md
9. vol-2-part-4-intro.md
