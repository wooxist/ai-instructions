# 🔄 Skeleton 구조 재귀적 적용 검토 지침

이 문서는 skeleton 구조를 프로젝트 내 서브프로젝트들에 재귀적으로 적용할 수 있는지 검토하는 지침입니다.

## 🎯 재귀적 적용의 의미

### 현재 구조 (단일 레벨)
```
ai-instructions/ (root)
├── ROADMAP.md         # 전체 프로젝트 로드맵
├── .session/          # root 작업 일기
├── .work/            # root 작업 관리
│   └── TODO.md
├── book/             # 서브프로젝트 1
├── templates/        # 서브프로젝트 2
└── agents/           # 서브프로젝트 3
```

### 재귀적 구조 (다중 레벨)
```
ai-instructions/ (root)
├── ROADMAP.md         # 전체 프로젝트 로드맵
├── .session/          # root 작업 일기
├── .work/            # root 작업 관리
│
├── book/             # 서브프로젝트 1
│   ├── ROADMAP.md    # book 전용 로드맵
│   ├── .session/     # book 전용 세션
│   └── .work/       # book 전용 작업
│
├── templates/        # 서브프로젝트 2
│   ├── ROADMAP.md    # templates 전용 로드맵
│   ├── .session/     # templates 전용 세션
│   └── .work/       # templates 전용 작업
│
└── agents/           # 서브프로젝트 3
    ├── ROADMAP.md    # agents 전용 로드맵
    ├── .session/     # agents 전용 세션
    └── .work/       # agents 전용 작업
```

## 🔍 검토 항목

### 1. 장점 검토

#### 1.1 독립성
- [ ] **질문**: 각 서브프로젝트가 독립적으로 작업 가능한가?
- [ ] **확인**: book/, templates/, agents/가 각각 별도 팀이나 시기에 작업되는가?
- [ ] **이점**: 각 팀이 자신의 세션과 TODO를 독립 관리

#### 1.2 확장성
- [ ] **질문**: 서브프로젝트가 계속 추가될 가능성이 있는가?
- [ ] **확인**: 새로운 모듈이나 기능이 자주 추가되는가?
- [ ] **이점**: 새 서브프로젝트 추가 시 동일한 구조로 즉시 시작

#### 1.3 이식성
- [ ] **질문**: 서브프로젝트를 별도 저장소로 분리할 가능성이 있는가?
- [ ] **확인**: book/을 별도 저장소로 만들 계획이 있는가?
- [ ] **이점**: 이미 완전한 구조를 가지고 있어 쉽게 분리 가능

### 2. 단점 검토

#### 2.1 복잡도 증가
- [ ] **문제**: 너무 많은 .session/ 폴더로 인한 혼란
- [ ] **확인**: AI가 어느 레벨의 세션을 읽어야 하는지 혼동할 가능성
- [ ] **영향도**: 높음 ⚠️

#### 2.2 중복 관리
- [ ] **문제**: ROADMAP.md와 TODO.md의 중복
- [ ] **확인**: root와 서브프로젝트 간 동기화 필요성
- [ ] **영향도**: 중간 ⚠️

#### 2.3 Git 관리 복잡도
- [ ] **문제**: 여러 레벨의 .session/ 파일들 관리
- [ ] **확인**: .gitignore 규칙 설정의 복잡도
- [ ] **영향도**: 낮음 ✅

### 3. 대안 검토

#### 대안 1: 선택적 적용 (추천) ⭐
```
ai-instructions/
├── .session/          # root만 세션 관리
├── .work/            # root만 작업 관리
│
├── book/             
│   └── ROADMAP.md    # book만 별도 ROADMAP
│
├── templates/        # 세션 불필요 (단순 저장소)
│
└── agents/           
    ├── ROADMAP.md    # agents만 별도 ROADMAP
    └── .work/       # agents만 별도 TODO
```

**적용 기준**:
- 활발한 개발이 진행되는 서브프로젝트만 적용
- 단순 저장소 역할은 제외

#### 대안 2: 네임스페이스 방식
```
ai-instructions/
├── .session/
│   ├── root-2025-10-06.md
│   ├── book-2025-10-06.md      # 프리픽스로 구분
│   └── agents-2025-10-06.md
│
└── .work/
    ├── TODO.md                  # root TODO
    ├── TODO-book.md             # book TODO
    └── TODO-agents.md           # agents TODO
```

