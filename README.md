# AI 작업 관리 시스템

## 사용 방법

### 1. 새 작업 시작
지시사항을 주면 자동으로 다음 워크플로우가 실행됩니다:

```
지시 → 분석 → 계획 → 체크리스트 → 실행 → 완료
```

### 2. 워크플로우 단계

#### Stage 1: Instruction (지시)
- 원본 지시사항이 `instruction.md`에 저장됨
- 변경 없이 보존

#### Stage 2: Analysis (분석)
- 요구사항 분석
- 컨텍스트 파악
- 결과가 `analysis.md`에 캐싱됨

#### Stage 3: Plan (계획)
- 구체적 실행 계획 수립
- 단계별 전략 수립
- `plan.md`에 저장됨

#### Stage 4: Checklist (체크리스트)
- 실행 가능한 아이템 목록 생성
- 진행 상황 추적 가능
- `checklist.md`에 저장됨

#### Stage 5: Execution (실행)
- 실제 작업 수행
- 산출물은 `artifacts/` 디렉토리에 저장

#### Stage 6: Completed (완료)
- 완료 보고서 작성
- 작업 상태가 "completed"로 변경

### 3. 작업 재개/인계

다른 AI나 새 세션에서 작업을 이어받으려면:

1. Task ID 확인
2. 해당 작업 폴더의 모든 파일 읽기
3. `status.json`에서 현재 단계 확인
4. 마지막 완료 단계부터 이어서 진행

### 4. 디렉토리 구조

```
.ai-workspace/
├── task_registry.json      # 전체 작업 목록
└── workflow_template.json  # 워크플로우 정의

tasks/
└── task_YYYYMMDD_HHMMSS/
    ├── instruction.md      # 원본 지시
    ├── analysis.md         # 분석 결과
    ├── plan.md            # 실행 계획
    ├── checklist.md       # 체크리스트
    ├── status.json        # 현재 상태
    ├── context/           # 컨텍스트 캐시
    │   ├── references.md
    │   └── decisions.md
    └── artifacts/         # 산출물
```

### 5. 명령어

#### 새 작업 시작
"[작업 내용]을 해주세요"라고 지시하면 자동으로 워크플로우가 시작됩니다.

#### 작업 상태 확인
"현재 진행중인 작업 보여줘"

#### 작업 재개
"task_YYYYMMDD_HHMMSS 이어서 해줘"

#### 작업 완료 확인
모든 단계가 완료되면 자동으로 완료 처리됩니다.
