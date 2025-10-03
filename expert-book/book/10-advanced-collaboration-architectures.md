# 10. 고급 협업 아키텍처 — 아키텍트·워커·비평가·라우터

목표
- 대형 과제를 역할 분할과 자동화된 품질 게이트로 처리한다. 아키텍트는 설계·분해, 워커는 생산, 비평가는 검증, 라우터는 분배를 담당.

역할 정의(샘플)
```yaml
roles:
  architect:
    goals: [분해, 기준 정의, 품질 게이트 설계]
  worker:
    goals: [산출물 생산, 템플릿 준수]
  critic:
    goals: [규정 준수 검토, 반례·리스크 표기]
  router:
    goals: [작업 분배, 난이도 기반 승급]
```

워크플로우 패턴
```yaml
steps:
  - name: plan
    agent: architect
  - name: draft
    agent: worker
  - name: critique
    agent: critic
  - name: fix
    when: "critique.ok == false"
    agent: worker
  - name: route
    agent: router
```

비평가 프롬프트 조각(예)
```text
다음 출력이 정책과 스키마를 준수했는지 점검하고, 실패 항목을 나열하세요.
출력: JSON {ok:boolean, failures:[{rule, reason, fix}]}
```

라우터 휴리스틱(예)
- 길이/주제/리스크에 따라 단계적 승급: 로컬→경량→고성능
- 최근 실패 패턴에 기반한 전문가 라우트로 분배

관측·회귀
- 각 역할의 산출물과 심사 기록을 JSONL로 보관해 누적 학습과 회귀 테스트에 사용

Human-in-the-Loop
- 최종 merge 전 사람 승인. 아키텍트는 결론과 근거, 잔여 리스크를 요약해 제시

연관 챕터
- [07. 워크플로우 패턴](07-process-workflow.md)
- [11-1. 단일 에이전트 패턴](11-1-single-agent-patterns.md)
- [11-2. 조직 표준](11-2-organizational-standards.md)