**장점**: 한 곳에서 모든 세션 관리
**단점**: 파일명 규칙 필요

#### 대안 3: 심볼릭 링크 활용
```
ai-instructions/
├── .session/          # 모든 세션 중앙 관리
│
├── book/
│   └── .session -> ../.session  # 심볼릭 링크
│
└── agents/
    └── .session -> ../.session  # 심볼릭 링크
```

**장점**: 중앙 집중 관리
**단점**: Windows 호환성 문제

## 📊 의사결정 매트릭스

| 검토 항목 | 가중치 | 단일 구조 | 재귀 구조 | 선택적 적용 |
|---------|-------|----------|----------|------------|
| 구현 단순성 | 30% | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| 유지보수성 | 25% | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| 확장성 | 20% | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| AI 이해도 | 15% | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| 팀 협업 | 10% | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **총점** | 100% | 2.5 | 1.65 | **2.4** |

## 🎯 권장 사항

### 즉시 적용 (Phase 1)
```bash
# 현재 구조 유지 (이미 적용됨)
ai-instructions/
├── ROADMAP.md
├── .session/
├── .work/
└── .instructions.md
```

### 선택적 적용 (Phase 2) - 필요시
```bash
# book 프로젝트가 독립적으로 커지면
cd book/
cp ../.project_template/skeleton/.instructions.md ./
mkdir -p .session .work
# book 전용 ROADMAP.md 생성
```

### 적용 기준 체크리스트

서브프로젝트에 skeleton 적용을 고려해야 할 때:

- [ ] **규모**: 파일 50개 이상 또는 3개월 이상 작업
- [ ] **팀**: 2명 이상이 주로 작업
- [ ] **독립성**: 다른 모듈과 독립적 릴리스 주기
- [ ] **복잡도**: 자체 Phase와 TODO가 10개 이상

위 조건 중 3개 이상 만족 시 → skeleton 구조 적용 권장

## 🔧 재귀 적용 스크립트 (필요시)

```bash
#!/bin/bash
# apply-recursive-skeleton.sh

SUBPROJECTS=("book" "agents")  # templates는 제외

for project in "${SUBPROJECTS[@]}"; do
    echo "Setting up $project..."
    
    cd $project
    
    # skeleton 구조 생성
    mkdir -p .session .work/tasks
    
    # 템플릿 복사
    cp ../.project_template/skeleton/.session/_template.md .session/
    cp ../.project_template/skeleton/.work/TODO.md .work/
    
    # .instructions.md 커스터마이징 필요
    echo "⚠️  $project/.instructions.md 수동 커스터마이징 필요"
    
    cd ..
done
```

## 📝 AI 지침 수정 (재귀 구조 사용 시)

`.instructions.md`에 추가할 내용:

```markdown
### 다중 레벨 세션 관리

프로젝트 구조가 재귀적일 때:
1. 현재 작업 디렉토리 확인
2. 가장 가까운 .session/ 폴더 사용
3. 없으면 상위로 이동하여 찾기

우선순위:
- `./book/.session/` > `./.session/` (book 작업 시)
- `./.session/` (root 작업 시)
```

## ✅ 최종 권장사항

### 현재 단계 (2025-10-06)
**단일 구조 유지** - root 레벨에서만 skeleton 적용 ✅

### 향후 고려사항
1. **3개월 후 재검토**: 서브프로젝트 성장 상황 평가
2. **book/ 우선 검토**: 가장 활발한 서브프로젝트부터
3. **점진적 적용**: 필요한 서브프로젝트만 선택적 적용

### 재귀 적용이 꼭 필요한 신호
- 서브프로젝트별 독립적 팀 구성
- 서브프로젝트 별도 저장소 분리 계획
- 서브프로젝트별 릴리스 주기 차이

## 🚨 주의사항

### 과도한 구조화의 함정
> "모든 문제가 못으로 보이면 모든 도구가 망치로 보인다"

- skeleton 구조가 좋다고 모든 폴더에 적용 ❌
- 실제 필요가 확인된 후 적용 ✅
- YAGNI (You Aren't Gonna Need It) 원칙 준수

### AI 혼동 방지
- 재귀 구조 사용 시 명확한 컨텍스트 제공 필요
- "book 세션 시작" vs "root 세션 시작" 구분

---

**작성일**: 2025-10-06  
**목적**: skeleton 구조의 재귀적 적용 가능성 검토  
**결론**: 현재는 단일 구조 유지, 필요시 선택적 적용 권장
