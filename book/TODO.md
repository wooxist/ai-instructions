# book/TODO

집필자용 작업 목록입니다. 책 콘텐츠 변경은 `.instructions.md`와 `book/WRITER.md`를 기준으로 하며, 시각 자료 스타일의 SSOT는 `book/WRITER.md` 부록 A입니다. 독자용 “실습 체크리스트”와 구분하여 운영합니다.

## 운영 규칙
- 체크박스 상태, 진행률 요약, 작업 이력을 함께 관리합니다. (`book/WRITER.md` 6항)
- `book/` 변경 시 영향 범위 점검: `book/index.md`(상세 목차), 루트 `README.md`(구조 변경 시), `ai-knowledge/meta-agent-design/` 내 book 요약.
- 시각 자료 스타일: WRITER 부록 A(SSOT)만 수정합니다. `book/visual-style-guide.md`는 안내 문서입니다.
- 실습 체크리스트 포맷 표준: 1장 형식(개념 이해/실습 능력/적용 및 활용 + 실습 과제)을 따릅니다.

---

## 우선순위 (P0)
- [x] 모든 다이어그램에 Mermaid 초기화 스니펫 적용(WRITER 부록 A 기준)
- [x] 01장 중복 “실습 체크리스트” 병합 및 표준 포맷 정리 (`book/01-introduction.md`)
- [x] 02장 오탈자 교정(“좌힐/좌혀서”→“조절/좁혀서” 등) (`book/02-questions.md`)
- [x] 내부 링크/앵커 검증 및 수정(`book/index.md`/`book/glossary.md`/06장 헤더 포함)

## 우선순위 (P1)
- [x] Part 라벨과 `book/index.md` 파트 구성을 동기화(모든 장)
- [x] 용어 일관화: `book/glossary.md` 기준으로 본문 용어 링크/표기 정리
- [x] 실습 심화 과제 연결: 각 장 말미에서 `book/practice-guide.md`로 연결 확인
- [x] `book/ROADMAP.md` 정비(루트 `ROADMAP.md`로 위임 또는 간단 요약 유지)

## 레퍼런스 정리
- [x] `book/visual-style-guide.md` 참고 문구를 WRITER 부록 A로 교체(전 파일 검색)
- [x] Mermaid 클래스/도형 매핑을 WRITER 부록 A 예시로 통일

---

## 챕터별 점검 메모
- [x] 03 좋은 인스트럭션: ‘검증 기준’ 템플릿의 placeholder(“기준 4/5”) 구체화 (`book/03-good-instructions.md`)
- [x] 04 메타 원칙: 요약표/다이어그램 가독성 점검 및 스니펫 적용 (`book/04-meta-principles.md`)
- [x] 05 역할·제약: 역할/제약 JSON·YAML 스니펫 유효성 보강 (`book/05-agent-constraints.md`)
- [x] 06 입력·출력: JSON Schema 예시 보강(`$schema`, 타입, 예제) (`book/06-input-output.md`)
- [x] 07 워크플로우: `workflow.yaml` 예시 1개 이상 추가 및 주석 명확화 (`book/07-process-workflow.md`)
- [x] 08 성능: 품질-비용-속도 표에 전제/단위/측정 방법 명시 (`book/08-performance.md`)
- [x] 09 생산성: ‘오답 노트’ 템플릿 추가(필드/주기/회귀 방지 절차) (`book/09-productivity.md`)
- [x] 10 협업 아키텍처: 다이어그램 클래스/레이블 표준화 및 산출물-다음 입력 연결 (`book/10-advanced-collaboration-architectures.md`)
- [x] 11-1 단일 에이전트: 사례 맵 앵커와 `index.md` 교차 링크 동기화 (`book/11-1-single-agent.md`)
- [x] 11-2 단위 조직: Human-in-the-Loop 지점·승인 기준 예시 명확화 (`book/11-2-unit-organization.md`)
- [x] 11-3 복합 조직: 팀 간 인터페이스(공통 스키마) 샘플 추가 (`book/11-3-complex-organization.md`)
- [x] 12 도구: 도구 명세 스키마/권한·가드레일 사례 추가 (`book/12-tools.md`)
- [x] 13 워크플로우 as Code: 장 제목과 루트 로드맵(DSL) 불일치 정리 (`book/13-workflow-as-code.md`)
- [x] 14 진화: 회귀 테스트/거버넌스 프로세스 다이어그램 추가 (`book/14-evolution.md`)
- [x] 15 결론: 전 장 핵심 연결·다음 단계 링크 정리 (`book/15-conclusion.md`)

