# 유지보수 가이드: 커지는 TODO/ROADMAP/세션 관리

이 문서는 `.work/TODO.md`, `ROADMAP.md`, `.session/`가 커졌을 때 가독성과 추적 가능성을 유지하는 운영 규칙과 도구를 제공합니다.

---

## 운영 원칙(요약)

- 단일 활성 파일, 다중 아카이브 파일 원칙
  - 활성: `.work/TODO.md`, `ROADMAP.md`, `.session/최근 N일`
  - 아카이브: `.work/archive/**`, `.session/archive/**`
- 주기적 롤오버(Weekly/Monthly)
  - TODO: 주간 단위로 완료 섹션을 아카이브로 이동
  - Session: 14일 지난 세션은 월별 폴더로 이동, `INDEX.md` 갱신
  - ROADMAP: Phase 상세는 별도 파일로 분리, 루트는 개요만 유지
- 크기·라인 예산
  - TODO ≤ 200줄, ROADMAP ≤ 150줄, 세션은 일일 1파일 유지

---

## 폴더 구조 권장

```
.work/
  TODO.md                # 활성 TODO
  roadmap/               # Phase 단위 문서화
    index.md
    phase-01.md
    phase-02.md
  archive/
    todo/
      2025-W41-done.md
      2025-W42-done.md
.session/
  2025-10-10.md         # 최근 14일
  archive/
    2025-09/
      2025-09-17.md
      ...
    INDEX.md            # 최근 10개 링크
```

---

## 롤오버/분리 방법(스크립트)

다음 스크립트는 프로젝트 루트에서 실행하세요.

```
./.project_template/tools/rollover.sh todo        # 완료된 TODO 주간 아카이브
./.project_template/tools/rollover.sh sessions    # 14일 지난 세션 아카이브
./.project_template/tools/rollover.sh roadmap     # ROADMAP Phase 분리/색인
./.project_template/tools/rollover.sh check       # 파일 크기·라인 수 점검
```

옵션 예시:
- `--days 21` 세션 보존일 변경
- `--week 2025-W42` 특정 주로 TODO 아카이브
- `--dest <path>` 아카이브/분리 대상 경로 지정

---

## 운영 절차(권장 루틴)

### 매주 금요일(주간 회고)
- `rollover.sh todo` 실행 → 완료 작업을 `.work/archive/todo/YYYY-WW-done.md`로 이동
- TODO 상단의 "이번 주 우선순위" 재설정, "마지막 업데이트" 갱신

### 매월 초(월간 정리)
- `rollover.sh sessions --days 14` 실행 → 2주 지난 세션 월별 폴더로 이동
- `.session/INDEX.md` 갱신(최근 10개 링크)

### Phase 확장 시
- `rollover.sh roadmap` 실행 → 루트 `ROADMAP.md`의 Phase들을 `.work/roadmap/phase-XX.md`로 분리, `index.md` 생성
- 루트 `ROADMAP.md`는 개요/마일스톤/링크만 유지

---

## 수동 운영 팁

- TODO의 "✅ 완료된 작업"은 날짜별 블록만 유지(최근 1~2일), 과거는 아카이브로 이동
- ROADMAP은 마일스톤과 진행률만 루트에 유지하고, 상세 체크리스트는 Phase 파일로 이동
- 세션은 하루 1파일 원칙, 세션 내 "중요 결정"만 굵게 표기해 검토성 확보

---

## 트러블슈팅

- 스크립트가 헤더를 찾지 못함 → 템플릿 헤더(예: `## ✅ 완료된 작업`)를 수동으로 복원
- 맥/리눅스 sed 차이 → 스크립트는 자동 감지하나 실패 시 GNU sed 사용 권장
- 잘못된 이동 복구 → Git 이력에서 파일 복원 또는 아카이브 파일을 병합 재적용