---

## 작업 이력
- 2025-10-05: WRITER 부록 A에 시각 스타일 가이드(SSOT) 통합, TODO 재정비
- 2025-10-05: P0 완료 — Mermaid init 스니펫 감사, 01장 체크리스트 병합, 02장 오탈자 교정, 06장 체크리스트 헤더 표준화, 10·13장 인덱스 앵커 수정, glossary 교차링크 수정
- 2025-10-05: P1 진행 — 07·15장 Part 라벨 보강, 각 장 ‘실습 체크리스트’에 practice-guide 링크 추가, book/ROADMAP.md를 루트 로드맵 안내로 정비, 용어 일관화(SSOT/SoC/MECE/Output-Driven/JSON Schema/Human-in-the-Loop/RAG/MCP 링크화)
- 2025-10-05: 레퍼런스 정리 — visual-style-guide 참고 문구를 WRITER 부록 A(SSOT)로 통일, Mermaid 클래스/도형 매핑을 WRITER 부록 A 예시로 일치(7장/11-2/11-3 갱신)
- 2025-10-05: 03장 업데이트 — ‘성공 기준’ 템플릿의 기준 4/5를 구체 예시로 채움(glossary 일관성, 보안/금지 항목 점검)
- 2025-10-05: 04장 업데이트 — 메타 원칙 관계도 Mermaid 스니펫을 WRITER 부록 A 테마변수로 보강(note 배경/텍스트 색상 포함)
- 2025-10-05: 05장 업데이트 — 역할·제약 JSON/YAML 스니펫 추가(유효한 예시, 평가 기준/금지 항목 포함)
- 2025-10-05: 06장 업데이트 — JSON Schema 예시 추가(`$schema`, 타입/enum/min-max, examples 포함)
- 2025-10-05: 07장 업데이트 — workflow.yaml 파이프라인/생성-검증+라우팅 예시 추가, Human-in-the-Loop 주석 명확화
- 2025-10-05: 08장 업데이트 — 성능 표 템플릿에 측정 전제·단위·방법 추가(TTFT/토큰 등)
- 2025-10-05: 09장 업데이트 — ‘오답 노트’ 템플릿 추가(필드/주기/회귀 방지 체크리스트 포함)
- 2025-10-05: 10장 업데이트 — 시퀀스 다이어그램에 산출물→다음 입력 인터페이스 노트 추가
- 2025-10-05: 11-1장 확인 — 사례 맵 앵커와 index.md 교차 링크 일치(변경 불요)
- 2025-10-05: 11-2장 업데이트 — Human-in-the-Loop 승인 기준/반려 절차 명시
- 2025-10-05: 11-3장 업데이트 — 팀 간 공통 산출물 스키마(JSON Schema) 예시 추가
- 2025-10-05: 12장 업데이트 — 도구 명세 스키마에 권한/가드레일(승인/도메인/시간/레이트리밋) 예시 추가
- 2025-10-05: 13장 업데이트 — 장 제목을 루트 로드맵 표기(DSL)와 일치시키도록 정리
- 2025-10-05: 14장 업데이트 — 회귀 테스트/거버넌스 프로세스 다이어그램 추가(Human/Decision/Artifact 클래스 적용)
- 2025-10-05: 내부 링크/앵커 검증 — book 전역 링크/앵커 검사 통과, 13장 placeholder 링크 정리
